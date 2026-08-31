# autourgos-buffer-memory

[![Framework: Autourgos](https://img.shields.io/badge/Framework-Autourgos-orange.svg)](https://github.com/devxjitin)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/autourgos-buffer-memory/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/devxjitin/autourgos-buffer-memory/blob/main/LICENSE)
[![Author](https://img.shields.io/badge/Author-Jitin%20Kumar%20Sengar-blue.svg)](https://github.com/devxjitin)
[![Contributor](https://img.shields.io/badge/Contributor-Sonia-blueviolet.svg)]()
[![Contributor](https://img.shields.io/badge/Contributor-Vishwanil%20Suman-blueviolet.svg)]()

In-memory short-term buffer for [Autourgos](https://github.com/devxjitin) agents. Two classes — a
message-count bounded ring buffer and an unbounded conversation buffer. Fast, zero I/O, ideal for
single-session use.

```python
from autourgos_buffer_memory import RuntimeShortTermMemory
from autourgos_agent import Agent
from autourgos_openaichat import OpenAIChatModel

my_llm = OpenAIChatModel(model="gpt-4o-mini")
memory = RuntimeShortTermMemory(max_messages=20)
agent  = Agent(llm=my_llm, memory=memory)

agent.invoke("My name is Jitin")
agent.invoke("What is my name?")
# → "Your name is Jitin."
```

---

## Features

- **`RuntimeShortTermMemory`** — keeps the last N messages in RAM, oldest dropped when the cap is exceeded
- **`ConversationBufferMemory`** — same shape, no truncation, keeps every message for the session
- Implements `autourgos_memory.BaseMemory` — drop-in for `Agent(memory=...)`
- Zero I/O, fastest option in the memory family

---

## Table of Contents

- [Install](#install)
- [Classes](#classes)
- [Parameters](#parameters)
- [API](#api)
- [License](#license)

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
from autourgos_agent import Agent
from autourgos_openaichat import OpenAIChatModel

my_llm = OpenAIChatModel(model="gpt-4o-mini")
memory = RuntimeShortTermMemory(max_messages=20)
agent  = Agent(llm=my_llm, memory=memory)

agent.invoke("My name is Jitin")
agent.invoke("What is my name?")
# → "Your name is Jitin."
```

### ConversationBufferMemory

Same as `RuntimeShortTermMemory` but with no truncation — keeps every message for the session.

```python
from autourgos_buffer_memory import ConversationBufferMemory

memory = ConversationBufferMemory()
agent  = Agent(llm=my_llm, memory=memory)
```

> For long conversations, use `autourgos-summary-memory` or `autourgos-token-memory` to stay within context
> window limits.

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

## License

Apache License 2.0, Copyright (c) 2026 Jitin Kumar Sengar
