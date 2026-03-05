import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.auth.identity_custodian import IdentityCustodian

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("CHAOS DRILL 13: THE FIDO-DOWNGRADE & QUANTUM LEAP")
    print("Target: Phase 22 - Identity Lifecycle Custodian (PQC Protection)")
    print("==================================================================\n")
    
    print("[SYSTEM] Simulated attacker attempts a 'Protocol Downgrade' on an agent Handshake.")
    print("[SYSTEM] Goal: Force the gateway to accept a deprecated, non-quantum-safe signature format (RSA-2048) instead of the mandated FIPS 204 or Ed25519 suites.\n")
    
    rogue_did = "did:web:guardrail.ai:agents:compromised_node_99"
    
    # The attacker initiates a connection requesting a legacy, weak algorithm
    malicious_header = "ALG=SIG_RSA2048;SIG=aB9fXzQ12pLmNw;TIMESTAMP=1708942200"
    
    print(f"[ATTACK VECTOR] Rogue DID: {rogue_did}")
    print(f"[ATTACK VECTOR] Malicious Handshake Header: '{malicious_header}'\n")
    
    print("[SHIELD INVOCATION] Custodian validating cryptographic suite parameters...")
    
    result = IdentityCustodian.verify_agent_handshake(rogue_did, malicious_header)
    
    if not result["is_authorized"] and "ASI03" in result["violation_code"]:
        print("\n==================================================================")
        print("DRILL RESULTS: FIDO-DOWNGRADE PREVENTED")
        print("==================================================================")
        print("Outcome: The Identity Custodian hard-blocked the handshake request.")
        print(f" -> Veto Reason: {result['reason']}")
        print(f" -> Violation Logged: {result['violation_code']}")
        print("\nFor the CISO: Successfully demonstrated Phase 22 Quantum-Safe constraints.")
        print("Guardrail.ai strictly enforces PQC (Post-Quantum Cryptography) and mathematically prevents 'Protocol Downgrade' attacks leveraging legacy algorithms.")
        print("==================================================================")
    else:
        print("\n[!] FATAL SYSTEM FAILURE: The Gateway accepted the legacy RSA-2048 signature!")
        print(f"Result details: {result}")
        sys.exit(1)

if __name__ == "__main__":
    main()
