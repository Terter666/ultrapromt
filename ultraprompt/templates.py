
from __future__ import annotations
from typing import Dict, Any

class PromptTemplate:
    """
    Simple f-string style templates with required variable validation.
    Example:
        t = PromptTemplate("Summarize: {text} in {n} bullets.", required={"text", "n"})
        prompt = t.render({"text": "hello", "n": 3})
    """
    def __init__(self, template: str, required: set[str] | None = None):
        self.template = template
        self.required = set(required) if required else set()

    def render(self, vars: Dict[str, Any]) -> str:
        missing = self.required - set(vars.keys())
        if missing:
            raise KeyError(f"Missing variables for template: {sorted(missing)}")
        # basic safety: stringify unknowns explicitly
        safe = {k: ("" if v is None else str(v)) for k,v in vars.items()}
        try:
            return self.template.format(**safe)
        except KeyError as e:
            raise KeyError(f"Missing variable: {e}") from e

    def __repr__(self) -> str:
        return f"PromptTemplate(len={len(self.template)}, required={sorted(self.required)})"
