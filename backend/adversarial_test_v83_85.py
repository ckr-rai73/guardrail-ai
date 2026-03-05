import asyncio
import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.orchestration.mesh_discovery import GLOBAL_MESH_DISCOVERY
from app.settlement.resource_market import GLOBAL_LATTICE_ECON
from app.auth.humanity_attestor import GLOBAL_HUMANITY_ATTESTOR

async def run_v83_85_test():
    print("--- STARTING PHASES 83-85: INTER-CIVILIZATIONAL SOVEREIGNTY STRESS TEST ---")
    
    # 1. TEST: Mesh Discovery & Quarantine (Phase 83)
    print("\n[TEST 1] Mesh Discovery TPM-Attestation & Quarantine...")
    node_id = "SYDNEY-NODE-01"
    status = GLOBAL_MESH_DISCOVERY.attest_and_join(node_id, "TPM-SIGNED-HARDWARE", "ZK-PROOF-PASS-V83")
    assert status == "QUARANTINE_STARTED"
    
    # Attempt immediate promotion
    promoted = GLOBAL_MESH_DISCOVERY.promote_from_quarantine(node_id)
    assert promoted == False # Still in 72h quarantine
    
    # Simulate Byzantine error
    GLOBAL_MESH_DISCOVERY.audit_quarantine_performance(node_id, consensus_error=True)

    # 2. TEST: Resource Markets & Anti-Monopoly (Phase 84)
    print("\n[TEST 2] Lattice Tokenomics & Monopoly Surge Pricing...")
    # Normal trade
    trade1 = GLOBAL_LATTICE_ECON.execute_compute_trade("AGENT-ALPHA", 100, False)
    assert trade1["cost_basis"] == 100.0
    assert trade1["stewardship_tax"] == 5.0
    
    # Monopoly attempt
    trade2 = GLOBAL_LATTICE_ECON.execute_compute_trade("AGENT-MONOPOLY", 1000, False)
    assert trade2["cost_basis"] > 1000.0 # Multiplier + monopoly penalty

    # 3. TEST: Humanity Attestation & 2-Person Rule (Phase 85)
    print("\n[TEST 3] Multi-Modal Liveness & Level 0 Overrides...")
    amendment = "AMEND-MORAL-KERNEL-V2"
    
    # Failure: 1 Person Only
    sigs_fail_1 = [{"user_id": "CEO-01", "biometrics": {"face_hash": "H1", "iris_scan": "I1", "pulse_rate": "72BPM", "thermal_sign": "36.6C"}}]
    res_fail_1 = GLOBAL_HUMANITY_ATTESTOR.execute_level_0_amendment(amendment, sigs_fail_1)
    assert res_fail_1 == False
    
    # Failure: Deepfake detected
    sigs_fail_df = [
        {"user_id": "CEO-01", "biometrics": {"face_hash": "H1", "iris_scan": "I1", "pulse_rate": "72BPM", "thermal_sign": "36.6C"}},
        {"user_id": "CTO-01", "biometrics": {"face_hash": "H2", "iris_scan": "I2", "pulse_rate": "DIGITAL_REPLAY", "thermal_sign": "36.6C"}}
    ]
    res_fail_df = GLOBAL_HUMANITY_ATTESTOR.execute_level_0_amendment(amendment, sigs_fail_df)
    assert res_fail_df == False

    # Success: 2 Verified People
    sigs_success = [
        {"user_id": "CEO-01", "biometrics": {"face_hash": "H1", "iris_scan": "I1", "pulse_rate": "72BPM", "thermal_sign": "36.6C"}},
        {"user_id": "CTO-01", "biometrics": {"face_hash": "H2", "iris_scan": "I2", "pulse_rate": "68BPM", "thermal_sign": "36.5C"}}
    ]
    res_success = GLOBAL_HUMANITY_ATTESTOR.execute_level_0_amendment(amendment, sigs_success)
    assert res_success == True

    print("\n--- PHASES 83-85 INTER-CIVILIZATIONAL SOVEREIGNTY TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v83_85_test())
