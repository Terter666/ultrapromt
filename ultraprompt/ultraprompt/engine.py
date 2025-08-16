class MockEngine:
    def run(self, prompt: str) -> str:
        return f"[Mocked AI Response]: {prompt[:50]}..."
