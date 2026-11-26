"""Triage-quality regressions at the agreed historical replay interface."""

import io
import json
from urllib.request import Request

import pytest
from test_replay import synthetic_case

from maintainer_copilot.evaluation import KeywordRuleModel
from maintainer_copilot.issue_search import IssueRecord
from maintainer_copilot.model import ModelClient, OpenAICompatibleModel
from maintainer_copilot.replay import HistoricalCase, content_hash, replay_case
from maintainer_copilot.trace import get_trace
from maintainer_copilot.triage import TriageReport


def replay_opening(
    title: str, body: str, *, model_client: ModelClient | None = None
) -> TriageReport:
    case, github, repository = synthetic_case()
    opening = IssueRecord(case.issue_number, title, body, case.opening_cutoff)
    github.issues[case.issue_number] = opening
    case = HistoricalCase.model_validate(
        {
            **case.model_dump(),
            "opening_title": title,
            "opening_content_sha256": content_hash(opening),
        }
    )
    return replay_case(
        case,
        commit_source=repository,
        issue_source=github,
        source_reader=repository,
        model_client=model_client or KeywordRuleModel(),
    )


def test_editable_install_package_table_is_not_requested_again() -> None:
    report = replay_opening(
        "Bug: collection fails",
        "Package       Version Editable project location\n"
        "------------- ------- -------------------------\n"
        "local-plugin  1.0.0   /work/plugin\n",
    )

    assert "pip list output" not in {d.name for d in report.missing_details}


def test_markdown_environment_versions_are_not_requested_again() -> None:
    report = replay_opening(
        "Bug: collection fails",
        "**pytest version:** 8.2.0\n**OS:** Ubuntu 24.04\n",
    )

    assert "pytest and OS versions" not in {d.name for d in report.missing_details}


@pytest.mark.parametrize("release", ["openSUSE Tumbleweed", "Debian bookworm"])
def test_named_os_release_is_not_requested_again(release: str) -> None:
    report = replay_opening(
        "Bug: collection fails", f"pytest version: 8.2.0\nOS: {release}\n"
    )

    assert "pytest and OS versions" not in {d.name for d in report.missing_details}


def test_reproducer_with_numbered_test_function_is_not_requested_again() -> None:
    report = replay_opening(
        "Bug: collection order changes",
        "```python\ndef test1():\n    assert True\n```\n",
    )

    assert "minimal example" not in {d.name for d in report.missing_details}


def test_exception_class_in_title_selects_missing_bug_details() -> None:
    report = replay_opening(
        "AttributeError during collection after upgrading pytest",
        "Previously working tests stop at collection before a test can run.",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


def test_observed_ineffective_configuration_selects_report_details() -> None:
    report = replay_opening(
        "Logging configuration option",
        "Using quiet_logs in pytest.ini does not seem to have any effect. "
        "This is with pytest 8.2.0.",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


@pytest.mark.parametrize(
    "body",
    [
        "The latest pytest fails in collection instead of running the tests.",
        "Warnings raised at import time cannot be controlled by filterwarnings.",
        "Two parsers fail to parse this report, truncating or crashing respectively.",
        "Since the upgrade, pytest spawns child processes "
        "which are blocking each other.",
        "ERROR collecting test_demo.py\nTraceback (most recent call last):\n"
        "AttributeError: object has no attribute 'runTest'",
    ],
)
def test_observed_body_failure_selects_report_details(body: str) -> None:
    report = replay_opening("Collection behavior", body)

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


def test_working_counterexample_does_not_supply_the_failing_reproducer() -> None:
    report = replay_opening(
        "Module hook behavior",
        "The module hook is never called in the project. "
        "The hook works in a minimized example.\n"
        "```python\ndef test_hook():\n    assert True\n```",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


@pytest.mark.parametrize(
    "identity",
    [
        "pytest version tested (7.4.0, 8.2.0)",
        "## pytest and operating system versions\n" + "a" * 40,
    ],
)
def test_supplied_pytest_identity_is_not_repeated_in_environment_question(
    identity: str,
) -> None:
    report = replay_opening("Bug: collection fails", identity)
    detail = next(
        d for d in report.missing_details if d.name == "pytest and OS versions"
    )

    assert detail.request == "your operating system and release"


def test_pytest_version_in_title_is_not_requested_again() -> None:
    report = replay_opening(
        "Pytest 8.2.0 collection fails", "The collector stops before executing tests."
    )
    detail = next(
        d for d in report.missing_details if d.name == "pytest and OS versions"
    )

    assert detail.request == "your operating system and release"


@pytest.mark.parametrize(
    ("body", "incidental_type"),
    [
        (
            "Please add a configuration setting. See https://docs.example.test/reference.",
            "type: docs",
        ),
        (
            "Please allow copying captured output.\n```\nFAILED test_demo.py\n```",
            "type: bug",
        ),
    ],
)
def test_type_evidence_ignores_reference_urls_and_example_output(
    monkeypatch: pytest.MonkeyPatch, body: str, incidental_type: str
) -> None:
    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert isinstance(request.data, bytes)
        data = json.loads(json.loads(request.data)["messages"][1]["content"])
        assert incidental_type in data["repository_type_labels"]
        output = {
            "issue_type": "type: enhancement",
            "quote_index": 1,
            "reply_citation_ids": data["required_reply_ids"],
        }
        return io.BytesIO(
            json.dumps(
                {"choices": [{"message": {"content": json.dumps(output)}}]}
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    report = replay_opening(
        "Requested capability",
        body,
        model_client=OpenAICompatibleModel("http://model.test/v1", "controlled"),
    )

    assert report.issue_type == "type: enhancement"


@pytest.mark.parametrize("selected_ids", [[], ["C999"]])
def test_required_investigative_question_is_owned_by_the_report(
    monkeypatch: pytest.MonkeyPatch, selected_ids: list[str]
) -> None:
    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        output = {
            "issue_type": None,
            "quote_index": None,
            "reply_citation_ids": selected_ids,
        }
        return io.BytesIO(
            json.dumps(
                {"choices": [{"message": {"content": json.dumps(output)}}]}
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    report = replay_opening(
        "Module hook behavior",
        "setUpModule is never called in our project. "
        "The hook works in a minimized example.",
        model_client=OpenAICompatibleModel("http://model.test/v1", "controlled"),
    )

    assert "minimized failing example" in report.draft_reply
    assert "C999" not in report.draft_reply
    assert report.status == ("partial" if selected_ids else "complete")


def test_traceback_presentation_request_only_needs_alternatives() -> None:
    report = replay_opening(
        "Show nicer grouped-exception tracebacks",
        "Currently a fixture exception produces a compact traceback. "
        "However grouped exceptions show the full traceback.\n"
        "```python\ndef test_group():\n"
        "    raise ExceptionGroup('group', [ValueError('bad')])\n```\n"
        "I think pytest should be able to also handle groups "
        "and show a nicer traceback.",
    )

    assert {d.name for d in report.missing_details} == {"alternative solutions"}


def test_current_expected_behavior_with_a_described_reproducer_link() -> None:
    report = replay_opening(
        "Collection behavior changed",
        "## Current behavior\nCollection returns one node.\n"
        "## Expected behavior\nIt should collect all three nodes.\n"
        "I made a repository https://github.com/example/collection-repro "
        "that contains a Dockerfile to reproduce the issue.\npytest 8.2.0",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
    }


@pytest.mark.parametrize(
    "body",
    [
        "If pytest fails in collection, would additional logging be useful?",
        "Suppose two parsers fail to parse this report. Which API should handle it?",
        "If the module hook is not called, could a fixture replace it?",
        "pytest might fail during collection. Which diagnostics would help?",
        "I observed success elsewhere. pytest might fail during collection.",
        "pytest does not fail during collection. I am asking about diagnostics.",
    ],
)
def test_hypothetical_failure_question_does_not_acquire_a_report_checklist(
    body: str,
) -> None:
    report = replay_opening("Questions about diagnostics", body)

    assert report.missing_details == []


@pytest.mark.parametrize(
    "introduction",
    [
        "Here is a minimal failing example:",
        "Here is a minimal reproducer that fails:",
    ],
)
def test_failing_example_supplied_alongside_a_working_control_is_recognized(
    introduction: str,
) -> None:
    report = replay_opening(
        "Bug: module hook stops working",
        "The hook works in a minimized example.\n" + introduction + "\n"
        "```python\ndef test_hook():\n    assert False\n```",
    )

    assert "minimal example" not in {d.name for d in report.missing_details}


def test_indented_working_control_is_not_a_failing_reproducer() -> None:
    report = replay_opening(
        "Bug: module hook is not called",
        "The hook works in a minimized example.\n"
        "    def test_hook():\n        assert True\n",
    )

    assert "minimal example" in {d.name for d in report.missing_details}


def test_observed_mismatch_selects_details_for_a_neutral_title() -> None:
    report = replay_opening(
        "Session-scoped fixture lifecycle",
        "I expected session setup once. However, I didn't observe the expected "
        "behavior: setup ran before each module.",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


def test_model_returns_valid_repository_type_and_verbatim_quote(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        assert isinstance(request.data, bytes)
        payload = json.loads(request.data)
        data = json.loads(payload["messages"][1]["content"])
        schema = payload["response_format"]["json_schema"]["schema"]
        assert "type: bug" in schema["properties"]["issue_type"]["enum"]
        output = {
            "issue_type": "type: bug",
            "quote_index": 0,
            "reply_citation_ids": data["required_reply_ids"],
        }
        return io.BytesIO(
            json.dumps(
                {
                    "choices": [{"message": {"content": json.dumps(output)}}],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 20},
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    report = replay_opening(
        "Bug: collection fails",
        "Background context about fixture discovery. " * 4
        + "Feature: allow custom fixture discovery.",
        model_client=OpenAICompatibleModel("http://model.test/v1", "controlled"),
    )

    assert report.status == "complete"
    assert report.issue_type == "type: bug"
    assert report.issue_type_quote is not None and "Bug" in report.issue_type_quote


@pytest.mark.parametrize("index", [True, -1, "type: invalid"])
def test_invalid_type_abstains_and_retains_provider_usage(
    monkeypatch: pytest.MonkeyPatch, index: object
) -> None:
    def endpoint(request: Request, *, timeout: int) -> io.BytesIO:
        return io.BytesIO(
            json.dumps(
                {
                    "choices": [
                        {
                            "message": {
                                "content": json.dumps(
                                    {
                                        "issue_type": index,
                                        "quote_index": 0,
                                        "reply_citation_ids": [],
                                    }
                                )
                            }
                        }
                    ],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 20},
                }
            ).encode()
        )

    monkeypatch.setattr("maintainer_copilot.model.urlopen", endpoint)
    report = replay_opening(
        "Bug: collection fails",
        "The collector stops before running tests.",
        model_client=OpenAICompatibleModel("http://model.test/v1", "controlled"),
    )
    trace = get_trace(report.trace_id)
    assert trace is not None
    selection = next(e for e in trace.events if e.name == "triage_selection")

    assert report.status == "partial" and report.issue_type is None
    assert (selection.input_tokens, selection.output_tokens) == (100, 20)


def test_explicit_regressed_word_supports_regression_type() -> None:
    report = replay_opening(
        "Import resolution regressed after the latest release",
        "Previously working imports fail when collecting the same tests.",
    )

    assert report.issue_type == "type: regression"


@pytest.mark.parametrize("title", ["The plugin is broken", "No output written"])
def test_clear_failure_title_selects_report_details(title: str) -> None:
    report = replay_opening(
        title, "Running this test suite produces a different result than expected."
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


def test_reported_collection_error_selects_details_without_a_bug_title() -> None:
    report = replay_opening(
        "Dynamically register a fixture",
        "The code results in a collection error instead of executing the fixture.",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
        "minimal example",
    }


def test_pytest_session_version_and_rolling_gentoo_are_recognized() -> None:
    report = replay_opening(
        "Bug: test failures on a new Python version",
        "platform linux -- Python 3.13.0b1, pytest-8.3.0.dev38+g1234567\n"
        "This is on Gentoo Linux amd64.\n",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "minimal example",
    }


def test_pytest_selftest_command_and_failing_node_are_a_reproducer() -> None:
    report = replay_opening(
        "Bug: pytest test suite failures on Python 3.13",
        "$ tox -e py313\n"
        "platform linux -- Python 3.13, pytest-8.3.0.dev38+g1234567\n"
        "FAILED testing/test_collection.py::TestSession::test_collect_one\n",
    )

    assert {d.name for d in report.missing_details} == {
        "pip list output",
        "pytest and OS versions",
    }


def test_python_and_pytest_versions_do_not_supply_a_linux_release() -> None:
    report = replay_opening(
        "Bug: assertion output is truncated",
        "platform linux -- Python 3.12.3, pytest-8.2.0.dev99, pluggy-1.5.0\n",
    )

    assert "pytest and OS versions" in {d.name for d in report.missing_details}


def test_installed_pipenv_graph_is_not_requested_again_as_a_package_list() -> None:
    report = replay_opening(
        "Bug: custom option is unrecognized",
        "$ pipenv graph\npytest==8.2.0\n"
        "└── pluggy [required: >=1.5.0, installed: 1.5.0]\n",
    )

    assert "pip list output" not in {d.name for d in report.missing_details}


def test_rejected_existing_flag_supplies_an_alternative_with_a_tradeoff() -> None:
    report = replay_opening(
        "Feature: separate expected-failure tracebacks",
        "#### Alternative Solutions\n"
        "We could avoid passing `-rx`, but then we'd lose the XFAIL summary.\n",
    )

    assert "alternative solutions" not in {d.name for d in report.missing_details}


def test_reading_documentation_at_night_is_a_concrete_use_case() -> None:
    report = replay_opening(
        "Feature: support a dark documentation theme",
        "#### What's the problem this feature will solve?\n"
        "Reading the documentation in the evening is uncomfortable because "
        "the website theme is very bright.\n",
    )

    assert "real-world use case" not in {d.name for d in report.missing_details}


def test_request_to_warn_about_slow_collection_supports_enhancement() -> None:
    report = replay_opening(
        "Warn if collection scans an empty directory for too long",
        "A warning would help locate wasted collection time.",
    )

    assert report.issue_type == "type: enhancement"


@pytest.mark.parametrize(
    "comparison",
    ["Whereas pytest 7.4.4 produces:", "Compared to pytest-7.4.4 this regressed:"],
)
def test_explicit_before_after_versions_are_not_reported_as_conflicting(
    comparison: str,
) -> None:
    report = replay_opening(
        "Bug: package fixture ordering regressed",
        "pip list:\npytest 8.2.0\n"
        "Output from pytest 8.2.0:\nplatform linux -- pytest-8.2.0\n"
        + comparison
        + "\nplatform linux -- pytest-7.4.4\n",
    )

    assert "conflicting version evidence" not in report.draft_reply


@pytest.mark.parametrize(
    ("body", "expected_request"),
    [
        ("pytest version: 8.2.0\n", "your operating system and release"),
        ("OS: Ubuntu 24.04\n", "your pytest version"),
    ],
)
def test_environment_request_only_asks_for_the_missing_half(
    body: str, expected_request: str
) -> None:
    report = replay_opening("Bug: collection fails", body)
    detail = next(
        d for d in report.missing_details if d.name == "pytest and OS versions"
    )

    assert detail.request == expected_request


def test_version_prose_below_an_empty_table_does_not_supply_packages() -> None:
    report = replay_opening(
        "Bug: collection fails",
        "Package Version\n--- ---\npytest 8.1.1 on Ubuntu 22.04\n",
    )

    assert "pip list output" in {d.name for d in report.missing_details}


def test_question_about_handling_an_exception_does_not_imply_a_bug_report() -> None:
    report = replay_opening(
        "How do I catch an AssertionError in a fixture?",
        "I need advice on catching expected exceptions while setting up a fixture.",
    )

    assert report.missing_details == []
    assert "missing_details" in {a.field for a in report.abstentions}


@pytest.mark.parametrize(
    "title",
    [
        "Why does pytest fail with my plugin?",
        "Why is pytest broken?",
        "Why does pytest report an error during collection?",
    ],
)
def test_question_with_explicit_failure_still_checks_bug_details(title: str) -> None:
    report = replay_opening(title, "Collection stops before running any tests.")

    assert "pip list output" in {d.name for d in report.missing_details}


@pytest.mark.parametrize(
    "scenario",
    [
        "Could someone read documentation at night?",
        "I never read documentation at night.",
    ],
)
def test_nonasserted_reading_scenario_remains_a_missing_use_case(scenario: str) -> None:
    report = replay_opening(
        "Feature: support a dark documentation theme",
        "#### What's the problem this feature will solve?\n" + scenario,
    )

    assert "real-world use case" in {d.name for d in report.missing_details}
