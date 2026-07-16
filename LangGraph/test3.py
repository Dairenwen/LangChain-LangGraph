# 工作流常见模式
import os
from dotenv import load_dotenv
load_dotenv()
import operator
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing_extensions import Annotated, Literal, TypedDict
from langgraph.types import Send
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field


model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

# 提示链模式
class InputState(TypedDict):
    topic: str
class OutputState(TypedDict):
    final_content: str
class OverallState(InputState, OutputState):
    outline: str
    draft: str
    polished_draft: str

PROMPT_1 = (
    "根据主题生成文章大纲。\n"
    "主题: {topic}\n"
    "要求: "
    "1.只需两个最核心标题"
    "2.不用进行说明，只返回最终大纲"
)
def generate_outline(state: InputState) -> OverallState:
    """根据主题生成内容大纲"""
    print("*" * 50)
    print(f"内容大纲生成中...\n")
    prompt = PROMPT_1.format(topic=state['topic'])
    outline = model.invoke([HumanMessage(content=prompt)]).content
    print(f"大纲已生成: \n{outline}\n")
    return {
        "outline": outline,
        "topic": state["topic"]
    }

# 第二步: 基于大纲生成初稿
PROMPT_2 = (
    "根据以下内容生成文章完整初稿。\n"
    "主题: {topic}\n"
    "大纲: "
    "{outline}\n"
    "要求: "
    "1.每个标题下，最多使用三句话的内容即可"
    "2.不用进行说明，只返回最终结果"
)
def generate_draft(state: OverallState) -> OverallState:
    """根据大纲生成完整初稿"""
    print("*" * 50)
    print(f"生成初稿中...\n")
    prompt = PROMPT_2.format(topic=state['topic'],outline=state['outline'])
    draft = model.invoke([HumanMessage(content=prompt)]).content
    print(f"初稿已生成: \n{draft}\n")
    return {"draft": draft}

# 第三步: 润色稿件
PROMPT_3 = (
    "根据文章初稿进行润色。\n"
    "主题: {topic}\n"
    "初稿: "
    "{draft}\n"
    "要求: "
    "1.润色后，文章不能太长"
)
def polish_content(state: OverallState) -> OverallState:
    """对初稿进行润色优化"""
    print("*" * 50)
    print(f"文章润色中...\n")
    prompt = PROMPT_3.format(topic=state['topic'],draft=state['draft'])
    polished = model.invoke([HumanMessage(content=prompt)]).content
    print(f"润色完成，内容如下: \n{polished}\n")
    return {"polished_draft": polished}

# 第四步: 生成最终稿
PROMPT_4 = (
    "根据润色版文章，生成文章终稿。\n"
    "主题: {topic}\n"
    "大纲: "
    "{outline}\n"
    "润色版文章: "
    "{polished_draft}\n"
)
def finalize_content(state: OverallState) -> OutputState:
    """生成最终版本的内容"""
    prompt = PROMPT_4.format(topic=state['topic'],outline=state['outline'],polished_draft=state['polished_draft'])
    final_content = model.invoke([HumanMessage(content=prompt)]).content
    return {"final_content": final_content}

# 构建工作流
builder = StateGraph(
    OverallState,                      # 内部状态模式
    input_schema=InputState,           # 输入验证模式
    output_schema=OutputState          # 输出过滤模式
)

# 添加节点
builder.add_node(generate_outline)     # 节点1: 生成大纲
builder.add_node(generate_draft)       # 节点2: 生成初稿
builder.add_node(polish_content)       # 节点3: 润色稿件
builder.add_node(finalize_content)     # 节点4: 生成最终稿

# 连接节点（直线流程）
builder.add_edge(START, "generate_outline")           # 开始 → 生成大纲
builder.add_edge("generate_outline", "generate_draft") # 大纲 → 生成初稿
builder.add_edge("generate_draft", "polish_content")   # 初稿 → 润色
builder.add_edge("polish_content", "finalize_content") # 润色 → 最终稿
builder.add_edge("finalize_content", END)              # 最终稿 → 结束

# 编译工作流
chain = builder.compile()

# 使用工作流
result = chain.invoke({"topic": "人工智能的未来发展"})
print("=" * 50)
print("最终创作结果:")
print("=" * 50)
print(result["final_content"])
print("=" * 50)


# 并行化模式
class AnalysisState(TypedDict):
    concept: str      # 概念
    market: str       # 市场分析
    competitor: str   # 竞品分析
    tech: str         # 技术分析
    report: str       # 汇总报告

# 三个并行分析任务
def market_task(state: AnalysisState):
    """市场分析"""
    return {"market": "用户关注续航、重量、防盗，对骑行社交有兴趣..."}

def competitor_task(state: AnalysisState):
    """竞品分析"""
    return {"competitor": "传统品牌智能化不足，互联网品牌续航和售后差..."}

def tech_task(state: AnalysisState):
    """技术分析"""
    return {"tech": "轻量化电池车身、GPS防盗、社交App集成..."}

# 汇总结果
def combine_results(state: AnalysisState):
    """生成最终报告"""
    report = f"产品分析报告\n\n"
    report += f"市场分析: \n{state['market']}\n\n"
    report += f"竞品分析: \n{state['competitor']}\n\n"
    report += f"技术分析: \n{state['tech']}\n\n"
    report += "建议: 聚焦续航、防盗、社交功能的平衡发展"
    return {"report": report}

# 构建工作流
builder = StateGraph(AnalysisState)
builder.add_node("market", market_task)
builder.add_node("competitor", competitor_task)
builder.add_node("tech", tech_task)
builder.add_node("combine", combine_results)

# 并行执行三个分析
builder.add_edge(START, "market")
builder.add_edge(START, "competitor")
builder.add_edge(START, "tech")

builder.add_edge("market", "combine")
builder.add_edge("competitor", "combine")
builder.add_edge("tech", "combine")
builder.add_edge("combine", END)

workflow = builder.compile()

# 使用
result = workflow.invoke({"concept": "城市通勤智能电动自行车"})
print(result["report"])

# 路由模式：
class State(TypedDict):
    input: str    # 用户输入
    decision: str # 路由决策
    output: str   # 最终输出

# 定义路由决策的数据结构
class Route(BaseModel):
    step: Literal["pre_sale", "after_sale", "technical"] = Field(
        description="根据用户问题类型决定路由到售前、售后还是技术处理"
    )

ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "你是一个客服问题路由器，只能把用户问题分成下面三类之一:\n"
        "1. pre_sale: 售前咨询，例如价格、功能、套餐、购买建议、产品介绍。\n"
        "2. after_sale: 售后问题，例如退款、退货、订单、物流、质保、售后政策、已购产品问题。\n"
        "3. technical: 技术问题，例如安装、配置、报错、接口、数据库、代码、运行故障。\n"
        "必须只选择一个最合适的类别，不要输出其他类别。"
    ),
    ("human", "用户问题: {input}")
])

# 路由决策节点
def model_call_router(state: State):
    """分析用户输入，决定问题类型"""
    model = ChatOpenAI(
        model="gpt-5.4",
        temperature=0,
        api_key=os.getenv("PACKYAPI_API_KEY"),
        base_url="https://www.packyapi.com/v1",
    )
    prompt = ROUTER_PROMPT.invoke({"input": state["input"]})
    decision = model.with_structured_output(
        Route,
        method="function_calling"
    ).invoke(prompt)
    return {"decision": decision.step}

# 三个不同的处理节点
def pre_sale_handler(state: State):
    """处理售前咨询"""
    return {"output": "售前咨询已处理，处理内容....."}

def after_sale_handler(state: State):
    """处理售后问题"""
    return {"output": "售后问题已处理，处理内容....."}

def technical_handler(state: State):
    """处理技术问题"""
    return {"output": "技术问题已处理，处理内容....."}

# 路由函数 - 根据决策返回下一个节点
def route_decision(state: State):
    if state["decision"] == "pre_sale":
        return "pre_sale_handler"  # 去售前处理节点
    elif state["decision"] == "after_sale":
        return "after_sale_handler"  # 去售后处理节点
    elif state["decision"] == "technical":
        return "technical_handler"  # 去技术处理节点

# 构建路由工作流
router_builder = StateGraph(State)

# 添加处理节点
router_builder.add_node(pre_sale_handler)
router_builder.add_node(after_sale_handler)
router_builder.add_node(technical_handler)
router_builder.add_node(model_call_router)

# 先经过路由决策
router_builder.add_edge(START, "model_call_router")

# 条件边: 根据路由结果选择分支
router_builder.add_conditional_edges(
    "model_call_router",
    route_decision,
    ["pre_sale_handler", "after_sale_handler", "technical_handler"]
)

# 所有分支最终都结束
router_builder.add_edge("pre_sale_handler", END)
router_builder.add_edge("after_sale_handler", END)
router_builder.add_edge("technical_handler", END)

router_workflow = router_builder.compile()

# 测试
test_cases = [
    "我想了解一下你们产品的价格和功能",  # 售前咨询
    "我购买的产品有质量问题，需要退货",  # 售后问题
    "这个软件安装后无法正常运行，报错代码0x80070005",  # 技术问题
    "请问你们的售后服务政策是什么", # 售后咨询
    "我的订单已经发货但还没收到", # 售后问题
    "如何配置数据库连接参数", # 技术问题
]
for test_case in test_cases:
    print("*" * 50)
    result = router_workflow.invoke({"input": test_case})
    print(f"用户问题: {test_case}\n{result['output']}")

# 协调者-工作者模式：
# 协调者像项目经理，负责分配任务和收集结果；工作者像员工，执行具体任务。
# 协调者动态派发任务，与并行模式的区别在于：这里的任务是动态生成的，而不是预先定义好的。

class State(TypedDict):
    topic: str
    sections: list  # 协调者生成的计划
    completed_sections: Annotated[list, operator.add]  # 工作者完成的结果
    final_report: str # 最终汇总报告

# 定义数据结构-结构化输出
class Section(BaseModel):
    name: str
    description: str

class Sections(BaseModel):
    sections: list[Section]

# 创建规划器
model = ChatOpenAI(
    model="gpt-5.4",
    temperature=0,
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1",
)

planner = model.with_structured_output(
    Sections,
    method="function_calling"
)

# 协调者节点 - 制定计划
def orchestrator(state: State):
    """协调者: 分析任务并制定执行计划"""
    report_sections = planner.invoke(
        f"为主题'{state['topic']}'制定报告大纲，包含3个章节"
    )
    return {"sections": report_sections.sections}

# 工作者节点 - 执行具体任务
def llm_call(state: State):
    """工作者: 根据分配的任务生成内容"""
    section = state["section"]  # 从协调者接收的任务
    result = model.invoke(
        f"编写报告章节: {section.name}, 内容要求: {section.description}"
    )
    return {"completed_sections": [result.content]}  # 结果会自动合并

# 汇总节点
def synthesizer(state: State):
    """汇总所有工作者的成果"""
    completed_sections = state["completed_sections"]
    final_report = "\n---\n".join(completed_sections)
    return {"final_report": final_report}

# 构建工作流
builder = StateGraph(State)
builder.add_node("orchestrator", orchestrator)
builder.add_node("llm_call", llm_call)
builder.add_node("synthesizer", synthesizer)
builder.add_edge(START, "orchestrator")

# 任务分配函数 - 关键部分!
def assign_workers(state: State):
    """为每个任务创建工作者"""
    # 为每个章节创建一个工作者任务
    worker_tasks = []
    for section in state["sections"]:
        worker_tasks.append(
            Send("llm_call", {"section": section})  # 发送任务给工作者
        )
    return worker_tasks


# 关键: 协调者后创建多个工作者
builder.add_conditional_edges(
    "orchestrator",
    assign_workers,
    ["llm_call"]  # 创建的工作者都指向llm_call节点
)

# 所有工作者完成后汇总
builder.add_edge("llm_call", "synthesizer")
builder.add_edge("synthesizer", END)

worker = builder.compile()
response = worker.invoke({"topic": "中国近代史"})
print(response)

# 最后一个评估器-优化器模式：
# 也就是进行一个循环迭代的过程，先生成初稿，然后进行评估和优化，直到达到满意的结果。
# 这一个流程在之前的RAG流程中已经实现过了
