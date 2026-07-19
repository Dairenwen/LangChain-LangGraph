import os
import operator
from dotenv import load_dotenv
from langchain_core.messages import RemoveMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import REMOVE_ALL_MESSAGES

load_dotenv()
from langchain_core.messages.utils import trim_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, MessagesState,END

# 消息裁剪
model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
)
# MessagesState 已经内置了一个 messages 字段
def call_model(state: MessagesState):
    # 只保留最近的128个token的消息
    messages = trim_messages(
        state["messages"],
        strategy="last",        # 策略: 保留最后的部分
        token_counter=model,    # 计算token数量
        max_tokens=128,         # 最大token数
        start_on="human",  # 从用户消息开始
        end_on=("human","tool")  # 结束于用户消息或工具消息
    )
    response = model.invoke(messages)
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node(call_model)
builder.add_edge(START, "call_model")
builder.add_edge("call_model",END)
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "1"}}
graph.invoke({"messages": "hi, my name is bob"}, config)
graph.invoke({"messages": "write a short poem about dogs"}, config)
graph.invoke({"messages": "now do the same but for cats"}, config)
final_response = graph.invoke({"messages": "what's my name?"}, config)
final_response["messages"][-1].pretty_print() # 找不到历史消息，所以模型无法记住之前的对话内容


# 删除消息

# 根据消息id删除state中的指定消息，RemoveMessage只能删除带有add_messages的消息,
# 而MessagesState中的messages字段已经内置了add_messages，所以可以直接使用RemoveMessage
def call_model(state: MessagesState):
    messages = state["messages"]

    if len(messages) > 6:
        # 删除最早的6条消息
        return {
            "messages": [RemoveMessage(id=m.id) for m in messages[:6]]
            # "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES)] 代表删除所有历史对话
        }

    response = model.invoke(messages)
    return {"messages": [response]}
# 。。。。。
# 测试: 可以发现只剩最后一条消息了
for message in final_response["messages"]:
    message.pretty_print()

# 每次聊天后自动总结，压缩上下文
class State(MessagesState):
    summary: str

def call_model(state: State):
    """调用模型，带上总结+用户问题生成AI回复"""
    # 使用历史总结+最新消息发起调用
    summary = state.get("summary", "")
    messages = [HumanMessage(content=summary)] + state["messages"]
    return {"messages": [model.invoke(messages)]}

def summarize_conversation(state: State):
    """根据旧summary+最新消息生成新的summary"""
    # 生成历史总结
    # 1. 创建总结提示词
    summary = state.get("summary", "")
    if summary:  # 有摘要（扩展）
        summary_message = (
            f"这是到目前为止的对话摘要: {summary}\n\n"
            "基于上面的新消息扩展摘要: "
        )
    else:    # 无摘要，新增
        summary_message = "创建上面对话的摘要: "

    # 2. 生成新总结: 消息列表 + 历史总结 调用模型
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # 3. 删除历史对话: 除了最新的AI消息，都可以删除
    return {
        "summary": response.content,  # 历史总结
        "messages": [RemoveMessage(id=m.id) for m in state["messages"][:-1]]  # 保留最后的消息是为了打印结果
    }


builder = StateGraph(State)
builder.add_node(call_model)
builder.add_node("summarize", summarize_conversation)
builder.add_edge(START, "call_model")
builder.add_edge("call_model", "summarize")  # 每次对话完，进行总结
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "1"}}
graph.invoke({"messages": "hi, my name is bob"}, config)
graph.invoke({"messages": "write a short poem about dogs"}, config)
graph.invoke({"messages": "now do the same but for cats"}, config)
final_response = graph.invoke({"messages": "what's my name?"}, config)
print("\n=========== final response ===========")
print(final_response["messages"][-1].content)
print("\n=========== summary ===========")
print(final_response["summary"])

# 打印结果如下:
# =================================== Ai Message
# Your name is Bob.
#
# Summary: 对话摘要: 用户自我介绍为Bob，并询问如何获得帮助。随后，用户请求写一首关于猫的短诗。接着，用户又请求写一首关于狗的短诗。用户对动物诗歌表现出兴趣，可能希望进一步采访与宠物相关的主题或创作。
