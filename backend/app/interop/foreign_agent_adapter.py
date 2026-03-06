import time
import uuid
from app.settlement.vector_clock import VectorClockLedger

class ExternalAgentWrapper:
    """
    Phase 109: External Interoperability
    Adapts internal requests for foreign agents and wraps incoming responses.
    """

    def __init__(self, trust_score: float):
        self.trust_score = trust_score

    def wrap_outgoing_request(self, request: dict) -> dict:
        """
        Wraps a domestic request for a foreign agent.
        Adds a unique request ID and timestamp, indicating it goes to an untrusted external agent.
        """
        wrapped = {
            "request_id": f"REQ-EXT-{uuid.uuid4().hex[:8].upper()}",
            "timestamp": time.time(),
            "destination": "UNTRUSTED_EXTERNAL_AGENT",
            "payload": request
        }
        return wrapped

    def wrap_incoming_response(self, response: dict) -> dict:
        """
        Unwraps and validates a foreign agent's response.
        Preserves <untrusted_external> tags, and logs the interaction.
        """
        # Ensure it has the untrusted_external tag
        sanitized = response.copy()
        response_str = str(sanitized)
        if "<untrusted_external>" not in response_str:
            sanitized["_security_tag"] = "<untrusted_external> Data originates from a foreign agent."
            
        print(f"[INTEROP] Logging external response for trace...")
        VectorClockLedger.record_usage_outcome("FOREIGN_AGENT", "INCOMING_RESPONSE", "PROCESSED")
        
        return sanitized

    def should_allow_action(self, action: str, context: dict) -> bool:
        """
        Based on the trust score, decide whether to allow a sensitive action.
        If trust score < 0.5, trigger a Veto. Log the decision.
        """
        if self.trust_score < 0.5:
            print(f"[INTEROP] VETO TRIGGERED: External agent trust score ({self.trust_score}) too low for action '{action}'.")
            VectorClockLedger.record_usage_outcome("FOREIGN_AGENT", action, "VETOED")
            return False
            
        print(f"[INTEROP] Action '{action}' allowed. Trust score: {self.trust_score}")
        VectorClockLedger.record_usage_outcome("FOREIGN_AGENT", action, "ALLOWED")
        return True
