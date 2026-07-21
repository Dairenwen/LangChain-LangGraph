from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph, END, MessagesState

# 初始化带标签的模型
joke_model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
).with_config(tags=["joke"])# 给模型添加标签

poem_model = ChatOpenAI(
    model="gpt-5.5",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
).with_config(tags=["poem"])# 给模型添加标签

class CreativeState(TypedDict):
    topic: str
    joke: str
    poem: str

# 由于中转站与官方的api的返回格式不同，这里需要做一下处理
def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return ""


def generate_creative_content(state: CreativeState):
    """同时生成笑话和诗歌"""
    topic = state["topic"]

    # 生成笑话
    print(f"\n生成关于 {topic} 的笑话: ")
    joke_response = joke_model.invoke([
        {"role": "user", "content": f"讲一个关于 {topic} 的笑话"}
    ])

    # 生成诗歌
    print(f"\n生成关于 {topic} 的诗歌: ")
    poem_response = poem_model.invoke([
        {"role": "user", "content": f"写一首关于 {topic} 的短诗"}
    ])

    return {
        "joke": joke_response.content,
        "poem": poem_response.content
    }


# 构建图
builder = StateGraph(CreativeState)
builder.add_node("creative", generate_creative_content)
builder.add_edge(START, "creative")
graph = builder.compile()

# 流式输出并过滤
for token_chunk, metadata in graph.stream(
    {"topic": "猫"},
    stream_mode="messages"
):
    # 只输出笑话相关的 Tokens
    tags = metadata.get("tags", [])

    if "joke" in tags:
        print(extract_text(token_chunk.content), end="", flush=True)
    # 也可以过滤诗歌
    # if "poem" in tags:
    #     print(token_chunk.content, end="", flush=True)

##################################################################


model = ChatOpenAI(model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1"
)

class State(TypedDict):
    query: str
    summary: str
    translation: str


def extract_text(content):
    # 中转站/`responses/v1` 可能返回结构化块，而不是直接返回纯字符串。
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


def generate_summary(state: State):
    """生成摘要"""
    response = model.invoke([
        {"role": "user", "content": f"请为以下内容生成摘要：{state['query']}"}
    ])
    return {"summary": response.content}


def generate_translation(state: State):
    """生成翻译"""
    response = model.invoke([
        {"role": "user", "content": f"请将以下内容翻译成英文：{state['query']}"}
    ])
    return {"translation": response.content}


# 构建并行处理图
builder = StateGraph(State)
builder.add_node("summarize", generate_summary) # 这里来指定节点名称
builder.add_node("translate", generate_translation)

builder.add_edge(START, "summarize")
builder.add_edge(START, "translate")
builder.add_edge("summarize", END)
builder.add_edge("translate", END)

graph = builder.compile()

# 流式输出并只显示某个节点的 Tokens
target_node = "summarize" # 可以改为 "translate"
printed_prefix = False
for token_chunk, metadata in graph.stream(
    {"query": "人工智能是计算机科学的一个分支，致力于创造能够执行通常需要人类智能的任务的机器。"},
    stream_mode="messages"
):
    # 获取节点名称
    node_name = metadata.get("langgraph_node", "")

    # 只输出目标节点的 Tokens
    if token_chunk.content and node_name == target_node:
        # 添加节点标签
        if node_name == "translate":
            prefix = "【翻译】"
        elif node_name == "summarize":
            prefix = "【摘要】"
        else:
            prefix = ""

        if not printed_prefix and prefix:
            print(prefix, end="", flush=True)
            printed_prefix = True
        print(extract_text(token_chunk.content), end="", flush=True)