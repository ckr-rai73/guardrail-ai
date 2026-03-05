import time
import uuid

# Mock active agents database
ACTIVE_AGENTS = {
    "agent-alpha-1": {"owner_id": "EMP-001", "status": "ACTIVE", "token": "tok_123"},
    "agent-beta-2": {"owner_id": "EMP-001", "status": "ACTIVE", "token": "tok_456"},
    "agent-gamma-3": {"owner_id": "EMP-002", "status": "ACTIVE", "token": "tok_789"}
}

# Mock Human Resource Information System (HRIS) status map
HUMAN_SPONSORS = {
    "EMP-001": {"status": "ACTIVE"},
    "EMP-002": {"status": "ACTIVE"}
}

class NHILifecycleCustodian:
    """
    Phase 22: Workforce Lifecycle (Non-Human Identity).
    Manages the lifecycle of AI agents tied to human sponsors. If the human Sponsor
    is deactivated (e.g., leaves the company), the system autonomously revokes all
    associated agent DIDs and rotates their credentials.
    """
    
    @classmethod
    def deactivate_human_sponsor(cls, sponsor_id: str) -> dict:
        """
        Triggered via HRIS webhook. Deactivates a human and cascadingly
        revokes all linked Non-Human Identities (Agents).
        """
        if sponsor_id not in HUMAN_SPONSORS:
            return {"status": "error", "message": "Sponsor ID not found"}
            
        # 1. Deactivate the human
        HUMAN_SPONSORS[sponsor_id]["status"] = "DEACTIVATED"
        print(f"\n[NHI CUSTODIAN] Human Sponsor {sponsor_id} marked DEACTIVATED.")
        
        # 2. Find and revoke all linked Agents
        revoked_agents = []
        rotated_tokens = []
        
        for agent_id, agent_data in ACTIVE_AGENTS.items():
            if agent_data["owner_id"] == sponsor_id and agent_data["status"] == "ACTIVE":
                agent_data["status"] = "REVOKED"
                old_token = agent_data["token"]
                agent_data["token"] = f"REVOKED_{uuid.uuid4().hex[:8]}"
                
                revoked_agents.append(agent_id)
                rotated_tokens.append({"agent_id": agent_id, "old_token": old_token, "new_status": "REVOKED"})
                
                print(f"[NHI CUSTODIAN] 🚨 SECURITY: Agent '{agent_id}' DID forcibly REVOKED.")
                print(f"[NHI CUSTODIAN] 🔄 Token '{old_token}' invalidated.")
                
        return {
            "status": "success",
            "sponsor_deactivated": sponsor_id,
            "agents_revoked": revoked_agents,
            "tokens_rotated": rotated_tokens,
            "timestamp": time.time()
        }
        
    @classmethod
    def verify_agent_active(cls, agent_id: str) -> bool:
        """Helper to check if an agent's lifecycle is still active during API calls."""
        if agent_id not in ACTIVE_AGENTS:
            return False
        return ACTIVE_AGENTS[agent_id]["status"] == "ACTIVE"

if __name__ == "__main__":
    # Test routine
    print("Pre-Deactivation Sponsor EMP-001 Agents:")
    print([k for k,v in ACTIVE_AGENTS.items() if v["owner_id"] == "EMP-001"])
    
    res = NHILifecycleCustodian.deactivate_human_sponsor("EMP-001")
    
    print("\nPost-Deactivation Results:")
    print(res)
    print(f"Is agent-alpha-1 active? {NHILifecycleCustodian.verify_agent_active('agent-alpha-1')}")
