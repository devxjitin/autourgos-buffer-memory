# autourgos-buffer-memory

[![Framework: Autourgos](https://img.shields.io/badge/Framework-Autourgos-orange.svg)](https://github.com/devxjitin)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/autourgos-buffer-memory/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/devxjitin/autourgos-buffer-memory/blob/main/LICENSE)
[![Author](https://img.shields.io/badge/Author-Jitin%20Kumar%20Sengar-blue.svg)](https://github.com/devxjitin)
[![Contributor](https://img.shields.io/badge/Contributor-Sonia-blueviolet.svg)](https://github.com/dahiyasonia)
[![Contributor](https://img.shields.io/badge/Contributor-Vishwanil%20Suman-blueviolet.svg)]()

In-memory short-term buffer for [Autourgos](https://github.com/devxjitin) agents. Three classes — a
message-count bounded ring buffer, an unbounded conversation buffer, and a TTL-expiring buffer.
Fast, zero I/O, ideal for single-session use.

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
- **`ExpiringBufferMemory`** — messages carry a time-to-live and are purged once expired; for a
  long-running/background agent's temporary, run-scoped facts that shouldn't outlive the run
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

### ExpiringBufferMemory

Each message carries a time-to-live; expired messages are purged automatically (lazily, on the
next add/read — no background thread) and never appear in `get_messages()`/`format_for_llm()`.
Meant for a long-running or background agent's temporary, run-scoped facts — worth remembering
for the next few minutes or hours of a task, but that shouldn't silently persist the way an
unbounded buffer would.

```python
from autourgos_buffer_memory import ExpiringBufferMemory

memory = ExpiringBufferMemory(default_ttl_seconds=3600)  # 1 hour default
agent  = Agent(llm=my_llm, memory=memory)

memory.add_user_message("Skip the venv folder for this run.")          # expires in 1 hour
memory.add_user_message("The deploy target is us-east-1.", ttl_seconds=None)  # never expires
```

Pass `ttl_seconds=` to any `add_*_message()` call to override `default_ttl_seconds` for that one
message; `ttl_seconds=None` (explicit) makes that message permanent even with a default TTL set.

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

### ExpiringBufferMemory

| Parameter | Type | Default | Description |
|---|---|---|---|
| `default_ttl_seconds` | float, optional | `None` | Applied when a message doesn't pass its own `ttl_seconds`. `None` = messages never expire unless given a per-call TTL. |
| `max_messages` | int, optional | `None` | Ring-buffer cap on *live* (non-expired) messages. `None` = unbounded. |
| `name` | str | `"expiring"` | Human-readable identifier. |

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
