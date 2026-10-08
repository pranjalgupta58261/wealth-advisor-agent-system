import json
from pathlib import Path
from typing import Any

class MemoryStore:
    def __init__(self, path: str = "data/memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(exist_ok=True)

    def save_summary(self, client_id: str, summary: dict[str, Any]) -> None:
        data = {}
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
            except json.JSONDecodeError:
                data = {}
        data[client_id] = summary
        self.path.write_text(json.dumps(data, indent=2))

    def get_summary(self, client_id: str) -> dict[str, Any] | None:
        if not self.path.exists():
            return None
        try:
            return json.loads(self.path.read_text()).get(client_id)
        except json.JSONDecodeError:
            return None
