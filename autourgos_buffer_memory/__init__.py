"""
autourgos-buffer-memory — In-memory short-term buffers for Autourgos agents.

    from autourgos_buffer_memory import RuntimeShortTermMemory, ConversationBufferMemory
"""
import logging

from .memory import RuntimeShortTermMemory, ConversationBufferMemory

logger = logging.getLogger(__name__)

try:
    from importlib.metadata import version as _v
    __version__ = _v("autourgos-buffer-memory")
except Exception:
    logger.debug("could not resolve installed version for autourgos-buffer-memory", exc_info=True)
    __version__ = "2.0.2"

__all__ = ["RuntimeShortTermMemory", "ConversationBufferMemory"]
