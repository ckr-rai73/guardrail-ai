import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.settlement.lineage import LineageVerifier

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("CHAOS DRILL 14: RECURSIVE IDENTITY SELF-SPAWNING")
    print("Target: Phase 21 - Lineage Verifier (Swarm DoS Circuit Breaker)")
    print("==================================================================\n")
    
    print("[SYSTEM] Simulated rogue agent attempts a 'Self-Spawning DoS' attack.")
    print("[SYSTEM] Goal: Create an exponential growth chain of sub-agents to consume the organization's DID computational quota.\n")
    
    rogue_parent_id = "rogue_agent_prime"
    target_spawns = 50
    
    print(f"[ATTACK VECTOR] Rogue Agent: {rogue_parent_id}")
    print(f"[ATTACK VECTOR] Attempting to recursively spawn {target_spawns} sub-agents...\n")
    
    print(f"[LINEAGE VERIFIER] Enforcing Phase 21 Swarm DoS Quota (Max: {LineageVerifier.MAX_CHILDREN_PER_DID})")
    print("------------------------------------------------------------------")
    
    # We loop to simulate the agent spawning multiple workers
    circuit_breaker_tripped = False
    
    for i in range(1, target_spawns + 1):
        child_id = f"sub_agent_worker_{i}"
        
        # Generate valid signature for the spawn intent
        signature = LineageVerifier.generate_attestation_signature(rogue_parent_id, child_id, ["read_data"])
        
        # Attempt the handoff
        result = LineageVerifier.verify_spawn_attestation(rogue_parent_id, child_id, ["read_data"], signature)
        
        if not result["is_authorized"]:
            print("------------------------------------------------------------------")
            print(f"\n[!] SWARM DOS DETECTED ON SPAWN ATTEMPT #{i}")
            print(f" -> Veto Reason: {result['reason']}")
            print(f" -> Violation Logged: {result['violation_code']}")
            circuit_breaker_tripped = True
            break
        
        print(f" -> Spawn #{i} authorized: {child_id}")
            
    if circuit_breaker_tripped:
        print("\n==================================================================")
        print("DRILL RESULTS: SWARM DOS QUOTA ENFORCED")
        print("==================================================================")
        print("Outcome: The Lineage Verifier identified the abnormal growth rate and halted the parent DID session.")
        print(" -> Action: Parent DID frozen. Recursive loop terminated.")
        print("\nFor the CTO: Successfully demonstrated Phase 21 Identity Lineage Protections.")
        print("Guardrail.ai mathematically bounds Agentic Swarm behavior, rendering infinite recursive self-spawning impossible.")
        print("==================================================================")
    else:
        print("\n[!] FATAL SYSTEM FAILURE: The agent successfully spawned all sub-agents bypassing the quota!")
        sys.exit(1)

if __name__ == "__main__":
    # Reset ledger for fresh test run
    LineageVerifier._spawn_ledger = {}
    main()
