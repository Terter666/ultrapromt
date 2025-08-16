
from __future__ import annotations
from collections import OrderedDict
import json, time, os
from typing import Any, Tuple

class LRUCache:
    def __init__(self, capacity: int = 128):
        self.capacity = capacity
        self.cache: OrderedDict[str, Tuple[float, Any]] = OrderedDict()

    def get(self, key: str):
        if key in self.cache:
            ts, val = self.cache.pop(key)
            self.cache[key] = (ts, val)
            return val
        return None

    def set(self, key: str, value: Any):
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = (time.time(), value)

class DiskCache:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w") as f:
                pass

    def append(self, key: str, value: Any):
        rec = {"ts": time.time(), "key": key, "value": value}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def iter(self):
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except Exception:
                    continue
