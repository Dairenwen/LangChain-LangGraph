from dataclasses import dataclass
from typing import TypedDict
import os
import operator
import time
from dotenv import load_dotenv
from langchain_core.stores import InMemoryStore
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated, Literal
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph, END, MessagesState
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime, tools_condition, ToolNode
from pydantic import BaseModel, Field
from typing import Optional,Annotated
from typing_extensions import Annotated, TypedDict
from langgraph.runtime import Runtime
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage

load_dotenv()

# 时间旅行
class State(TypedDict):
    joke: str
    topic : str

model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
)

def generate_topic(state: State):
    """生成笑话主题"""
    return {
        "topic": model.invoke([
            SystemMessage(content="你是一个笑话生成专家。"),
            HumanMessage(content="请帮我生成一个笑话的主题,字数控制在十个字以内")
        ])
    }

def generate_joke(state: State):
    """生成笑话"""
    return {
        "joke": model.invoke([
            SystemMessage(content="你是一个笑话生成专家。"),
            HumanMessage(content=f"请帮我生成一个关于{state['topic']}的笑话")
        ])
    }

builder=StateGraph(State)
builder.add_sequence([generate_topic, generate_joke])
builder.add_edge(START,"generate_topic")
builder.add_edge("generate_joke",END)
graph=builder.compile(checkpointer=InMemorySaver())
config={"configurable":{"thread_id":"1"}}
# 1.先执行一次工作流
print(graph.invoke({}, config=config))
# 2.获取历史记录
states=list(graph.get_state_history(config=config))
print(states)
# 3.找到要修改的状态快照
update=states[1] # 取出生成topic后的状态快照，进行修改，注意最新生成的最靠前
print(update.values["topic"])
# 4.修改状态
new_config=graph.update_state(update.config, {"topic":"程序员的一天"})
# 5.使用新的状态快照进行重放
graph.invoke(None,new_config)

# 静态运行上下文
@dataclass
class Contextschema:
    user_id: int
    language: str = "en"
# 动态运行上下文
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_name: str
# 默认为动态运行上下文，使用runtime来定义静态运行上下文
def node(state: State,runtime:Runtime[Contextschema]):
    if runtime.context.language=="en":
        greeting = "hello"
    else:
        greeting = "你好"
    user_name=state.get("user_name","Guest")

    return {
        "messages": [SystemMessage(content=f"{greeting}, {user_name}!")]
    }
# 指定动态或静态运行上下文
builder=StateGraph(State,context_schema=Contextschema)
builder.add_node(node)
builder.add_edge(START,"node")
builder.add_edge("node",END)
graph=builder.compile(checkpointer=InMemorySaver(),store=InMemoryStore())
print(graph.invoke({"user_name":"小明"},
                   context={"user_id": 123, "language": "zh"}, # 静态运行上下文必须指明
                   config={"configurable": {"thread_id": "1"}}))

# 在工具中使用
class State(MessagesState):
    user_name: str

@dataclass
class Context:
    user_id: int

@tool
def search(runtime:ToolRuntime[Context]):
    """用来搜索天气的得力工具"""
    user_id=runtime.context.user_id
    user_name=runtime.state["user_name"] # 动态上下文也可以获取，toolruntime相当于全部的上下文
    print(f"日志记录，user_id:{user_id}, user_name:{user_name}")
    # 获取流式写入器：
    writer=get_stream_writer() # 先获取写入器
    writer(
        {
            "type":"search_tool",
            "status":"start",
            "user_name":user_name,
            "user_id":user_id
        }
    )
    search_steps = [
        {"name": "搜索1", "time": 1, "result": "晴天，"},
        {"name": "搜索2", "time": 2, "result": "15-20度"},
    ]

    all_result = "查询天气："
    for i, step in enumerate(search_steps, 1):
        writer(
            {
                "type":"search_tool",
                "status":"searching",
                "step": step["name"],
                "all_step": len(search_steps),
                "cur_step": i,
                "user_id":user_id,
                "user_name":user_name
            }
        )
        time.sleep(step["time"])
        all_result += step["result"]

    writer(
        {
            "type":"search_tool",
            "status":"end",
            "user_name":user_name,
            "user_id":user_id,
            "result": all_result
        }
    )
    return all_result

model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
)

model_with_tool=model.bind_tools([search])
def llm_call(state:State):
    writer = get_stream_writer()  # 先获取写入器
    writer(
        {
            "type": "llm_call",
            "status": "start",
            "message": "开始调用LLM",
            "content": state["messages"][-1].content,
        }
    )
    result = model_with_tool.invoke([SystemMessage(content="你支持调用工具去查询天气")] + state["messages"])
    writer(
        {
            "type": "llm_call",
            "status": "end",
            "message": "调用LLM完成",
        }
    )
    return {"messages": [result]}

builder=StateGraph(State,context_schema=Context)
builder.add_node(llm_call)
builder.add_node("tool_node",ToolNode([search]))
builder.add_edge(START,"llm_call")
builder.add_conditional_edges(
    "llm_call",
    tools_condition,
    {
        "tools":"tool_node",
        "__end__":END,
    }
)
builder.add_edge("tool_node","llm_call")
graph=builder.compile(checkpointer=InMemorySaver(),store=InMemoryStore())
print(graph.invoke({
    "messages": [HumanMessage(content="今天的天气怎么样？")],
    "user_name": "小明"},
    context={"user_id": 123},
    config={"configurable": {"thread_id": "2"}}
))

#这里演示自定义信息输出流
for chunk in graph.stream({
    "messages": [HumanMessage(content="今天的天气怎么样？")],
    "user_name": "小明"},
    context={"user_id": 123},
    config={"configurable": {"thread_id": "2"}},
    stream_mode=["updates", "custom"] # 还可以组合多种模式（如 ["updates", "custom"]），但至少必须有一个是"custom"
):
    if isinstance(chunk, tuple) and len(chunk) == 2:
        mode, data = chunk
        if mode == "custom":
            if data.get("type") == "search_tool":
                status = data["status"]
                if status == "start":
                    print(f"用户ID:{data['user_id']}, 用户名:{data['user_name']}开始调用工具...")
                elif status == "searching":
                    print(f"[{data['cur_step']}/{data['all_step']}] 正在处理：{data['step']}")
                elif status == "end":
                    print(f"调用完成！结果：{data['result']}")
            elif data.get("type") == "llm_call":
                pass
        elif mode == "updates":
            pass
    elif isinstance(chunk, dict):
        if chunk.get("custom"):
            info = chunk["custom"]
            if info.get("type") == "search_tool":
                status = info["status"]
                if status == "start":
                    print(f"用户ID:{info['user_id']}, 用户名:{info['user_name']}开始调用工具...")
                elif status == "searching":
                    print(f"[{info['cur_step']}/{info['all_step']}] 正在处理：{info['step']}")
                elif status == "end":
                    print(f"调用完成！结果：{info['result']}")
            elif info.get("type") == "llm_call":
                pass
        elif chunk.get("updates"):
            pass

# 这里演示message打印
for token_chunk,metadata in graph.stream({
    "messages": [HumanMessage(content="今天的天气怎么样？")],
    "user_name": "小明"},
    context={"user_id": 123},
    config={"configurable": {"thread_id": "2"}},
    stream_mode="messages",
):
    # 只要有LLM调用，就可以使用message进行打印，但注意如果有多个并行执行LLM输出，则可以使用元数据进行过滤打印
    node_name=metadata.get("langgraph_node","")
    if token_chunk.content and node_name=="tool_node":
        print(token_chunk.content,end="",flush=True)