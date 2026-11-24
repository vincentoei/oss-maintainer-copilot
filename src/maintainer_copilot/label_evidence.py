"""Shared mechanical quote/negation checks, independent of repository policy."""

import re


def quote_supports_label(
    cues: dict[str, str], label: str, quote: str, issue_text: str
) -> bool:
    cue = cues.get(label)
    if cue is None:
        return False
    spans = [(m.start(), m.end()) for m in re.finditer(re.escape(quote), issue_text)]
    for match in re.finditer(cue, issue_text, re.I):
        if not any(
            start <= match.start() and match.end() <= end for start, end in spans
        ):
            continue
        prefix = issue_text[max(0, match.start() - 32) : match.start()]
        suffix = issue_text[match.end() : match.end() + 32]
        if not re.search(
            r"\b(?:no|not|never|without)(?:\s+\w+){0,3}\s*$", prefix, re.I
        ) and not re.match(
            r"\s+(?:is|was|are|were|has|does|can|will)\s+(?:not|no|never)\b",
            suffix,
            re.I,
        ):
            return True
    return False
