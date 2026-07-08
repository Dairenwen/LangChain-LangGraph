from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from typing import Optional, Union
from typing_extensions import Annotated, TypedDict

# 返回 Pydantic 对象
search_model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key="YOUR_PACKYAPI_API_KEY",
    base_url="https://www.packyapi.com/v1",
)

# 定义消息列表
search_msg = [
    SystemMessage("你是一个有帮助的助手。"),
    HumanMessage("请帮我搜索一下广西南宁的天气情况，以及那里发生了什么重大事件？")
]

# 定义返回的结构化格式
class SearchOutput(BaseModel):
    """搜索结果"""
    weather: str = Field(..., description="广西南宁的天气情况")
    events: str = Field(..., description="广西南宁发生的重大事件")
    rating: Optional[int] = Field(..., description="从1-10给事件严重等级评分")

model_with_structure = search_model.with_structured_output(
    schema=SearchOutput,
    method="function_calling"
)

# print(model_with_structure.invoke(search_msg))


# 返回 TypedDict
class Joke(TypedDict):
    """定义一个笑话"""
    setup: Annotated[str,...,"笑话的开头"]
    punchline: Annotated[str,...,"笑话的结尾"]
    rating: Annotated[Optional[int],..., "从1-10给笑话的评分"]
model_with_structure = search_model.with_structured_output(
    schema=Joke,
    method="function_calling",
)
# print(model_with_structure.invoke(search_msg))

# 返回json
json_schema = {
    "title": "Joke",
    "description": "给用户讲一个笑话。",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "这个笑话的开头",
        },
        "punchline": {
            "type": "string",
            "description": "这个笑话的妙语",
        },
        "rating": {
            "type": "integer",
            "description": "从1到10分，给这个笑话评分",
            "default": None,
        },
    },
    "required": ["setup", "punchline"],
}

model_with_structure = search_model.with_structured_output(
    schema=json_schema,
    method="function_calling",
)
# print(model_with_structure.invoke(search_msg))


# 选择结构（使用Pydantic对象）
class chat(BaseModel):
    """关于不是笑话的定义"""
    output: Annotated[str,...,"模型输出"]
class joke(BaseModel):
    """关于一个笑话的定义"""
    setup: Annotated[str, ..., "笑话的开头"]
    punchline: Annotated[str, ..., "笑话的结尾"]
class finaloutput(BaseModel):
    finaloutput: Union[chat,joke] # 让模型选择输出结构
    #对于符合笑话定义的回答输出笑话结构，而对于不是笑话定义的输出普通content回答

model_with_structure = search_model.with_structured_output(
    schema=finaloutput,
    method="function_calling",
)
print(model_with_structure.invoke("输出一个笑话"))
print(model_with_structure.invoke("输出一个定义"))
