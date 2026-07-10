# 这里来学习RAG以及输出解析器进行结构化输出
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional,Annotated

model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

class Joke(BaseModel):
    """定义一个笑话"""
    setup: Annotated[str,...,"笑话的开头"]
    punchline: Annotated[str,...,"笑话的结尾"]
    rating: Annotated[Optional[int],..., "从1-10给笑话的评分"]


# 定义 Pydantic 输出解析器。
# parser 知道最终目标是 Joke，因此它负责两件事：
# - 生成给模型看的格式说明：parser.get_format_instructions()
# - 把模型返回的 JSON 解析成 Joke 对象
parser = PydanticOutputParser(pydantic_object=Joke)
parser = JsonOutputParser(pydantic_object=Joke)


prompt_template = ChatPromptTemplate(
    [
        ("system","你是一个笑话助手。请严格按照下面的结构要求返回结果：{format_instructions}"),
        ("user", "{query}"),
    ]
)

chain = prompt_template | model | parser


result = chain.invoke(
    {
        "format_instructions": parser.get_format_instructions(),
        "query": "讲一个关于程序员的简短笑话，并给它评分。",
    }
)

print(result)
