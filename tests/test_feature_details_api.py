"""Issue #45 at the report APIs; controlled selections are not quality evidence."""

import asyncio
from typing import Any, cast

import httpx2
import pytest

from maintainer_copilot.agent import AgentStepRequest
from maintainer_copilot.model import ModelRequest
from maintainer_copilot.web import app, get_agent_client, get_model_client


class SelectRequiredStatements:
    def next_step(self, request: AgentStepRequest) -> object:
        return {"tool": "finish", "arguments": {}}

    def generate(self, request: ModelRequest) -> object:
        return {
            "issue_type": None,
            "issue_type_quote": None,
            "reply_citation_ids": list(request.required_reply_ids),
        }


def report_for(body: str, endpoint: str = "/api/triage") -> dict[str, Any]:
    async def controlled_client() -> SelectRequiredStatements:
        return SelectRequiredStatements()

    async def request() -> httpx2.Response:
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=app), base_url="http://testserver"
        ) as client:
            return await client.post(
                endpoint,
                json={"title": "Feature: configure the debugger", "body": body},
            )

    app.dependency_overrides[get_model_client] = controlled_client
    app.dependency_overrides[get_agent_client] = controlled_client
    try:
        response = asyncio.run(request())
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200, response.text
    return cast(dict[str, Any], response.json())


def test_plain_feature_headings_keep_answers_in_their_own_sections() -> None:
    report = report_for(
        "What's the problem this feature will solve?\n"
        "The debugger command is too long.\n\n"
        "Describe the solution you'd like\n"
        "A configuration setting would shorten it.\n\n"
        "Real-world use case\n\n"
        "Alternative Solutions\n"
        "I tried a shell alias.\n"
    )

    assert [item["name"] for item in report["missing_details"]] == [
        "real-world use case"
    ]


def test_project_usage_in_problem_prose_supplies_a_feature_use_case() -> None:
    report = report_for(
        "#### What's the problem this feature will solve?\n"
        "The debugger command is too long. For some projects, an interactive "
        "debugger with rich inspection helps investigate production errors.\n\n"
        "#### Describe the solution you'd like\n"
        "A configuration setting would shorten it.\n\n"
        "#### Alternative Solutions\n"
        "I tried a shell alias.\n"
    )

    assert report["missing_details"] == []


@pytest.mark.parametrize("prefix", ["", "#### "])
@pytest.mark.parametrize("endpoint", ["/api/triage", "/api/agent/triage"])
def test_current_cli_usage_is_not_requested_again_as_an_alternative(
    prefix: str, endpoint: str
) -> None:
    report = report_for(
        f"{prefix}What's the problem this feature will solve?\n"
        "For some projects, I always use "
        "`pytest --pdb --pdbcls=tools.CustomDebugger` to inspect failing tasks. "
        "The command is long.\n\n"
        f"{prefix}Describe the solution you'd like\n"
        "A settings entry could shorten the command.\n\n"
        "[tool.pytest.ini_options]\npdbcls = 'tools.CustomDebugger'\n",
        endpoint,
    )

    assert report["missing_details"] == []
    assert "Could you add" not in report["draft_reply"]


@pytest.mark.parametrize(
    "answer",
    [
        "",
        "<!-- Have you tried a workaround? -->",
        "I have not tried a workaround.",
        "I could use a wrapper script.",
        "A workaround might be to write an alias.",
        "I currently use pytest 8.1. I could try a wrapper.",
        "I currently use pytest without any plugin.",
        "If I tried a plugin, it might help.",
        "Could I use a plugin as a workaround?",
        "I tried nothing else.",
        "Have you tried a wrapper script?",
        "Describe any alternatives you have tried.",
        "Please elaborate here.",
    ],
)
def test_untried_or_absent_alternatives_still_receive_a_detail_request(
    answer: str,
) -> None:
    report = report_for(
        "What's the problem this feature will solve?\n"
        "The debugger command is lengthy.\n\n"
        "Describe the solution you'd like\n"
        "A stored debugger-class setting would shorten it.\n\n"
        "Real-world use case\n"
        "Investigating failures in a billing project.\n\n"
        f"Alternative Solutions\n{answer}\n"
    )

    assert [item["name"] for item in report["missing_details"]] == [
        "alternative solutions"
    ]


@pytest.mark.parametrize("prefix", ["", "#### "])
def test_template_placeholders_and_comment_instructions_are_not_answers(
    prefix: str,
) -> None:
    report = report_for(
        f"{prefix}What's the problem this feature will solve?\nTODO\n\n"
        f"{prefix}Describe the solution you'd like\n"
        "<!-- Please add the requested solution here. -->\n"
        "```toml\n```\n\n"
        f"{prefix}Real-world use case\nTBD\n\n"
        f"{prefix}Alternative Solutions\n"
        "<!-- I tried a workaround: describe it here. -->\nTBD\n"
    )

    assert [item["name"] for item in report["missing_details"]] == [
        "problem to solve",
        "proposed solution",
        "real-world use case",
        "alternative solutions",
    ]


@pytest.mark.parametrize(
    "answer", ["No alternatives exist.", "There are no alternatives available."]
)
def test_explicit_absence_of_alternatives_in_prose_is_an_answer(answer: str) -> None:
    report = report_for(
        "What's the problem this feature will solve?\n"
        "The debugger command is lengthy.\n\n"
        "Describe the solution you'd like\n"
        "A stored debugger-class setting would shorten it.\n\n"
        "Real-world use case\n"
        f"Investigating failures in a billing project.\n\n{answer}\n"
    )

    assert report["missing_details"] == []
