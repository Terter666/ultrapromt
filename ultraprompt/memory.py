
from __future__ import annotations
from typing import List, Tuple

class ConversationMemory:
    """
    Rolling buffer + tiny summarizer.
    """
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.buffer: List[Tuple[str,str]] = []  # (role, content)

    def add(self, role: str, content: str) -> None:
        self.buffer.append((role, content))
        if len(self.buffer) > self.max_messages:
            self.buffer.pop(0)

    def get(self) -> List[Tuple[str,str]]:
        return list(self.buffer)

    def summarize(self) -> str:
        # naive: join last 8 messages, keep role tags
        last = self.buffer[-8:]
        lines = [f"{r.upper()}: {c}" for r,c in last]
        text = " | ".join(lines)
        if len(text) > 500:
            text = text[:497] + "..."
        return text
