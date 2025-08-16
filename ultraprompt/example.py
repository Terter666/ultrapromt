from ultraprompt import PromptTemplate, MockEngine, Step, Chain

engine = MockEngine()

steps = [
    Step("draft", PromptTemplate("Answer briefly: {q}", {"q"})),
    Step("refine", PromptTemplate("Make concise: {draft}"))
]

chain = Chain(engine, steps)
result = chain.run({"q": "Explain AI prompting in one sentence."})
print("Final:", result)
