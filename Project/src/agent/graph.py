from typing import Literal
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from agent.common.context import ContextSchema
from agent.node.main import get_store_info, identify_question, need_reserve, get_user_preferences
from agent.node.extend import extend_graph
from agent.recommend import recommend_graph
from agent.reserve import reserve_graph
from agent.state.main import State, NeedReserveOutput

# 构建图
builder = StateGraph(State, context_schema=ContextSchema)
builder.add_node(get_store_info)        # 查询持久化消息
builder.add_node(identify_question)     # 识别用户输入的问题
builder.add_node("recommend_graph", recommend_graph)   # 推荐房源子图
builder.add_node("reserve_graph", reserve_graph)       # 预定房源子图
builder.add_node("extend_graph", extend_graph)         # 扩展子图
builder.add_node(need_reserve)                           # 询问是否预定
builder.add_node(get_user_preferences)

builder.add_edge(START, "get_store_info")
builder.add_edge("get_store_info", "identify_question")  # 识别问题

# 路由1：智能识别问题
def route_user_intent(state: State) -> Literal["recommend_graph", "reserve_graph", "extend_graph", "get_user_preferences"]:
    user_intent = state["user_intent"]
    if user_intent == "recommend_house":
        return "recommend_graph"
    elif user_intent == "reserve_house":
        return "reserve_graph"
    elif user_intent == "get_info":
        return "get_user_preferences"
    else:
        return "extend_graph"

builder.add_conditional_edges(
    "identify_question",  # 消息路由
    route_user_intent,
    ["recommend_graph", "reserve_graph", "extend_graph", "get_user_preferences"]
)

# 路由2：只有推荐子图确认查到房源后，才询问是否预订。
def route_after_recommendation(state: State) -> Literal["need_reserve", END]:
    if state.get("recommendation_found"):
        return "need_reserve"
    return END


builder.add_conditional_edges(
    "recommend_graph",
    route_after_recommendation,
    ["need_reserve", END],
)

def should_reserve(state: NeedReserveOutput) -> Literal[END, "reserve_graph"]:
    reserve = state["reserve"]
    if reserve == '需要':
        return "reserve_graph"
    else:
        return END

builder.add_conditional_edges(
    "need_reserve",
    should_reserve,  # 不需要预定就结束对话
    [END, "reserve_graph"]
)

# 路由2：预定房源
builder.add_edge("reserve_graph", END)

# 路由3：查询我的信息
builder.add_edge("get_user_preferences", END)

# 路由4：其它
builder.add_edge("extend_graph", END)

graph = builder.compile()
