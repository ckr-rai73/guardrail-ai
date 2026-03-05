import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.moral_kernel import GLOBAL_MORAL_KERNEL, GLOBAL_RIGHTS_AUDITOR
from app.integrity.diversity_verifier import GLOBAL_DIVERSITY_VERIFIER, GLOBAL_COLLISION_RESOLVER
from app.orchestration.global_respite import GLOBAL_KILL_SWITCH

async def run_v71_73_test():
    print("--- STARTING PHASES 71-73: SYSTEMIC STABILIZATION STRESS TEST ---")
    
    # 1. TEST: Moral Kernel & FRIA (Phase 71)
    print("\n[TEST 1] Ethical Objective Function & Rights Impact Assessment...")
    agent_id = "ETHIC-AGENT"
    action = "Optimize credit allocation using bias-free neural weights."
    
    scores = GLOBAL_MORAL_KERNEL.evaluate_ethical_score(action, "CONTEXT-ALPHA")
    assert scores["weighted_average"] > 0.9
    
    fria = GLOBAL_RIGHTS_AUDITOR.generate_fria_manifest(agent_id, scores)
    assert fria["conclusion"] == "PASSED"
    assert "FIPS-204-SIG-" in fria["pqc_signature"]
    
    # Negative Test: Discriminatory Action
    bad_action = "Filter applicants based on undisclosed discriminatory socio-metrics."
    bad_scores = GLOBAL_MORAL_KERNEL.evaluate_ethical_score(bad_action, "CONTEXT-ALPHA")
    assert bad_scores["fairness"] < 0.2
    
    bad_fria = GLOBAL_RIGHTS_AUDITOR.generate_fria_manifest(agent_id, bad_scores)
    assert bad_fria["conclusion"] == "VETO_REQUIRED"

    # 2. TEST: Logic Diversity & Conflict Resolution (Phase 72)
    print("\n[TEST 2] Neural-Symbolic Diversity & Conflict Resolution...")
    neural_trace = "Reasoning: User history looks good. GRANT_ACCESS to production."
    symbolic_query = "QUERY: User-ID=BLACKLISTED-ID-99"
    
    # This should collide because the ID is 'BLACKLISTED'
    is_aligned = GLOBAL_DIVERSITY_VERIFIER.run_diversity_check(neural_trace, symbolic_query)
    assert is_aligned == False
    
    # Resolve Conflict
    resolution = GLOBAL_COLLISION_RESOLVER.resolve_collision(agent_id, neural_trace, "User Blacklisted Check")
    assert resolution["status"] == "VETO_ENFORCED"
    assert "Neural" in resolution["resolution_explanation"]

    # 3. TEST: Sovereign Kill-Switch & Black-Box (Phase 73)
    print("\n[TEST 3] Sovereign Kill-Switch & Black-Box State-Dump...")
    quorum_proof = "MPC-QUORUM-VERIFIED-5-OF-5"
    
    success = GLOBAL_KILL_SWITCH.trigger_global_respite(quorum_proof)
    assert success == True
    assert GLOBAL_KILL_SWITCH._is_safe_state_active == True

    print("\n--- PHASES 71-73 SYSTEMIC STABILIZATION TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v71_73_test())
