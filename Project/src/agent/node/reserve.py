import uuid
from typing import Annotated, Any
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import InjectedStore, ToolRuntime
from langgraph.types import interrupt
from langchain_core.tools import tool
from agent.common.llm import model
from agent.common.store import UserPreferences, ReservedInfo
from agent.common.tool_call_ids import ensure_tool_call_ids
from agent.state.reserve import ReserveState

# 节点：获取用户预定房源
def get_title(state: ReserveState):
    prompt = "请输入要预定的房源名称"
    while True: # 这里进行循环验证，如果没有输入正确就一直中断
        title = interrupt(prompt)
        if title:  # 可以进行验证
            return {"title": title}
        # 每次验证失败后，提示信息会更新
        prompt = f"'{title}' 不是一个有效的房源名称，请更正。"

# 节点：获取用户预定电话
def get_phone(state: ReserveState):
    prompt = "请输入要预定的手机号"
    while True:
        phone_number = interrupt(prompt)
        if phone_number:  # 可以进行验证
            return {"phone_number": phone_number}
        # 每次验证失败后，提示信息会更新
        prompt = f"'{phone_number}' 不是一个有效的电话，请更正。"

# 节点：获取用户身份证
def get_id(state: ReserveState):
    prompt = "请输入要预定的身份证号码"
    while True:
        id_card = interrupt(prompt)
        if id_card:
            return {"id_card": id_card}
        # 每次验证失败后，提示信息会更正
        prompt = f"'{id_card}' 不是一个有效的身份证，请更正。"

# 节点：新增预定消息，将输入的用户信息转为humanmessage
def add_reserve_message(state: ReserveState):
    reserve_prompt = """根据提供的信息，帮我预定房源。
- 预定的房源标题：{title}
- 用户预定号码：{phone_number}
- 用户身份证号码：{id_card}"""
    reserve_message = HumanMessage(content=reserve_prompt.format(
        title=state['title'],
        phone_number=state['phone_number'],
        id_card=state['id_card']
    ))
    return {"messages": [reserve_message]}

# 工具：生成工单，这里涉及到在工具中使用静态上下文，在工具中使用store，需要InjectedStore注入，此为固定用法
@tool
def generate_orders(phone_number: str, id_card: str, house_title: str, runtime: ToolRuntime, store: Annotated[Any, InjectedStore()]) -> str:
    """根据用户电话，身份证，预定房源。
    Args:
        phone_number: 用户电话
        id_card: 用户身份证
        house_title: 用户预定的房源标题
        runtime: 注入工具运行时信息
        store: 注入的持久信息
    """
    # 1. 生成工单号
    order_id = str(uuid.uuid4())
    # 2. 构建预定信息
    reserved_house = ReservedInfo(
        order_id=order_id,
        phone_number=phone_number,
        title=house_title
    )
    # 3. 持久化用户偏好（预定信息）
    context = runtime.context or {}
    user_id = context.get("user_id", "anonymous")
    namespace = (user_id, "preferences")
    prefs_result = store.search(namespace)
    # 同时读取旧版本误拼写的命名空间，避免用户历史预算和订单被覆盖。
    if not prefs_result:
        prefs_result = store.search((user_id, "perferences"))
    if len(prefs_result) == 0:
        # 没有持久化信息，新增
        prefs = UserPreferences(
            reserved_info=[reserved_house]
        )
        store.put(
            namespace,
            str(uuid.uuid4()),
            prefs.model_dump(exclude_none=True)
        )
    else:
        # 有值，更新
        prefs = prefs_result[0].value or {}
        # Store 中保存普通字典，避免 Pydantic 对象在序列化或下一次读取时失真。
        prefs.setdefault("reserved_info", []).append(reserved_house.model_dump())
        store.put(
            namespace,
            prefs_result[0].key,
            prefs
        )
    # 4. 扩展：持久化工单表
    return f"已成功预定房源：{house_title}，预订单号为：{order_id}"

# 节点：生成工单结果
def call_orders(state: ReserveState):
    response = ensure_tool_call_ids(model.bind_tools([generate_orders]).invoke(
        [SystemMessage(content=(
            "你是一个工单生成助手，支持调用工具进行房源预定工单生成。"
            "若历史消息已有工具执行结果，直接向用户确认结果，绝不能再次创建工单。"
        ))]
        + state["messages"]
    ))
    return {"messages": [response]}
