"""The fixed pytest issue-template evidence used by the first report."""

import re
from dataclasses import dataclass
from typing import Literal, assert_never

type TemplateKind = Literal["bug", "feature"]

TEMPLATE_REVISION = "50234b4e670064c42a4c29cb6258115a2079ba4c"
TEMPLATE_BASE = (
    f"https://github.com/pytest-dev/pytest/blob/{TEMPLATE_REVISION}/"
    ".github/ISSUE_TEMPLATE/"
)


@dataclass(frozen=True)
class TemplateDetail:
    name: str
    request: str
    line: int


BUG_DETAILS = (
    TemplateDetail(
        "bug description",
        "a detailed description of the bug or problem",
        13,
    ),
    TemplateDetail(
        "pip list output",
        "the output of `pip list` from the virtual environment you are using",
        14,
    ),
    TemplateDetail(
        "pytest and OS versions",
        "your pytest and operating system versions",
        15,
    ),
    TemplateDetail(
        "minimal example",
        "a minimal example, if possible",
        16,
    ),
)

FEATURE_DETAILS = (
    TemplateDetail(
        "problem to solve",
        "the problem this feature would solve",
        13,
    ),
    TemplateDetail(
        "proposed solution",
        "the solution you would like",
        16,
    ),
    TemplateDetail(
        "real-world use case",
        "a real-world use case this would enable",
        19,
    ),
    TemplateDetail(
        "alternative solutions",
        "any workaround or alternative you have tried, or that there is none",
        21,
    ),
)


def _missing_details(
    details: tuple[TemplateDetail, ...], provided: tuple[bool, ...]
) -> list[TemplateDetail]:
    return [
        detail for detail, present in zip(details, provided, strict=True) if not present
    ]


def template_for(title: str, body: str) -> TemplateKind | None:
    title = title.lower().strip()
    if re.match(r"^(?:\[\s*)?bug\b", title):
        return "bug"
    if re.match(r"^(?:\[\s*)?(?:feature|enhancement)\b", title):
        return "feature"
    feature_hint = bool(
        re.search(r"\b(feature request|feature|enhancement|add support)\b", title)
    )
    bug_hint = bool(
        re.search(r"\b(bug|error|fails?|crashes?|regression|hangs?)\b", title)
    )
    if bug_hint and not feature_hint:
        return "bug"
    if feature_hint and not bug_hint:
        return "feature"
    if "what's the problem this feature will solve?" in body.lower():
        return "feature"
    if "a detailed description of the bug or problem" in body.lower():
        return "bug"
    return None


def missing_bug_details(body: str) -> list[TemplateDetail]:
    body_lower = body.lower()
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    without_code = re.sub(r"```.*?```", "", without_comments, flags=re.DOTALL)
    description_lines = [
        line.strip()
        for line in without_code.splitlines()
        if line.strip()
        and not re.match(
            r"(?i)^\s*(?:pytest(?: version)?|os|operating system|pip list|"
            r"minimal example|package\s+version)\s*:",
            line,
        )
        and not re.match(r"^\s*[\w.-]+\s+\d+(?:\.\d+)*\s*$", line)
        and not re.match(r"^\s*(?:#|-\s*\[[ x]\])", line)
    ]
    has_description = len(" ".join(description_lines)) >= 30
    has_pip_list = _has_pip_list_output(body)
    has_versions = bool(
        re.search(r"\bpytest(?:\s+version)?\s*[:= ]\s*v?\d", body_lower)
        and (
            re.search(r"(?im)^\s*(?:os|operating system)\s*:\s*[^\n]*\d", body)
            or re.search(
                r"\b(?:ubuntu|windows|macos|linux|fedora|debian|freebsd|openbsd|"
                r"netbsd)\b[^\n]*\d",
                body_lower,
            )
        )
    )
    has_example = _has_minimal_example(body)
    provided = (has_description, has_pip_list, has_versions, has_example)
    return _missing_details(BUG_DETAILS, provided)


def _has_pip_list_output(body: str) -> bool:
    package_row = re.compile(r"^[\w.-]+\s+\d+(?:\.\d+)+(?:\S*)$")
    lines = body.splitlines()
    for index, line in enumerate(lines):
        heading = re.match(r"(?i)^\s*(?:pip list|packages installed)\s*:\s*(.*)$", line)
        if heading is None:
            continue
        if package_row.match(heading.group(1).strip()):
            return True
        for output_line in lines[index + 1 :]:
            if not output_line.strip() or re.match(r"^\s*#{1,6}\s+", output_line):
                break
            if package_row.match(output_line.strip()):
                return True
    return False


def _has_minimal_example(body: str) -> bool:
    if re.search(r"\bdef\s+test_\w+\s*\(", body):
        return True
    heading = re.search(r"(?im)^\s*minimal example:[ \t]*(.*)$", body)
    if heading is None:
        return False
    if heading.group(1).strip() and not heading.group(1).lstrip().startswith("```"):
        return True
    following = body[heading.end() :]
    code_block = re.match(r"\s*```[^\n]*\n(.*?)```", following, flags=re.DOTALL)
    if code_block is not None:
        return bool(re.search(r"\w", code_block.group(1)))
    for line in following.splitlines():
        if line.strip():
            return not line.lstrip().startswith(("#", "<!--"))
    return False


def _section_has_answer(body: str, heading: str) -> bool:
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    match = re.search(
        rf"(?im)^\s*#{{1,6}}\s*{re.escape(heading)}\s*$", without_comments
    )
    if match is None:
        return False
    remainder = without_comments[match.end() :]
    next_heading = re.search(r"(?m)^\s*#{1,6}\s+", remainder)
    answer = remainder[: next_heading.start()] if next_heading else remainder
    return bool(re.search(r"\w{3,}", answer))


def missing_feature_details(body: str) -> list[TemplateDetail]:
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    has_problem = _section_has_answer(
        body, "What's the problem this feature will solve?"
    ) or bool(re.search(r"\b(?:i cannot|i can't|i need|the problem is)\b", body, re.I))
    has_solution = _section_has_answer(
        body, "Describe the solution you'd like"
    ) or bool(re.search(r"\b(?:i would like|please add|the solution is)\b", body, re.I))
    has_use_case = bool(
        re.search(r"\b(?:for example|use case|e\.g\.)\b", without_comments, re.I)
        or re.search(
            r"\b(?:we (?:maintain|use|run|manage)|our (?:test suite|monorepo|"
            r"repository|project)|in our|in (?:a|an|the) (?:\w+\s+){0,2}"
            r"(?:project|repository|monorepo|test suite))\b[^.!?\n]{25,}",
            without_comments,
            re.I,
        )
    )
    has_alternatives = _section_has_answer(body, "Alternative Solutions") or bool(
        re.search(r"\b(?:i tried|workaround|no alternatives)\b", without_comments, re.I)
    )
    provided = (has_problem, has_solution, has_use_case, has_alternatives)
    return _missing_details(FEATURE_DETAILS, provided)


def citation_url(template: TemplateKind, line: int) -> str:
    if template == "bug":
        filename = "1_bug_report.md"
    elif template == "feature":
        filename = "2_feature_request.md"
    else:
        assert_never(template)
    return f"{TEMPLATE_BASE}{filename}#L{line}"
