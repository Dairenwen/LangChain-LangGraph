# 这里来学习嵌入模型以及如何生成向量
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(
    model="qwen3-embedding:latest",
)

# embed_query 用来处理“用户的一次查询”。它的输入是一个字符串 str，返回值是一维向量 List[float]。
# 在 RAG 中，用户每次提问时，通常会实时把这个问题转成查询向量，再拿这个查询向量去向量数据库里搜索相似的文档片段。
vector = embeddings.embed_query("你好，我想生成一段文本的向量")
print(f"查询向量维度: {len(vector)}", flush=True)
print(f"查询向量前 5 个数值: {vector[:5]}", flush=True)

# embed_documents 用来处理“文档列表”。它的输入是多个字符串 List[str]，返回值是二维向量列表 List[List[float]]。
# 在 RAG 中，知识库文档通常会先离线切分成多个 Document，然后把每个 Document 的 page_content 转成向量，存入向量数据库，方便后续检索。
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

# 先打印切割后的文档，再去生成文档向量。
# 如果先执行 embed_documents，大量文档向量化会比较慢，你可能要等很久才看到后面的 print。
print(f"文档切割完成，切割后的文档块数量: {len(documents)}", flush=True)
for index, doc in enumerate(documents[:3], start=1):
    print("=" * 30, flush=True)
    print(f"第 {index} 个文档块内容:", flush=True)
    print(doc.page_content, flush=True)
    print(f"第 {index} 个文档块元数 据: {doc.metadata}", flush=True)

# split_documents 得到的是 List[Document]。嵌入模型真正需要的是字符串，所以这里要取出每个 Document 的 page_content。
texts = [doc.page_content for doc in documents]

# 将文本列表转换为向量列表。documents_vector 的长度和 texts/documents 的长度一致：第 1 个向量对应第 1 个文档块，第 2 个向量对应第 2 个文档块，以此类推。
print("开始将切割后的文档块转换为向量，请稍等...", flush=True)
documents_vector = embeddings.embed_documents(texts)

print(f"文档块数量: {len(documents)}", flush=True)
print(f"生成的文档向量数量: {len(documents_vector)}", flush=True)
print(f"第一个文档向量维度: {len(documents_vector[0])}", flush=True)

# 这里演示如何存入向量数据库。先使用内存向量数据库：只需要先定义一个向量数据库，再将上面的 documents_vector存入向量数据库即可。
vector_store = InMemoryVectorStore(embedding=embeddings)
ids=vector_store.add_documents(documents) # 这里直接传入documents即可, 因为 InMemoryVectorStore 内部会自动调用 embed_documents 将文档转成向量，不需要我们人为去转
# 返回的是索引列表
print(f"向量数据库中存储的文档数量: {len(vector_store.store)}", flush=True)
first_id = ids[0]
first_vector = vector_store.store[first_id]["vector"]
print(f"向量数据库中存储的文档向量数量: {len(ids)}", flush=True)
print(f"向量数据库中第一个文档向量维度: {len(first_vector)}", flush=True)

# 根据索引获取文档
print(vector_store.get_by_ids(ids[:3]), flush=True)
# 删除文档
vector_store.delete(ids=ids[:2])
print(f"删除文档后，向量数据库中存储的文档数量: {len(vector_store.store)}", flush=True)

# 检索
print("开始检索向量数据库，请稍等...", flush=True)
# similiarity_search 用来做向量检索。它的输入是一个字符串 str，表示用户的查询；k 表示返回最相似的 k 个文档块。
# 实际上根据余弦相似度计算
print(vector_store.similarity_search("LangGraph 能力详解", k=3), flush=True)

# 元数据过滤
def filter_func(doc: Document) -> bool:
    # 只保留 metadata 中包含 "LangGraph" 的文档块
    return "../Docs/markdown/LangGraph 能力详解.md" in doc.metadata.get("source")

search_results = vector_store.similarity_search(
     query="LangGraph 能力详解",
     k=3,
     filter=filter_func)

print(search_results, flush=True)
