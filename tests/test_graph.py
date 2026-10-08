from app.graph import build_graph
from app.tools.mock_crm import MockCRMClient

class NullLogger:
    def info(self, *args, **kwargs): pass
    def error(self, *args, **kwargs): pass

def test_graph_runs():
    graph = build_graph(MockCRMClient(), NullLogger())
    result = graph.invoke({
        "client": {
            "client_id": "C001",
            "transactions": [
                {"transaction_id": "T1", "amount": 100, "category": "food"},
                {"transaction_id": "T2", "amount": 120, "category": "food"},
                {"transaction_id": "T3", "amount": 5000, "category": "travel"}
            ]
        },
        "errors": [],
        "session_id": "test"
    })
    assert "analysis" in result
    assert "decision" in result
    assert result["decision"]["recommendation"] == "REVIEW"
