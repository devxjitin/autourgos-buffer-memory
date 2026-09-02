# Changelog

## [2.1.1] - 2026-09-01

- Metadata: added `maintainers` (Sonia, Vishwanil Suman) to `pyproject.toml`,
  and linked the README's existing Sonia contributor badge to her GitHub
  profile (https://github.com/dahiyasonia). No code changes.

## [2.1.0] - 2026-08-31

- Added: `ExpiringBufferMemory` — a `BaseMemory` implementation where each message carries a
  time-to-live (`default_ttl_seconds` at construction, or a per-call `ttl_seconds` override).
  Expired messages are purged lazily on the next add/read and never appear in
  `get_messages()`/`format_for_llm()`. For a long-running/background agent's temporary,
  run-scoped facts that shouldn't silently persist into a later, unrelated run.

## [2.0.1] - 2026-07-27

- Added: module logger. Docs: added explicit Quick Start heading and fixed the undefined my_llm placeholder.

All notable changes to `autourgos-buffer-memory` are documented here.

---

## [2.0.0] - 2026-07-27

### Changed
- BREAKING: this package now depends on `autourgos-memory>=1.0.1` (previously zero-dependency). `BaseMemory`/`BaseRetriever`/`Document`/`MemoryMessage` are now re-exported from `autourgos-memory` instead of duplicated locally. No public API/behavior change for typical usage.

## [1.0.1] - 2026-07-27

### Fixed
- `__version__` fallback in `__init__.py` now matches `pyproject.toml` (was incorrectly `1.0.2`, now `1.0.0`).
- Wording correction: CHANGELOG previously referenced a non-existent `autourgos-core` package; now correctly states there is no dependency on `autourgos-memory` or any other Autourgos package.

## [1.0.0] - 2026-06-17

### Added
- Initial release.
- Runtime and unbounded conversation buffer memory implementations.
- Self-contained package — no dependency on `autourgos-memory` or any other Autourgos package.
- All base interfaces (`BaseMemory`, `BaseRetriever`, `MemoryMessage`, `Document`) inlined.
- Thread-safe implementation using `threading.RLock`.
- Full type annotations and `py.typed` marker.

