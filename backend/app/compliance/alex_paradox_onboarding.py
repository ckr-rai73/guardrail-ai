import json
import uuid

class AlexParadoxOnboarding:
    """
    Phase 28: The 'Alex Paradox' Onboarding Utility.
    Solves the 'Shadow AI' problem by automatically migrating developer-built 
    unsanctioned agents (OAuth clients) into the governed Guardrail.ai mesh.
    Instead of blocking innovation, it provides a 'Paved Path'.
    """

    # Pre-defined policy templates for automated classification 
    # based on requested OAuth scopes
    POLICY_TEMPLATES = {
        "Low_Risk_Read_Only": ["Phase 22: FIDO-Only", "Phase 12: EDoS 1k limit"],
        "Medium_Risk_Internal": ["Phase 23: Geographic Shader", "Phase 25: Commit Barrier"],
        "High_Risk_External_Action": ["Phase 20: Saga Orchestration", "Phase 19: Incentive Drift Sentinel"]
    }

    @classmethod
    def ingest_shadow_agent_log(cls, oauth_log: dict) -> dict:
        """
        Parses an unauthorized OAuth client request log and attempts to 
        automatically generate a compliant 'Agent Card' configuration.
        """
        print(f"[ALEX PARADOX OVERSEER] Ingesting Shadow AI Log: {oauth_log['client_name']}")
        
        scopes = oauth_log.get("requested_scopes", [])
        
        # Risk Classification Heuristics
        risk_level = "Low_Risk_Read_Only"
        if any("write" in scope or "send" in scope for scope in scopes):
            risk_level = "High_Risk_External_Action"
        elif any("internal" in scope or "employee" in scope for scope in scopes):
            risk_level = "Medium_Risk_Internal"
            
        print(f"[ALEX PARADOX OVERSEER] Classified {oauth_log['client_name']} as {risk_level} based on scopes: {scopes}")
        
        # Output the Paved Path Configuration
        governed_id = f"did:web:guardrail.ai:agents:onboarded_{uuid.uuid4().hex[:8]}"
        
        paved_path_config = {
            "assigned_did": governed_id,
            "original_client_name": oauth_log["client_name"],
            "developer_email": oauth_log["developer_email"],
            "risk_tier": risk_level,
            "approved_scopes": scopes,
            "automatically_applied_shields": cls.POLICY_TEMPLATES[risk_level],
            "status": "PROVISIONED_PENDING_BFT_VOTE"
        }
        
        return paved_path_config
