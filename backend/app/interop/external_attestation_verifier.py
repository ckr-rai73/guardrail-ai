import time
import json
import os
from typing import Dict, Any

# Mock public key registry for testing
MOCK_PUBLIC_KEY_REGISTRY = {
    "did:web:partner1.com": "pub_key_partner1_mock_123456",
    "did:web:guardrailaialliance.org": "pub_key_alliance_mock_789012",
}

def load_trusted_issuers() -> Dict[str, Any]:
    """Helper to load trusted issuers from config file."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "trusted_issuers.json")
    try:
        with open(config_path, "r") as f:
            data = json.load(f)
            return data.get("trusted_issuers", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print("[VERIFIER] Warning: Could not load trusted_issuers.json.")
        return {}

def verify_attestation(attestation: dict, issuer: str) -> float:
    """
    Phase 109: External Interoperability
    Evaluates the provided attestation payload and returns a calculated trust score.
    
    Args:
        attestation (dict): The attestation data payload.
        issuer (str): The entity that issued the attestation.
        
    Returns:
        float: A trust score between 0.0 and 1.0.
    """
    score = 0.0
    
    # 1. Validate Timestamp (Reject if older than 5 minutes)
    metadata = attestation.get("metadata", {})
    timestamp = attestation.get("timestamp") or metadata.get("timestamp", 0)
    current_time = time.time()
    
    if (current_time - float(timestamp)) > 300: # 5 minutes
        print(f"[VERIFIER] VETO: Attestation timestamp is too old (> 5 mins).")
        return 0.0
        
    if timestamp > current_time + 5: # Allow small positive clock drift
        print(f"[VERIFIER] VETO: Attestation timestamp is in the future.")
        return 0.0

    # 2. Signature Validation (0.5 if valid, else 0)
    signature = attestation.get("signature")
    expected_pub_key = MOCK_PUBLIC_KEY_REGISTRY.get(issuer)
    
    # Simple mock check for testing: assuming signature contains the pubkey
    is_signature_valid = False
    if signature and expected_pub_key and expected_pub_key in signature:
        is_signature_valid = True
        score += 0.5
        print(f"[VERIFIER] Signature mathematically valid for issuer {issuer}.")
    elif signature:
        print(f"[VERIFIER] WARNING: Signature present but issuer {issuer} pubkey unknown. Partial math trust.")
        score += 0.1
    else:
        print(f"[VERIFIER] WARNING: Invalid or missing signature for issuer {issuer}.")
        
    # 3. Issuer Reputation (0.3 if known, else 0)
    trusted_issuers = load_trusted_issuers()
    if issuer in trusted_issuers:
        score += 0.3
        print(f"[VERIFIER] Issuer {issuer} is recognized in trusted registry.")
    else:
        print(f"[VERIFIER] WARNING: Issuer {issuer} is UNKNOWN.")
        
    # 4. Claimed Governance Features (e.g., Veto-like control) (0.2 if present)
    claims = attestation.get("claims", {})
    if claims.get("has_veto_protocol") or claims.get("strict_governance_enforced"):
        score += 0.2
        print(f"[VERIFIER] Issuer claims sufficient governance/veto controls.")
        
    final_score = min(1.0, score)
    # Round to 2 decimal places
    final_score = round(final_score, 2)
    
    print(f"[VERIFIER] Final Trust Score for {issuer}: {final_score}")
    return final_score
