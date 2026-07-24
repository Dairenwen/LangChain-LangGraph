from langchain_core.messages import AIMessage, SystemMessage
from langgraph.constants import START,END
from langgraph.graph import StateGraph, MessagesState
from agent.common.llm import model

def extend_node(state: MessagesState):
    response = model.invoke(
        [SystemMessage(content="你是一个乐于助人的助手，可以根据历史对话进行回复。")]
        + state["messages"]
    )
    return {
        "messages": [response]
    }

extend_graph = (
    StateGraph(MessagesState)
    .add_node(extend_node)
    .add_edge(START, "extend_node")
    .add_edge( "extend_node",END)
    .compile()
)
