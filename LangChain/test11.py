# 这里来学习示例选择器
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, PromptTemplate


model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

# 反义词示例集合
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]

# 长度选择器需要先把每个示例变成字符串，才能计算它有多长。
# 这个模板只负责“计算长度”，不会作为最终的聊天消息发送给模型。
length_example_prompt = PromptTemplate.from_template(
    "Input: {input}\nOutput: {output}"
)


# 创建长度示例选择器：
# 它会按照 examples 原来的顺序选择示例，直到接近 max_length。
#
# 这里虽然没有写 get_text_length=...，但 LengthBasedExampleSelector会自动调用 LangChain 提供的默认 get_text_length 函数。
# 默认算法等价于：先根据空格或换行切分字符串，再统计切出了多少部分。
# 例如 "Input: happy\nOutput: sad" 的默认长度约为 4：
#     Input: / happy / Output: / sad
#
# 因此，max_length 限制的是 get_text_length 返回的数值，默认算法主要适合使用空格分词的英文。中文句子通常没有空格，整句话可能只被算作 1，所以在中文场景中只能作为粗略估算。
example_selector = LengthBasedExampleSelector(
    examples=examples,
    example_prompt=length_example_prompt,
    max_length=5,
)

# 规定“被选中的一个示例”如何转换成聊天消息。
chat_example_prompt = ChatPromptTemplate(
    [
        ("user", "{input}"),
        ("ai", "{output}"),
    ]
)

# 使用 example_selector 动态选择示例。
# 这里不再写 examples=examples，因为示例由选择器提供。
few_shot_prompt_template = FewShotChatMessagePromptTemplate(
    example_selector=example_selector,
    example_prompt=chat_example_prompt,
)

# 任务说明 + 动态选择的示例 + 用户输入
prompt_template = ChatPromptTemplate(
    [
        ("system", "给出用户输入的英文单词的反义词，只输出反义词。"),
        few_shot_prompt_template,
        ("user", "{input}"),
    ]
)


chain = prompt_template | model
input_word = "hot"

# 先打印本次选中的示例，观察选择器是否生效。
selected_examples = example_selector.select_examples({"input": input_word})
print("本次选中的示例：", selected_examples)

response = chain.invoke({"input": input_word})
response.pretty_print()


# 按照语义相似性选择：
from langchain_openai import OpenAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector,MaxMarginalRelevanceExampleSelector
from langchain_chroma import Chroma


# 1. 创建嵌入模型。
# 嵌入模型不负责回答反义词，而是把单词转换成向量（一组数字）。
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

# 2. 创建语义相似度示例选择器。
# from_examples 会先把 examples 中的 input 转换成向量并存入内存向量库。
# 当出现新输入时，再搜索语义最接近的 k 个示例。
# 如果要使用MMR进行多样化选择，只需要换成MaxMarginalRelevanceExampleSelector选择器即可
semantic_example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples=examples,
    embeddings=embeddings,
    vectorstore_cls=Chroma,# 使用 Chroma 作为向量数据库
    k=5,                   # 每次选择语义最接近的5个示例，如果是mmr选择器，则是先选出5个最相似的示例，再从中挑选多样化的示例。
    input_keys=["input"],  # 只比较 input，不使用 output 参与相似度计算
)

# 继续复用上面已经定义好的 chat_example_prompt：
# user: {input}
# ai: {output}
semantic_few_shot_prompt_template = FewShotChatMessagePromptTemplate(
    example_selector=semantic_example_selector,
    example_prompt=chat_example_prompt,
)

# 4. 组成语义选择版本的完整提示词。
semantic_prompt_template = ChatPromptTemplate(
    [
        ("system", "给出用户输入的英文单词的反义词，只输出反义词。"),
        semantic_few_shot_prompt_template,
        ("user", "{input}"),
    ]
)

# 5. 查看语义选择器选择了哪些示例，然后调用模型。
semantic_input_word = "hot"
semantic_selected_examples = semantic_example_selector.select_examples(
    {"input": semantic_input_word}
)
print("本次语义最相近的示例：", semantic_selected_examples)

semantic_chain = semantic_prompt_template | model
semantic_response = semantic_chain.invoke({"input": semantic_input_word})
semantic_response.pretty_print()

# 按照ngram重叠选择示例

# NGramOverlapExampleSelector 使用 NLTK 的 BLEU 分数比较新输入和示例中
# 出现了多少相同的 n-gram。当前示例的 input 都只有一个单词，所以这里
# 主要体现为 unigram（单个单词）重叠。
from langchain_community.example_selectors import NGramOverlapExampleSelector

examples = [
    {"input": "See Spot run.", "output": "看见Spot跑。"},
    {"input": "My dog barks.", "output": "我的狗叫。"},
    {"input": "Spot can run.", "output": "Spot可以跑。"},
]

# 创建 n-gram 重叠选择器。
# length_example_prompt 在这里不是为了限制长度，而是告诉选择器：每个示例中需要参与比较的输入字段是 input。
ngram_example_selector = NGramOverlapExampleSelector(
    examples=examples,
    example_prompt=length_example_prompt,
    threshold=0.0,  # 排除与新输入完全没有单词重叠的示例
)

# 继续复用前面的聊天示例模板，把选中的示例转换成 user/ai 消息。
ngram_few_shot_prompt_template = FewShotChatMessagePromptTemplate(
    example_selector=ngram_example_selector,
    example_prompt=chat_example_prompt,
)

# 任务说明 + n-gram 重叠示例 + 真正的新输入。
ngram_prompt_template = ChatPromptTemplate(
    [
        ("system", "给出用户输入的英文单词或短语的反义表达，只输出答案。"),
        ngram_few_shot_prompt_template,
        ("user", "{input}"),
    ]
)

# "very sunny" 和示例 "sunny" 都包含单词 sunny，因此该示例会被选中。
ngram_input = "very sunny"
ngram_selected_examples = ngram_example_selector.select_examples(
    {"input": ngram_input}
)
print("本次 n-gram 重叠示例：", ngram_selected_examples)

ngram_chain = ngram_prompt_template | model
ngram_response = ngram_chain.invoke({"input": ngram_input})
ngram_response.pretty_print()
