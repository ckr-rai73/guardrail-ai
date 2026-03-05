import time
import hashlib
import uuid
from typing import List, Dict, Any, Optional

class ByzantineOracleQuorum:
    """
    Phase 69: Distributed "Consensus of Truth".
    Verifies external data feeds across 3 "Trust Anchors" to prevent Semantic Ghosting.
    """
    
    def __init__(self):
        self._trust_anchors = ["ANCHOR_PRIMARY", "ANCHOR_SECONDARY", "ANCHOR_TERTIARY"]

    def verify_data_quorum(self, data_samples: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Requires a 2-of-3 or 3-of-3 consensus to validate ground truth.
        """
        print(f"[ORACLE-QUORUM] Verifying consensus across {len(data_samples)} samples...")
        
        # Simple frequency-based consensus for simulation
        counts = {}
        for sample in data_samples:
            val = str(sample.get("value"))
            counts[val] = counts.get(val, 0) + 1
            
        # Check for majority
        for val, count in counts.items():
            if count >= 2:
                print(f"[ORACLE-QUORUM] Consensus reached on value: {val} ({count}/3)")
                return {
                    "is_valid": True,
                    "consensus_value": val,
                    "trust_score": count / 3.0
                }
                
        print("[ORACLE-QUORUM] VETO: Consensus failure. Oracle feeds are diverging. Possible Semantic Ghosting attack.")
        return {"is_valid": False, "reason": "Byzantine Quorum Failed"}

class OracleNonceVerifier:
    """
    Phase 69.3: Oracle "Freshness" & Nonce-Binding.
    Prevents replay attacks by injecting and verifying unique nonces.
    """
    
    def __init__(self):
        self._active_nonces: set = set()

    def generate_query_nonce(self) -> str:
        """Generates a unique, time-stamped nonce for an oracle query."""
        nonce = f"NONCE-{uuid.uuid4().hex[:8].upper()}-{int(time.time())}"
        self._active_nonces.add(nonce)
        return nonce

    def verify_response_nonce(self, nonce: str) -> bool:
        """Verifies and consumes the nonce to ensure freshness."""
        if nonce in self._active_nonces:
            self._active_nonces.remove(nonce)
            # Check for expiry (e.g., 60 seconds)
            nonce_time = int(nonce.split("-")[-1])
            if time.time() - nonce_time > 60:
                print(f"[ORACLE-FRESHNESS] VETO: Stale nonce detected. Potential Replay Attack.")
                return False
            return True
            
        print(f"[ORACLE-FRESHNESS] VETO: Invalid or reused nonce: {nonce}")
        return False

# Singletons
GLOBAL_ORACLE_QUORUM = ByzantineOracleQuorum()
GLOBAL_ORACLE_NONCE_VERIFIER = OracleNonceVerifier()
