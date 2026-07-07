from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated


# 第一步：定义工具函数（@tool 装饰器自动生成工具描述和参数 schema）
@tool
def add(
    a: Annotated[int, ..., "first int"],
    b: Annotated[int, ..., "second int"]
) -> int:
    """两数相加"""
    return a + b


@tool
def multiply(
    a: Annotated[int, ..., "first int"],
    b: Annotated[int, ..., "second int"]
) -> int:
    """两数相乘"""
    return a * b



# 第二步：创建模型
model = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com/v1",
)

# bind_tools 的作用：把工具列表注入到每次 API 请求中，
# 告诉模型"你可以用这些工具"。此后模型看到需要计算的问题，就不会瞎编答案，而是返回 tool_calls。
model_with_tools = model.bind_tools(tools=[add, multiply])


# 第三步：两轮对话完成"工具调用 + 自然语言回答"
messages = [
    HumanMessage("3乘4等于多少？3加4又等于多少？")
]

# --- 第 1 轮：模型判断"需要什么工具" ---
# 模型看到自己绑了 add/multiply，判断"这个问题需要计算"，
# 所以不会直接回答，而是返回 AIMessage，其中 content 可能是一句过渡语，
# tool_calls 里装了调用计划。
ai_msg = model_with_tools.invoke(input=messages)
messages.append(ai_msg)

# --- 中间环节：执行工具 ---
for tool_call in ai_msg.tool_calls:
    # tool_call = {"name": "add", "args": {"a": 3, "b": 4}, "id": "call_xxx"}
    # 选择对应的工具
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    # ① invoke(tool_call) → 工具内部自动提取 tool_call["args"] 作为函数参数
    # ② 执行函数 add(3, 4) → 得到 7
    # ③ 因为 tool_call 里有 "id" 字段，工具自动把 7 包装成：
    #    ToolMessage(content="7", tool_call_id="call_xxx")
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# 此时 messages = [
#     HumanMessage("3乘4等于多少？..."),
#     AIMessage(tool_calls=[add(3,4), multiply(3,4)]),
#     ToolMessage(content="7",  tool_call_id="call_xxx"),  ← 自动生成的
#     ToolMessage(content="12", tool_call_id="call_yyy"),  ← 自动生成的
# ]

# --- 第 2 轮：模型根据工具结果，组织自然语言回答 ---
# 用裸 model，不需要再调工具，纯做文本生成
print(model.invoke(messages).content)
