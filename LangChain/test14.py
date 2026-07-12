# 这里来连接redis
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_ollama import OllamaEmbeddings
# 先定义嵌入模型
embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest",
)
# 初始化red
config = RedisConfig(
    index_name="langchain_docs",            # 索引名称，向量数据库中所有文档都会存入这个索引下
    redis_url="redis://localhost:6379",     # redis连接地址，默认是本地的6379端口
    vector_field_name="vector",             # 向量字段名称，向量数据库中所有文档的向量都会存入这个字段下
    vector_dim=1536,
    distance_metric="COSINE",
    metadata_schema=[
        {"name": "source", "type": "tag"},  # 文档来源，类型是tag，表示可以用来过滤检索
        {"name": "num", "type": "numeric"}, # 文档页码，类型是numeric，表示可以用来排序统计
    ],
)
# 初始化redis向量存储
vector_store = RedisVectorStore(
    embeddings=embeddings,
    config=config,
)
