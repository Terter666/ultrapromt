
"""
ultraprompt: A compact, advanced prompt-engineering toolkit.
- Prompt templating with variable validation
- Conversation memory (buffer + summarizer)
- Safety filters (PII redaction, simple profanity)
- Lightweight tool system (calculator, safe python evaluator)
- Simple LLM engine interface with a Mock engine
- Chain and a tiny ReAct-like Agent
- Caching (in-memory LRU + JSONL disk cache)
- Evaluation helpers
All stdlib, zero external deps.
"""
from .templates import PromptTemplate
from .memory import ConversationMemory
from .safety import redact_pii, contains_profanity
from .tools import Tool, CalculatorTool, PythonTool, ToolResult
from .engines import LLMEngine, MockEngine
from .cache import LRUCache, DiskCache
from .chain import Chain, Step, ReActAgent
from .eval import exact_match, regex_match, contains, timeblock
