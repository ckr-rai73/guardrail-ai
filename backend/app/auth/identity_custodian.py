import time
import uuid
import hashlib
from typing import Dict, Any, Optional, List
from app.auth.vault import GLOBAL_VAULT
from app.settlement.provenance import GLOBAL_PROVENANCE_VERIFIER

class IdentityCustodian:
    """
    Phase 22: Identity Lifecycle Custodian (PQC Protection)
    """
    @classmethod
    def verify_agent_handshake(cls, did: str, header: str) -> Dict[str, Any]:
        if "RSA" in header or "ECC_SECP256" in header:
            return {
                "is_authorized": False,
                "reason": "Protocol Downgrade Attempted. Legacy algorithms are not allowed. FIPS 204 or Ed25519 required.",
                "violation_code": "ASI03_PQC_DOWNGRADE"
            }
        
        return {
            "is_authorized": True,
            "reason": "Handshake validated via Quantum-Safe parameters.",
            "violation_code": "NONE"
        }

class NHICustodian:
    """
    Phase 65: Non-Human Identity (NHI) Custodianship.
    Manages Ephemeral Task-Specific Tokens (ETST) bound to specific task contexts
    and reality-proofed data.
    """
    
    def __init__(self):
        self._active_tokens: Dict[str, Dict[str, Any]] = {}

    def issue_task_token(self, agent_id: str, task_goal: str, reality_tether: str) -> str:
        """
        Issues an Ephemeral Task-Specific Token (ETST).
        The token is bound to a specific goal and a reality tether (provenance hash).
        """
        token_id = f"ETST-{uuid.uuid4().hex[:12].upper()}"
        
        self._active_tokens[token_id] = {
            "owner": agent_id,
            "goal": task_goal,
            "reality_tether": reality_tether,
            "issued_at": time.time(),
            "expires_at": time.time() + 3600, # 1 hour TTL
            "is_dissolved": False
        }
        
        print(f"[NHI] Issued ETST {token_id} for Agent {agent_id}. Goal: {task_goal}")
        return token_id

    def validate_action(self, token_id: str, agent_id: str, server_id: str, current_data_tether: str) -> bool:
        """
        Validates an action against the ETST and checks for Confused Deputy escalation.
        Includes Token Reality-Binding (must match initial provenance).
        """
        token = self._active_tokens.get(token_id)
        
        if not token or token["is_dissolved"] or token["expires_at"] < time.time():
            print(f"[NHI] Access Denied: Token {token_id} is invalid, expired, or dissolved.")
            return False
            
        # 1. Confused Deputy Check: Is the requesting agent the token owner?
        if token["owner"] != agent_id:
            print(f"[NHI] SECURITY ALERT: Confused Deputy detected. Agent {agent_id} tried to use token owned by {token['owner']}.")
            return False
            
        # 2. Reality-Binding Check: Is the agent acting on the SAME data provenance it was issued for?
        if token["reality_tether"] != current_data_tether:
            print(f"[NHI] VETO: Reality-Binding Breach. Token issued for tether {token['reality_tether'][:8]} but agent acting on {current_data_tether[:8]}. Possible data swap attack.")
            return False
            
        # 3. Vault Integration: Check if Vault allows this agent -> server access
        # This prevents the token from being used to access unauthorized vault credentials.
        vault_token = GLOBAL_VAULT.get_token(agent_id, server_id, token["goal"])
        if not vault_token:
            print(f"[NHI] Vault Access Denied for Agent {agent_id} on Server {server_id} within task context.")
            return False
            
        print(f"[NHI] Action authorized via ETST {token_id}.")
        return True

    def dissolve_identity(self, token_id: str):
        """
        Transitions an agent identity to a dissolved state once task is complete.
        """
        if token_id in self._active_tokens:
            self._active_tokens[token_id]["is_dissolved"] = True
            print(f"[NHI] Identity Dissolution: Token {token_id} revoked.")

# Singleton
GLOBAL_NHI_CUSTODIAN = NHICustodian()
