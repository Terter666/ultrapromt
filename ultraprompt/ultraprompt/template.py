class PromptTemplate:
    def __init__(self, template: str, required_vars=None):
        self.template = template
        self.required_vars = set(required_vars or [])

    def format(self, **kwargs):
        missing = self.required_vars - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing variables: {missing}")
        return self.template.format(**kwargs)
