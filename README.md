# autourgos-buffer-memory

In-memory short-term buffer for [Autourgos](https://github.com/devxjitin) agents.

Two classes — a message-count bounded ring buffer and an unbounded conversation buffer. Fast, zero I/O, ideal for single-session use.

---

## Install

```bash
pip install autourgos-buffer-memory
```

---

## Classes

### RuntimeShortTermMemory

Keeps the last N messages in RAM. Oldest messages are dropped when the cap is exceeded.

```python
from autourgos_buffer_memory import RuntimeShortTermMemory
from autourgos_react_agent import ReactAgent

memory = RuntimeShortTermMemory(max_messages=20)
agent  = ReactAgent(llm=my_llm, memory=memory)

agent.invoke("My name is Jitin")
agent.invoke("What is my name?")
# → "Your name is Jitin."
```

### ConversationBufferMemory

Same as `RuntimeShortTermMemory` but with no truncation — keeps every message for the session.

```python
from autourgos_buffer_memory import ConversationBufferMemory

memory = ConversationBufferMemory()
agent  = ReactAgent(llm=my_llm, memory=memory)
```

> For long conversations, use `autourgos-summary-memory` or `autourgos-token-memory` to stay within context window limits.

---

## Parameters

### RuntimeShortTermMemory

| Parameter | Type | Default | Description |
|---|---|---|---|
| `max_messages` | int | `20` | Max messages kept. Oldest dropped when exceeded. |
| `name` | str | `"runtime"` | Human-readable identifier. |

### ConversationBufferMemory

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | str | `"conversation"` | Human-readable identifier. |

---

## API

```python
memory.add_user_message("Hello")
memory.add_agent_message("Hi there!")
memory.add_tool_message("search", "Found 5 results")
memory.add_system_message("You are a helpful assistant")

messages = memory.get_messages()   # list of role/content dicts
context  = memory.format_for_llm() # formatted string for LLM prompt
memory.clear()
```

---

## Links

- PyPI: https://pypi.org/project/autourgos-buffer-memory/
- GitHub: https://github.com/devxjitin/autourgos-buffer-memory
- Issues: https://github.com/devxjitin/autourgos-buffer-memory/issues

---

## License

MIT — see [LICENSE](LICENSE)
