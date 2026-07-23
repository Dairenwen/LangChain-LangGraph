import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
# 定义好模型，统一使用
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)