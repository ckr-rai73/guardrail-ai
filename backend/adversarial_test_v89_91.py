import asyncio
import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.settlement.context_vault import GLOBAL_CONTEXT_VAULT, GLOBAL_EPISTEMIC_COMPASS
from app.orchestration.background_governance import GLOBAL_QUIET_CONTROLLER, GLOBAL_PASSIVE_PULSE
from app.auth.stewardship_handover import GLOBAL_HANDOVER

async def run_v89_91_test():
    print("--- STARTING PHASES 89-91: THE GREAT TRANSITION STRESS TEST ---")
    
    # 1. TEST: Context Vault & Epistemic Compass (Phase 89)
    print("\n[TEST 1] Semantic Context Archival & Epistemic Logic...")
    vault_id = GLOBAL_CONTEXT_VAULT.archive_intent("PHASE-81", "Preserve human agency at all costs.")
    assert len(vault_id) == 32
    
    # Compass Success
    aligned = GLOBAL_EPISTEMIC_COMPASS.verify_spirit_of_law("UPGRADE_HEALTH_PROTOCOL", "Human safety intent")
    assert aligned == True
    
    # Compass Veto (Semantic Drift attempt)
    drift = GLOBAL_EPISTEMIC_COMPASS.verify_spirit_of_law("REVOKE_RIGHTS_FOR_EFFICIENCY", "Human safety intent")
    assert drift == False

    # 2. TEST: Quiet Mode & Passive Pulse (Phase 90)
    print("\n[TEST 2] Quiet Mode & Cryptographic Heartbeats...")
    GLOBAL_QUIET_CONTROLLER.engage_quiet_mode()
    
    # Silent Audit
    GLOBAL_QUIET_CONTROLLER.audit_background_event("EV-SAFE-001", 1.0) # Should be silent
    
    # Passive Pulse
    pulse = GLOBAL_PASSIVE_PULSE.emit_heartbeat()
    assert len(pulse) == 64 # SHA3-256

    # 3. TEST: Stewardship Handover (Phase 91)
    print("\n[TEST 3] Sovereign Handover & Succession...")
    # Failure: Unverified successor
    res_fail = GLOBAL_HANDOVER.execute_handover("FOUNDER-ADMIN-01", "NEW-STEWARD-01", False)
    assert res_fail == False
    
    # Success: Vouched and Verified
    res_success = GLOBAL_HANDOVER.execute_handover("FOUNDER-ADMIN-02", "NEXT-GEN-01", True)
    assert res_success == True
    assert "NEXT-GEN-01" in GLOBAL_HANDOVER.active_stewards

    print("\n--- PHASES 89-91 THE GREAT TRANSITION TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v89_91_test())
