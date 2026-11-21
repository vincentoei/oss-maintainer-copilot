"""Bounded investigative questions supported by the submitted opening only."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FollowUp:
    text: str
    passage: str


def supported_follow_up(body: str) -> FollowUp | None:
    """Offer one question, never a diagnosis or a claim about pytest behavior.

    All matches use the complete opening, not later comments or external links.
    The report builder requires an issue number to cite this submitted evidence.
    """
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    versions: dict[str, list[str]] = {}
    version_lines: list[str] = []
    for package in ("pytest", "pluggy"):
        matches = list(
            re.finditer(
                rf"\b{package}(?:\s+version)?[\s:=\-]+v?(\d+(?:\.\d+)+)",
                body,
                re.I,
            )
        )
        versions[package] = list(dict.fromkeys(m.group(1) for m in matches))
        for match in matches:
            if len(versions[package]) > 1:
                version_lines.append(match.group(0))
    if (
        len(versions["pytest"]) > 1
        and re.search(r"\bscope\b", body, re.I)
        and re.search(r"\bvariables?\b", body, re.I)
        and re.search(r"hardcoded|directly specify", body, re.I)
        and re.search(r"parametrize", body, re.I)
    ):
        return FollowUp(
            "The supplied scenarios use different pytest versions "
            f"({' / '.join(versions['pytest'])}). Could you compare both scenarios "
            "using the same pytest version and identical tuple values, including "
            "their order, changing only how the values are constructed? "
            "Please include fixture setup/teardown output from both runs.",
            "\n".join(dict.fromkeys(version_lines)),
        )
    conflicting = {}
    for package, values in versions.items():
        listed_versions = re.findall(rf"(?im)^\s*{package}\s+(\d+(?:\.\d+)+)\s*$", body)
        session_versions = re.findall(rf"\b{package}-(\d+(?:\.\d+)+)", body)
        if (
            listed_versions
            and session_versions
            and set(listed_versions) != set(session_versions)
        ):
            conflicting[package] = values
    if conflicting:
        listed = "; ".join(
            f"{package}: {' / '.join(values)}"
            for package, values in conflicting.items()
        )
        return FollowUp(
            f"The opening contains conflicting version evidence ({listed}). "
            "Could you confirm which pytest/pluggy versions produced the output "
            "using that run's environment?",
            "\n".join(dict.fromkeys(version_lines)),
        )
    working = re.search(
        r"[^.\r\n!?]*\b(?:hook|example)\b[^.!?\r\n]*"
        r"\b(?:honored|works?|succeeds?)\s+(?:in|for|with)\s+"
        r"(?:the|a|this)\s+minimi[sz]ed example[^.!?\r\n]*(?:[.!?]|$)",
        body,
        re.I,
    )
    if (
        working
        and not re.search(
            r"\b(?:not|never|no|without|fails?|doesn't|cannot|can't|"
            r"might|may|could|would|should|if|whether)\b|\?",
            working.group(0),
            re.I,
        )
        and re.search(r"setUpModule|tearDownModule", body)
    ):
        return FollowUp(
            "You report that the hook works in the minimized example. Could you "
            "reduce the affected project's case to a minimized failing example, "
            "including its module layout, configuration and exact command? "
            "Compare that with the working example to isolate what prevents "
            "the hook from running.",
            working.group(0),
        )
    return None
