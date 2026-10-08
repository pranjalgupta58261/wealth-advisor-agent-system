from typing import Any

class MockCRMClient:
    """Deterministic CRM implementation used for the assessment."""

    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    def get_client_context(self, client_id: str) -> dict[str, Any]:
        if self.should_fail:
            raise ConnectionError("Mock CRM unavailable")
        profiles = {
            "C001": {
                "client_id": "C001",
                "risk_profile": "moderate",
                "relationship_tier": "premium",
                "advisor_notes": "Client prefers diversified long-term investments.",
            },
            "C002": {
                "client_id": "C002",
                "risk_profile": "conservative",
                "relationship_tier": "standard",
                "advisor_notes": "Preserve liquidity and avoid concentrated risk.",
            },
        }
        return profiles.get(
            client_id,
            {
                "client_id": client_id,
                "risk_profile": "unknown",
                "relationship_tier": "standard",
                "advisor_notes": "",
            },
        )
