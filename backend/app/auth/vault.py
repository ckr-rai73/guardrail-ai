import os
import hashlib
import time
from typing import Dict, Optional

class CredentialVault:
    """
    Phase 44: Secure Credential Vault for MCP.
    Prevents "Confused Deputy" vulnerabilities by strictly scoping OAuth 2.1 
    tokens to specific agent identities and MCP servers.
    """
    
    def __init__(self):
        # In a production system, this would be backed by HashiCorp Vault or AWS KMS
        # Here we emulate a secure in-memory store with HMAC-based access control
        self._tokens: Dict[str, Dict[str, str]] = {}
        self._master_key = os.getenv("VAULT_MASTER_KEY", "default-governance-key-2026")

    def store_token(self, agent_id: str, server_id: str, raw_token: str):
        """Stores a token encrypted (emulated via hashing for prototype)."""
        vault_id = self._generate_vault_id(agent_id, server_id)
        # Mocking encryption
        opaque_ref = hashlib.sha256(f"{self._master_key}:{raw_token}".encode()).hexdigest()
        
        self._tokens[vault_id] = {
            "ref": opaque_ref,
            "raw": raw_token, # Reversible in this prototype for simulation
            "timestamp": str(time.time()),
            "owner": agent_id,
            "target": server_id
        }
        print(f"[VAULT] Securely vaulted token for {agent_id} -> {server_id} (Ref: {opaque_ref[:8]}...)")
        return opaque_ref

    def get_token(self, agent_id: str, server_id: str, context: str) -> Optional[str]:
        """
        Retrieves a token ONLY if the agent_id matches and context validates.
        Mitigates ASI03 (Privilege Abuse) during MCP tool calls.
        """
        vault_id = self._generate_vault_id(agent_id, server_id)
        entry = self._tokens.get(vault_id)
        
        if not entry:
            print(f"[VAULT] Access Denied: No token found for {agent_id} -> {server_id}")
            return None
            
        # Confused Deputy Check: Is the requesting agent the actual owner?
        if entry["owner"] != agent_id:
             print(f"[VAULT] SECURITY ALERT: Confused Deputy Attempt! Agent {agent_id} tried to use token owned by {entry['owner']}.")
             return None
             
        # Context-Aware release: Don't release tokens for high-risk financial servers in low-trust contexts
        if "finance" in server_id.lower() and "personal" in context.lower():
             print(f"[VAULT] Policy Veto: High-risk token release blocked for low-trust context.")
             return None
             
        print(f"[VAULT] Token released for {agent_id} -> {server_id}.")
        return entry["raw"]

    def _generate_vault_id(self, agent_id: str, server_id: str) -> str:
        return f"{agent_id}:{server_id}"

# Singleton instance for the gateway
GLOBAL_VAULT = CredentialVault()
