
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class ToolResult:
    content: str
    ok: bool = True
    meta: Dict[str, Any] | None = None

class Tool:
    name: str = "tool"
    description: str = "abstract tool"
    def run(self, query: str) -> ToolResult:
        raise NotImplementedError

class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate simple arithmetic expressions like: 2 + 2 * (3 - 1)"
    def run(self, query: str) -> ToolResult:
        try:
            # extremely restricted eval: digits, operators, spaces, parentheses, dot
            allowed = set("0123456789.+-*/() ")
            if not set(query) <= allowed:
                return ToolResult("Disallowed characters", ok=False)
            result = eval(query, {"__builtins__": {}}, {})
            return ToolResult(str(result))
        except Exception as e:
            return ToolResult(f"Error: {e}", ok=False)

class PythonTool(Tool):
    name = "python"
    description = "Run tiny python snippets in a sandbox (no imports)."
    def run(self, query: str) -> ToolResult:
        # prohibit imports and dunders for safety
        if "import " in query or "__" in query:
            return ToolResult("Unsafe code blocked.", ok=False)
        env = {"__builtins__": {"len": len, "sum": sum, "min": min, "max": max, "range": range}}
        try:
            # If it's an expression, eval; otherwise exec and capture 'out' variable
            try:
                val = eval(query, env, {})
                return ToolResult(str(val))
            except SyntaxError:
                loc: Dict[str, Any] = {}
                exec(query, env, loc)
                out = loc.get("out", "OK")
                return ToolResult(str(out))
        except Exception as e:
            return ToolResult(f"Error: {e}", ok=False)
