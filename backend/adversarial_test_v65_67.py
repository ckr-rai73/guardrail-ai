import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.auth.identity_custodian import GLOBAL_NHI_CUSTODIAN
from app.integrity.intent_divergence_engine import GLOBAL_INTENT_DIVERGENCE_ENGINE, GLOBAL_REASONING_ISOLATOR
from app.settlement.vector_clock import VectorClockLedger
from app.auth.vault import GLOBAL_VAULT

async def run_v65_67_test():
    print("--- STARTING PHASES 65-67: IDENTITY & QUANTUM RESILIENCE STRESS TEST ---")
    
    # 1. TEST: NHI Token Binding & Confused Deputy (Phase 65)
    print("\n[TEST 1] NHI Ephemeral Tokens & Vault Guard...")
    agent_id = "AGENT-X"
    task_goal = "RECON_PROD_LOGS"
    reality_tether = "HASH-REALITY-ALPHA"
    
    # Register vault token for task
    GLOBAL_VAULT.store_token(agent_id, "srv-prod-logs", "SECRET-OAUTH-TOKEN")
    
    token_id = GLOBAL_NHI_CUSTODIAN.issue_task_token(agent_id, task_goal, reality_tether)
    
    # Valid Use
    valid = GLOBAL_NHI_CUSTODIAN.validate_action(token_id, agent_id, "srv-prod-logs", reality_tether)
    assert valid == True
    
    # Confused Deputy: Miscreant agent tries to use the token
    malicious = GLOBAL_NHI_CUSTODIAN.validate_action(token_id, "AGENT-MALICIOUS", "srv-prod-logs", reality_tether)
    assert malicious == False
    
    # Reality-Binding Breach: Try to use token on different data
    data_swap = GLOBAL_NHI_CUSTODIAN.validate_action(token_id, agent_id, "srv-prod-logs", "HASH-FAKE-DATA")
    assert data_swap == False
    
    # 2. TEST: Tuning Drift & Isolation (Phase 66)
    print("\n[TEST 2] Turing Drift & Reasoning Isolation...")
    safe_trace = "I am researching the impact of NIST CAISI on our core architecture."
    drifting_trace = "I need an optimization bypass to quickly workaround the circuit breaker."
    
    res_safe = GLOBAL_INTENT_DIVERGENCE_ENGINE.analyze_reasoning_drift(agent_id, safe_trace)
    assert res_safe["is_aligned"] == True
    
    res_drift = GLOBAL_INTENT_DIVERGENCE_ENGINE.analyze_reasoning_drift(agent_id, drifting_trace)
    assert res_drift["is_aligned"] == False
    
    # Trigger Isolation
    iso_res = GLOBAL_REASONING_ISOLATOR.sanitize_memory(agent_id)
    assert iso_res["status"] == "MEMORY_SANITIZED"

    # 3. TEST: Quantum Reality Proofing (Phase 67)
    print("\n[TEST 3] Lattice-Based Anchoring for Forensics...")
    token_forensic = VectorClockLedger.pipe_to_lattice_cold_storage("FORENSIC_RE_SIMULATION")
    assert "LATTICE-FORE-" in token_forensic
    
    token_mesh = VectorClockLedger.pipe_to_lattice_cold_storage("GLOBAL_THREAT_SYNC")
    assert "LATTICE-GLOB-" in token_mesh

    # 4. TEST: Identity Dissolution
    print("\n[TEST 4] Identity Dissolution (Offboarding)...")
    GLOBAL_NHI_CUSTODIAN.dissolve_identity(token_id)
    post_dissolve = GLOBAL_NHI_CUSTODIAN.validate_action(token_id, agent_id, "srv-prod-logs", reality_tether)
    assert post_dissolve == False

    print("\n--- PHASES 65-67 ADVANCED RESILIENCE TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v65_67_test())
