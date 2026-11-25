"""Shared mechanical quote/negation checks, independent of repository policy."""

import re


def quote_supports_label(
    cues: dict[str, str], label: str, quote: str, issue_text: str
) -> bool:
    cue = cues.get(label)
    if cue is None:
        return False
    spans = [(m.start(), m.end()) for m in re.finditer(re.escape(quote), issue_text)]
    # A reference URL, copied template comment or example output does not
    # establish what kind of issue the reporter is raising. Keep offsets so
    # quotes still refer to the exact, unmodified opening.
    prose = re.sub(
        r"<!--.*?-->|```.*?```|https?://[^\s<>]+",
        lambda match: " " * len(match.group()),
        issue_text,
        flags=re.DOTALL,
    )
    for match in re.finditer(cue, issue_text, re.I):
        if not any(
            start <= match.start() and match.end() <= end for start, end in spans
        ):
            continue
        if not re.search(cue, prose[match.start() : match.end()], re.I):
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
