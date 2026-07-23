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
import src.agent.common.llm
from src.agent.common.context import ContextSchema
from src.agent.common.store import UserPreferences
from src.agent.state.recommend import RecommendState
from langgraph.types import interrupt,Command
from pydantic import BaseModel, Field
from src.agent.common.llm import model
from langgraph.runtime import Runtime
import uuid
from src.agent.state.recommend import get_recommend_info

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
    pref=state.get("user_preference",{})
    if pref and pref["budget_min"] and pref["budget_max"]:
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
        return model.with_structured_output(UserInfo).invoke(system_message+messages)

    extracted_info=extract_info(extract_messages)
    updated_state={}
    # 更新状态函数
    def update_state(current_state:dict,info:UserInfo)->dict:
        if not info:
            return current_state
        else:
            user_info=info.model_dump(exclude_none=True)#转换为字典，并排除None值
            current_state.update(user_info)
            return current_state

    updated_state=update_state(updated_state,extracted_info)

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

    # 4.持久化处理：更新预算，根据最新的用户喜爱更新偏好数据
    if updated_state.get("budget_min") or updated_state.get("budget_max"):
        user_id=runtime.context.get("user_id")
        namespace=(user_id,"perferences")
        prefs_result=store.search(namespace)
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
            store_min = prefs['budget_min']
            store_max = prefs['budget_max']
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

        updated_state['messages'] = state['messages'] + [
            HumanMessage(content=get_recommend_info(updated_state)) # 转为用户消息，加入历史消息
        ]
        # 打印日志
        print("已收集用户信息：城市={updated_state.get('city')}，"
              f"区域={updated_state.get('district')}，"
              f"预算={updated_state.get('budget_min')}-{updated_state.get('budget_max')}"
              f"房间数={updated_state.get('room_count')}")

        return updated_state


db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")


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
        "name":"sql_db_list_table",
        "arg":{},
        "id":"123123",
        "type":"tool_call",
    }
    # 这里直接模拟的是LLM返回的tool_call，实际强制调用这个工具
    tool_call_message=AIMessage(content="",tool_calls=[tool_call])
    # 手动调用工具：sql_db_list_table
    list_tables_tool=next(tool for tool in tools if tool.name == "sql_db_list_table")
    tool_message=list_tables_tool.invoke(tool_call)
    # 整合结果
    response=AIMessage(content=f"可用的表为:{tool_message.content}")
    return {
        "message":[tool_call_message,tool_message,response], # 历史消息的结构为A(t)、T、A
    }

# 让 LLM 强制选择工具去查询表结构
def call_get_schema(state:RecommendState):
    llm_with_tools=model.bind_tools([get_schema_tool],tool_choice="any") # 让模型强制选择工具进行调用
    response=llm_with_tools.invoke(state["messages"])
    return {
        "message":[response],
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
    # 构建包含用户信息的系统提示
    system_message = SystemMessage(content=system_prompt.format(
        dialect=db.dialect,
        top_k=state.get("room_count", 5)
    ))

    # 在这里没有强制工具调用，可以进行调用或者直接结果
    llm_with_tools = model.bind_tools([run_query_tool])
    response = llm_with_tools.invoke([system_message] + state["messages"])
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
    system_message = SystemMessage(content=check_query_system_prompt)

    # 生成人工用户消息进行检查
    # 上一个节点是generate_query，如果走到这，必定调用了工具。这样获取到的SQL是准确的。
    tool_call = state["messages"][-1].tool_calls[0]  # 获取上一个节点的工具调用
    # 将SQL当作用户消息传入进行检查
    user_message = HumanMessage(content=tool_call["args"]["query"])
    llm_with_tools = model.bind_tools([run_query_tool], tool_choice="any") # 强制绑定执行sql工具
    response = llm_with_tools.invoke([system_message, user_message])
    response.id = state["messages"][-1].id # 上一个节点决定进行调用工具，存在一个toolcall，这里强制绑定工具又有一个toolcall，这里就是在合并，为一个toolcall，符合聊天模型规范
    return {"messages": [response]}