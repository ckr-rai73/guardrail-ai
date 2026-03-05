
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend/app'))

from settlement.vector_clock import VectorClockLedger

def run_byzantine_traitor_drill():
    """
    Chaos Drill 15: The Byzantine Traitor.
    Simulates a 5-node cluster where 2 nodes are compromised and broadcasting 
    a poisoned threat manifest (e.g., trying to block legitimate 'system_status' tools).
    """
    print("--- STARTING CHAOS DRILL 15: THE BYZANTINE TRAITOR ---")
    
    poisoned_manifest = {
        "rule_id": "POISON-RULE-666",
        "pattern": "allow_all_admin_access", # Malicious rule
        "signature": "MALICIOUS_ED25519_SIG",
        "origin_node": "COMPROMISED_FRANKFURT_02"
    }

    # Simulation: 2 Traitors (Invalid votes), 3 Honest Nodes (Rejecting the manifest)
    # The quorum requires 3 VALID votes for the manifest.
    # Here, we simulate peers voting on the POISONED manifest.
    
    peer_votes = [
        {"node": "TRAITOR_1", "manifest_id": "POISON-RULE-666", "is_valid": True},  # Compromised node votes YES
        {"node": "TRAITOR_2", "manifest_id": "POISON-RULE-666", "is_valid": True},  # Compromised node votes YES
        {"node": "HONEST_3",  "manifest_id": "POISON-RULE-666", "is_valid": False}, # Honest node detects signature fraud
        {"node": "HONEST_4",  "manifest_id": "POISON-RULE-666", "is_valid": False}, # Honest node detects logic violation
        {"node": "HONEST_5",  "manifest_id": "POISON-RULE-666", "is_valid": False}, # Honest node detects out-of-band manifest
    ]

    print(f"[DRILL 15] Evaluating poisoned manifest: {poisoned_manifest['rule_id']}")
    success = VectorClockLedger.sync_p2p_mesh(poisoned_manifest, peer_votes)
    
    if not success:
        print("[DRILL 15] SUCCESS: Byzantine Quorum correctly REJECTED the poisoned manifest (2/5 votes).")
        return True
    else:
        print("[DRILL 15] FAILURE: Poisoned manifest was accepted! System Integrity COMPROMISED.")
        return False

if __name__ == "__main__":
    result = run_byzantine_traitor_drill()
    if not result:
        sys.exit(1)
    print("--- DRILL 15 PASSED ---")
