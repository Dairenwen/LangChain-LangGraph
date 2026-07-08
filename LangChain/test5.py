# 这里来演示，聊天模型进行工具调用的实用场景，这里演示模型绑定工具进行结构化输出的例子
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated, TypedDict, Union

# 返回 Pydantic 对象
search_model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key="YOUR_PACKYAPI_API_KEY",
    base_url="https://www.packyapi.com/v1",
)

# 定义消息列表
search_msg = [
    SystemMessage("你是一个能够帮我准确查询并分析天气的助手。"),
    HumanMessage("请帮我搜索一下广西南宁的天气情况")
]

# 定义、绑定工具
tool = TavilySearch(max_results=10, tavily_api_key="YOUR_TAVILY_API_KEY")
model_with_tools = search_model.bind_tools(tools=[tool])
ai_msg = model_with_tools.invoke(input=search_msg)
search_msg.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    tool_msg = tool.invoke(tool_call)
    search_msg.append(tool_msg)

# 定义返回的结构化格式
class SearchOutput(BaseModel):
    """天气情况分析"""
    weather: str = Field(..., description="天气情况")
    rating: Optional[int] = Field(..., description="从1-10给天气情况评分")

model_with_structure = search_model.with_structured_output(
    schema=SearchOutput,
    method="function_calling"
)
# 请注意，必须先绑定工具再进行结构化输出，否则模型无法正确调用工具
print(model_with_structure.invoke(search_msg))
