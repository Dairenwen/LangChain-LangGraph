# 正式开始LangGraph
# langgraph设计的流程是：状态定义->节点定义->定义图->添加节点->添加边->运行图
# 1.状态定义
import operator
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
class PackageState(TypedDict):
    package_id: int             # 包裹id
    origin: str                 # 包裹起点
    destination: str            # 包裹终点
    status: str                 # 包裹状态
    # history: list[str]          # 包裹状态历史记录，这样是覆盖更新
    history_append: Annotated[list[str], operator.add]  # 包裹状态历史记录，这样是追加更新
    priority: str               # 包裹优先级
#                                  加急配送
#                                /         \
# 整个流程初步定义为：揽收站->分拣中心            派送站
#                                \         /
#                                  标准配送
# 2.节点定义

# 揽收站节点
def receive_package(state: PackageState):
    origin = state["origin"]
    return {
        "status": "已揽收",
        "history_append": [f"包裹已从{origin}揽收"],
    }
# 分拣中心节点：根据目的地进行分拣
def sort_package(state: PackageState):
    """分拣中心"""
    destination = state["destination"]
    if destination in ["北京", "上海", "广州"]:
        return {
            "status": "已分拣",
            "history_append": [f"包裹已分拣到{destination}"],
        }
    else:
        return {
            "status": "已分拣",
            "history_append": [f"包裹已分拣到其他城市"],
        }
# 配送站节点
def final_delivery(state: PackageState):
    """派送站"""
    destination = state["destination"]
    return {
        "status": "已派送",
        "history_append": [f"包裹已派送到{destination}"],
    }
# 标准配送节点
def standard_delivery(state: PackageState):
    """标准配送"""
    return {
        "status": "已派送",
        "history_append": [f"包裹正在标准配送"],
    }
# 加急配送节点
def express_delivery(state: PackageState):
    """加急配送"""
    return {
        "status": "已派送",
        "history_append": [f"包裹正在加急配送"],
    }

# 3.定义图
delivery=StateGraph(PackageState)

# 4.添加节点
delivery.add_node("揽收站", receive_package)
delivery.add_node("分拣中心", sort_package)
delivery.add_node("派送站", final_delivery)
delivery.add_node("标准配送", standard_delivery)
delivery.add_node("加急配送", express_delivery)

# 5.添加边
# 固定边
delivery.add_edge(START, "揽收站")
delivery.add_edge("揽收站", "分拣中心")
# 条件边
def select_delivery(state: PackageState):
    """根据包裹的优先级选择配送方式"""
    if state["priority"] == "加急":
        return "加急配送"
    else:
        return "标准配送"
delivery.add_conditional_edges(
    "分拣中心",
    select_delivery, # 确定下一个节点名称的函数
    ["标准配送", "加急配送"], # 可能的下一个节点名称列表
)
delivery.add_edge("标准配送", "派送站")
delivery.add_edge("加急配送", "派送站")
delivery.add_edge("派送站", END)

# 6.编译图
delivery_system=delivery.compile()
# 7.运行图
result = delivery_system.invoke({
    "package_id": 1,
    "origin": "深圳",
    "destination": "北京",
    "priority": "加急",
    "history_append": [],
})
print(result)

# 示例二：
class MessageState(TypedDict):
    # 消息列表：
    # 1.会话记忆，记录对话历史；2.上下文维护，方便获取上下文信息；3.消息发送，记录消息发送状态
    messages: Annotated[list[str], operator.add]  # 上下文消息列表
    # 调用LLM次数
    llm_call_count: int
