from app.state import AdvisorState

class DecisionAgent:
    def __init__(self, logger):
        self.logger = logger

    def run(self, state: AdvisorState) -> AdvisorState:
        self.logger.info("DecisionAgent started")
        analysis = state.get("analysis", {})
        client = state.get("enriched_client", {})
        risk_profile = client.get("crm_context", {}).get("risk_profile", "unknown")

        anomaly_count = len(analysis.get("anomalies", []))
        signal_count = len(analysis.get("risk_signals", []))

        if anomaly_count > 0 or signal_count >= 2:
            recommendation = "REVIEW"
            rationale = "Unusual activity or multiple risk signals require advisor review."
        elif signal_count == 1:
            recommendation = "MONITOR"
            rationale = "A risk signal is present; monitor before taking action."
        else:
            recommendation = "NORMAL"
            rationale = "No material risk signals were detected."

        decision = {
            "recommendation": recommendation,
            "risk_profile": risk_profile,
            "rationale": rationale,
            "suggested_actions": [
                "Review flagged transactions with the client",
                "Confirm whether unusual activity is expected",
                "Reassess allocation if concentration persists",
            ] if recommendation != "NORMAL" else [
                "Continue routine monitoring"
            ],
        }
        self.logger.info("Decision generated: %s", recommendation)
        return {
            **state,
            "decision": decision,
            "human_review_required": recommendation == "REVIEW",
        }
