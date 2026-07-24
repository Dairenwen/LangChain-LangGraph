from langgraph.graph import StateGraph

from agent.common.context import ContextSchema
from agent.node.recommend import collect_user_info, list_table, call_get_schema, check_query, generate_query, \
    get_schema_node, run_query_node, ask_for_new_criteria
from agent.state.recommend import RecommendState
from langgraph.graph import START, StateGraph, END, MessagesState

# 构建推荐子图
builder=StateGraph(RecommendState,context_schema=ContextSchema) # 使用静态上下文
builder.add_node(collect_user_info)
builder.add_node(list_table)
builder.add_node(call_get_schema)
builder.add_node("get_schema",get_schema_node)
builder.add_node(generate_query)
builder.add_node(check_query)
builder.add_node("run_query", run_query_node)
builder.add_node(ask_for_new_criteria)

builder.add_edge(START,"collect_user_info")
builder.add_edge("collect_user_info", "list_table")
builder.add_edge("list_table", "call_get_schema")
builder.add_edge("call_get_schema", "get_schema")
builder.add_edge("get_schema", "generate_query")
def should_continue(state:RecommendState):
    last_msg=state["messages"][-1]
    if not last_msg.tool_calls:
        return END
    return "check_query"

builder.add_conditional_edges(
    "generate_query",
    should_continue,
    [END,"check_query"]
)

builder.add_edge("check_query","run_query")
builder.add_edge("run_query", "ask_for_new_criteria")


def route_after_query(state: RecommendState):
    if state.get("search_cancelled"):
        return END
    if state.get("recommendation_found"):
        # 查询结果已经确认非空，再交由模型组织推荐文案。
        return "generate_query"
    # interrupt 恢复后带着用户的新条件重新收集并查询。
    return "collect_user_info"


builder.add_conditional_edges(
    "ask_for_new_criteria",
    route_after_query,
    [END, "generate_query", "collect_user_info"],
)
recommend_graph=builder.compile() # langgraph dev默认带上内存checkpoint和内存store
