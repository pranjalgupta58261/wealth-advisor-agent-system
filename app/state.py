from typing import Any, TypedDict

class AdvisorState(TypedDict, total=False):
    client: dict[str, Any]
    enriched_client: dict[str, Any]
    analysis: dict[str, Any]
    decision: dict[str, Any]
    errors: list[str]
    session_id: str
    human_review_required: bool
    human_override: str | None
