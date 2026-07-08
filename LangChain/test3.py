from langchain_core.tools import tool
from pydantic import BaseModel,Field
from typing import Annotated


# 函数名、字符串文档以及类型提示都需要定义

# 这里定义了一个输入模型，用于描述工具的输入参数
class AddInput(BaseModel):
    """两数之和""" # 文档字符串，用于描述工具的功能
    a: int = Field(...,description="first int")
    b: int = Field(...,description="second int")


@tool(args_schema=AddInput) # 输入规范去addinput类中寻找
def add(a:int,b:int):
    """两数相加

    Args:
        a (int): 第一个加数
        b (int): 第二个加数
    Returns:
        int: 两数之和
    """
    return a+b

@tool
def multiply(
    a: Annotated[int, ..., "first int"],
    b: Annotated[int, ..., "second int"]
)-> int:
    """两数相乘"""
    return a*b

# 还可以通过StructuredTool来定义工具，StructuredTool是一个更为结构化的工具定义方式，可以更好地描述工具的输入输出和行为
from langchain_core.tools import StructuredTool
class structured_tool_input(BaseModel):
    """结构化工具输入"""
    a: int = Field(...,description="first int")
    b: int = Field(...,description="second int")

def structured_tool(a:int,b:int):
    """结构化调用"""
    return a+b

add_structured_tool = StructuredTool.from_function(func=structured_tool,
                                                   name="add_structured_tool",  # 工具名
                                                   description="两数相加",       # 工具描述
                                                   args_schema=structured_tool_input  # 工具参数
                                                   )


# 工具函数：返回二元组
def Multiply(a: int, b: int) -> tuple[int, dict]:
    """Multiply two numbers."""
    result = a * b
    # artifact：存放原始参数、执行时间等后台数据
    artifact = {"input_a": a, "input_b": b, "calc_time": "2026-07-07"}
    # 按顺序返回：(给模型的内容, 给程序的工件)
    return result, artifact

# 创建工具时开启双返回模式
calc_tool = StructuredTool.from_function(
    func=Multiply,
    response_format="content_and_artifact"  # 关键配置
)

# 这是一个工具调用示例，模拟模型调用工具的过程
print(calc_tool.invoke(
    {
        "name":"multiply",
        "args":{"a":1,"b":2},
        "type":"tool_call", # 必填
        "id":"001", #必填，用来将工具调用请求和结果关联起来
    }
))
