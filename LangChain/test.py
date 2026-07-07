from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama

ollama_model=ChatOllama(model="gemma4:31b",base_url="http://localhost:11434")
print(ollama_model.invoke("你是什么模型？").content) # 输出模型的回答

# 1.定义OpenAI模型（使用中转站）
model = ChatOpenAI(
    model="deepseek-v4-flash",
    temperature=0, # 温度越高越发散，越低越保守
    api_key="YOUR_DEEPSEEK_API_KEY",       # 替换成你的实际 key
    base_url = "https://api.deepseek.com/v1",  # 替换成你的中转站地址
)

# 2.定义消息列表
messages = [
    SystemMessage(content="你是一个有帮助的助手。"), # 这是系统消息，告诉模型它的角色和行为
    HumanMessage(content="你是什么模型？请用一句话回答。"), # 这是人类消息，向模型提出问题
]

# 3.调用大模型
result = model.invoke(messages)  # 调用模型，传入消息列表
# 返回的其实是一个包含模型输出的对象，通常包括 content、usage 等信息，其中AIMessage表示ai返回的消息
print(result) # 输出模型的回答

# 4.定义输出解析器
parser=StrOutputParser() # 创建一个字符串输出解析器实例
print(parser.invoke(result)) # 解析模型的输出内容，并打印结果

# 5.定义链
chain=model | parser
print(chain.invoke(messages)) # 直接调用链，传入消息列表，返回解析后的结果


# 还可以使用init的方式来定义
model=init_chat_model("deepseek-v4-flash",model_provider="deepseek",api_key="YOUR_DEEPSEEK_API_KEY")
print(model.invoke(messages))

model=init_chat_model("deepseek-v4-flash",
                      model_provider="deepseek",
                      api_key="YOUR_DEEPSEEK_API_KEY",
                      temperature=0,
                      configurable_fields=["temperature"],
                      config_prefix="change")

print(model.invoke(input=messages,
                   config={
                       "configurable": {
                            "change_temperature":0.5,
                       }
                   },)) # 通过config参数来修改模型的温度






