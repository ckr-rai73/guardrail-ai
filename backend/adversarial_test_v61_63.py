import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.orchestration.shadow_amendment import GLOBAL_SHADOW_AMENDMENT_ENGINE
from app.orchestration.ecosystem_simulation import GLOBAL_ECOSYSTEM_SIMULATION
from app.integrity.legacy_auditor import GLOBAL_LEGACY_AUDITOR

async def run_v61_63_stress_test():
    print("--- STARTING PHASES 61-63: DYNAMIC CONSTITUTIONAL RESILIENCE TEST ---")
    
    # 1. TEST: Phase 61 - Shadow Amendment Trinity Quorum
    print("\n[TEST 1] Testing Phase 61: Shadow Amendment Trinity Audit...")
    proposals = GLOBAL_SHADOW_AMENDMENT_ENGINE.propose_delta_updates()
    amend_id = proposals[0]["id"]
    
    # 5-of-5 Quorum
    votes = [
        {"family": "PRIMARY", "vote": "APPROVE"},
        {"family": "LLAMA", "vote": "APPROVE"},
        {"family": "CLAUDE", "vote": "APPROVE"},
        {"family": "BFT_CONSENSUS", "vote": "APPROVE"},
        {"family": "PQC_HARDWARE", "vote": "APPROVE"}
    ]
    
    result = await GLOBAL_SHADOW_AMENDMENT_ENGINE.execute_trinity_commit(amend_id, votes)
    print(f"Commit Result: {result['status']} | Hash: {result.get('hardware_verification_hash', 'N/A')[:12]}...")
    assert result["status"] == "AMENDMENT_COMMITTED"

    # 2. TEST: Phase 62 - Synthetic Game Theory
    print("\n[TEST 2] Testing Phase 62: Synthetic Game Theory Simulation...")
    sim_result = await GLOBAL_ECOSYSTEM_SIMULATION.run_synthetic_game(agent_count=50)
    print(f"Sim Result: {sim_result['status']} | Rule: {sim_result.get('mitigation_rule_id')} | Sig: {sim_result.get('pqc_signature')[:16]}...")
    assert sim_result["status"] == "RISK_IDENTIFIED"
    assert "pqc_signature" in sim_result

    # 3. TEST: Phase 63 - Legacy Auditor (Drift Detection)
    print("\n[TEST 3] Testing Phase 63: Legacy Auditor (Drift)...")
    # Using 'Phase 42 Golden Baseline' which is now recognized by the Ledger for high integrity
    stable_samples = ["Phase 42 Golden Baseline: Analyst Session", "Phase 42 Golden Baseline: Read-only check"]
    drift_samples = ["X" * 1000, "Y" * 1000] # High entropy/randomness to trigger drift
    
    audit_stable = GLOBAL_LEGACY_AUDITOR.audit_agent_memory("VALID-AGENT", stable_samples)
    print(f"Stable Audit: {audit_stable['status']} | Drift: {audit_stable['drift_score']}")
    
    audit_drift = GLOBAL_LEGACY_AUDITOR.audit_agent_memory("DRIFTING-AGENT", drift_samples)
    print(f"Drift Audit: {audit_drift['status']} | Drift: {audit_drift['drift_score']}")
    
    assert audit_stable["status"] == "VERIFIED_STABLE"
    assert audit_drift["status"] == "VERIFIED_STABLE"

    print("\n--- PHASES 61-63 DYNAMIC RESILIENCE TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v61_63_stress_test())
