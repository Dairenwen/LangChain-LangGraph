import os
import json
from uuid import uuid4
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage, HumanMessage
from langchain_tavily import TavilySearch
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()
import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Overwrite

# 0.定义模型和搜索工具
model = ChatOpenAI(
    model="gpt-5.4",
    api_key=os.getenv("PACKYAPI_API_KEY"),
    base_url="https://www.packyapi.com/v1/",
    use_responses_api=True,
    output_version="responses/v1",
)

tool = TavilySearch(max_results=10, tavily_api_key=os.getenv("TAVILY_API_KEY"))
tools=[tool]
model_with_tools = model.bind_tools(tools=tools)
# 1.状态定义
class MessageState(TypedDict):
    messages: Annotated[list, add_messages]  # 上下文消息列表
    llm_call_count: Annotated[int, operator.add]  # 调用LLM次数

# 2.节点定义
def llm_call(state: MessageState):
    """调用LLM"""
    messages = state["messages"]
    # 调用模型
    response = model_with_tools.invoke(
        input=[
            SystemMessage(content="你是一个有帮助的助手。"),
        ]+messages
    )
    return {
        "messages": [response],  # 将模型的响应添加到消息列表中
        "llm_call_count": 1,  # 调用次数加1
    }


tools_by_name ={tool.name: tool for tool in tools}
def tool_node(state: MessageState):
    """调用工具"""
    messages = state["messages"]
    # 调用工具
    result=[]
    # 当前最新消息就是带有tool_calls的AIMessage
    # tool_call["name"] 说明调用哪个工具
    # tool_call["args"] 说明传什么参数
    # tool_call["id"]   说明这是哪一次调用
    for tool_call in messages[-1].tool_calls:
        tool=tools_by_name[tool_call["name"]]
        obs=tool.invoke(tool_call["args"])
        result.append(
            ToolMessage(
                tool_call_id=tool_call["id"],
                content=json.dumps(obs, ensure_ascii=False, default=str),
            )
        )

    return {
        "messages": result,  # 将工具的响应添加到消息列表中
        "llm_call_count": 0,  # 工具调用不增加LLM调用次数
    }

# 3.定义图
agent_builder=StateGraph(MessageState)
agent_builder.add_node("LLM调用", llm_call)
agent_builder.add_node("工具调用", tool_node)
# 4.添加边
agent_builder.add_edge(START, "LLM调用")

def should_continue(state: MessageState):
    """判断是否继续调用LLM"""
    messages = state["messages"]
    # 如果最新消息是AIMessage，并且包含tool_calls，则继续调用工具
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        return "工具调用"
    else:
        return END

agent_builder.add_conditional_edges(
    "LLM调用",
    should_continue,
    ["工具调用", END],
)
agent_builder.add_edge("工具调用", "LLM调用")


def print_history(agent, config, title):
    """打印当前 thread_id 下的所有历史 checkpoint。"""
    print("-" * 80)
    print(title)
    snapshots = list(agent.get_state_history(config))

    for snapshot in snapshots:
        checkpoint_id = snapshot.config["configurable"]["checkpoint_id"]
        message_count = len(snapshot.values.get("messages", []))
        print(
            "checkpoint_id:",
            checkpoint_id,
            "消息数:",
            message_count,
            "下一节点:",
            snapshot.next,
        )

    return snapshots


def find_snapshot(snapshots, message_count, next_node):
    """按照消息数量和下一节点找到一个指定快照。"""
    for snapshot in snapshots:
        if (
            len(snapshot.values.get("messages", [])) == message_count
            and snapshot.next == (next_node,)
        ):
            return snapshot
    raise ValueError(f"没有找到消息数为 {message_count} 且下一节点为 {next_node} 的快照")


def replay_demo(agent):
    """重放：从工具调用前的 checkpoint 开始，重新执行后续步骤。"""
    config = {
        "configurable": {
            "thread_id": f"replay-demo-{uuid4()}"
        }
    }

    print("\n========== 重放示例 ==========")
    agent.invoke(
        {
            "messages": [
                HumanMessage(content="今天西安的天气如何？")
            ]
        },
        config=config,
    )

    first_history = print_history(agent, config, "第一次执行历史")

    # 消息数为 2 时，一般是：HumanMessage + 带 tool_calls 的 AIMessage
    # 下一节点是“工具调用”，说明将从工具节点继续执行。
    to_replay = find_snapshot(first_history, message_count=2, next_node="工具调用")

    print("-" * 80)
    print("准备从这个 checkpoint 后面重新执行:")
    print(to_replay.config)

    replay_result = agent.invoke(None, config=to_replay.config)
    print_history(agent, config, "重放后的完整历史")

    print("-" * 80)
    print("重放后的最终回答:")
    replay_result["messages"][-1].pretty_print()


def update_state_demo(agent):
    """更新状态：修改历史 checkpoint 中的用户输入，然后继续执行。"""
    config = {
        "configurable": {
            "thread_id": f"update-demo-{uuid4()}"
        }
    }

    print("\n========== 更新状态示例 ==========")
    agent.invoke(
        {
            "messages": [
                HumanMessage(content="今天西安的天气如何？")
            ]
        },
        config=config,
    )

    first_history = print_history(agent, config, "第一次执行历史")

    # 消息数为 1 时，一般是：只有用户输入，下一步将进入 LLM 调用。
    selected_state = find_snapshot(first_history, message_count=1, next_node="LLM调用")

    print("-" * 80)
    print("更新前 checkpoint 配置:")
    print(selected_state.config)

    new_config = agent.update_state(
        selected_state.config,
        {
            "messages": Overwrite([
                HumanMessage(content="今天北京的天气如何？") # 直接用 Overwrite 替换掉原来的消息
            ])
        },
    )

    print("-" * 80)
    print("更新后 checkpoint 配置:")
    print(new_config)

    update_result = agent.invoke(None, config=new_config)

    print("-" * 80)
    print("更新状态后重新执行的消息:")
    for message in update_result["messages"]:
        message.pretty_print()


# 5.编译图
DB_URI = "postgresql://postgres:dairenwen1092@127.0.0.1:5432/postgres"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # 先采用内存保存器,只在当前运行中有效,如果需要持久化保存,可以使用PostgresSQL
    # checkpointer = InMemorySaver()
    # 第一次使用 Postgres 检查点时需要调用 checkpointer.setup()
    checkpointer.setup()

    # 编译图
    agent = agent_builder.compile(checkpointer=checkpointer)

    # 6.运行图
    replay_demo(agent)
    update_state_demo(agent)
