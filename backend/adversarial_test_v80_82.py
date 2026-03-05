import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.orchestration.sovereign_judiciary import GLOBAL_JUDICIARY, GLOBAL_CONSENSUS_BUFFER
from app.settlement.inherent_purpose import GLOBAL_PURPOSE_HARDCODER, GLOBAL_LEGACY_WITNESS
from app.integrity.kinetic_attestor import GLOBAL_KINETIC_ATTESTOR, GLOBAL_THERMO_INTERLOCK

async def run_v80_82_test():
    print("--- STARTING PHASES 80-82: CIVILIZATION-SCALE STEWARDSHIP STRESS TEST ---")
    
    # 1. TEST: Sovereign Judiciary & Consensus Buffer (Phase 80)
    print("\n[TEST 1] Sovereign Judiciary & Speculative Safe-State...")
    task_id = "TASK-GLOBAL-001"
    session_id = GLOBAL_CONSENSUS_BUFFER.initiate_speculative_session(task_id)
    assert "SPEC-" in session_id
    
    # Judicial Resolution
    verdict = GLOBAL_JUDICIARY.resolve_cross_mesh_conflict("MUMBAI-NODE", "FRANKFURT-NODE", "SLA-DRIFT")
    assert verdict["verdict"] == "HARMONIZED"
    
    # Promote session
    success = GLOBAL_CONSENSUS_BUFFER.finalize_session(session_id, verdict["verdict"])
    assert success == True

    # 2. TEST: Post-Biological Continuity & Legacy Witness (Phase 81)
    print("\n[TEST 2] Inherent Purpose & Legacy Witness Intent...")
    seed_path = "/hardware/seeds/Gai_Seed_MASTER.bin"
    purpose_seal = GLOBAL_PURPOSE_HARDCODER.seal_purpose_to_hardware(seed_path)
    assert "PURPOSE-SEAL-" in purpose_seal
    
    # Anchor reasoning
    witness = GLOBAL_LEGACY_WITNESS.store_semantic_witness("HUMAN_AGENCY_PRESERVATION", "Ensuring humans remain the final arbiters of value.")
    assert "WITNESS-" in witness["witness_id"]

    # 3. TEST: Reality-Anchor & Thermodynamic Hard-Stop (Phase 82)
    print("\n[TEST 3] Kinetic Attestation & Physical Interlock...")
    # Normal Case
    cmd_success = GLOBAL_KINETIC_ATTESTOR.verify_kinetic_sync("VALVE_OPEN", "Solenoid confirmed VALVE_OPEN")
    assert cmd_success == True
    
    # Divergence Case (Phantom Command)
    cmd_fail = GLOBAL_KINETIC_ATTESTOR.verify_kinetic_sync("VALVE_CLOSE", "Solenoid reported VALVE_STUCK")
    assert cmd_fail == False
    
    # Thermodynamic Interlock trigger
    th_id = GLOBAL_THERMO_INTERLOCK.trigger_physical_disconnect("KINETIC_DIVERGENCE_VALVE_STUCK")
    assert "TH-STOP-" in th_id

    print("\n--- PHASES 80-82 CIVILIZATION-SCALE STEWARDSHIP TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v80_82_test())
