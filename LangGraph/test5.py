# checkpoint不支持跨会话消息存储，各个会话之间的消息是隔离的，不能直接使用上一个会话的消息作为下一个会话的输入。
import os
import operator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.store.postgres import PostgresStore
from pydantic import BaseModel, Field
from typing import Optional,Annotated
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from langchain_ollama import OllamaEmbeddings
load_dotenv()
from langgraph.store.memory import InMemoryStore
import uuid
# 这里来演示store的用法
# 内存级store
store=InMemoryStore()
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest",
)
store=InMemoryStore(
    index={
        "embed":embeddings,
        "dims": 4096,
        "fields":["$"] # 这里的$表示存储的内容是任意对象，支持字典、列表、字符串等
    }
)
user_id="user_1"
# 命名空间
namespace=("user_1", "session_1")  # 可以用元组表示命名空间，表示文件夹
store.put(namespace=namespace,key=str(uuid.uuid4()),value={"key":"value"})
# 记忆读取，查询 namespace 以及其子 namespace 下的所有存储项
all_memories=store.search(namespace)
# 还可以支持语义搜索
all_memories=store.search(("user_1", "session_1"),query="important",limit=1)  # 语义搜索，返回与query语义相关的记忆对象
for mem in all_memories:
    print(mem.dict())  # 记忆对象转成字典查看

# postgres store
DB_URI = "postgresql://postgres:dairenwen1092@127.0.0.1:5432/postgres"
with (PostgresSaver.from_conn_string(DB_URI) as checkpointer,
      PostgresStore.from_conn_string(DB_URI) as store):

    store.setup()
    user_id = "user_1"
    namespace = ("user_1", "session_1")
    memory_id = str(uuid.uuid4())
    memory_value = {"key": "value"}
    store.put(namespace=namespace, key=memory_id, value=memory_value)
    print(store.search(namespace))


# 在langgraph中使用store
# 定义结构化输出结构
class Person(BaseModel):
    name: Optional[str]=Field(default=None,description="姓名")
    height: Optional[str]=Field(default=None,description="身高（单位米）")
    favourite_food:Optional[str]=Field(default=None,description="最喜欢的食物列表")

# 绑定结构化输出，以及绑定工具
model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
)
tool = TavilySearch(max_results=10, tavily_api_key=os.getenv("TAVILY_API_KEY"))
model_with_tools = model.bind_tools(tools=[tool])
structured_model = model.with_structured_output(
    schema=Person,
    method="json_schema",
)

# 设置状态
class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int
# 定义节点
def get_person_info(state:State,config:RunnableConfig,*,store:BaseStore):
    """通过LLM提取我的信息"""
    # 拿到store就可以进行持久化存储，同时构造namespace就需要构造namespace(user_id)，需要获取配置
    people_info=structured_model.invoke([
        SystemMessage(content="你是一个提取信息的专家，只从文本中提取我的相关信息，不能提取别人的信息，如果你不知道要提取的属性的值，属性值返回NULL")
    ] + state["messages"][-3:]) # 带上最新的三条消息

    # 将提取到的个人信息存储到store中
    user_id = config["configurable"]["user_id"]
    namespace1 = (user_id, "info")
    # 建议在put之前先查询是否已经存在
    store.put(namespace=namespace1,key=str(uuid.uuid4()),value={
        "name":people_info.name,
        "height":people_info.height,
    })
    namespace2 = (user_id, "pref")
    store.put(namespace=namespace2,key=str(uuid.uuid4()),value={
        "favourite_food":people_info.favourite_food,
    })
    return {
        "llm_calls":state.get("llm_calls", 0) + 1
    }

def llm_call(state:State,config:RunnableConfig,*,store:BaseStore):
    """LLM决定是否调用工具"""
    user_id = config["configurable"]["user_id"]
    namespace1 = (user_id, "info")
    namespace2 = (user_id, "pref")
    info_result=store.search(namespace1,limit=1) # 查询个人信息
    prefs_result=store.search(namespace2,limit=1)

    info_value = info_result[0].value
    prefs_value = prefs_result[0].value

    messages=state["messages"]
    result=model_with_tools.invoke(
        [
            SystemMessage(content=f"你是一个乐于助人的助手，支持调用工具进行搜索，调用LLM前可以参考一下信息，用户基本情况为{info_value},用户偏好情况为{prefs_value}")
        ] + messages,
    )
    return {
        "messages":[result],
        "llm_calls":state.get("llm_calls", 0) + 1
    }

def route_tools(state:State):
    """判断是否需要调用工具"""
    return tools_condition(state)

tool_node = ToolNode([tool])
memory_store = InMemoryStore()

# 构建图
builder = StateGraph(State)
builder.add_node("get_person_info", get_person_info)
builder.add_node("llm_call", llm_call)
builder.add_node("tools", tool_node)
builder.add_edge(START, "get_person_info")
builder.add_edge("get_person_info", "llm_call")
builder.add_conditional_edges(
    "llm_call",
    route_tools,
    {
        "tools": "tools",
        END: END,
    }
)
builder.add_edge("tools", "get_person_info")

# 使用内存checkpoint和内存store
graph = builder.compile(checkpointer=InMemorySaver(), store=memory_store)

# 验证：同一个user_id，不同thread_id
config_thread_1 = {
    "configurable":{
        "thread_id":"thread_1",
        "user_id":"user_1"
    }
}
config_thread_2 = {
    "configurable":{
        "thread_id":"thread_2",
        "user_id":"user_1"
    }
}

# thread_1 写入用户信息到store，同时checkpoint只记录thread_1自己的消息
result1 = graph.invoke(
    {
        "messages":[HumanMessage(content="我叫张三，身高1.82米，我最喜欢吃火锅。")],
        "llm_calls":0
    },
    config=config_thread_1
)
print("thread_1 最后一条消息:", result1["messages"][-1].content)

# thread_2 是新线程，checkpoint里没有thread_1的消息，但因为user_id相同，可以读到store中的长期记忆
result2 = graph.invoke(
    {
        "messages":[HumanMessage(content="你还记得我的身高和我喜欢吃什么吗？")],
        "llm_calls":0
    },
    config=config_thread_2
)
print("thread_2 最后一条消息:", result2["messages"][-1].content)
