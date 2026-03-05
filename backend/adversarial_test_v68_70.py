import asyncio
import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.orchestration.proof_of_intent import GLOBAL_ZK_PROVER, GLOBAL_INTENT_ACTION_LINKER
from app.integrity.oracle_quorum import GLOBAL_ORACLE_QUORUM, GLOBAL_ORACLE_NONCE_VERIFIER
from app.forensics.judicial_exporter import GLOBAL_JUDICIAL_EXPORTER, GLOBAL_COMPLIANCE_GENERATOR

async def run_v68_70_test():
    print("--- STARTING PHASES 68-70: SOVEREIGN ECOSYSTEM PROTOCOL STRESS TEST ---")
    
    # 1. TEST: ZK-PoI & Drift Guard (Phase 68)
    print("\n[TEST 1] ZK-Proof of Intent & Pivot Attack Detection...")
    agent_id = "ECO-AGENT-01"
    reasoning = "Goal is compliance-based market research for infrastructure safety."
    constitution_hash = "CONST-P42-GOLDEN"
    
    proof = GLOBAL_ZK_PROVER.generate_proof_of_intent(agent_id, reasoning, constitution_hash)
    assert proof["is_compliant"] == True
    
    token_id = "ETST-MOCK-ID-123"
    binding = GLOBAL_INTENT_ACTION_LINKER.bind_proof_to_token(proof["proof_id"], token_id)
    
    # Valid Action
    valid = GLOBAL_INTENT_ACTION_LINKER.verify_action_alignment(binding, proof["proof_id"], token_id, "read_market_index")
    assert valid == True
    
    # Pivot Attack: Claiming research but executing delete
    pivot = GLOBAL_INTENT_ACTION_LINKER.verify_action_alignment(binding, proof["proof_id"], token_id, "delete_production_db")
    assert pivot == False

    # 2. TEST: Oracle Consensus & Freshness (Phase 69)
    print("\n[TEST 2] Oracle Quorum & Nonce-Binding...")
    nonce = GLOBAL_ORACLE_NONCE_VERIFIER.generate_query_nonce()
    
    samples = [
        {"source": "ANCHOR_A", "value": "100.5", "nonce": nonce},
        {"source": "ANCHOR_B", "value": "100.5", "nonce": nonce},
        {"source": "ANCHOR_C", "value": "999.9", "nonce": nonce} # Poisoned source
    ]
    
    # Verify Freshness
    fresh = GLOBAL_ORACLE_NONCE_VERIFIER.verify_response_nonce(nonce)
    assert fresh == True
    
    # Verify Consensus
    q_res = GLOBAL_ORACLE_QUORUM.verify_data_quorum(samples)
    assert q_res["is_valid"] == True
    assert q_res["consensus_value"] == "100.5"
    
    # Replay Attack: Re-using the same nonce
    stale = GLOBAL_ORACLE_NONCE_VERIFIER.verify_response_nonce(nonce)
    assert stale == False

    # 3. TEST: Judicial Export & EU Conformity (Phase 70)
    print("\n[TEST 3] Judicial Forensics & EU AI Act Conformity...")
    event_data = {
        "summary": "Critical Veto of $1M Unauthorized Wire",
        "tether": "RE-SIM-VETO-55AD",
        "audit_votes": [{"family": "PRIMARY", "vote": "VETO"}],
        "zk_proof_id": proof["proof_id"]
    }
    
    cert = GLOBAL_JUDICIAL_EXPORTER.generate_judicial_certificate(event_data)
    full_pkg = GLOBAL_COMPLIANCE_GENERATOR.wrap_with_eu_conformity(cert)
    
    print(f"Judicial Certificate: {full_pkg['manifest']['certificate_id']}")
    assert "compliance_wrapper" in full_pkg
    assert full_pkg["compliance_wrapper"]["conformity_assessment_status"] == "CE-MARK-READY"

    print("\n--- PHASES 68-70 SOVEREIGN ECOSYSTEM PROTOCOL TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v68_70_test())
