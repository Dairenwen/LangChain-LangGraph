from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, trim_messages, filter_messages, \
    merge_message_runs
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

# model = ChatOpenAI(
#     model="qwen3.6-27b-base",
#     temperature=0,
#     api_key="not-needed",
#     base_url="http://192.168.247.161:8000/v1",
# )
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key="YOUR_PACKYAPI_API_KEY",
    base_url="https://www.packyapi.com/v1",
)


# 这里来实现多轮对话，根据对话id来查询会话里的消息列表

store = {}  # 用于存储对话消息，key为对话id，value为消息列表
# 根据会话id查找会话的历史记录
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory() # 如果没有这个会话id，就创建一个新的InMemoryChatMessageHistory实例
    return store[session_id] # 返回这个会话id对应的InMemoryChatMessageHistory实例

# 包装了model，让model具备存储历史消息的能力
with_history_message_model=RunnableWithMessageHistory(model, get_session_history)

# 第一轮对话
response1 = with_history_message_model.invoke(
    input=[HumanMessage("你好，我是一名程序员")],
    config={"configurable": {"session_id": "1"}}
)
# print("第一轮:", response1.content)

# 第二轮对话（同一个 session_id，模型能记住上一轮说过的话）
response2 = with_history_message_model.invoke(
    input=[HumanMessage("我刚才说我的职业是什么？")],
    config={"configurable": {"session_id": "1"}}
)
# print("第二轮:", response2.content)


# 使用trim来进行消息裁剪
messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
    HumanMessage(content="What's my name?"),
]

# 使用 trim_messages 减少发送给模型的消息数量
trimmer = trim_messages(
    max_tokens=65,        # 修剪消息的最大令牌数，根据你想要的谈话长度来调整
    strategy="last",      # 修剪策略:
                          # "last"(默认)：保留最后的消息。
                          # "first": 保留最早的消息。
    token_counter=len,  # 传入一个函数或一个语言模型（因为语言模型有消息令牌计数方法） 如果要基于消息数量裁剪，就指定为len
    include_system=True,  # 如果想始终保留初始系统消息，可以指定 include_system=True
    allow_partial=False,  # 是否允许拆分消息的内容
    start_on="human",     # 如果需要确保我们的第一条消息（不包括系统消息）始终是特定类型，可以指定 start_on
    end_on="human", # 最后一条消息以human消息结尾
)

chain = trimmer | model # 一定要先裁剪消息，再发给model
# print(chain.invoke(messages))

messages = [
    SystemMessage("你是一个聊天助手", id="1"),
    HumanMessage("示例输入", id="2"),
    AIMessage("示例输出", id="3"),
    HumanMessage("真实输入", id="4"),
    AIMessage("真实输出", id="5"),
]

# 按照类型进行筛选：
# print(filter_messages(messages,include_types="human"))
# 按照ID来进行筛选：
# print(filter_messages(messages,exclude_ids=["1"]))
# 按照类型+ID进行筛选
# print(filter_messages(messages,include_types=[HumanMessage,AIMessage],exclude_ids=["3"]))


# merge_message_runs：合并连续的同类消息，减少消息数量
messages = [
    SystemMessage("你是一个聊天助手。"),
    SystemMessage("你总是以笑话回应。"),
    HumanMessage("为什么要使用 LangChain?"),
    AIMessage("因为当你试图让你的代码更有条理时，LangGraph 会让你感到“节点”是个好主意！"),
    AIMessage("不过别担心，它不会分散你的注意力！"),
    AIMessage("选择LangChain还是LangGraph?"),
]

# 方式一：带参数调用 → 直接返回合并后的列表，再用 model.invoke()
merged_result = merge_message_runs(messages)  # 传 messages → 返回 list
print("合并后:", merged_result)
model.invoke(merged_result).pretty_print()

# 方式二：不带参数 → 返回 Runnable，可以用 | 串进链
merger = merge_message_runs()  # 不传参 → 返回 Runnable
chain = merger | model
chain.invoke(messages).pretty_print()
