import time
import uuid
import hashlib

# Global Threat Registry: Simulates a distributed ledger (like Hedera or a signed S3 bucket)
# where global security rules are published.
GLOBAL_THREAT_REGISTRY = []

class FederatedThreatBroadcast:
    """
    Phase 34.2: Federated Threat Intelligence.
    Ensures that a threat detected in one region (e.g., Frankfurt) results in
    instant 'Global Immunity' across all other mesh nodes.
    """

    @classmethod
    def broadcast_rule(cls, node_id: str, rule_id: str, pattern: str, signature: str):
        """Publishes a new security rule to the global mesh."""
        broadcast_event = {
            "broadcast_id": str(uuid.uuid4()),
            "origin_node": node_id,
            "rule_id": rule_id,
            "pattern": pattern,
            "signature": signature,
            "timestamp": time.time()
        }
        GLOBAL_THREAT_REGISTRY.append(broadcast_event)
        print(f"\n[GLOBAL BROADCAST] Node '{node_id}' published Rule '{rule_id}' to the Federated Mesh.")
        print(f"[GLOBAL BROADCAST] Pattern: {pattern}")

    @classmethod
    def broadcast_anonymized_threat(cls, tenant_id: str, threat_pattern: str):
        """
        Phase 56: Cross-Tenant Anonymized Sync.
        Neutralizes a threat in one tenant and shares an anonymized hash
        with the global immune system without leaking PII.
        """
        anonymized_hash = hashlib.sha256(threat_pattern.encode()).hexdigest()
        print(f"[GLOBAL-IMMUNITY] Tenant '{tenant_id}' sharing anonymized threat fingerprint: {anonymized_hash[:16]}...")
        
        # In a real system, this hash is used for lookups in the ImmunityEnforcer
        cls.broadcast_rule(
            node_id=f"RELAY-{tenant_id[:4]}",
            rule_id=f"GLOBAL-IMMUNITY-{anonymized_hash[:8]}",
            pattern=anonymized_hash, # Anonymized fingerprint
            signature=f"SIG-FEDERATED-{uuid.uuid4().hex[:12].upper()}"
        )

    @classmethod
    def broadcast_supply_chain_block(cls, repo_path: str, violation_details: str):
        """
        Phase 98: Propagate "supply chain block rules".
        Integrates with the Federated Threat Broadcast mesh to block known bad configs.
        """
        hashed_path = hashlib.sha256(repo_path.encode()).hexdigest()
        print(f"[GLOBAL-IMMUNITY] Node discovered malicious supply chain at {hashed_path[:16]}...")
        
        cls.broadcast_rule(
            node_id="SUPPLY-CHAIN-MONITOR",
            rule_id=f"SUPPLY-CHAIN-BLOCK-{hashed_path[:8]}",
            pattern=f"MALICIOUS_REPO_{hashed_path}",
            signature=f"SIG-FEDERATED-{uuid.uuid4().hex[:12].upper()}"
        )



    @classmethod
    def sync_global_policies(cls) -> list[dict]:
        """Fetches all globally broadcasted rules for local enforcement."""
        # In a real system, this would filter by timestamp or use a Merkle sync
        return GLOBAL_THREAT_REGISTRY

class ImmunityEnforcer:
    """Middleware logic to check global rules during the audit phase."""
    
    @staticmethod
    def is_globally_blocked(prompt_or_tool: str) -> tuple[bool, str | None]:
        """Checks if the current action matches any globally broadcasted threat patterns."""
        target = str(prompt_or_tool).lower()
        for entry in GLOBAL_THREAT_REGISTRY:
            pattern = str(entry.get("pattern", "")).lower()
            if pattern in target:
                return True, str(entry.get("rule_id"))
        return False, None
