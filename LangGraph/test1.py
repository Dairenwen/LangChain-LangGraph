# 正式开始LangGraph
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage, AnyMessage, filter_messages
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
load_dotenv()
# langgraph设计的流程是：状态定义->节点定义->定义图->添加节点->添加边->运行图
# 1.状态定义
import operator
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field
class PackageState(TypedDict):
    package_id: int             # 包裹id
    origin: str                 # 包裹起点
    destination: str            # 包裹终点
    status: str                 # 包裹状态
    # history: list[str]          # 包裹状态历史记录，这样是覆盖更新
    history_append: Annotated[list[str], operator.add]  # 包裹状态历史记录，这样是追加更新
    priority: str               # 包裹优先级
#                                  加急配送
#                                /         \
# 整个流程初步定义为：揽收站->分拣中心            派送站
#                                \         /
#                                  标准配送
# 2.节点定义

# 揽收站节点
def receive_package(state: PackageState):
    origin = state["origin"]
    return {
        "status": "已揽收",
        "history_append": [f"包裹已从{origin}揽收"],
    }
# 分拣中心节点：根据目的地进行分拣
def sort_package(state: PackageState):
    """分拣中心"""
    destination = state["destination"]
    if destination in ["北京", "上海", "广州"]:
        return {
            "status": "已分拣",
            "history_append": [f"包裹已分拣到{destination}"],
        }
    else:
        return {
            "status": "已分拣",
            "history_append": [f"包裹已分拣到其他城市"],
        }
# 配送站节点
def final_delivery(state: PackageState):
    """派送站"""
    destination = state["destination"]
    return {
        "status": "已派送",
        "history_append": [f"包裹已派送到{destination}"],
    }
# 标准配送节点
def standard_delivery(state: PackageState):
    """标准配送"""
    return {
        "status": "已派送",
        "history_append": [f"包裹正在标准配送"],
    }
# 加急配送节点
def express_delivery(state: PackageState):
    """加急配送"""
    return {
        "status": "已派送",
        "history_append": [f"包裹正在加急配送"],
    }

# 3.定义图
delivery=StateGraph(PackageState)

# 4.添加节点
delivery.add_node("揽收站", receive_package)
delivery.add_node("分拣中心", sort_package)
delivery.add_node("派送站", final_delivery)
delivery.add_node("标准配送", standard_delivery)
delivery.add_node("加急配送", express_delivery)

# 5.添加边
# 固定边
delivery.add_edge(START, "揽收站")
delivery.add_edge("揽收站", "分拣中心")
# 条件边
def select_delivery(state: PackageState):
    """根据包裹的优先级选择配送方式"""
    if state["priority"] == "加急":
        return "加急配送"
    else:
        return "标准配送"
delivery.add_conditional_edges(
    "分拣中心",
    select_delivery, # 确定下一个节点名称的函数
    ["标准配送", "加急配送"], # 可能的下一个节点名称列表
)
delivery.add_edge("标准配送", "派送站")
delivery.add_edge("加急配送", "派送站")
delivery.add_edge("派送站", END)

# 6.编译图
delivery_system=delivery.compile()
# 7.运行图
result = delivery_system.invoke({
    "package_id": 1,
    "origin": "深圳",
    "destination": "北京",
    "priority": "加急",
    "history_append": [],
})
print(result)

# 示例二：
# class MessageState(TypedDict):
#     # 消息列表：
#     # 1.会话记忆，记录对话历史；2.上下文维护，方便获取上下文信息；3.消息发送，记录消息发送状态
#     messages: Annotated[list[str], operator.add]  # 上下文消息列表
#     # 调用LLM次数
#     llm_call_count: int

# 0.定义模型和搜索工具
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)
tool = TavilySearch(max_results=10, tavily_api_key=os.getenv("TAVILY_API_KEY"))
tools=[tool]
model_with_tools = model.bind_tools(tools=tools)
# 1.状态定义
class MessageState(TypedDict):
    messages: Annotated[list[str], add_messages]  # 上下文消息列表
    llm_call_count: Annotated[int, operator.add]  # 调用LLM次数

# 2.节点定义
def llm_call(state: MessageState):
    """调用LLM"""
    messages = state["messages"]
    # 调用模型
    response = model_with_tools.invoke(
        input=[
            SystemMessage(content="你是一个有帮助的助手。"),
        ]+messages
    )
    return {
        "messages": [response],  # 将模型的响应添加到消息列表中
        "llm_call_count": 1,  # 调用次数加1
    }


tools_by_name ={tool.name: tool for tool in tools}
def tool_node(state: MessageState):
    """调用工具"""
    messages = state["messages"]
    # 调用工具
    result=[]
    # 当前最新消息就是带有tool_calls的AIMessage
    # tool_call["name"] 说明调用哪个工具
    # tool_call["args"] 说明传什么参数
    # tool_call["id"]   说明这是哪一次调用
    for tool_call in messages[-1].tool_calls:
        tool=tools_by_name[tool_call["name"]]
        obs=tool.invoke(tool_call["args"])
        result.append(ToolMessage(tool_call_id=tool_call["id"], content=obs))

    return {
        "messages": result,  # 将工具的响应添加到消息列表中
        "llm_call_count": 0,  # 工具调用不增加LLM调用次数
    }

# 3.定义图
agent_builder=StateGraph(MessageState)
agent_builder.add_node("LLM调用", llm_call)
agent_builder.add_node("工具调用", tool_node)
# 4.添加边
agent_builder.add_edge(START, "LLM调用")

def should_continue(state: MessageState):
    """判断是否继续调用LLM"""
    messages = state["messages"]
    # 如果最新消息是AIMessage，并且包含tool_calls，则继续调用工具
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        return "工具调用"
    else:
        return END

agent_builder.add_conditional_edges(
    "LLM调用",
    should_continue,
    ["工具调用", END],
)
agent_builder.add_edge("工具调用", "LLM调用")
# 5.编译图
agent=agent_builder.compile()
# 6.运行图
# result = agent.invoke({
#     "messages":[
#         HumanMessage(content="请帮我查询武汉的天气情况。")
#     ],
#     "llm_call_count": 0,
# })
# 其实可以画出mermaid图出来
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
try:
    # 生成 Mermaid 图表并保存为图片
    mermaid_code = agent.get_graph(xray=True).draw_mermaid_png()
    # 保存文件
    graph_path = Path(__file__).resolve().parents[1] / "jpg/graph1.jpg"
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    with open(graph_path, "wb") as f:
        f.write(mermaid_code)

    #使用 matplotlib 显示图像
    img = mpimg.imread(graph_path)
    plt.imshow(img)  # 显示图片
    plt.axis('off')  # 关闭坐标轴
    # plt.show()       # 弹出窗口显示图片
except Exception as e:
    print(f"An error occurred: {e}")


# 示例三
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.tools.retriever import create_retriever_tool

# 聊天模型与嵌入模型
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest",
)

# 加载文档列表
paths = [
    Path(__file__).resolve().parents[1] / "Docs/markdown/UML建模.md",
]
docs_list = [UnstructuredMarkdownLoader(str(path)).load() for path in paths]
docs = [item for sublist in docs_list for item in sublist]

# from tiktoken_token_encoder: 使用 tiktoken 编码器来计算长度的文本分割器。
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000,
    chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs)

# 使用内存中向量存储(还可以选择redis和pinecone等)来存储文档向量
vectorstore = InMemoryVectorStore.from_documents(
    documents=doc_splits,
    embedding=embeddings
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 使用 LangChain 的预构建 create_retriever_tool 创建检索器工具:
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="uml_docs_retriever",
    description="检索本地 UML建模.md 文档，用于回答 UML、建模图、类图、用例图等相关问题。",
)

# print(retriever_tool.invoke({"query": "UML是什么？"}))

# 可以直接定义节点
def generate_query_or_respond(state: MessageState):
    """调用模型以基于当前状态生成响应"""
    result=model.bind_tools(tools=[retriever_tool]).invoke(state["messages"])
    return {
        "messages": [result],
    }
# 工具节点
retriever_node=ToolNode([retriever_tool], name="检索器工具节点")
# 重写节点
REWRITE_PROMPT = (
    "查看输入并尝试推断潜在的语义意图/含义。\n"
    "这是最初的问题:\n"
    "\n"
    "<question>\n"
    "{question}\n"
    "</question>\n"
    "提出一个改进后的问题: "
)
def rewrite_question(state: MessagesState):
    """重写原始用户问题"""
    # state["messages"]中第一个消息是用户的原始问题，包含H、A、T
    # 重写就是要模范返回的新问题转换为HumanMessage，再让模型生成答案
    question = state["messages"][0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = model.invoke([HumanMessage(content=prompt)])
    return {"messages": [{"role": "user", "content": response.content}]}

# 生成答案
GENERATE_PROMPT = (
    "你是负责回答问题的助手。 "
    "使用以下检索到的上下文片段来回答问题。 "
    "如果你不知道答案，就说你不知道。 "
    "最多只用三句话，回答要简明扼要。\n"
    "Question: {question} \n"
    "Context: {context}"
)

def generate_answer(state: MessagesState):
    """生成答案"""
    # 最原始问题
    question = state["messages"][0].content
    # 最新问题的检索结果，是ToolMessage
    context = state["messages"][-1].content
    prompt = GENERATE_PROMPT.format(question=question, context=context)
    # 让模型根据开始的问题和检索到的上下文生成答案
    response = model.invoke([HumanMessage(content=prompt)])
    return {"messages": [response]}

# 3.定义图
workflow=StateGraph(MessageState)
workflow.add_node("是否需要检索", generate_query_or_respond)
workflow.add_node("重写问题", rewrite_question)
workflow.add_node("检索器工具节点", retriever_node)
workflow.add_node("生成答案", generate_answer)
workflow.add_edge(START, "是否需要检索")
workflow.add_conditional_edges(
    "是否需要检索",
    tools_condition, #langgraph提供的工具条件函数，判断是否包含tool_calls
    {
        "tools": "检索器工具节点",
        "__end__":END,
    }
)


GRADE_PROMPT = (
    "你是一个评分员，评估检索到的文档与用户问题的相关性。 \n "
    "以下是检索到的文档: \n {context} \n\n"
    "以下是用户的问题: {question} \n"
    "如果文档包含与用户问题相关的关键字或语义，则将其评为相关。\n"
    "给出一个二元分数“yes”或“no”，以表明该文档是否与问题相关。"
)

class GradeDocuments(BaseModel):
    """对检索到的文档进行相关性检查。"""
    score: str = Field(
        description="相关性评分: 如果相关则为\"yes\", 如果不相关则为\"no\""
    )

def grade_documents(state: MessagesState)->Literal["重写问题", "生成答案"]:
    """检索到的内容是否合格"""
    # 取出最新的用户消息和检索到的内容
    user_message=filter_messages(state["messages"], include_types="human")
    question = user_message[-1].content
    context = state["messages"][-1].content
    prompt = GRADE_PROMPT.format(question=question, context=context)
    # 将检索到的内容和用户问题转换为humanMessage传给模型进行评分
    response = model.with_structured_output(
        GradeDocuments,
        method="function_calling"
    ).invoke([HumanMessage(content=prompt)])
    score = response.score

    if score == "yes":
        return "生成答案"
    else:
        return "重写问题"

workflow.add_conditional_edges(
    "检索器工具节点",
    grade_documents,
    ["重写问题", "生成答案"],
)

workflow.add_edge("生成答案", END)
workflow.add_edge("重写问题", "是否需要检索")

# 编译图
workflow_system=workflow.compile()

# 运行图（进行流式输出）
for chunk in workflow_system.stream(
    {
        "messages":[
            HumanMessage(content="请帮我查询UML的相关知识。")
        ]
    }
):
    print(chunk)
