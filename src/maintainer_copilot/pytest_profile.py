"""Pytest issue types, templates, and pinned historical evidence."""

import builtins
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, assert_never

if TYPE_CHECKING:
    from maintainer_copilot.repository import DetailRequest

from maintainer_copilot.documentation import DocumentationTopic
from maintainer_copilot.label_evidence import quote_supports_label

REPOSITORY = "pytest-dev/pytest"
GITHUB_ID = 37489525
SEARCH_STOPWORDS = frozenset({"pytest"})
DISPLAY_NAME = "pytest"


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
    "type: enhancement": r"\b(?:feature|enhancement|add|support|allow|warn if)\b",
    "type: infrastructure": r"\b(?:infrastructure|build|release|ci|workflow)\b",
    "type: performance": r"\b(?:performance|slow|latency|memory|speed)\b",
    "type: proposal": r"\b(?:proposal|propose|design)\b",
    "type: question": r"\b(?:question|how|why)\b|\?",
    "type: refactoring": r"\b(?:refactor\w*|cleanup)\b",
    "type: regression": (
        r"\b(?:regress(?:ions?|ed|es|ing)?|used to work|worked before)\b"
    ),
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
    return quote_supports_label(TYPE_EVIDENCE_CUES, label, quote, issue_text)


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


PREPARED_TEMPLATES = (
    ("bug", "1_bug_report.md", BUG_DETAILS),
    ("feature", "2_feature_request.md", FEATURE_DETAILS),
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
    instructional_question = bool(
        re.match(r"^(?:how|what|why|when|where|can|could|should|question)\b", title)
    )
    bug_hint = bool(
        re.search(
            r"\b(bug|error|broken|fail(?:ure)?s?|crashes?|regress(?:ion|ed)|"
            r"hangs?|truncated|no output)\b",
            title,
        )
    ) or (not instructional_question and bool(re.search(r"\b\w+error\b", title)))
    if bug_hint and not feature_hint:
        return "bug"
    if feature_hint and not bug_hint:
        return "feature"
    if "what's the problem this feature will solve?" in body.lower():
        return "feature"
    if "a detailed description of the bug or problem" in body.lower():
        return "bug"
    if re.search(
        r"\b(?:didn't|did not) observe (?:the )?expected (?:behavio[u]?r|result)\b",
        body,
        re.I,
    ):
        return "bug"
    problem = r"\bresults? in (?:a |an )?(?:collection )?(?:error|exception|failure)\b"
    if quote_supports_label({"problem": problem}, "problem", body, body):
        return "bug"
    return None


def missing_bug_details(body: str) -> list[TemplateDetail]:
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
    has_versions = all(_provided_environment(body))
    has_example = _has_minimal_example(body)
    provided = (has_description, has_pip_list, has_versions, has_example)
    return _missing_details(BUG_DETAILS, provided)


def _provided_environment(body: str) -> tuple[bool, bool]:
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    environment_text = re.sub(r"[*`]", "", without_comments)
    body_lower = environment_text.lower()
    os_text = re.sub(
        r"\b(?:python|pytest|pluggy)(?:\s+version)?[ :=-]*v?\d[\w.+-]*",
        "",
        environment_text,
        flags=re.I,
    )
    has_pytest = bool(re.search(r"\bpytest(?:\s+version)?\s*[:= -]\s*v?\d", body_lower))
    has_os = bool(
        re.search(r"(?im)^\s*(?:os|operating system)\s*:\s*[^\n]*\d", os_text)
        or re.search(
            r"\b(?:ubuntu|windows|macos|linux|fedora|debian|freebsd|openbsd|"
            r"netbsd)\b[^\n]*\d",
            os_text,
            re.I,
        )
        or re.search(
            r"\b(?:opensuse\s+tumbleweed|gentoo(?:\s+linux)?|"
            r"debian\s+(?:buster|bullseye|bookworm|trixie))\b",
            body_lower,
        )
    )
    return has_pytest, has_os


def _has_pip_list_output(body: str) -> bool:
    if (
        re.search(r"(?m)^\s*\$?\s*pipenv graph\s*$", body)
        and re.search(r"(?m)^[\w.-]+==\d+(?:\.\d+)+", body)
        and re.search(r"\[required:[^\]\n]+, installed:\s*\d", body)
    ):
        return True
    package_row = re.compile(
        r"^[\w.-]+\s+\d+(?:\.\d+)+(?:\S*)"
        r"(?:\s+(?:/|[A-Za-z]:[\\/])[^\r\n]*)?$"
    )
    lines = body.splitlines()
    # pip's own table header is stronger evidence than the reporter's heading.
    # Require actual rows, so a copied empty table is still missing.
    for index, line in enumerate(lines):
        if re.fullmatch(
            r"\s*Package\s+Version(?:\s+Editable project location)?\s*", line, re.I
        ):
            rows = lines[index + 1 :]
            if rows and re.fullmatch(r"\s*-+\s+-+(?:\s+-+)?\s*", rows[0]):
                rows = rows[1:]
            if rows and package_row.fullmatch(rows[0].strip()):
                return True
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
    if re.search(r"\bdef\s+test\w*\s*\(", body):
        return True
    if (
        re.search(r"\btox\s+-e\s+py\d+\b", body)
        and re.search(r"(?m)^FAILED testing/\S+::\S+", body)
        and re.search(r"\bpytest-\d[^\s,]*\.dev", body)
    ):
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
        if re.match(r"(?:please\s+)?(?:describe|elaborate)\b", text, re.I):
            continue
        if re.search(r"\w{3,}", text):
            return True
    return False


def _section_has_answer(body: str, heading: str) -> bool:
    return _answer_has_content(_section_answer(body, heading))


def _has_concrete_scenario(body: str) -> bool:
    for scenario in re.finditer(
        r"\b(?:reading|read|viewing|view)\b[^\n.!?]{0,80}"
        r"\b(?:docs|documentation)\b[^\n.!?]{0,80}"
        r"\b(?:evening|night|low.light)\b",
        body,
        re.I,
    ):
        prefix = re.split(
            r"[.!?\n]", body[max(0, scenario.start() - 64) : scenario.start()]
        )[-1]
        ending = re.search(r"[.!?\n]|$", body[scenario.end() :])
        assert ending is not None
        if (
            re.search(
                r"\b(?:if|unless|could|would|might|may|should|whether|never|not|don't)\b",
                prefix,
                re.I,
            )
            or ending.group() == "?"
        ):
            continue
        return True
    if re.search(
        r"\b(?:i'm|i am|we are)\s+(?:currently\s+)?writing tests\b[^\n]{20,}",
        body,
        re.I,
    ) or re.search(
        r"\bi want to (?:run|collect)\b[^\n]{10,}\btests\b[^\n]*\bto \w+",
        body,
        re.I,
    ):
        return True
    if re.search(r"\bci (?:systems?|scripts?|pipelines?)\b", body, re.I) and re.search(
        r"\b(?:bash|shell)\b[^\n]{10,}", body, re.I
    ):
        return True
    if (
        re.search(r"\b(?:docs|documentation)\b", body, re.I)
        and re.search(r"\b(?:toml|pyproject\.toml|ini_options)\b", body, re.I)
        and re.search(r"`[^`\n]*(?:=|addopts)[^`\n]*`", body)
    ):
        return True
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
    if re.search(
        r"\b(?:could|can) (?:avoid|omit|drop|remove|disable)\b[^\n]*"
        r"--?[a-z][\w-]*[^\n]*\bbut\b[^\n]*\b(?:lose|losing|no longer)\b",
        answer,
        re.I,
    ):
        return True
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
    if re.search(
        r"\b(?:i'm|i am|we are)\s+(?:currently\s+)?making use of\s+"
        r"(?:the\s+)?`[^`\n]+`[^\n]*\bcopy\b[^\n]*\btests\b",
        body,
        re.I,
    ):
        return True
    for attempt in re.finditer(
        r"\b(?:(?:i|we)\s+(?:have\s+)?tried\s+(?!(?:no|nothing)\b)\S|"
        r"(?:my|our|current) workaround (?:is|uses?)\s+"
        r"(?!(?:(?:a|an|the)\s+)?(?:not|no|never|nothing|unavailable|"
        r"unimplemented|propos\w*|planned)\b)\S)",
        body,
        re.I,
    ):
        if not _hypothetical_prefix(body, attempt.start()):
            return True
    for statement in re.split(r"(?<=[.!?])[ \t]+|\r?\n+", answer):
        if statement.strip().endswith("?"):
            continue
        if re.search(
            r"\b(?:no|not|never|nothing|without|if|could|would|might|may|plan|"
            r"propos\w*|planned|unavailable|unimplemented)\b|"
            r"\b(?:haven't|hasn't|didn't|don't|doesn't)\b",
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
            r"\b(?:for example|e\.g\.)\s*[:,]?\s*\S[^\n]{20,}",
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


def owns_documentation_url(url: str) -> bool:
    from urllib.parse import urlsplit

    parsed = urlsplit(url)
    return (
        parsed.scheme == "https"
        and parsed.netloc == "docs.pytest.org"
        and parsed.path.startswith("/en/")
    )


def profile_details(
    title: str, body: str, revision: str
) -> list["DetailRequest"] | None:
    from maintainer_copilot.repository import DetailRequest

    template = template_for(title, body)
    if template is None:
        return None
    missing = (
        missing_bug_details(body)
        if template == "bug"
        else missing_feature_details(body)
    )
    version_request = None
    if template == "bug":
        has_pytest, has_os = _provided_environment(body)
        if has_pytest and not has_os:
            version_request = "your operating system and release"
        elif has_os and not has_pytest:
            version_request = "your pytest version"
    return [
        DetailRequest(
            name=d.name,
            request=(version_request or d.request)
            if d.name == "pytest and OS versions"
            else d.request,
            url=citation_url(template, d.line, revision),
            description=f"pytest {template} report template: {d.name}",
        )
        for d in missing
    ]


@dataclass(frozen=True)
class _Connection:
    key: str
    description: str
    patterns: tuple[str, ...]


# Bounded connections require behavior-bearing evidence in both reports. Shared
# template headings, stack-frame vocabulary and URLs cannot establish a match.
_CONNECTIONS = (
    _Connection(
        "fixture_values",
        "fixture-derived parameter values",
        (
            r"\bfixtures?\b",
            r"\bparametrize\b",
            r"parameters_fixture|fixture[- ]derived parameter|"
            r"Using fixtures in.*parametrize|"
            r"fixture.{0,20}(?:_value_|supplies parameter|provides parameter)",
        ),
    ),
    _Connection(
        "readouterr",
        "readouterr consuming captured output",
        (
            r"\breadouterr\b",
            r"reset|consum|missing|keep.*output|(?:remain|preserve).*?(?:visible|output)",
        ),
    ),
    _Connection(
        "runtest_import",
        "the call_runtest_hook import failure",
        (
            r"call_runtest_hook",
            r"ImportError|cannot import",
        ),
    ),
    _Connection("pdbcls", "custom debugger selection with --pdbcls", (r"--pdbcls",)),
    _Connection(
        "argument_file",
        "reading test-selection arguments from a file",
        (
            r"\b(?:text file|from (?:a )?file|from-file)\b",
            r"\b(?:arguments?|subsets?|positional)\b",
        ),
    ),
    _Connection(
        "module_hooks",
        "module setup/teardown hooks",
        (r"setUpModule", r"tearDownModule"),
    ),
    _Connection("fixture_cache", "fixture caching", (r"fixture cach",)),
)


def match_connection(first: str, second: str) -> _Connection | None:
    for connection in _CONNECTIONS:
        if all(
            re.search(pattern, text, re.I)
            for text in (first, second)
            for pattern in connection.patterns
        ):
            return connection
    # A named exception is a stronger anchor than generic stack-frame words.
    exceptions = set(re.findall(r"\b[A-Z][a-zA-Z]+(?:Error|Exception)\b", first))
    shared = sorted(
        name for name in exceptions if name in second and name not in vars(builtins)
    )
    return (
        _Connection(
            "named_exception", f"the {shared[0]} failure", (re.escape(shared[0]),)
        )
        if shared
        else None
    )


def match_distinction(
    body: str,
    candidate_body: str,
    title: str,
    candidate_title: str,
    connection_key: str,
) -> tuple[bool, bool, bool, str]:
    from maintainer_copilot.issue_search import (
        _fixture_scopes,
        _negated_terms,
        _opposing_actions,
        _terms,
    )

    shared_body = _terms(body) & _terms(candidate_body)
    review_scopes = _fixture_scopes(body)
    candidate_scopes = _fixture_scopes(candidate_body)
    different_scopes = bool(
        review_scopes
        and candidate_scopes
        and review_scopes.isdisjoint(candidate_scopes)
    )
    different_polarity = bool(
        (_negated_terms(body) ^ _negated_terms(candidate_body)) & shared_body
    )
    opposing_actions = _opposing_actions(
        title + " " + body, candidate_title + " " + candidate_body
    )
    distinction = (
        "The reports describe different fixture scopes."
        if different_scopes
        else "One report negates a shared condition."
        if different_polarity and connection_key == "named_exception"
        else "The reports request opposing actions."
        if opposing_actions
        else "This requests session-derived parameters; the earlier example passes "
        "fixture functions instead of values."
        if connection_key == "fixture_values"
        and "session" in body
        and re.search(r"fixture _?function_?", candidate_body)
        else "This requests a configuration setting; the earlier issue concerns "
        "command-line help."
        if connection_key == "pdbcls"
        and "configuration" in title.lower()
        and "help" in candidate_title.lower()
        else "This opening names copyouterr; compare its proposed behavior with "
        "the earlier readouterr report."
        if connection_key == "readouterr" and "copyouterr" in body
        else "This reports hooks not running; the earlier issue "
        "questions the documentation."
        if connection_key == "module_hooks"
        and "docs" in candidate_title.lower()
        and "not invoked" in title.lower()
        else "the same failure or request is not established."
    )
    return different_scopes, different_polarity, opposing_actions, distinction
