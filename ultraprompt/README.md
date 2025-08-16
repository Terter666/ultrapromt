
# ultraprompt

A compact, advanced prompt-engineering toolkit (stdlib only).

## Features
- Prompt templates with required-variable validation
- Conversation memory with naive summarizer
- Safety filters: PII redaction, simple profanity check
- Tool system: Calculator and sandboxed Python
- LLM engine interface + MockEngine for offline demos
- Chain and tiny ReAct-like agent loop
- Caching: in-memory LRU and JSONL disk cache
- Evaluation helpers and timing context manager

## Quickstart
```bash
python example.py
```

## Use in your own code
```python
from ultraprompt import PromptTemplate, MockEngine, Step, Chain

engine = MockEngine()
steps = [
  Step("draft", PromptTemplate("Answer briefly: {q}", {"q"})),
  Step("refine", PromptTemplate("Make concise: {previous}"))
]
print(Chain(engine, steps).run({"q": "What is prompt engineering?"}))
```
