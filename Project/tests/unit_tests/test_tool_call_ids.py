from agent.common.tool_call_ids import ensure_tool_call_ids
from langchain_core.messages import AIMessage


def test_ensure_tool_call_ids_adds_missing_id():
    message = AIMessage(
        content="",
        tool_calls=[{"name": "demo", "args": {}, "id": None, "type": "tool_call"}],
    )

    normalized = ensure_tool_call_ids(message)

    assert normalized.tool_calls[0]["id"].startswith("call_")


def test_ensure_tool_call_ids_preserves_existing_id():
    message = AIMessage(
        content="",
        tool_calls=[{"name": "demo", "args": {}, "id": "provider-call-1", "type": "tool_call"}],
    )

    normalized = ensure_tool_call_ids(message)

    assert normalized.tool_calls[0]["id"] == "provider-call-1"
