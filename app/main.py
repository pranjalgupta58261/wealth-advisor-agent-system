import argparse
import json
import uuid
from pathlib import Path

from app.agents.analyzer import AnalyzerAgent
from app.graph import build_graph
from app.logging_config import configure_logging
from app.memory.store import MemoryStore
from app.tools.mock_crm import MockCRMClient

def main():
    parser = argparse.ArgumentParser(description="Wealth Advisor Assistant")
    parser.add_argument("--input", required=True)
    parser.add_argument("--human-review", action="store_true")
    args = parser.parse_args()

    logger = configure_logging()
    payload = json.loads(Path(args.input).read_text())
    state = {
        "client": payload,
        "errors": [],
        "session_id": str(uuid.uuid4()),
    }

    graph = build_graph(MockCRMClient(), logger, human_review=args.human_review)
    result = graph.invoke(state)

    if args.human_review and result.get("human_review_required"):
        print("\nHuman review required.")
        print(json.dumps(result["decision"], indent=2))
        choice = input("Approve (a), reject (r), or override (o)? ").strip().lower()
        if choice == "o":
            override = input("Enter override recommendation: ").strip()
            result["decision"]["recommendation"] = override
        elif choice == "r":
            result["decision"]["recommendation"] = "REJECTED_BY_REVIEWER"

    client_id = payload.get("client_id", "unknown")
    MemoryStore().save_summary(
        client_id,
        {
            "last_recommendation": result.get("decision", {}).get("recommendation"),
            "risk_signals": result.get("analysis", {}).get("risk_signals", []),
            "anomaly_count": len(result.get("analysis", {}).get("anomalies", [])),
        },
    )

    output = {
        "status": "completed" if not result.get("errors") else "completed_with_warnings",
        "session_id": result["session_id"],
        "analysis": result.get("analysis", {}),
        "decision": result.get("decision", {}),
        "errors": result.get("errors", []),
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
