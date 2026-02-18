from __future__ import annotations

from collections import deque
from typing import Deque, Iterable


class MemoryManager:
    """Short-term in-memory conversation buffer for LLM context."""

    def __init__(self, limit: int = 12) -> None:
        self.limit = max(2, int(limit))
        self._buffer: Deque[dict[str, str]] = deque(maxlen=self.limit)

    def prime(self, history: Iterable[dict[str, str]]) -> None:
        """Load initial items (e.g., from persisted history)."""
        for item in history:
            role = item.get("role")
            text = item.get("text")
            if isinstance(role, str) and isinstance(text, str):
                self.append(role, text)

    def append(self, role: str, text: str) -> None:
        if not role or not text:
            return
        self._buffer.append({"role": role, "text": text})

    def as_list(self) -> list[dict[str, str]]:
        return list(self._buffer)

    def clear(self) -> None:
        self._buffer.clear()

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._buffer)
