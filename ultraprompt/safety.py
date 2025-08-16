
import re

_PROFANITY = {"damn", "hell"}  # demo list; extend in real use

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})")
_IP = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")

def redact_pii(text: str) -> str:
    """
    Redact common PII patterns (email, phone, IP).
    """
    text = _EMAIL.sub("[REDACTED_EMAIL]", text)
    text = _PHONE.sub("[REDACTED_PHONE]", text)
    text = _IP.sub("[REDACTED_IP]", text)
    return text

def contains_profanity(text: str) -> bool:
    tokens = {t.strip(".,!?;:").lower() for t in text.split()}
    return any(t in _PROFANITY for t in tokens)
