"""为模型返回的工具调用补齐必需的调用 ID。"""

from uuid import uuid4

from langchain_core.messages import AIMessage


def ensure_tool_call_ids(message: AIMessage) -> AIMessage:
    """补齐缺失的工具调用 ID，保留模型已返回的有效 ID。

    部分 OpenAI 兼容接口偶尔省略工具调用 ID。LangGraph 的 ``ToolNode``
    需要该 ID 将工具结果关联回对应的 ``AIMessage``，因此在进入 ToolNode
    前统一补齐。
    """
    message.tool_calls = [
        {
            **tool_call,
            "id": tool_call.get("id") or f"call_{uuid4().hex}",
        }
        for tool_call in message.tool_calls
    ]
    return message
