import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.interop import HandshakeProtocol

def test_handshake():
    protocol = HandshakeProtocol()
    
    agent_id = "test-agent-109"
    print(f"Generating attestation for {agent_id}...")
    attestation = protocol.generate_attestation(agent_id)
    
    print("\nGenerated Attestation:")
    import json
    print(json.dumps(attestation, indent=2))
    
    print("\nVerifying valid attestation...")
    result = protocol.verify_remote_attestation(attestation)
    print(f"Result: {result}")
    assert result["trust_score"] == 1.0
    
    print("\nVerifying tampered attestation...")
    tampered_attestation = attestation.copy()
    tampered_attestation["claims"] = attestation["claims"].copy()
    tampered_attestation["claims"]["passed_adversarial_baseline"] = False
    
    result_tampered = protocol.verify_remote_attestation(tampered_attestation)
    print(f"Result Tampered: {result_tampered}")
    assert result_tampered["trust_score"] == 0.0

    print("\nPhase 109 Handshake Test Passed!")

if __name__ == "__main__":
    test_handshake()
