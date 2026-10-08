from typing import Protocol, Any

class CRMClient(Protocol):
    def get_client_context(self, client_id: str) -> dict[str, Any]:
        ...
