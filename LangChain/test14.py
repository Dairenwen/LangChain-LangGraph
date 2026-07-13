# 这里来连接redis
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from redisvl.query.filter import Num, Tag

# 先定义嵌入模型
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest",
)
# 初始化redis
config = RedisConfig(
    index_name="langchain_docs",            # 索引名称，向量数据库中所有文档都会存入这个索引下
    redis_url="redis://localhost:6379",     # redis连接地址，默认是本地的6379端口
    vector_field_name="embedding",          # 向量字段名称，需要和 Redis 中的索引字段保持一致
    vector_dim=4096,                        # qwen3-embedding:latest 生成的是 4096 维向量
    distance_metric="COSINE",
    metadata_schema=[
        {"name": "source", "type": "tag"},  # 文档来源，类型是tag，表示可以用来过滤检索
        {"name": "category", "type": "tag"}, # 文档分类，类型是tag，表示可以用来过滤检索
        {"name": "num", "type": "numeric"}, # 文档页码，类型是numeric，表示可以用来排序统计
    ],
)
# 初始化redis向量存储
vector_store = RedisVectorStore(
    embeddings=embeddings,
    config=config,
)
# 进行CRUD
markdownpath= "../Docs/markdown/"
markdown_loader =UnstructuredMarkdownLoader(
    markdownpath+"LangGraph 能力详解.md",
    mode="single",
)
load = markdown_loader.load()
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", # 按照 tiktoken 的 cl100k_base 编码器计算 token 数量
    chunk_size=100,
    chunk_overlap=20,
)
documents= text_splitter.split_documents(load)
# 为文档添加元数据，这是使用元数据过滤的必要条件，如果只是普通的相似性搜索，也可以不添加元数据
for index, doc in enumerate(documents, start=1):
    doc.metadata["category"] = "QA"
    doc.metadata["num"] = index

ids=vector_store.add_documents(documents)
print(f"向量数据库中存储的文档数量: {len(ids)}", flush=True)
print(ids[:3], flush=True)
print(vector_store.get_by_ids(["01KXCHYGVFFKPHS720BAJXPG5Z"])) # 根据id获取文档,注意langchain_docs是索引名称

# 删除
vector_store.delete(["01KXCHYGVFFKPHS720BAJXPG5Z"])

# 检索
# similarity_search 根据查询文本生成向量，然后去 Redis 中做向量相似度搜索。
search_docs = vector_store.similarity_search("LangGraph 能力详解", k=3)
print(search_docs, flush=True)
# 还可以使用
search_docs = vector_store.similarity_search_with_score("LangGraph 能力详解", k=3) # 结果打分，分数越低表示越相似
print(search_docs, flush=True)
# 加入元数据过滤。
filter_expression = Num("num") > 6 # RedisVectorStore 过滤条件是 RedisVL 过滤表达式，因为过滤要被转换成 RediSearch 查询语句，发送给 Redis 执行。
search_results = vector_store.similarity_search_with_score(
     query="LangGraph 能力详解",
     k=3,
     filter=filter_expression
)
print(search_results, flush=True)

# MMR
category_is_qa = Tag("category") == "QA"
num_is_under_50 = Num("num") < 50
filter_condition = category_is_qa & num_is_under_50

mmr_results = vector_store.max_marginal_relevance_search(
    query="数据库表怎么设计的？",
    k=2,
    fetch_k=10,
    filter=filter_condition
)

for doc in mmr_results:
    print("*" * 30)
    print(f"Content: {doc.page_content[:100]}...")
    print(f"Metadata: {doc.metadata}")

# 这里来连接 Pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

# 创建 Pinecone 客户端。
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
index_name = "standard-dense-py"
# 判断索引是否已经存在。
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=4096,
        metric="cosine",            # metric 表示相似度计算方式。cosine 表示余弦相似度，适合大多数文本 embedding 检索场景。
        spec=ServerlessSpec(
            cloud="aws",            # ServerlessSpec 表示创建 Pinecone Serverless 索引。cloud 是云服务商，region 是区域。
            region="us-east-1",
        ),
    )
    print(f"已创建 Pinecone 索引: {index_name}", flush=True)
else:
    print(f"Pinecone 索引已存在: {index_name}", flush=True)

# 这里才是把 Pinecone 索引包装成 LangChain 的向量数据库对象。后续可以像 RedisVectorStore 一样调用 add_documents、similarity_search 等方法。
pinecone_vector_store = PineconeVectorStore(
    index_name=index_name,
    embedding=embeddings,
)

# 进行 CRUD
markdownpath= "../Docs/markdown/"
markdown_loader =UnstructuredMarkdownLoader(
    markdownpath+"练习-文档语义拆分.md",
    mode="single",
)
load = markdown_loader.load()
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", # 按照 tiktoken 的 cl100k_base 编码器计算 token 数量
    chunk_size=100,
    chunk_overlap=20,
)
documents= text_splitter.split_documents(load)
# 为文档添加元数据，这是使用元数据过滤的必要条件，如果只是普通的相似性搜索，也可以不添加元数据
for index, doc in enumerate(documents, start=1):
    doc.metadata["category"] = "QA"
    doc.metadata["num"] = index

# 写入 Pinecone。
ids = pinecone_vector_store.add_documents(documents)
print(f"向量数据库中存储的文档数量: {len(ids)}", flush=True)
print(ids[:3], flush=True)


# 检索
# similarity_search 根据查询文本生成向量，然后去 Pinecone 中做向量相似度搜索。
search_docs = pinecone_vector_store.similarity_search("选课准备", k=3)
print(search_docs, flush=True)

# 定义检索器 Retriever。
# 向量数据库 vector_store 负责“存储和搜索向量”，而 retriever 是 LangChain 对检索能力的一层统一包装。
# 包装成 retriever 之后，它就可以像普通 Runnable 一样使用 invoke()，后续也更方便接到 RAG 链中，例如：retriever -> prompt -> model。

# 示例 1：普通相似度检索器。
similarity_retriever = pinecone_vector_store.as_retriever(
    search_type="similarity",   # search_type="similarity" 表示使用普通向量相似度搜索，也可以选择 search_type="mmr" 使用 MMR 检索。
    search_kwargs={"k": 3},     # search_kwargs={"k": 3} 表示每次检索返回最相似的 3 个文档块。
)

similarity_docs = similarity_retriever.invoke("选课前需要做什么准备？")
print("普通相似度检索结果:", flush=True)
for doc in similarity_docs:
    print("*" * 30, flush=True)
    print(doc.page_content[:200], flush=True)
    print(doc.metadata, flush=True)

# 自己定义一个检索器
from langchain_core.runnables import chain

@chain
def my_retriever(query: str) -> list:
    # 这里可以自定义检索逻辑，例如：先做相似度检索，再做 MMR 检索，最后合并结果。
    similarity_docs = similarity_retriever.invoke(query,k=5)
    return similarity_docs

print(f"自定义检索器结果:{my_retriever.invoke('选课前需要做什么准备？')}", flush=True)
