from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import filter_messages, HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.store.base import BaseStore
import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from typing import Optional,TypedDict
import agent.common.llm
from agent.common.context import ContextSchema
from agent.common.store import UserPreferences
from agent.common.city_aliases import (
    city_search_terms,
    district_search_terms,
    normalized_city_name,
    sql_city_predicate,
    sql_district_predicate,
)
from agent.common.tool_call_ids import ensure_tool_call_ids
from agent.state.recommend import RecommendState
from langgraph.types import interrupt,Command
from pydantic import BaseModel, Field
from agent.common.llm import model
from langgraph.runtime import Runtime
import uuid
from agent.state.recommend import get_recommend_info

# 定义用户信息的数据模型(结构化输出)
class UserInfo(BaseModel):
    """用户的租房需求信息"""
    city: Optional[str] = Field(
        default=None,
        description="用户所在或想要租房的城市，例如：西安、北京、上海"
    )
    district: Optional[str] = Field(
        default=None,
        description="用户想要租房的具体区域或行政区，例如：雁塔区、碑林区、海淀区"
    )
    budget_min: Optional[float] = Field(
        default=None,
        description="用户的最低预算，单位为元/月"
    )
    budget_max: Optional[float] = Field(
        default=None,
        description="用户的最高预算，单位为元/月"
    )
    room_type: Optional[str] = Field(
        default=None,
        description="房屋类型，例如：整租、合租、公寓、一室一厅、两室一厅"
    )
    orientation: Optional[str] = Field(
        default=None,
        description="房屋朝向，例如：朝南、朝北、东南、南北通透"
    )
    room_count: Optional[int] = Field(
        default=None,
        description="需要推荐的房屋数量"
    )
    others: Optional[str] = Field(
        default=None,
        description="特殊要求，例如：带阳台、独立卫生间、近地铁、可养宠物、有电梯等"
    )

def collect_user_info(state:RecommendState,runtime:Runtime[ContextSchema],*,store:BaseStore):
    """收集用户信息，并且能够获取到用户静态上下文"""
    # 1.获取需要被解析的数据，最新的用户消息+用户的偏好数据
    user_messages=filter_messages(state["messages"],include_types="human")
    pref=state.get("user_preferences", {})
    if pref and pref.get("budget_min") is not None and pref.get("budget_max") is not None:
        extract_messages=[
            HumanMessage(content="用户的历史偏好信息如下："+
                         f"最低预算为：{pref["budget_min"]}，最高预算为：{pref["budget_max"]}"),
            user_messages[-1]
        ]
    else:
        extract_messages=[user_messages[-1]]
    # 2.提取信息
    def extract_info(messages)->UserInfo:
        system_message=SystemMessage(
            content="""你是一个租房需求信息提取专家。请从用户的描述与历史信息中提取租房相关信息。
                    如果用户历史偏好信息与最新用户消息冲突，以最新的用户消息为主。
                    只提取用户明确提到的信息，不要猜测或推断。
                    如果某个信息用户没有提到，就返回空。
                    注意预算的单位可能是元/月、元/天等，请统一转换为元/月。
                    如果用户提到价格范围，请分别提取最低和最高预算。
                    如果用户提到推荐几套，请提取room_count字段。"""
        )
        return model.with_structured_output(UserInfo).invoke([system_message, *messages])

    extracted_info=extract_info(extract_messages)
    # 无结果后的下一轮只会包含用户新补充的条件。先继承已有条件，再由新输入覆盖，
    # 这样“预算改为 1000-3000”不会意外丢掉上一轮已经确认的城市。
    search_fields = (
        "city", "city_search_terms", "district_search_terms", "budget_min", "budget_max", "district",
        "room_type", "orientation", "room_count", "others",
    )
    updated_state = {
        field: state[field]
        for field in search_fields
        if state.get(field) is not None
    }
    updated_state["recommendation_found"] = False
    updated_state["search_cancelled"] = False
    # 更新状态函数
    def update_state(current_state:dict,info:UserInfo)->dict:
        if not info:
            return current_state
        else:
            user_info=info.model_dump(exclude_none=True)#转换为字典，并排除None值
            current_state.update(user_info)
            return current_state

    updated_state=update_state(updated_state,extracted_info)
    # 无结果追问中“取消区域/不限区域”是控制指令，不能依赖模型恰好把它
    # 结构化为 district；否则上一轮的区域条件会被继承回来。
    latest_user_text = str(user_messages[-1].content).strip()
    if "不限区域" in latest_user_text or "取消区域" in latest_user_text:
        updated_state["district"] = "不限区域"

    # 3.中断咨询推荐的必须参数，如果最新的用户消息没有表明推荐城市，模糊推荐
    # 检查是否存在缺失信息
    missing_info = []
    if not updated_state.get("city"):
        missing_info.append("**城市**")
    if updated_state.get("budget_min") is None or updated_state.get("budget_max") is None:
        missing_info.append("**预算范围**")

    if missing_info:
        prompt = f"为了给您推荐合适的房源，请提供以下信息：{', '.join(missing_info)}和其它信息。\n"
        prompt += "如果您不想提供，请输入'**不提供**'，我会根据已有信息为您推荐房源。"
        # 中断，等待用户输入
        answer = interrupt(prompt)
        if str(answer).strip() == "不提供":
            # 如果用户选择不提供，设置默认值
            if not updated_state.get("city"):
                updated_state["city"] = "随机城市"
            if not updated_state.get("budget_min"):
                updated_state["budget_min"] = 500.0
            if not updated_state.get("budget_max"):
                updated_state["budget_max"] = 5000.0
            if not updated_state.get("room_count"):
                updated_state["room_count"] = 5
            print(f"用户选择不提供信息，使用默认值：城市={updated_state.get('city')}，"
                  f"预算={updated_state['budget_min']}-{updated_state['budget_max']}")
        else:
            # 用户提供了更多信息，再次提取
            user_response_msg = HumanMessage(content=str(answer))
            extracted_response_info = extract_info([user_response_msg])
            updated_state = update_state(updated_state, extracted_response_info)

    if updated_state.get("city"):
        city = updated_state["city"]
        updated_state["city"] = normalized_city_name(city)
        updated_state["city_search_terms"] = city_search_terms(city)
        if updated_state.get("district"):
            updated_state["district_search_terms"] = district_search_terms(
                city,
                updated_state["district"],
            )

    # 4.持久化处理：更新预算，根据最新的用户喜爱更新偏好数据
    if updated_state.get("budget_min") or updated_state.get("budget_max"):
        context = runtime.context or {}
        user_id = context.get("user_id", "anonymous")
        namespace=(user_id,"preferences")
        prefs_result=store.search(namespace)
        # 兼容历史版本写入的拼写错误命名空间；一旦后续发生更新，会写回正确位置。
        if not prefs_result:
            prefs_result = store.search((user_id, "perferences"))
        # 新增或更新
        if len(prefs_result)==0:
            prefs=UserPreferences(
                budget_min=updated_state.get("budget_min"),
                budget_max=updated_state.get("budget_max"),
            )
            store.put(namespace,str(uuid.uuid4()),prefs.model_dump(exclude_none=True))
            updated_state["user_preferences"]=prefs.model_dump(exclude_none=True)
        else:
            # 有持久化信息，判断更新，上下限更宽则更新，否则不更新
            prefs = prefs_result[0].value
            # 用户可能只有预约记录而尚未设置过预算，读取时不能假设键一定存在。
            store_min = prefs.get('budget_min')
            store_max = prefs.get('budget_max')
            cur_min = updated_state.get('budget_min')
            cur_max = updated_state.get('budget_max')
            update_min = False
            update_max = False
            if store_min and cur_min and cur_min < store_min:
                # 都有，就比较
                update_min = True
            elif not store_min and cur_min:
                # store 没有，cur 有，就更新
                update_min = True

            if store_max and cur_max and cur_max > store_max:
                update_max = True
            elif not store_max and cur_max:
                update_max = True

            if update_min or update_max:
                if update_min:
                    prefs['budget_min'] = cur_min
                    print(f"更新用户最低预算={cur_min}")
                if update_max:
                    prefs['budget_max'] = cur_max
                    print(f"更新用户最高预算={cur_max}")
                store.put(namespace,prefs_result[0].key,prefs)
            # 更新用户偏好
            updated_state['user_preferences'] = prefs

    # 无论本轮是否更新预算，都必须把当前检索条件交给后续 SQL 节点；否则在无结果
    # 循环中用户只修改区域等条件时，节点会返回 None，流程无法继续。
    updated_state['messages'] = state['messages'] + [
        HumanMessage(content=get_recommend_info(updated_state))
    ]
    print(f"已收集用户信息：城市={updated_state.get('city')}，"
          f"区域={updated_state.get('district')}，"
          f"预算={updated_state.get('budget_min')}-{updated_state.get('budget_max')}，"
          f"房间数={updated_state.get('room_count')}")
    return updated_state


db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?ssl_disabled=true"
)


# 获取数据库工具
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

# 获取表信息
get_schema_tool = next(tool for tool in tools if tool.name == "sql_db_schema")
get_schema_node = ToolNode([get_schema_tool], name="get_schema")

# 根据SQL查询结果
run_query_tool = next(tool for tool in tools if tool.name == "sql_db_query")
run_query_node = ToolNode([run_query_tool], name="run_query")

# 不用模型参与，直接拿到数据库有哪些表
def list_table(state:RecommendState):
    # 1.调用LLM获取带有AIMessage的上下文
    tool_call={
        "name":"sql_db_list_tables",
        "args":{},
        "id":"123123",
        "type":"tool_call",
    }
    # 这里直接模拟的是LLM返回的tool_call，实际强制调用这个工具
    tool_call_message=AIMessage(content="",tool_calls=[tool_call])
    # 手动调用工具：sql_db_list_tables
    list_tables_tool=next(tool for tool in tools if tool.name == "sql_db_list_tables")
    tool_message=list_tables_tool.invoke(tool_call)
    # 整合结果
    response=AIMessage(content=f"可用的表为:{tool_message.content}")
    return {
        "messages":[tool_call_message,tool_message,response], # 历史消息的结构为A(t)、T、A
    }

# 让 LLM 强制选择工具去查询表结构
def call_get_schema(state:RecommendState):
    llm_with_tools=model.bind_tools([get_schema_tool],tool_choice="any") # 让模型强制选择工具进行调用
    response=ensure_tool_call_ids(llm_with_tools.invoke(state["messages"]))
    return {
        "messages":[response],
    }

# 节点：根据输入判断是否调用查询SQL的工具
def generate_query(state: RecommendState):
    system_prompt = """
    您是一个设计用于与SQL数据库交互的代理。
    需要一个输入问题，创建一个语法正确的{dialect}查询来运行，然后查看查询的结果并返回答案。
    需要根据rows_from_table的示例设置真实查询的值。
    您可以按行对结果排序，以返回最感兴趣的结果。请始终将查询限制为最多{top_k}个结果。
    不要对数据库做任何SQL语句（INSERT，UPDATE，DELETE，DROP等）。
    """
    city_predicate = sql_city_predicate(state.get("city", ""))
    if city_predicate:
        system_prompt += f"""
    用户指定了城市。城市条件必须原样使用以下 SQL 谓词：
    {city_predicate}
    不要把城市名翻译为其它语言，也不要删除其中任一中英文候选值。
    """
    district_predicate = sql_district_predicate(
        state.get("city", ""),
        state.get("district", ""),
    )
    if district_predicate:
        system_prompt += f"""
    用户指定了区域或商圈。区域条件必须原样使用以下 SQL 谓词：
    {district_predicate}
    这个条件已经包含手动映射出的周边行政区，不要只使用原始商圈名称做等值比较。
    """
    # 构建包含用户信息的系统提示
    system_message = SystemMessage(content=system_prompt.format(
        dialect=db.dialect,
        top_k=state.get("room_count", 5)
    ))

    # 在这里没有强制工具调用，可以进行调用或者直接结果
    llm_with_tools = model.bind_tools([run_query_tool])
    response = ensure_tool_call_ids(llm_with_tools.invoke([system_message] + state["messages"]))
    return {"messages": [response]}

# 检查SQL是否合法，是否能够执行正确
def check_query(state: RecommendState):
    check_query_system_prompt = """
    你是一个非常注重细节的SQL专家。仔细检查{dialect}查询中的常见错误，包括:
    -使用非值使用NOT IN
    -使用UNION而非UNION ALL
    -使用BETWEEN表示独立范围
    -谓词中的数据类型不匹配
    -正确引用标识符
    -使用正确数量的函数参数
    -转换为正确的数据类型
    -使用合适的列进行连接
    如果存在上述任何错误，请重写查询。如果没有错误，只需复制原始查询即可。
    在运行此检查之后，您将调用适当的工具来执行查询。
    """.format(dialect=db.dialect)
    city_predicate = sql_city_predicate(state.get("city", ""))
    if city_predicate:
        check_query_system_prompt += (
            "\n用户指定的城市条件必须原样保留：\n"
            f"{city_predicate}\n"
        )
    district_predicate = sql_district_predicate(
        state.get("city", ""),
        state.get("district", ""),
    )
    if district_predicate:
        check_query_system_prompt += (
            "\n用户指定的区域条件必须原样保留：\n"
            f"{district_predicate}\n"
        )
    system_message = SystemMessage(content=check_query_system_prompt)

    # 生成人工用户消息进行检查
    # 上一个节点是generate_query，如果走到这，必定调用了工具。这样获取到的SQL是准确的。
    tool_call = state["messages"][-1].tool_calls[0]  # 获取上一个节点的工具调用
    # 将SQL当作用户消息传入进行检查
    user_message = HumanMessage(content=tool_call["args"]["query"])
    llm_with_tools = model.bind_tools([run_query_tool], tool_choice="any") # 强制绑定执行sql工具
    response = ensure_tool_call_ids(llm_with_tools.invoke([system_message, user_message]))
    response.id = state["messages"][-1].id # 上一个节点决定进行调用工具，存在一个toolcall，这里强制绑定工具又有一个toolcall，这里就是在合并，为一个toolcall，符合聊天模型规范
    return {"messages": [response]}


def query_has_listings(state: RecommendState) -> bool:
    """判断最近一次 ``sql_db_query`` 是否确实返回了至少一条房源。"""
    for message in reversed(state.get("messages", [])):
        if getattr(message, "type", None) != "tool":
            continue
        if getattr(message, "name", None) != run_query_tool.name:
            continue

        content = message.content
        if isinstance(content, (list, tuple, dict)):
            return bool(content)

        text = str(content or "").strip()
        # SQLDatabase 在查询没有行时通常返回空字符串；不同驱动也可能返回 []。
        if not text or text in {"[]", "()", "None", "null"}:
            return False
        # SQL 执行错误同样不能被当作“已推荐到房源”。
        if text.casefold().startswith(("error:", "error executing", "sql error")):
            return False
        return True
    return False


def ask_for_new_criteria(state: RecommendState):
    """没有房源时暂停图执行，收到新条件后回到推荐子图重新查询。"""
    if query_has_listings(state):
        return {"recommendation_found": True, "search_cancelled": False}

    answer = interrupt(
        "当前条件没有查到房源，因此不会进入预订流程。\n"
        "请直接输入新的或放宽后的条件，我会继续查询；例如：武汉 洪山区 1000-3000 元。\n"
        "也可以输入‘不限区域’或‘取消区域’来放宽区域。输入‘取消’可结束本次查询。"
    )
    if str(answer).strip() in {"取消", "结束", "退出"}:
        return {"recommendation_found": False, "search_cancelled": True}
    return {
        "messages": [HumanMessage(content=str(answer))],
        "recommendation_found": False,
        "search_cancelled": False,
    }
