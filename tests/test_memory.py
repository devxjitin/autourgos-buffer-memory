"""Smoke tests for RuntimeShortTermMemory and ConversationBufferMemory."""
from autourgos_buffer_memory import RuntimeShortTermMemory, ConversationBufferMemory


def test_add_and_get_messages_normal():
    mem = RuntimeShortTermMemory(max_messages=10)
    mem.add_user_message("hello")
    mem.add_agent_message("hi there")
    msgs = mem.get_messages()
    assert [m["role"] for m in msgs] == ["user", "assistant"]
    assert [m["content"] for m in msgs] == ["hello", "hi there"]


def test_ring_buffer_evicts_oldest():
    mem = RuntimeShortTermMemory(max_messages=2)
    mem.add_user_message("a")
    mem.add_user_message("b")
    mem.add_user_message("c")
    msgs = mem.get_messages()
    assert [m["content"] for m in msgs] == ["b", "c"]


def test_clear_empties_buffer():
    mem = RuntimeShortTermMemory(max_messages=5)
    mem.add_user_message("x")
    mem.clear()
    assert mem.get_messages() == []
    assert mem.format_for_llm() == ""


def test_conversation_buffer_memory_is_unbounded():
    mem = ConversationBufferMemory()
    for i in range(50):
        mem.add_user_message(str(i))
    assert len(mem.get_messages()) == 50
