"""
memory.py — In-memory short-term buffers.
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional

from autourgos_memory import BaseMemory, MemoryMessage


class RuntimeShortTermMemory(BaseMemory):
    """In-memory ring buffer bounded by message count.

    Parameters
    ----------
    max_messages : int
        Maximum messages kept. Oldest are dropped when exceeded. Default 20.
    name : str
        Human-readable identifier.
    """

    def __init__(self, max_messages: int = 20, name: str = "runtime") -> None:
        if not isinstance(max_messages, int) or max_messages < 1:
            raise ValueError("max_messages must be an integer >= 1")
        self.max_messages = max_messages
        self.name = name
        self._messages: List[MemoryMessage] = []

    def add_message(self, role: str, content: str, timestamp: Optional[datetime] = None) -> MemoryMessage:
        msg = MemoryMessage(role=role, content=content, timestamp=timestamp or datetime.now(timezone.utc))
        self._messages.append(msg)
        if len(self._messages) > self.max_messages:
            self._messages = self._messages[-self.max_messages:]
        return msg

    def add_user_message(self, content: str) -> MemoryMessage:
        return self.add_message("user", content)

    def add_agent_message(self, content: str) -> MemoryMessage:
        return self.add_message("agent", content)

    def add_system_message(self, content: str) -> MemoryMessage:
        return self.add_message("system", content)

    def add_tool_message(self, tool_name: str, result: str) -> MemoryMessage:
        return self.add_message("tool", f"[{tool_name} returned]: {result}")

    def get_messages(self) -> List[Dict[str, str]]:
        _ROLE = {"user": "user", "agent": "assistant", "system": "system", "tool": "tool"}
        return [{"role": _ROLE.get(m.role, m.role), "content": m.content} for m in self._messages]

    def clear(self) -> None:
        self._messages = []

    def format_for_llm(self, query: Optional[str] = None) -> str:
        if not self._messages:
            return ""
        lines = "\n".join(f"{m.role}: {m.content}" for m in self._messages)
        return f"\n--- Previous Conversation Context ---\n{lines}\n--------------------------------------\n"


class ConversationBufferMemory(RuntimeShortTermMemory):
    """Unbounded in-memory conversation buffer (no truncation).

    Use this when you want to keep every message in RAM for the session.
    For long conversations, prefer :class:`RuntimeShortTermMemory` with a cap,
    or :class:`~autourgos_summary_memory.SummaryBufferedMemory` for LLM compression.
    """

    def __init__(self, name: str = "conversation") -> None:
        super().__init__(max_messages=sys.maxsize, name=name)
