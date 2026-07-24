from typing import Literal

from langchain_core.messages import SystemMessage, HumanMessage, filter_messages, AIMessage
from langgraph.runtime import Runtime
from langgraph.store.base import BaseStore
from langgraph.types import interrupt
from pydantic import BaseModel, Field

from agent.common.context import ContextSchema
from agent.common.llm import model
from agent.common.store import UserProfile
from agent.state.main import State, NeedReserveOutput

class UserMessage(BaseModel):
    """用户提问的消息摘要"""
    type: Literal["recommend_house", "reserve_house", "get_info", "others"] = (
        Field(description="根据用户问题描述判断问题类型：推荐房源、预定房源、获取信息、其他内容")
    )


# 节点：识别用户问题：预定、推荐、我的，进行一个路由功能
def identify_question(state: State) -> State:

    def extract_info(messages) -> UserMessage:
        system_message = SystemMessage(
            content="""
你是一个根据描述提取信息提取专家。请从用户的描述中提取用户想要咨询的相关信息。
请严格根据语义推断信息，但不能猜测或编造信息。"""
        )
        # 创建结构化提取模型
        return (model.with_structured_output(schema=UserMessage)
                .invoke([system_message] + messages))

    # 最新的用户消息
    user_question = state["messages"][-1].content
    user_message = extract_info([HumanMessage(content=user_question)])
    return {"user_intent": user_message.type}

# 节点：查询持久化消息
def get_store_info(state: State, runtime: Runtime[ContextSchema], *, store: BaseStore):
    # 用户档案与偏好都写入由 Agent Server 注入的 BaseStore。Docker 部署时
    # BaseStore 由 PostgreSQL 支撑，线程状态和跨会话偏好均可在服务重启后恢复。
    context = runtime.context or {}
    user_id = context.get("user_id", "anonymous")
    profile_namespace = (user_id, "profile")
    profile_item = store.get(profile_namespace, "profile")
    if profile_item:
        profile = UserProfile.now(
            user_id,
            first_seen_at=profile_item.value.get("first_seen_at"),
            conversation_count=int(profile_item.value.get("conversation_count", 0)),
        )
    else:
        profile = UserProfile.now(user_id, conversation_count=1)
    store.put(profile_namespace, "profile", profile.model_dump())

    # 查询跨线程的租房偏好。
    namespace = (user_id, "preferences")
    pref_result = store.search(namespace)
    # 兼容早期版本误写为 "perferences" 的已保存数据。
    if not pref_result:
        pref_result = store.search((user_id, "perferences"))
    if pref_result and pref_result[0]:
        return {"user_preferences": pref_result[0].value}
    else:
        return {}

# 节点：中断询问是否主要帮助预定房源，注意这里返回的是私有状态
def need_reserve(state: State) -> NeedReserveOutput:
    prompt = "已经为您推荐合适的房源，是否需要帮您预订房源？\n"
    prompt += "如果不需要，请输入‘不需要’。\n"
    prompt += "如果需要，请输入‘需要’。\n"
    while True:
        answer = str(interrupt(prompt)).strip()
        if answer in {"需要", "不需要"}:
            return {"reserve": answer}
        prompt = "请输入‘需要’或‘不需要’。"

# 节点：返回用户偏好信息
def get_user_preferences(state: State):
    prefs = state.get("user_preferences", {})
    user_messages = filter_messages(state["messages"], include_types="human")

    # 格式化已预定过的信息
    reserved_list = prefs.get('reserved_info', [])

    if reserved_list:
        reserved_str = "\n"
        for i, item in enumerate(reserved_list, 1):
            if hasattr(item, "model_dump"):
                item = item.model_dump()
            reserved_str += f"{i}. 预定工单ID：{item.get('order_id')}, " \
                            f"房源标题：{item.get('title')}, " \
                            f"预定电话：{item.get('phone_number')}\n"
    else:
        reserved_str = "无"

    response = model.invoke([
        SystemMessage(content="""你是一个乐于助人的助手，可以根据用户偏好信息进行回复。
如果有的偏好数据为空，不要猜测或编造数据。
不要直接回复偏好数据是什么，要结合问题进行主动回复。
如果问题与用户偏好数据无关，直接回复即可。"""),
        HumanMessage(
            content="用户的历史偏好信息如下："
                    f"1. 最低预算：{prefs.get('budget_min')}"
                    f"2. 最高预算：{prefs.get('budget_max')}"
                    f"3. 已预定过的信息：{reserved_str}"
        ),
        user_messages[-1] # 还需要获取最新的消息
    ])
    return {"messages": [response]}
