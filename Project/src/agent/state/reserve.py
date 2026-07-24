# 这里是预定子图的状态定义
from langgraph.graph import MessagesState

# 预定状态
class ReserveState(MessagesState):
    title: str         # 预定的房源
    phone_number: str  # 预定电话
    id_card: str       # 身份证