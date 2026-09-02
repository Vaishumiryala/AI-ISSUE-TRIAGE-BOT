from __future__ import annotations
import re
from dataclasses import dataclass, field

RULES: list[tuple[str, list[str]]] = [
    ("bug", [r"\bbug\b", r"\bcrash(es|ed|ing)?\b", r"\berror\b", r"\bexception\b", r"\bnot working\b", r"\bbroken\b", r"\bfails?\b", r"\bfailing\b", r"\bregression\b", r"\bstack ?trace\b"]),
    ("enhancement", [r"\bfeature\b", r"\benhancement\b", r"\bfeature request\b", r"\bwould be nice\b", r"\bplease add\b", r"\bsupport for\b", r"\bimprove(ment)?\b"]),
    ("question", [r"\bhow do i\b", r"\bhow to\b", r"\bquestion\b", r"\bis it possible\b", r"\?\s*$"]),
    ("documentation", [r"\bdocs?\b", r"\bdocumentation\b", r"\breadme\b", r"\btypo\b", r"\bunclear\b", r"\bexample(s)? missing\b"]),
    ("security", [r"\bvulnerabilit(y|ies)\b", r"\bsecurity\b", r"\bcve-\d+\b", r"\bexploit\b", r"\binjection\b"]),
]
PRIORITY_RULES: list[tuple[str, list[str]]] = [("priority: high", [r"\burgent\b", r"\bcritical\b", r"\bblocker\b", r"\bproduction down\b", r"\bdata loss\b"])]

@dataclass
class ClassificationResult:
    labels: list[str] = field(default_factory=list)
    matched_rules: dict[str, list[str]] = field(default_factory=dict)
    def as_dict(self) -> dict:
        return {"labels": self.labels, "matched_rules": self.matched_rules}

def classify(title: str, body: str) -> ClassificationResult:
    text = f"{title or ''}\n{body or ''}".lower()
    result = ClassificationResult()
    for label, patterns in RULES + PRIORITY_RULES:
        hits = [p for p in patterns if re.search(p, text, flags=re.IGNORECASE)]
        if hits:
            result.labels.append(label)
            result.matched_rules[label] = hits
    if not result.labels:
        result.labels.append("needs-triage")
    return result
