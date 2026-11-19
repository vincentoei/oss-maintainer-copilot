"""Pytest issue types, templates, and pinned historical evidence."""

import re
from dataclasses import dataclass
from typing import Literal, assert_never

from maintainer_copilot.documentation import DocumentationTopic

type TemplateKind = Literal["bug", "feature"]

# The issue-oriented type labels from pytest's public label list. The
# feature-branch label routes pull requests, so it is not an issue type. A
# selected label needs an unnegated cue in the quote's original issue context;
# otherwise the model must return unknown. This is a conservative check, not a
# correctness score.
TYPE_EVIDENCE_CUES = {
    "type: backward compatibility": r"\b(?:backward compatib\w*|breaking change)\b",
    "type: bug": r"\b(?:bug|broken|crash\w*|fail\w*|error|incorrect|wrong)\b",
    "type: deprecation": r"\bdeprecat\w*\b",
    "type: docs": r"\b(?:docs|documentation|guide|manual|typo)\b",
    "type: enhancement": r"\b(?:feature|enhancement|add|support|allow)\b",
    "type: infrastructure": r"\b(?:infrastructure|build|release|ci|workflow)\b",
    "type: performance": r"\b(?:performance|slow|latency|memory|speed)\b",
    "type: proposal": r"\b(?:proposal|propose|design)\b",
    "type: question": r"\b(?:question|how|why)\b|\?",
    "type: refactoring": r"\b(?:refactor\w*|cleanup)\b",
    "type: regression": r"\b(?:regression|used to work|worked before)\b",
    "type: removal": r"\bremov\w*\b",
    "type: selftests": r"\b(?:selftests|pytest test suite)\b",
}
TYPE_LABELS = tuple(TYPE_EVIDENCE_CUES)
BASELINE_TYPE_PRIORITY = (
    "type: regression",
    "type: docs",
    "type: enhancement",
    "type: bug",
)


def type_quote_supports_label(label: str, quote: str, issue_text: str) -> bool:
    cue = TYPE_EVIDENCE_CUES.get(label)
    if cue is None:
        return False
    quote_spans = [
        (match.start(), match.end())
        for match in re.finditer(re.escape(quote), issue_text)
    ]
    for match in re.finditer(cue, issue_text, re.I):
        if not any(
            start <= match.start() and match.end() <= end for start, end in quote_spans
        ):
            continue
        prefix = issue_text[max(0, match.start() - 32) : match.start()]
        suffix = issue_text[match.end() : match.end() + 32]
        if not re.search(
            r"\b(?:no|not|never|without)(?:\s+\w+){0,3}\s*$",
            prefix,
            re.I,
        ) and not re.match(
            r"\s+(?:is|was|are|were|has|does|can|will)\s+(?:not|no|never)\b",
            suffix,
            re.I,
        ):
            return True
    return False


TEMPLATE_REVISION = "50234b4e670064c42a4c29cb6258115a2079ba4c"

DOCUMENTATION_TOPICS = (
    DocumentationTopic(
        key="capture",
        url=(
            "https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html"
            "#accessing-captured-output-from-a-test-function"
        ),
        section="accessing-captured-output-from-a-test-function",
        passage=(
            "fixtures allow access to stdout/stderr output created during "
            "test execution."
        ),
        claim=(
            "pytest documents that capture fixtures let tests access stdout and stderr "
            "created during execution."
        ),
        relevance=r"\b(?:capsys|capfd|capteesys|capsysbinary|capfdbinary)\b",
    ),
    DocumentationTopic(
        key="fixture_scope",
        url="https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes",
        section="fixture-scopes",
        passage=(
            "Fixtures are created when first requested by a test, and are "
            "destroyed based on their scope"
        ),
        claim=(
            "pytest documents that fixture scope determines when a fixture "
            "is destroyed."
        ),
        relevance=(
            r"\bfixture scopes?\b|\bscope\s*=\s*['\"]"
            r"(?:function|class|module|package|session)['\"]"
        ),
    ),
)


@dataclass(frozen=True)
class HistoricalReplayEvidence:
    documentation_key: str
    documentation_path: str
    documentation_start_line: int
    documentation_lines: tuple[str, ...]
    documentation_section: str
    documentation_claim: str
    documentation_relevance: str
    source_path: str
    source_line: int
    source_line_text: str

    def topic(self, commit: str) -> DocumentationTopic:
        end_line = self.documentation_start_line + len(self.documentation_lines) - 1
        return DocumentationTopic(
            key=self.documentation_key,
            url=(
                "https://github.com/pytest-dev/pytest/blob/"
                f"{commit}/{self.documentation_path}"
                f"#L{self.documentation_start_line}-L{end_line}"
            ),
            section=self.documentation_section,
            passage=" ".join(self.documentation_lines),
            claim=self.documentation_claim,
            relevance=self.documentation_relevance,
        )


HISTORICAL_REPLAY_EVIDENCE = {
    12081: HistoricalReplayEvidence(
        documentation_key="capture",
        documentation_path="doc/en/how-to/capture-stdout-stderr.rst",
        documentation_start_line=109,
        documentation_lines=(
            "The ``capsys``, ``capsysbinary``, ``capfd``, and ``capfdbinary`` fixtures",
            "allow access to stdout/stderr output created during "
            "test execution.  Here is",
        ),
        documentation_section="accessing-captured-output-from-a-test-function",
        documentation_claim=(
            "pytest documents that capture fixtures let tests access stdout and stderr "
            "created during execution."
        ),
        documentation_relevance=r"\b(?:capsys|capfd|capteesys|capsysbinary|capfdbinary)\b",
        source_path="src/_pytest/capture.py",
        source_line=935,
        source_line_text=(
            '        """Read and return the captured output so far, '
            "resetting the internal"
        ),
    )
}


def relevant_documentation_topics(
    title: str,
    body: str,
    topics: tuple[DocumentationTopic, ...] = DOCUMENTATION_TOPICS,
) -> list[DocumentationTopic]:
    issue_text = f"{title}\n{body}"
    return [topic for topic in topics if re.search(topic.relevance, issue_text, re.I)]


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
        heading = re.match(
            r"(?i)^\s*(?:#{1,6}\s+)?(?:pip list|packages installed)\s*(?::\s*(.*))?$",
            line,
        )
        if heading is None:
            continue
        if package_row.match((heading.group(1) or "").strip()):
            return True
        for output_line in lines[index + 1 :]:
            if re.match(r"^\s*#{1,6}\s+", output_line):
                break
            if not output_line.strip():
                continue
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


_FEATURE_SECTION_HEADINGS = (
    "What's the problem this feature will solve?",
    "Describe the solution you'd like",
    "Use case",
    "Real-world use case",
    "Alternative Solutions",
    "Additional context",
)


def _section_answer(body: str, heading: str) -> str:
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    match = re.search(
        rf"(?im)^[ \t]*(?:#{{1,6}}[ \t]+)?{re.escape(heading)}[ \t]*\r?$",
        without_comments,
    )
    if match is None:
        return ""
    remainder = without_comments[match.end() :]
    known_headings = "|".join(re.escape(item) for item in _FEATURE_SECTION_HEADINGS)
    next_heading = re.search(
        rf"(?im)^[ \t]*(?:#{{1,6}}[ \t]+[^\r\n]*|(?:{known_headings})[ \t]*)\r?$",
        remainder,
    )
    answer = remainder[: next_heading.start()] if next_heading else remainder
    return answer.strip()


def _answer_has_content(answer: str) -> bool:
    for line in answer.splitlines():
        text = line.strip().strip("*_. ")
        if text.startswith(("```", "~~~")) or re.fullmatch(
            r"(?:todo|tbd|n/?a|none|not (?:yet )?provided)[.!]?", text, re.I
        ):
            continue
        if re.search(r"\w{3,}", text):
            return True
    return False


def _section_has_answer(body: str, heading: str) -> bool:
    return _answer_has_content(_section_answer(body, heading))


def _has_concrete_scenario(body: str) -> bool:
    for sentence in re.split(r"[.!?\n]+", body):
        if len(sentence.split()) < 12:
            continue
        if not re.search(r"\b(?:when|while|during|after|before)\b", sentence, re.I):
            continue
        if re.search(
            r"\b(?:\d+|ci|pytest|test|fixture|suite|pipeline|project|"
            r"repository|plugin)\b",
            sentence,
            re.I,
        ):
            return True
    return False


def _hypothetical_prefix(body: str, start: int) -> bool:
    return bool(
        re.search(
            r"\b(?:if|unless|could|would|might|may|should|can|will|whether)\s*$",
            body[max(0, start - 48) : start],
            re.I,
        )
    )


def _has_current_alternative(body: str) -> bool:
    """Recognize a current concrete approach, rather than version metadata."""
    for match in re.finditer(
        r"\b(?:i|we)\s+(?:(?:currently|already|always|usually|often|normally)\s+)*"
        r"(?:use|run|invoke)\s+([^\r\n]+)",
        body,
        re.I,
    ):
        if _hypothetical_prefix(body, match.start()):
            continue
        approach = re.split(r"(?<=[.!?])[ \t]+", match.group(1), maxsplit=1)[0].strip()
        if re.match(r"(?:no|not|neither|nothing)\b", approach, re.I):
            continue
        for marker in re.finditer(
            r"--[a-z][\w-]*|\b(?:script|alias|plugin|wrapper)\b", approach, re.I
        ):
            if not re.search(
                r"\b(?:no|not|without|neither)(?:\s+\w+){0,2}\s*$",
                approach[max(0, marker.start() - 32) : marker.start()],
                re.I,
            ):
                return True
    return False


def _has_alternative_detail(body: str) -> bool:
    answer = _section_answer(body, "Alternative Solutions")
    # Explicitly reporting that none exists answers the template's "or none"
    # question. Saying an approach has not been tried does not.
    if re.fullmatch(
        r"(?:none|no alternatives(?: exist| are available)?)[.!]?",
        answer,
        re.I,
    ):
        return True
    for statement in re.split(r"(?<=[.!?])[ \t]+|\r?\n+", body):
        if re.fullmatch(
            r"(?:there (?:are|is) )?no (?:other )?(?:alternatives?|workarounds?)"
            r"(?: (?:exist|are available|available))?[.!]?",
            statement.strip(),
            re.I,
        ):
            return True
    if _has_current_alternative(body):
        return True
    for attempt in re.finditer(
        r"\b(?:(?:i|we)\s+(?:have\s+)?tried\s+(?!(?:no|nothing)\b)\S|"
        r"(?:my|our|current) workaround (?:is|uses?)\s+\S)",
        body,
        re.I,
    ):
        if not _hypothetical_prefix(body, attempt.start()):
            return True
    for statement in re.split(r"(?<=[.!?])[ \t]+|\r?\n+", answer):
        if statement.strip().endswith("?") or re.match(
            r"(?:please\s+)?(?:describe|elaborate)\b", statement.strip(), re.I
        ):
            continue
        if re.search(
            r"\b(?:no|not|never|nothing|without|if|could|would|might|may|plan|"
            r"propos\w*)\b|\b(?:haven't|hasn't|didn't|don't|doesn't)\b",
            statement,
            re.I,
        ):
            continue
        if re.fullmatch(
            r"(?:i|we)\s+(?:currently\s+)?use\s+\S+\s+v?\d[\w.-]*[.!]?",
            statement.strip(),
            re.I,
        ):
            continue
        if _answer_has_content(statement):
            return True
    return False


def missing_feature_details(body: str) -> list[TemplateDetail]:
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    has_problem = _section_has_answer(
        body, "What's the problem this feature will solve?"
    ) or bool(
        re.search(
            r"\b(?:i cannot|i can't|i need|the problem is)\b", without_comments, re.I
        )
    )
    has_solution = _section_has_answer(
        body, "Describe the solution you'd like"
    ) or bool(
        re.search(
            r"\b(?:i would like|please add|the solution is)\b", without_comments, re.I
        )
    )
    has_use_case = bool(
        _section_has_answer(body, "Use case")
        or _section_has_answer(body, "Real-world use case")
        or re.search(
            r"\b(?:for example|e\.g\.)\s*[:,]?\s*\w[^\n]{20,}",
            without_comments,
            re.I,
        )
        or re.search(
            r"\b(?:we (?:maintain|use|run|manage)|our (?:test suite|monorepo|"
            r"repository|project)|in our|(?:in|for) "
            r"(?:a|an|the|my|our|some|several|many) (?:\w+\s+){0,2}"
            r"(?:projects?|repositories|monorepos?|test suites?))\b[^.!?\n]{25,}",
            without_comments,
            re.I,
        )
        or _has_concrete_scenario(without_comments)
    )
    has_alternatives = _has_alternative_detail(without_comments)
    provided = (has_problem, has_solution, has_use_case, has_alternatives)
    return _missing_details(FEATURE_DETAILS, provided)


def citation_url(
    template: TemplateKind, line: int, revision: str = TEMPLATE_REVISION
) -> str:
    if template == "bug":
        filename = "1_bug_report.md"
    elif template == "feature":
        filename = "2_feature_request.md"
    else:
        assert_never(template)
    return (
        "https://github.com/pytest-dev/pytest/blob/"
        f"{revision}/.github/ISSUE_TEMPLATE/{filename}#L{line}"
    )
