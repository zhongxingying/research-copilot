# app/core/context_monitor.py
import tiktoken

from app.core.logging import get_logger

logger = get_logger(__name__)

# DeepSeek 兼容 OpenAI tokenizer，用 cl100k_base 近似
_encoder = tiktoken.get_encoding("cl100k_base")

# DeepSeek-chat 上下文窗口 64k
DEFAULT_CONTEXT_WINDOW = 64_000


def count_tokens(text: str) -> int:
    return len(_encoder.encode(text))


def count_messages_tokens(messages: list[dict]) -> int:
    """近似计算 messages 的 token 数（含 role 开销）。"""
    total = 0
    for m in messages:
        total += count_tokens(m.get("content", ""))
        total += 4  # 每条消息的 role/分隔符开销
    return total + 2


def context_usage(messages: list[dict], window: int = DEFAULT_CONTEXT_WINDOW) -> dict:
    used = count_messages_tokens(messages)
    return {
        "used_tokens": used,
        "window": window,
        "usage_ratio": round(used / window, 4),
        "remaining": window - used,
    }
