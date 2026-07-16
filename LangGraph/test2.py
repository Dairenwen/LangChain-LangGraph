# 介绍langgraph新特性
import operator
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import Overwrite

class State(TypedDict):
    messages: Annotated[list[str], operator.add]
def add_messages(state: State):
    return {
        "messages": ["Hello, world!"]
    }
def overwrite_messages(state: State):
    return {
        "messages": Overwrite(["Goodbye, world!"])
    }

builder = StateGraph(State)
builder.add_node(add_messages)
builder.add_node(overwrite_messages)
builder.add_edge(START, "add_messages")
builder.add_edge("add_messages", "overwrite_messages")
builder.add_edge("overwrite_messages", END)

workflow=builder.compile()
print(workflow.invoke({
    "messages": []
}))


# 单独定义输入输出
from typing_extensions import TypedDict

# 1. 定义输入模式 - 只包含用户问题
class InputState(TypedDict):
    question: str

# 2. 定义输出模式 - 只包含AI答案
class OutputState(TypedDict):
    answer: str

# 3. 定义完整状态模式（内部使用）
class OverallState(InputState, OutputState):
    pass # 表示内部状态同时包含输入和输出字段

def answer_node(state: InputState):
    """处理输入并生成答案"""
    # 这里可以访问 question，生成 answer
    return {
        "answer": f"Answer to: {state['question']}",
        "question": state["question"]
    }

# 构建图时指定输入输出模式
builder = StateGraph(
    OverallState,
    input_schema=InputState,    # 输入验证
    output_schema=OutputState   # 输出过滤
)
builder.add_node("answer_node", answer_node)
builder.add_edge(START, "answer_node")
builder.add_edge("answer_node", END)
graph = builder.compile()

# 测试
result = graph.invoke({"question": "What is LangGraph?"})
print(result)  # 输出: {'answer': 'Answer to: What is LangGraph?'}
# 注意: question 字段被过滤掉了，不在输出中


