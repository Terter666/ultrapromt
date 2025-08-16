
from __future__ import annotations
from typing import List, Tuple

class LLMEngine:
    """
    Abstract LLM interface. Implement `complete` to return a string.
    """
    def complete(self, prompt: str, history: List[Tuple[str,str]] | None = None) -> str:
        raise NotImplementedError

class MockEngine(LLMEngine):
    """
    A tiny rule-based engine useful for demos/tests.
    - Echoes the prompt
    - If prompt contains "calc(", it extracts and computes basic arithmetic inside
    """
    def complete(self, prompt: str, history: List[Tuple[str,str]] | None = None) -> str:
        if "calc(" in prompt and ")" in prompt:
            expr = prompt.split("calc(",1)[1].split(")",1)[0]
            try:
                allowed = set("0123456789.+-*/() ")
                if set(expr) <= allowed:
                    val = eval(expr, {"__builtins__": {}}, {})
                    return f"[calc:{expr}] => {val}"
            except Exception:
                pass
        return f"[mock] {prompt[:300]}"
