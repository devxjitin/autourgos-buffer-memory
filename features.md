# autourgos-buffer-memory — Features

In-memory short-term conversation buffer for Autourgos agents. Three classes covering the three common shapes of "keep recent chat history in RAM": a message-count-bounded ring buffer, an unbounded buffer, and a TTL-expiring buffer. Zero I/O, implements `autourgos_memory.BaseMemory` as a drop-in `Agent(memory=...)` backend.

## Full Feature List

- **`RuntimeShortTermMemory`** — ring buffer capped at `max_messages` (default 20); oldest messages dropped once the cap is exceeded
- **`ConversationBufferMemory`** — same message shape, no truncation, keeps the entire session
- **`ExpiringBufferMemory`** — per-message TTL (`default_ttl_seconds`, or a per-call `ttl_seconds=` override, including an explicit `ttl_seconds=None` to make one message permanent); expired messages are purged lazily on the next add/read (no background thread) and never surface in `get_messages()`/`format_for_llm()`; optional `max_messages` ring cap on live messages
- Uniform API across all three: `add_user_message`, `add_agent_message`, `add_tool_message`, `add_system_message`, `get_messages()`, `format_for_llm()`, `clear()`
- Implements `autourgos_memory.BaseMemory` — plugs directly into `Agent(memory=...)` with no adapter code
- Zero I/O — no disk, no network, the fastest backend in the Autourgos memory family, but not persistent across restarts and not shared across processes

## Competitor Comparison

Landscape research on in-process/short-term chat memory libraries, current as of the search date.

| Capability | **autourgos-buffer-memory** | [LangChain `ConversationBufferMemory`/`ConversationBufferWindowMemory`](https://python.langchain.com/) | [LangGraph `MemorySaver` (in-memory checkpointer)](https://langchain-ai.github.io/langgraph/) | [Mem0](https://mem0.ai/) | Plain Python list/`collections.deque` |
|---|---|---|---|---|---|
| Scope | Standalone library, zero dependencies | Part of a large orchestration framework | Part of LangGraph's state/checkpoint system | Managed cross-session memory layer (API/service or self-hosted) | DIY |
| Ring-buffer (last-N messages) | Yes, `RuntimeShortTermMemory` | Yes, `ConversationBufferWindowMemory` (last k *interactions*, i.e. k turns not k messages) | Not directly — it checkpoints full graph state, not a bounded chat window | N/A — memory is fact/summary based, not a raw window | Yes, if hand-rolled with `deque(maxlen=N)` |
| Unbounded full-history buffer | Yes, `ConversationBufferMemory` | Yes, `ConversationBufferMemory` | Yes, effectively (full state per checkpoint) | N/A (extracted-memory model, not raw transcript) | Yes, trivially |
| TTL / time-scoped message expiry | Yes, `ExpiringBufferMemory`, lazy purge, per-message override | No built-in equivalent | No | Yes, via memory decay/expiry policies (managed feature) | No, unless hand-built |
| Persistence across process restarts | No (by design — that's `autourgos-local-memory`'s job) | No (in-memory variant); needs a message-history backend for persistence | Yes, with `PostgresSaver`/`SqliteSaver` instead of `MemorySaver` | Yes, managed | No |
| Dependencies | Zero | Full LangChain core | Full LangGraph/LangChain core | SDK + managed backend (or self-hosted vector/graph store) | None |
| Cross-session / cross-user long-term recall | No — explicitly short-term/session-scoped | No (that's LangMem/other LangChain memory modules) | No (thread-scoped state, not user memory) | Yes — this is Mem0's core specialty | No |
| Pricing | Free, open source | Free, open source | Free, open source | Free tier + paid managed plans | Free |

### How to read this

- **vs. LangChain's buffer memories**: functionally close cousins — both offer bounded/unbounded in-memory chat buffers — but autourgos-buffer-memory is a zero-dependency standalone package rather than a slice of a much larger framework, and it adds a TTL-expiring class LangChain's core memory types don't have.
- **vs. LangGraph's `MemorySaver`**: LangGraph's in-memory checkpointer solves a different problem — durable, resumable *graph execution state* — not a simple bounded chat-message window; adopting it means adopting LangGraph.
- **vs. Mem0**: Mem0 operates one layer up — extracted, deduplicated, cross-session *facts* about a user, typically via a managed service — not a raw short-term message buffer. The two are complementary rather than substitutes; a Mem0-backed agent would still want something like this for the current turn's raw scratchpad.
- **vs. a plain list/deque**: this package's value-add over rolling your own is the shared `BaseMemory` interface (drop-in for `Agent(memory=...)` and any middleware written against that contract), the TTL class, and the tested edge cases (lazy expiry, per-message TTL override) that a five-minute `deque` doesn't have.
- Buffer memory is intentionally the "cheapest, dumbest, fastest" tier of the Autourgos memory family — for anything needing persistence, semantic recall, or summarization, the README itself points to `autourgos-local-memory`, `autourgos-semantic-memory`, `autourgos-summary-memory`, or `autourgos-token-memory`.

Sources:
- [LangChain Memory Component Deep Dive: Chain Components and Runnable Study](https://dev.to/jamesli/langchain-memory-component-deep-dive-chain-components-and-runnable-study-359p)
- [ConversationBufferWindowMemory — LangChain 0.0.149 docs](https://lagnchain.readthedocs.io/en/latest/modules/memory/types/buffer_window.html)
- [ConversationBufferMemory — LangChain 0.0.107 docs](https://langchain-doc.readthedocs.io/en/latest/modules/memory/types/buffer.html)
- [How to Implement LangChain Memory](https://oneuptime.com/blog/post/2026-01-27-langchain-memory/view)
- [LangGraph Memory vs Mem0: Which Should You Use in 2026?](https://atlan.com/know/ai-agent/ai-agent-memory/langgraph-memory-vs-mem0/)
- [Best AI Agent Memory Frameworks in 2026: Compared and Ranked](https://atlan.com/know/best-ai-agent-memory-frameworks-2026/)
