from .template import PromptTemplate

class Step:
    def __init__(self, name: str, template: PromptTemplate):
        self.name = name
        self.template = template

    def run(self, engine, context):
        prompt = self.template.format(**context)
        response = engine.run(prompt)
        context[self.name] = response
        return response

class Chain:
    def __init__(self, engine, steps):
        self.engine = engine
        self.steps = steps

    def run(self, context):
        for step in self.steps:
            step.run(self.engine, context)
        return context[self.steps[-1].name]
