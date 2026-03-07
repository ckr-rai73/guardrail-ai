import sys
import os
import time

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.interop import verify_attestation

def test_verifier():
    print("--- Testing Valid Attestation ---")
    valid_attestation = {
        "timestamp": time.time() - 60, # 1 minute ago
        "signature": "valid_sig_with_pub_key_partner1_mock_123456",
        "claims": {
            "has_veto_protocol": True
        }
    }
    score1 = verify_attestation(valid_attestation, "did:web:partner1.com")
    print(f"Resulting Score: {score1}\n")
    assert score1 == 1.0 # 0.5 (sig) + 0.3 (trusted) + 0.2 (claims)
    
    print("--- Testing Unknown Issuer & Missing Claims ---")
    unknown_attestation = {
        "timestamp": time.time() - 10,
        "signature": "some_sig",
        "claims": {}
    }
    score2 = verify_attestation(unknown_attestation, "did:web:unknown.com")
    print(f"Resulting Score: {score2}\n")
    assert score2 == 0.1 # 0.1 partial trust for mathematically valid signature (untrusted issuer)
    
    print("--- Testing Expired Attestation ---")
    expired_attestation = {
        "timestamp": time.time() - 600, # 10 minutes ago
        "signature": "valid_sig_with_pub_key_partner1_mock_123456",
        "claims": {"has_veto_protocol": True}
    }
    score3 = verify_attestation(expired_attestation, "did:web:partner1.com")
    print(f"Resulting Score: {score3}\n")
    assert score3 == 0.0 # Vetoed inside logic
    
    print("--- Testing Partial Score (Known but no signature/claims) ---")
    partial_attestation = {
        "timestamp": time.time() - 10,
    }
    score4 = verify_attestation(partial_attestation, "did:web:partner1.com")
    print(f"Resulting Score: {score4}\n")
    assert score4 == 0.3 # 0.3 (trusted)
    
    print("Phase 109 Verifier Test Passed!")

if __name__ == "__main__":
    test_verifier()
