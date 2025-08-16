
from __future__ import annotations
import time, re
from contextlib import contextmanager

def exact_match(a: str, b: str) -> bool:
    return a.strip() == b.strip()

def regex_match(text: str, pattern: str) -> bool:
    return re.search(pattern, text) is not None

def contains(text: str, substring: str) -> bool:
    return substring in text

@contextmanager
def timeblock():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"Elapsed: {end - start:.4f}s")
