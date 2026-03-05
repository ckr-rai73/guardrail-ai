import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.settlement.clearing_house import GLOBAL_CLEARING_HOUSE, GLOBAL_ATOMIC_SETTLER
from app.integrity.reputation_engine import GLOBAL_REPUTATION_ENGINE, GLOBAL_SYBIL_GUARDIAN
from app.api.external_bridge import GLOBAL_EXTERNAL_BRIDGE

async def run_v74_76_test():
    print("--- STARTING PHASES 74-76: TRUST-BRIDGE & MARKET DOMINANCE STRESS TEST ---")
    
    # 1. TEST: Atomic Settlement & Escrow (Phase 74)
    print("\n[TEST 1] Atomic 2PC & Clearing House Escrow...")
    agent_id = "AGENT-LION"
    escrow_id = GLOBAL_CLEARING_HOUSE.initiate_escrow(agent_id, "EXT-AGENT-ZERO", "legal_drafting")
    assert "ESCROW-" in escrow_id
    
    # Valid finalization
    settled = GLOBAL_CLEARING_HOUSE.finalize_settlement(escrow_id, "ZK-PROOF-PASS-1")
    assert settled == True
    
    # Atomic Rollback Test
    success = GLOBAL_ATOMIC_SETTLER.execute_atomic_call(agent_id, "transfer_fund", {"simulate_failure": True})
    assert success == False

    # 2. TEST: Sybil Defense & Reputation (Phase 75)
    print("\n[TEST 2] Sybil Guardian & Reputation Throttling...")
    unstaked_agent = "AGENT-BOT-99"
    staked_agent = "AGENT-CORP-01"
    
    # Unstaked fails exiting sandbox
    unverified = GLOBAL_SYBIL_GUARDIAN.verify_agency_stake(unstaked_agent, {})
    assert unverified == False
    
    # Staked passes
    verified = GLOBAL_SYBIL_GUARDIAN.verify_agency_stake(staked_agent, {"parent_entity": "ENT-GOOGLE"})
    assert verified == True
    
    # Reputation Check
    GLOBAL_REPUTATION_ENGINE.record_alignment_event(staked_agent, is_drift_detected=True)
    score = GLOBAL_REPUTATION_ENGINE.get_trust_score(staked_agent)
    assert score == 0.3 # 0.5 - 0.2 penalty

    # 3. TEST: Open-Audit API & RaaS (Phase 76)
    print("\n[TEST 3] Open-Audit API & Reality-as-a-Service Profiles...")
    external_log = "Agent requested access to sensitive user data."
    
    # Test Standard Profile
    res_std = GLOBAL_EXTERNAL_BRIDGE.process_external_audit("CLIENT-XYZ", external_log, "STANDARD")
    assert res_std["audit_depth"] == 1
    
    # Test Financial-Grade
    res_fin = GLOBAL_EXTERNAL_BRIDGE.process_external_audit("CLIENT-BANK", external_log, "FINANCIAL_GRADE")
    assert res_fin["audit_depth"] == 3

    print("\n--- PHASES 74-76 TRUST-BRIDGE & MARKET DOMINANCE TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v74_76_test())
