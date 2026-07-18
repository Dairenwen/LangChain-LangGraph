# checkpoint不支持跨会话消息存储，各个会话之间的消息是隔离的，不能直接使用上一个会话的消息作为下一个会话的输入。
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
from langgraph.store.memory import InMemoryStore
import uuid
# 这里来演示store的用法
# 内存级store
store=InMemoryStore()
user_id="user_1"
# 命名空间
namespace=("user_1", "session_1")  # 可以用元组表示命名空间，表示文件夹
memory_id=str(uuid.uuid4())  # 同一个namespace下的不同记忆可以用不同的id区分，namespace和id组合起来就是唯一的记忆标识
memory_value={"key": "value"} # 要存储的记忆内容，可以是任意对象，比如字典、列表、字符串等
# 记忆存储
store.put(namespace=namespace,key=memory_id,value=memory_value)
# 记忆读取，查询 namespace 以及其子 namespace 下的所有存储项
all_memories=store.search(namespace)
for mem in all_memories:
    print(mem.dict())  # 记忆对象转成字典查看
