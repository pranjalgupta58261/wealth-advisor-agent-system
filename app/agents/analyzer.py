from statistics import mean, pstdev
from app.state import AdvisorState

class AnalyzerAgent:
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def analyze_transactions(transactions: list[dict]) -> dict:
        if not transactions:
            return {
                "transaction_count": 0,
                "total_spend": 0.0,
                "average_transaction": 0.0,
                "anomalies": [],
                "risk_signals": ["No transaction history available"],
            }

        amounts = [float(t.get("amount", 0)) for t in transactions]
        avg = mean(amounts)
        std = pstdev(amounts) if len(amounts) > 1 else 0.0
        threshold = avg + max(3 * std, avg * 2)

        anomalies = []
        for tx in transactions:
            amount = float(tx.get("amount", 0))
            if amount >= threshold:
                anomalies.append({
                    "transaction_id": tx.get("transaction_id"),
                    "reason": "Amount is materially above historical transaction baseline",
                    "amount": amount,
                    "threshold": round(threshold, 2),
                })

        risk_signals = []
        categories = [t.get("category") for t in transactions]
        if categories:
            largest_category = max(set(categories), key=categories.count)
            share = sum(
                float(t.get("amount", 0)) for t in transactions
                if t.get("category") == largest_category
            ) / max(sum(amounts), 1)
            if share >= 0.60:
                risk_signals.append(
                    f"Spending concentration: {largest_category} represents {share:.0%} of observed spend"
                )

        if anomalies:
            risk_signals.append("Unusual transaction activity detected")

        return {
            "transaction_count": len(transactions),
            "total_spend": round(sum(amounts), 2),
            "average_transaction": round(avg, 2),
            "anomalies": anomalies,
            "risk_signals": risk_signals,
        }

    def run(self, state: AdvisorState) -> AdvisorState:
        self.logger.info("AnalyzerAgent started")
        client = state.get("enriched_client", state.get("client", {}))
        analysis = self.analyze_transactions(client.get("transactions", []))
        self.logger.info(
            "Analysis complete: %d anomalies, %d risk signals",
            len(analysis["anomalies"]),
            len(analysis["risk_signals"]),
        )
        return {**state, "analysis": analysis}
