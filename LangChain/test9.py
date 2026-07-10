# 这里来学习“少样本提示”（Few-shot Prompting）
#
# 少样本提示的核心思想：
# 不只是告诉模型“你要做什么”，还先给模型几个“输入 -> 输出”的例子。
# 模型看到这些例子后，会模仿例子的格式和规律来回答新的问题。
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 定义模型
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

# 1. 定义少样本示例
#
# 这里就是“少样本”的原始数据：
# 每一个字典都是一个示例，text 是用户输入，output 是期望的 AI 输出。
# 这两个示例都在演示一件事：把英文问句翻译成中文问句。
examples = [
    {"text": "hi, what is your name?", "output": "你好，你叫什么名字？"},
    {"text": "hi, what is your age?", "output": "你好，你多大了？"},
]

# 2. 定义“单个示例”应该长什么样
#
# LangChain 不会自动知道 examples 里的 text/output 应该变成什么聊天消息。
# 所以这里用 ChatPromptTemplate 告诉它：
# - text 放进 user 消息
# - output 放进 ai 消息
#
# 例如：
# {"text": "hi, what is your name?", "output": "你好，你叫什么名字？"}
# 会被转换成：
# user: hi, what is your name?
# ai: 你好，你叫什么名字？
examples_prompt_templates = ChatPromptTemplate(
    [
        ("user", "{text}"),  # 这里是用户的输入
        ("ai", "{output}")   # 这里是 AI 的示范回答
    ]
)

# 3. 这里就是“少样本提示”的核心对象
#
# FewShotChatMessagePromptTemplate 会做两件事：
# - 读取上面的 examples 示例列表
# - 用 examples_prompt_templates 把每个示例转换成聊天消息
#
# 最终它会生成类似这样的消息：
# user: hi, what is your name?
# ai: 你好，你叫什么名字？
# user: hi, what is your age?
# ai: 你好，你多大了？
few_shot_prompt_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=examples_prompt_templates,
)

# 4. 先查看少样本提示最终生成了哪些 message
# invoke({}) 表示先把 few_shot_prompt_template 渲染出来。
# to_messages() 表示把它转换成 LangChain 的消息列表。
print(few_shot_prompt_template.invoke({}).to_messages())
# [HumanMessage(content='hi, what is your name?', additional_kwargs={}, response_metadata={}),
# AIMessage(content='你好，你叫什么名字？', additional_kwargs={}, response_metadata={}),
# HumanMessage(content='hi, what is your age?', additional_kwargs={}, response_metadata={}),
# AIMessage(content='你好，你多大了？', additional_kwargs={}, response_metadata={})]


# 5. 最终提示词模板
# 这里把三部分拼在一起：
# - system：告诉模型它的任务是什么
# - few_shot_prompt_template：给模型看几个示例，这里就是少样本提示插入的位置
# - user：真正的新问题
chat_prompt_template = ChatPromptTemplate(
    [
        ("system", "你是一个翻译助手，帮我把{input_language}翻译成{output_language}。"),
        few_shot_prompt_template,  # 这里插入少样本提示
        ("user", "{text}"),        # 这里是真正要模型回答的新输入
    ]
)

# 6. 组成链
# 链的顺序一定是：提示词模板 -> 模型
# 也就是先把变量填进 prompt，再把完整 prompt 发给模型。
chain = chat_prompt_template | model

# 7. 调用链
# 这个 text 是新的输入，不在 examples 里。
# 模型会参考上面两个少样本示例，推断出应该把英文翻译成中文。
print(chain.invoke(
    {
        "input_language": "英语",
        "output_language": "中文",
        "text": "hi, what is your hobby?",
    }
).pretty_print())

# 下面是使用示例：

# 创建示例集
examples = [
    {
        "question": "李白和杜甫，谁更长寿？",
        "answer": """
			是否需要后续问题：是的。
			后续问题：李白享年多少岁？
			中间答案：李白享年61岁。
			后续问题：杜甫享年多少岁？
			中间答案：杜甫享年58岁。
			所以最终答案是：李白
			""",
    },
    {
        "question": "腾讯的创始人什么时候出生？",
        "answer": """
			是否需要后续问题：是的。
			后续问题：腾讯的创始人是谁？
			中间答案：腾讯由马化腾创立。
			后续问题：马化腾什么时候出生？
			中间答案：马化腾出生于1971年10月29日。
			所以最终答案是：1971年10月29日
			""",
    },
    {
        "question": "孙中山的外祖父是谁？",
        "answer": """
			是否需要后续问题：是的。
			后续问题：孙中山的母亲是谁？
			中间答案：孙中山的母亲是杨太夫人。
			后续问题：杨太夫人的父亲是谁？
			中间答案：杨太夫人的父亲是杨胜辉。
			所以最终答案是：杨胜辉
			""",
    },
    {
        "question": "电影《红高粱》和《霸王别姬》的导演来自同一个国家吗？",
        "answer": """
			是否需要后续问题：是的。
			后续问题：《红高粱》的导演是谁？
			中间答案：《红高粱》的导演是张艺谋。
			后续问题：张艺谋来自哪里？
			中间答案：中国。
			后续问题：《霸王别姬》的导演是谁？
			中间答案：《霸王别姬》的导演是陈凯歌。
			后续问题：陈凯歌来自哪里？
			中间答案：中国。
			所以最终答案是：是
			""",
    },
]

examples_prompt_templates = ChatPromptTemplate(
    [
        ("user", "{question}"),  # 这里是用户的输入
        ("ai", "{answer}")   # 这里是 AI 的示范回答
    ]
)

few_shot_prompt_template = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=examples_prompt_templates,
)

# 测试实例化第一个示例
print(few_shot_prompt_template.invoke({}).to_messages())


chat_prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            """
            你是一个擅长分步骤推理的问答助手。

            请参考前面的示例回答。
            对于需要多个步骤才能回答的问题，必须严格使用以下格式：

            是否需要后续问题：是的。
            后续问题：问题1
            中间答案：答案1
            后续问题：问题2
            中间答案：答案2
            所以最终答案是：最终答案

            不要只给最终结论。
            """
        ),
        few_shot_prompt_template,
        ("user", "{text}"),
    ]
)

chain = chat_prompt_template | model
print(chain.invoke(
    {
        "text": "电影《盗梦空间》和《星际穿越》的导演来自同一个国家吗？",
    }
).pretty_print())
