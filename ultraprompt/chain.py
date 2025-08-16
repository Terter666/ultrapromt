
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Callable, Optional
from .templates import PromptTemplate
from .engines import LLMEngine
from .tools import Tool, ToolResult
from .safety import redact_pii

@dataclass
class Step:
    name: str
    template: PromptTemplate
    postprocess: Optional[Callable[[str], str]] = None

class Chain:
    """
    Linear chain: render -> engine.complete -> optional postprocess.
    """
    def __init__(self, engine: LLMEngine, steps: List[Step]):
        self.engine = engine
        self.steps = steps
        self.history: List[Tuple[str,str]] = []

    def run(self, variables: Dict[str, str]) -> str:
        out = ""
        for step in self.steps:
            prompt = step.template.render(variables | {"previous": out})
            prompt = redact_pii(prompt)
            response = self.engine.complete(prompt, self.history)
            if step.postprocess:
                response = step.postprocess(response)
            self.history.append(("user", prompt))
            self.history.append(("assistant", response))
            out = response
        return out

class ReActAgent:
    """
    Tiny ReAct-like loop:
    - Uses engine to propose next action
    - If the text contains "TOOL:<name>:<query>", run a tool by that name and feed result back.
    - Stops when engine returns a line beginning with "FINAL:"
    """
    def __init__(self, engine: LLMEngine, tools: List[Tool], max_iters: int = 5):
        self.engine = engine
        self.tools = {t.name: t for t in tools}
        self.max_iters = max_iters
        self.trace: List[str] = []

    def run(self, task: str) -> str:
        context = task
        for i in range(self.max_iters):
            thought = self.engine.complete(f"Task: {context}\nThink then act. Use TOOL:name:query if needed. End with FINAL: answer.")
            self.trace.append(f"THOUGHT_{i}: {thought}")
            if "TOOL:" in thought:
                try:
                    _, rest = thought.split("TOOL:", 1)
                    name, query = rest.split(":", 1)
                    name = name.strip()
                    query = query.strip()
                    tool = self.tools.get(name)
                    if not tool:
                        context += f"\nTool {name} not found."
                        continue
                    result: ToolResult = tool.run(query)
                    context += f"\nObservation({name}): {result.content}"
                    continue
                except Exception as e:
                    context += f"\nTool parse error: {e}"
                    continue
            if thought.strip().startswith("FINAL:"):
                return thought.strip()[6:].strip()
            context += f"\nAssistant: {thought}"
        return "Reached max iterations without FINAL."
