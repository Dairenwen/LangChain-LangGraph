import os
from dotenv import load_dotenv
load_dotenv()  # 自动加载项目根目录的 .env 文件
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, trim_messages, filter_messages, \
    merge_message_runs
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

# 这里来学习提示词模版，如何写提示词
model = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0,
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


# 方式一：直接定义提示词模版
prompt_template = PromptTemplate(
    input_variables=["name", "age"],                    # 输入变量
    template="Hello, {name}! You are {age} years old."  # 模版
)
# print (prompt_template.invoke({"name":"ALlen", "age":18}))
# 方式二：
prompt_template = PromptTemplate.from_template("Hello, {name}! You are {age} years old.")
# print(prompt_template.invoke({"name":"ALlen", "age":18})) # 打印的方式是一样的

# 处理聊天消息的模版：
chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "{system_message}"), # 这里是系统消息
        ("user","{text}"), # 这里是用户的输入
        MessagesPlaceholder("message"),
        ("ai","{response}") # 这里是AI的回答
    ]
)


message_holder = [
    SystemMessage(content="你是一个有帮助的助手。"), # 这是系统消息，告诉模型它的角色和行为
    HumanMessage(content="你是什么模型？请用一句话回答。"), # 这是人类消息，向模型提出问题
]


message=chat_prompt_template.invoke({"system_message":"you are a helpful assistant",
                             "text":"what is your name?",
                             "response":"I am an AI model.",
                             "message":message_holder})


model.invoke(message).pretty_print()


# 或者采用链式方式调用
chain=chat_prompt_template|model
# print(chain.invoke({
#     "system_message":"you are a helpful assistant",
#     "text":"what is your name?",
#     "response":"I am an AI model.",
#     "message":message_holder
# }))


# hub提示词模版调用
# Create a LangSmith API in Settings > API Keys
# Make sure API key env var is set:
# import os; os.environ["LANGSMITH_API_KEY"] = "<your-api-key>"
from langsmith import Client
client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
prompt = client.pull_prompt("hardkothari/prompt-maker")

chain=prompt|model
task=input("请输入你要优化的提示词：").strip()
lazy_prompt=input("请输入当前拉垮提示词：").strip()
print(chain.invoke(input={
    "task":task,
    "lazy_prompt":lazy_prompt,
}).pretty_print())

