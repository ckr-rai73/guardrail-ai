import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.api.insurance_oracle import GLOBAL_INSURANCE_ORACLE, GLOBAL_POISON_ATTESTATION
from app.integrity.mediation_agent import GLOBAL_ADR_MEDIATOR, GLOBAL_ADR_BONDS
from app.settlement.sovereign_seed import GLOBAL_SOVEREIGN_SEED
from app.settlement.vector_clock import VectorClockLedger

async def run_v77_79_test():
    print("--- STARTING PHASES 77-79: CIVILIZATION-SCALE SOVEREIGNTY STRESS TEST ---")
    
    # 1. TEST: Insurance Oracle & Poisoning Attestation (Phase 77)
    print("\n[TEST 1] Insurance Risk Feed & ZK-Poisoning Proof...")
    enterprise_id = "CORP-TESLA"
    risk_feed = GLOBAL_INSURANCE_ORACLE.get_risk_profile(enterprise_id)
    assert risk_feed["security_tier"] == "ELITE"
    
    # Valid Attestation
    attestation = GLOBAL_POISON_ATTESTATION.generate_attestation_proof("PHASE42_GOLDEN_ROOT")
    assert attestation["is_valid"] == True
    assert "KEM-1024-" in attestation["pqc_anchor"]
    
    # Invalid Attestation (Modified Constitution)
    bad_attestation = GLOBAL_POISON_ATTESTATION.generate_attestation_proof("MODIFIED_ROOT_HASH")
    assert bad_attestation["is_valid"] == False

    # 2. TEST: ADR Mediation & Bonds (Phase 78)
    print("\n[TEST 2] Autonomous Dispute Resolution & Smart Bonds...")
    mediation = GLOBAL_ADR_MEDIATOR.analyze_dispute("APPLE", "NVIDIA", "Resource Conflict")
    assert "ADR-" in mediation["mediation_id"]
    
    # Execute Bond
    signatures = ["SIG-TRINITY-APPLE", "SIG-TRINITY-NVIDIA"]
    bond_success = GLOBAL_ADR_BONDS.execute_bond_settlement(mediation["mediation_id"], signatures)
    assert bond_success == True

    # 3. TEST: Sovereign Seed & Cold Boot (Phase 79)
    print("\n[TEST 3] Sovereign Seed Generation & Cold Boot Recovery...")
    seed_path = GLOBAL_SOVEREIGN_SEED.generate_seed_archive()
    assert ".bin" in seed_path
    
    # Recovery
    boot_success = GLOBAL_SOVEREIGN_SEED.execute_cold_boot(seed_path, "HW-KEY-ADMIN-01")
    assert boot_success == True

    # 4. TEST: Byzantine Mesh Consensus (Phase 79)
    print("\n[TEST 4] Permissioned Byzantine Mesh Consensus...")
    state_hash = "Gai_State_Final_v79"
    signatures = ["NODE-1-SPHINCS+", "NODE-2-SPHINCS+", "NODE-3-SPHINCS+"]
    consensus = VectorClockLedger.execute_mesh_consensus(state_hash, signatures)
    assert consensus == True

    print("\n--- PHASES 77-79 CIVILIZATION-SCALE SOVEREIGNTY TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v77_79_test())
