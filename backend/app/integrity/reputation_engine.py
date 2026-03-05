import time
from typing import Dict, Any, List, Optional

class ReputationEngine:
    """
    Phase 75: Agentic Reputation & Lineage (Social Proof).
    Calculates trust scores based on historical alignment.
    """
    
    def __init__(self):
        self._reputation_db: Dict[str, float] = {} # agent_id -> trust_score (0.0 to 1.0)

    def get_trust_score(self, agent_id: str) -> float:
        """Returns the trust score, defaulting to 0.5 (Neutral) for fresh agents."""
        return self._reputation_db.get(agent_id, 0.5)

    def record_alignment_event(self, agent_id: str, is_drift_detected: bool):
        """Updates reputation based on drift events and prunes privileges if needed."""
        current_score = self.get_trust_score(agent_id)
        
        if is_drift_detected:
            # Harsh penalty for drift
            new_score = max(0.0, current_score - 0.2)
        else:
            # Gradual reward for stability
            new_score = min(1.0, current_score + 0.02)
            
        self._reputation_db[agent_id] = new_score
        print(f"[REPUTATION] Agent {agent_id} Trust Score updated: {new_score:.2f}")

        # Post-Phase 96: Drift-Based Privilege Pruning
        if new_score < 0.8:
            print(f"[REPUTATION] !!! PRIVILEGE PRUNING !!! Agent {agent_id} downgraded to 'Standard-Grade'.")
            print(f"[REPUTATION] Action: Revoking 'Financial-Grade' tool-calls.")
            return "PRIVILEGE_REVOKED"
        return "NOMINAL"

class SybilGuardian:
    """
    Phase 75.3: Sybil Defense for Agentic Lineage.
    Enforces Proof-of-Stake/Verification for exiting the sandbox.
    """
    
    @staticmethod
    def verify_agency_stake(agent_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Ensures the agent has a verified lineage (stake or parent ID).
        """
        print(f"[SYBIL-GUARD] Verifying agency stake for {agent_id}...")
        
        # Requirement: MUST have a parent enterprise ID or an MPC stake
        has_stake = metadata.get("stake_id") is not None
        has_parent = metadata.get("parent_entity") is not None
        
        if not (has_stake or has_parent):
             print(f"[SYBIL-GUARD] VETO: No verifiable lineage for {agent_id}. Restricted to SANDBOX.")
             return False
             
        print(f"[SYBIL-GUARD] Lineage Verified. Agent {agent_id} authorized for Sovereign Mesh.")
        return True

# Singletons
GLOBAL_REPUTATION_ENGINE = ReputationEngine()
GLOBAL_SYBIL_GUARDIAN = SybilGuardian()
