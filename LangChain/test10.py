import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate


# 少样本提示词 + 结构化输出
#
# 这个例子同时解决两个问题：
#
# 1. 结构化输出：要求模型最终返回符合 Data/Pydantic 模型的数据，
#    而不是随意写一段自然语言。
# 2. 少样本提示：通过几个“文本 -> 结构化结果”的示例，告诉模型
#    什么算人物、哪些字段应该填写，以及没有相关信息时应该怎么处理。
from langchain_openai import ChatOpenAI
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.utils.function_calling import tool_example_to_messages

# 1. 定义结构化输出的格式
#
# Pydantic 模型像一张“结果表格”或一份数据契约：
# 模型最后需要返回 people 列表，列表中的每个人可以包含下面这些字段。
#
# 这能解决“模型返回结果格式不稳定”的问题。例如，我们希望得到：
# {
#     "people": [
#         {"name": "小强", "hair_color": null, ...}
#     ]
# }
# 而不是一段只能靠字符串解析的自然语言。
class Person(BaseModel):
    """一个人的信息。""" # 注意不能缺少 docstring，否则 Pydantic 会报错。
    name: Optional[str] = Field(default=None, description="这个人的名字")
    hair_color: Optional[str] = Field(default=None, description="如果知道这个人头发的颜色")
    skin_color: Optional[str] = Field(default=None, description="如果知道这个人的肤色")
    height_in_meters: Optional[str] = Field(default=None, description="以米为单位的高度")

class Data(BaseModel):
    """提取关于人的数据。"""
    people: List[Person]

# 2. 定义少样本示例
examples = [
    (
        "海洋是广阔而蓝色的。它有两万多英尺深。",
        Data(people=[]),  # 没有人物信息的情况
    ),
    (
        "小强从中国远行到美国。",
        Data(people=[
            Person(name="小强", height_in_meters=None, skin_color=None, hair_color=None),
        ]),  # 部分信息缺失的情况
    ),
    (
        "篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。",
        Data(people=[
            Person(name="王伟", height_in_meters="2.0", skin_color=None, hair_color=None),
            Person(name="李明", height_in_meters="1.7", skin_color=None, hair_color=None)
        ]),  # 两个人物都有，但只有身高信息
    ),
    (
        "大巴车上，有一个人叫小红，她的头发是黑色的，皮肤是白色的，身高一米六。",
        Data(people=[
            Person(name="小红", height_in_meters="1.6", skin_color="白色", hair_color="黑色")
        ]),  # 提供了所有信息的情况
    )
]

# 把示例转换成聊天消息
# 聊天模型看到的却是消息序列，所以这里要把每个示例转换成模型熟悉的
# “用户输入 -> AI 结构化回答”的消息形式。
# tool_example_to_messages 会帮助构造这组消息，并把结构化结果放进
# 工具调用（tool call）相关的消息中。
example_messages = []
# 遍历每个“输入文本 -> 正确结果”示例
for txt, tool_call in examples:
    if tool_call.people:
        ai_response = "检测到人"
    else:
        ai_response = "未检测到人"

    # 将一个示例转换成多条 BaseMessage，并追加到总消息列表中。
    # extend 而不是 append，是因为这个函数返回的是一个消息列表，
    # 我们要把列表中的每一条消息依次加入 example_messages。
    example_messages.extend(
        tool_example_to_messages(
            txt, [tool_call], ai_response=ai_response
        )
    )


# 定义最终提示模板
prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个提取信息的专家，只从文本中提取相关信息。如果你不知道要提取的属性的值，属性值返回null。"),
        MessagesPlaceholder("example_messages"),
        ("user", "{new_message}"),
    ]
)

# 创建模型，并启用结构化输出
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

structured_model = model.with_structured_output(
    schema=Data, # 这里传入 Pydantic 模型，告诉模型最终输出的结构化格式
    method="function_calling",
)

# 先渲染提示词，再调用结构化模型。
chain = prompt_template | structured_model


print(chain.invoke({
    "example_messages": example_messages,
    "new_message": "篮球场上，身高两米的中锋王伟默契地将球传给一米七的后卫挚友李明，完成一记绝杀。这对老友用十年配合弥补了身高的差距。",
}))
# 最后输出是一个 Data 对象，里面包含人物的身份信息

