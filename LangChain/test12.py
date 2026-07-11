# 这里来学习RAG以及输出解析器进行结构化输出
import os
import logging
logging.getLogger("pypdf").setLevel(logging.ERROR)
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


#RAG离线：
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, UnstructuredMarkdownLoader

# 这里来手动定义文档列表。
# 在 LangChain 中，很多不同来源的数据最后都会被统一包装成 Document 对象。Document 可以理解为“进入 RAG 流程的标准文档格式”，它主要包含两部分：
# - page_content：真正要给模型检索、切分、向量化的文本内容
# - metadata：描述这段文本来源和属性的元数据，比如文件名、页码、URL、标题、作者、创建时间等
documents = (
    # 对于单个文档，一般表示较大文档的某一个块或者某一页
    Document(
        # 这里的 page_content 是文档的内容。metadata 是文档的元数据字典，元数据属性可以包括：文档源、作者、时间、标签等。
        # 手动创建 Document 时，metadata 由我们自己写。用加载器加载文件时，metadata 通常由加载器自动生成，例如 PDF 的 source、page 等。
        page_content="为什么程序员总是混淆万圣节和圣诞节？因为 Oct 31 == Dec 25。",
        metadata={"source": "笑话文档1"},
    ),
    Document(
        page_content="有两个程序员走进一家酒吧。第一个说：“我想要一杯啤酒。”第二个说：“我也想要一杯啤酒。”酒保问：“你们是兄弟吗？”第一个程序员回答：“不，我们只是共享代码。”",
        metadata={"source": "笑话文档2"},
    ),
)

# 文档加载器（PDF）。
# 文档加载器负责把外部数据源读取进来，并转换成 List[Document]。
# 常见可加载的数据类型包括：
# - 本地文件：PDF、txt、Markdown、Word、HTML、CSV、JSON、Excel 等
# - 网页内容：普通网页、站点地图、在线文档等
# - 数据库：SQL 数据库、MongoDB 等
# - 第三方知识库或平台：Notion、GitHub、Google Drive、Slack 等
# - API 或自定义数据：只要能读取出文本，也可以自己包装成 Document
#
# 对图片的处理要特别注意：
# - 普通文档加载器主要处理“文本”，不会真正理解图片内容
# - 如果 PDF 里是可复制文字，PyPDFLoader 可以直接提取文字
# - 如果 PDF 是扫描件，文字其实是图片，需要先 OCR，把图片中的文字识别出来
# - 如果图片本身包含流程图、结构图、截图等语义信息，需要用多模态模型理解图片，或者手动把图转换成文字说明、Mermaid 图、结构化描述
# - RAG 检索通常检索的是文本向量，所以图片要么转成文字描述，要么使用支持图像向量/多模态检索的方案


# PyPDFLoader 加载 PDF 后，默认会按照页数进行划分
# 每个 Document 的 page_content 是这一页提取出的文本；metadata 通常会自动包含 source（文件路径）和 total_pages（总页数）、page等信息。
pdfpath= "../Docs/pdf/"
pdf_loader = PyPDFLoader(pdfpath+"2026-2027学年第一学期选课指引.pdf")
# 加载：生成文档列表，也就是 List[Document]
documents = pdf_loader.load()

print("文档加载完成，文档页数：", len(documents))
# 查看第n页前m个字符内容
print("第1页前100个字符内容：", documents[0].page_content[:100])
# 查看元数据字典
print("第1页元数据字典：", documents[0].metadata)

# 文档加载器（markdown）
markdownpath= "../Docs/markdown/"
markdown_loader =UnstructuredMarkdownLoader(
    markdownpath+"LangGraph 能力详解.md",
    mode="elements", # 这是 Unstructured 的模型参数，表示单页模式
    # 还可以设置为elements，表示按元素模式，按标题、段落、列表等元素切分。elements 模式下，文档会被切分成更多的 Document，每个 Document 对应一个元素。
)
documents = markdown_loader.load()
print("文档加载完成，文档页数：", len(documents))
print("第1页前100个字符内容：", documents[0].page_content[:100])
print("第1页元数据字典：", documents[0].metadata)
print()

# 文档分割器：
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
# 先按照长度划分：
markdown_loader =UnstructuredMarkdownLoader(
    markdownpath+"练习-文档长度拆分.md",
    mode="single",
)
load = markdown_loader.load()
# 定义文本分割器
# CharacterTextSplitter：只使用 separator 指定的一个分隔符做基础切分。
# 例如 separator="\n\n" 表示只按段落切，再把切出来的小段合并成接近 chunk_size 的块。
# 如果某个段落本身已经超过 chunk_size，它不会自动换用 "\n"、"。" 或字符继续细切。
text_splitter = CharacterTextSplitter(
    separator="\n\n",  # 只按两个换行符分割，通常相当于按段落分割
    chunk_size=100,  # 每个块的最大长度(只是参考)
    chunk_overlap=20,  # 块之间的重叠长度，为了让后面的文本看起来更加完整，太长太短都不好
    length_function=len,  # 计算长度的函数
    is_separator_regex=False,  # 是否使用正则表达式分割
)

documents= text_splitter.split_documents(load)
print("文档分割完成，分割后文档块数：", len(documents))
print("第2个文档块字符内容：", documents[1].page_content)
print("第2个文档块元数据字典：", documents[1].metadata)
print()
# RecursiveCharacterTextSplitter：按照 separators 列表递归切分。
# 它会先尝试按 "\n\n" 切；如果某一块仍然超过 chunk_size，
# 再对这一块继续尝试按 "\n" 切；如果还太长，再按 "。"、"，" 继续切；
# 最后如果还无法满足长度要求，就按字符 "" 切。
recursive_text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", ""],
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
recursive_documents = recursive_text_splitter.split_documents(load)
print("递归文档分割完成，分割后文档块数：", len(recursive_documents))
print("递归分割第2个文档块字符内容：", recursive_documents[1].page_content)
print("递归分割第2个文档块元数据字典：", recursive_documents[1].metadata)
print()
# 如果要按照token划分：
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", # 按照 tiktoken 的 cl100k_base 编码器计算 token 数量
    chunk_size=100,
    chunk_overlap=20,
)
documents= text_splitter.split_documents(load)
print("文档分割完成，分割后文档块数：", len(documents))
print("第2个文档块字符内容：", documents[1].page_content)
print("第2个文档块元数据字典：", documents[1].metadata)
print()

# 补充的其他分割器
from langchain_text_splitters import PythonCodeTextSplitter
# 字符串文档
python_code = """
def hello_world():
    print("Hello, World!")

def hello_python():
    print("Hello, Python!")
"""

python_splitter = PythonCodeTextSplitter(chunk_size=50, chunk_overlap=0)
python_docs = python_splitter.create_documents([python_code])

for document in python_docs[:2]:
    print("*" * 30)
    print(f"{document}\n")
