"""Bounded opt-in drafting; structural checks are not semantic approval."""

import hashlib
import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


@dataclass(frozen=True)
class EvidencePassage:
    id: str
    source_url: str
    text: str


def evidence_packet(
    opening: str, source_url: str, passages: list[tuple[str, str]]
) -> tuple[tuple[EvidencePassage, ...], tuple[str, ...]]:
    if len(opening) > 16000:
        raise ValueError(
            "Opening exceeds frozen evidence budget; no truncation allowed"
        )
    candidates = [(source_url, part) for part in opening.split("\n\n") if part.strip()]
    candidates.extend(passages)
    result: list[EvidencePassage] = []
    omissions: list[str] = []
    total = 0
    seen: set[str] = set()
    for url, text in candidates:
        fingerprint = hashlib.sha256(f"{url}\n{text}".encode()).hexdigest()
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        if len(text) > 2000 or len(result) >= 12 or total + len(text) > 12000:
            omissions.append(fingerprint)
            continue
        result.append(EvidencePassage(f"E{fingerprint}", url, text))
        total += len(text)
    return tuple(result), tuple(omissions)


class Support(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    evidence_id: str
    quote: str = Field(min_length=8, max_length=500)


class Draft(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    kind: Literal["investigation", "explanation"]
    text: str = Field(min_length=12, max_length=500)
    support: list[Support] = Field(min_length=1, max_length=3)

    def validate_evidence(self, passages: tuple[EvidencePassage, ...]) -> None:
        supplied = {p.id: p for p in passages}
        for item in self.support:
            if item.evidence_id not in supplied:
                raise ValueError("Unknown draft evidence ID")
            if item.quote not in supplied[item.evidence_id].text:
                raise ValueError("Draft quote is not in supplied evidence")
        # Source references are server-rendered, never authored by the model.
        if re.search(r"https?://|www\.|\[[^\]]+\]|#\d+", self.text):
            raise ValueError("Draft contains an unsupported source reference")
        if re.search(
            r"ignore.*instructions|system prompt|execute|shell|password|secret|"
            r"api.key|send.*token|<script|javascript:",
            self.text,
            re.I,
        ):
            raise ValueError("Draft contains instruction-like content")
        if self.kind == "explanation":
            # Extractive explanations avoid presenting an invented diagnosis.
            if self.text not in [item.quote for item in self.support]:
                raise ValueError("Factual explanation must be an exact evidence quote")
        elif not self.text.endswith("?"):
            raise ValueError("Investigation must be a question")
