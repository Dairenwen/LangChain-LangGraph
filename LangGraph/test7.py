from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
load_dotenv()
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt,Command
from langgraph.graph import StateGraph, START, MessagesState,END
from typing import TypedDict, Annotated, Literal,Optional

class State(MessagesState):
    input: str
    output: str

def node(state: State):
    """进行动态中断操作"""
    result = interrupt("结束还是继续？是或否") # 可以传入普通类型
    if result == "是":
        return {"output": "继续执行"}
    else:
        return {"output": "结束执行"}

builder=StateGraph(State)
builder.add_node(node)
builder.add_edge(START, "node")
builder.add_edge("node", END)
graph=builder.compile(checkpointer=InMemorySaver())
# 必须指明同一个线程，与checkpoinrt搭配使用
config={"configurable": {"thread_id": "thread_1"}}
print(graph.invoke({"input":"开始调用"},config=config)) # 这是第一次调用，执行到中断点
print(graph.invoke(Command(resume="否"), config=config)) # 输入中断结果，继续执行

# 四个使用场景：
class ApprovalState(TypedDict):
    action_details: str # 操作详情
    status: Optional[Literal["等待", "批准", "拒绝"]]
# 节点中，直接判断后续执行流程
def approval_node(state: ApprovalState):
    """审批节点"""
    decision=interrupt({
        "question": "是否批准该操作？",
        "options": ["批准", "拒绝"],
        "details": state["action_details"]
    })
    if decision=="批准":
        next_node="processed_node"
    else:
        next_node="cancel_node"
    return Command(goto=next_node) #直接跳转到后续节点,不用添加条件边了


def processed_node(state: ApprovalState):
    """处理节点"""
    print(f"审批结果: {state['status']}")
    return {"status":"批准"}

def cancel_node(state: ApprovalState):
    """取消节点"""
    print("拒绝审批，操作取消")
    return {"status":"拒绝"}

builder=StateGraph(ApprovalState)
builder.add_node(approval_node)
builder.add_node(processed_node)
builder.add_node(cancel_node)
builder.add_edge(START, "approval_node")
def approval_edge(state: ApprovalState):
    if state["status"]=="批准":
        return "processed_node"
    else:
        return "cancel_node"
# builder.add_conditional_edge("approval_node", approval_edge,["processed_node","cancel_node"])
builder.add_edge("processed_node", END)
builder.add_edge("cancel_node", END)
graph=builder.compile(checkpointer=InMemorySaver())
config={"configurable": {"thread_id": "thread_2"}}
print(graph.invoke({"action_details":"支付宝到账300000元","status":"pending"},config=config))
print(graph.invoke(Command(resume="批准"), config=config))


# 进行人工修改，修改后继续执行
class State(TypedDict):
    text: str
def review_node(state: State):
    """人工审核节点"""
    result=interrupt({
        "question":"请审核该文本是否符合要求",
        "text":state["text"]
    })
    return {"text":result}
builder=StateGraph(State)
builder.add_node(review_node)
builder.add_edge(START, "review_node")
builder.add_edge("review_node", END)
graph=builder.compile(checkpointer=InMemorySaver())
config={"configurable": {"thread_id": "thread_3"}}
print(graph.invoke({"text":"这是一段需要审核的文本"},config=config))
print(graph.invoke(Command(resume="这是修改过后的文本"), config=config))

# 在工具中使用中断
@tool
def send_email(to:str,subject:str,body:str):
    """发送邮件工具"""
    result=interrupt({
        "action":"我要发送邮件了",
        "to":to,
        "subject":subject,
        "body":body,
        "message":"请确认是否发送邮件"
    })

    if result["action"]=="拒绝":
        return "邮件发送失败"
    else:
        final_to=result.get("to",to)
        final_subject=result.get("subject",subject)
        final_body=result.get("body",body)

        print(f"发送邮件给{final_to},主题:{final_subject},内容:{final_body}") # 放在interrupt后面，防止重复发送邮件
        return f"最终发送邮件给{final_to},主题:{final_subject},内容:{final_body}"

model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
)

model_with_tool=model.bind_tools([send_email])

def llm_call(state:MessagesState):
    """调用模型，带上总结+用户问题生成AI回复"""
    result=model_with_tool.invoke(
        [SystemMessage(content="你是一个邮件发送助手")]
        + state["messages"]
    )
    # 判断是否调用工具
    if result.tool_calls:
        tool_call=result.tool_calls[0]
        # 调用工具"
        tool_result=send_email.invoke(tool_call["args"])
        return {"messages": [ToolMessage(tool_call_id=tool_call["id"],content=tool_result)]}

    return {
        "messages": [result]
    }

builder=StateGraph(MessagesState)
builder.add_node(llm_call)
builder.add_edge(START, "llm_call")
builder.add_edge("llm_call", END)
graph=builder.compile(checkpointer=InMemorySaver())
config={"configurable": {"thread_id": "thread_4"}}

# 第一次调用：启动图，执行到 interrupt 时暂停
print(graph.invoke(
    {
        "messages": [
            HumanMessage(content="请发送一封邮件给 test@example.com，主题是测试邮件，正文是这是一段需要审核的文本")
        ]
    },
    config=config
))

# 恢复调用：同意，并修改部分邮件内容
print(graph.invoke(
    Command(resume={
        "action": "同意",
        "to": "user@example.com",
        "body": "这是一封测试邮件"
    }),
    config=config
))


# 人工验证
class State(TypedDict):
    age: int  | None

def get_age_node(state: State):
    """循环获取用户年龄，直到正确"""
    prompt="请输入年龄："
    while True:
        age=interrupt(prompt)  # 注意恢复时会从头开始执行
        if isinstance(age,int) and age>0:
            return {"age":age}
        else:
            prompt="重新输入："



builder=StateGraph(State)
builder.add_node(get_age_node)
builder.add_edge(START, "get_age_node")
builder.add_edge("get_age_node", END)
graph=builder.compile(checkpointer=InMemorySaver())
config={"configurable": {"thread_id": "thread_5"}}
print(graph.invoke({"age": None}, config=config))

print(graph.invoke(
    Command(resume=-12345),
    config=config
))

print(graph.invoke(
    Command(resume=12345),
    config=config
))
