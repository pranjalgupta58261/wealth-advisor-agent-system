from app.agents.analyzer import AnalyzerAgent

class NullLogger:
    def info(self, *args, **kwargs): pass
    def error(self, *args, **kwargs): pass

def test_detects_large_transaction():
    tx = [
        {"transaction_id": "1", "amount": 100, "category": "food"},
        {"transaction_id": "2", "amount": 120, "category": "food"},
        {"transaction_id": "3", "amount": 130, "category": "food"},
        {"transaction_id": "4", "amount": 5000, "category": "travel"},
    ]
    result = AnalyzerAgent(NullLogger()).analyze_transactions(tx)
    assert any(x["transaction_id"] == "4" for x in result["anomalies"])

def test_empty_transactions():
    result = AnalyzerAgent(NullLogger()).analyze_transactions([])
    assert result["transaction_count"] == 0
    assert result["anomalies"] == []
