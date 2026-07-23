# 子图的几种调用方式
from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from langchain_core.stores import InMemoryStore
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated, Literal
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt,Command

# 子图
class State(TypedDict):
    sub_1: str
    sub_2: str


def sub_node_1(state: State):
    """节点1"""
    return {"sub_1": "pass node 1"}


def sub_node_2(state: State):
    """节点2"""
    return {"sub_2": "pass node 2"}

sub_builder = StateGraph(State)
sub_builder.add_node("sub_node_1", sub_node_1)
sub_builder.add_node("sub_node_2", sub_node_2)
sub_builder.add_edge(START, "sub_node_1")
sub_builder.add_edge("sub_node_1", "sub_node_2")
sub_builder.add_edge("sub_node_2", END)
sub_graph = sub_builder.compile()

# 主图
class ParentState(TypedDict):
    parent: str  # 输入


def node_1(state: ParentState):
    return {"parent": "111" + state["parent"]}


def node_2(state: ParentState):
    """更新parent，替换为子图中的sub_2参数值"""
    result = sub_graph.invoke({})  # 直接执行子图，拿到结果，如果需要checkpoint和store，可以传入config参数
    return {"parent": "222" + result["sub_2"]}

builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)
graph = builder.compile()

for chunk in graph.stream(input={"parent": "000"}, stream_mode="updates", subgraphs=True):
    print(chunk)
# 上面的子图和主图状态不同，下面是共享模式
class Substate(TypedDict):
    sub: str # sub私有
    parent: str # 可以与主图进行共享

def sub_node_1(state: Substate):
    return {"sub": "pass node 1"}
def sub_node_2(state: Substate):
    return {"sub": "pass node 2","parent":state["parent"]+"pass node 2"}

sub_builder = StateGraph(Substate)
sub_builder.add_node("sub_node_1", sub_node_1)
sub_builder.add_node("sub_node_2", sub_node_2)
sub_builder.add_edge(START, "sub_node_1")
sub_builder.add_edge("sub_node_1", "sub_node_2")
sub_builder.add_edge("sub_node_2", END)
sub_graph = sub_builder.compile()

# 主图
class State(TypedDict):
    parent: str
def node_1(state: State):
    return {"parent": "111" + state["parent"]}

builder=StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2",sub_graph) # 直接把子图作为节点添加到主图中，需要checkpoint和store直接复用主图的
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)
graph = builder.compile()
for chunk in graph.stream(input={"parent": "111"}):
    print(chunk)


# 在子图中使用中断

class State(TypedDict):
    foo: str

# 子图
def subgraph_node_1(state: State):
    print("sub_node_1")
    return {}

def subgraph_node_2(state: State):
    print("sub_node_2")
    value = interrupt("输入值:")
    return {"foo": state["foo"] + value}

subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph_builder.add_edge("subgraph_node_2", END)
subgraph = subgraph_builder.compile()

# 主图1
# builder = StateGraph(State)
# builder.add_node("node_1", subgraph)
# builder.add_edge(START, "node_1")
# # 将子图直接当作节点添加，可以使用checkpoint和store
# graph = builder.compile(checkpointer=InMemorySaver())

# 主图2，如果是在主图的节点中调用子图，则即便存在相同的字段也互不影响
def node_1(state: State):
    print("node_1")
    # 调用子图后返回的结果是子图的最终state，和主图的foo字段没有关系
    # 子图中断再恢复，调用子图节点也会再执行一次
    result=subgraph.invoke({"foo":state["foo"]})
    return {
        "foo":result["foo"]
    }

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo":""}, config)
parent_state = graph.get_state(config)
# 访问子图状态只能在子图被中断时才可用。
# 一旦恢复了图，将无法访问子图状态。
subgraph_state = graph.get_state(config, subgraphs=True).tasks[0].state
print(subgraph_state)
print(graph.invoke(Command(resume="bar"), config))