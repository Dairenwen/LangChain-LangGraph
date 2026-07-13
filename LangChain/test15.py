# RAG综合案例
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

load_dotenv()

# 1.定义嵌入模型
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest",
)
# 初始化redis
config = RedisConfig(
    index_name="langchain_rag",
    redis_url="redis://localhost:6379",
    vector_field_name="embedding",
    vector_dim=4096,
    distance_metric="COSINE",
    metadata_schema=[
        {"name": "source", "type": "tag"},
        {"name": "category", "type": "tag"},
        {"name": "num", "type": "numeric"},
    ],
)
# 初始化redis向量存储
vector_store = RedisVectorStore(
    embeddings=embeddings,
    config=config,
)
# 2.定义检索器
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)
# 3.定义提示词模版
# 提示词模板使用你当前代码中的 ChatPromptTemplate([...]) 格式来定义。
# 这里的 {context} 会接收检索器找回来的文档内容，
# {question} 会接收用户原始问题。
prompt_template = ChatPromptTemplate(
    [
        ("system", "你是负责回答问题的助手。使用以下检索到的上下文片段来回答问题。如果你不知道答案，就说不知道答案。最多回复三句话的结果，回答要简明扼要。"),
        ("user", "Question:{question}\nContext:{context}\nAnswer:"),
    ]
)

# 4.传入LLM
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

# 5.进行结构化输出，输出解析器
parser = StrOutputParser()

# 将检索出来的文档转换成文本传递给提示词模板。retriever 返回的是 List[Document]，而 prompt 里的 {context} 需要的是字符串，
# 所以这里把每个文档块的 page_content 提取出来，并用空行拼接。
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# 6. 定义链，执行时需要传入 question。
# 分支 1：retriever 根据 question 检索相关文档，再通过 format_docs 转成 context 字符串。
# 分支 2：RunnablePassthrough() 保持原始 question 不变，直接传递给后续 prompt。
# 然后依次经过 prompt -> model -> parser，最终得到字符串答案。
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt_template
    | model
    | parser
)

# 7. 执行流：
# 输入问题："项目介绍" 同时执行两个分支：context：检索器检索文档，并格式化成上下文，question：保留原始问题
result = chain.invoke("langchain到底是什么？")
print(result, flush=True)
