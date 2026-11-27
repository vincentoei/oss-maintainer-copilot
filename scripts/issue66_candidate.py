"""Unadopted prompt-only candidate for issue #66; no execution entry point."""

from maintainer_copilot.model import OpenAICompatibleModel

SUPPORT_INSTRUCTION = (
    " Before selecting a type, check two separate questions: does the whole "
    "issue support it, and does the selected quote express the evidence for it? "
    "For a regression, require a credible comparison showing the same behavior "
    "working before a version change and failing after it; the selected quote "
    "must retain that comparison. Older documentation, an old feature's existence, "
    "or a malfunction alone does not demonstrate a version break. A malfunction "
    "without that comparison may support an ordinary bug. A requested extension "
    "may support enhancement, but its quote must express the requested change, "
    "not just an incidental failure. When a malfunction and requested extension "
    "overlap, prefer the supported reported problem; do not invent intent. "
    "These distinctions apply only where the supplied repository labels have "
    "those meanings; all supplied labels remain eligible without literal cues. "
    "If no offered quote supports a supported category, return null for both "
    "type fields even if the full issue contains stronger evidence. Do not "
    "treat exact copying or valid JSON as proof of semantic support."
)


class SemanticSupportCandidate(OpenAICompatibleModel):
    def generate_json(
        self,
        system_prompt: str,
        user_data: object,
        *,
        max_tokens: int,
        response_schema: dict[str, object] | None = None,
    ) -> object:
        return super().generate_json(
            system_prompt + SUPPORT_INSTRUCTION,
            user_data,
            max_tokens=max_tokens,
            response_schema=response_schema,
        )
