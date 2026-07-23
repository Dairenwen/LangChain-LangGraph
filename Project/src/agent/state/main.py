# 主图的状态，可共享，为全局
from typing import TypedDict
from langgraph.graph import MessagesState

class State(MessagesState):
    user_intent: str                # 用户意图
    user_preferences: dict          # 用户偏好

class NeedReserveOutput(TypedDict):
    reserve: str  # 这个字段不会出现在最终状态中