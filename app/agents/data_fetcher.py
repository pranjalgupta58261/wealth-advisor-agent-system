from app.state import AdvisorState
from app.tools.interfaces import CRMClient

class DataFetcherAgent:
    def __init__(self, crm: CRMClient, logger):
        self.crm = crm
        self.logger = logger

    def run(self, state: AdvisorState) -> AdvisorState:
        self.logger.info("DataFetcherAgent started")
        client = state.get("client", {})
        errors = list(state.get("errors", []))

        if not client.get("client_id"):
            errors.append("Missing required field: client_id")
            return {**state, "errors": errors}

        enriched = dict(client)
        try:
            crm_context = self.crm.get_client_context(client["client_id"])
            enriched["crm_context"] = crm_context
            self.logger.info("CRM enrichment successful for %s", client["client_id"])
        except Exception as exc:
            msg = f"CRM enrichment failed: {exc}"
            errors.append(msg)
            enriched["crm_context"] = {
                "risk_profile": "unknown",
                "relationship_tier": "unknown",
                "advisor_notes": "",
            }
            self.logger.error(msg)

        return {**state, "enriched_client": enriched, "errors": errors}
