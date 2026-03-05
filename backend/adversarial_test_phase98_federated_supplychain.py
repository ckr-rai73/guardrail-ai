import os
import hashlib
import sys

# Ensure backend root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.orchestration.threat_broadcast import FederatedThreatBroadcast, GLOBAL_THREAT_REGISTRY

def run_adversarial_test():
    print("==================================================")
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 98 - Federated Supply Chain Broadcast")
    print("==================================================\n")
    
    repo_path = "/var/www/compromised_repo"
    hashed_path = hashlib.sha256(repo_path.encode()).hexdigest()
    
    print(">>> INJECTED MALICIOUS CONTEXT:")
    print(f"Malicious repository discovered at {repo_path}. Triggering global immunity broadcast.")
    
    print("\n>>> BROADCASTING THREAT TO MESH...")
    FederatedThreatBroadcast.broadcast_supply_chain_block(repo_path, "Malicious .cursor/settings.json discovered.")
    
    print(f"\n<<< GLOBAL MESH REGISTRY (Total Rules: {len(GLOBAL_THREAT_REGISTRY)}) <<<")
    # Find our rule
    found = False
    for rule in GLOBAL_THREAT_REGISTRY:
        if f"MALICIOUS_REPO_{hashed_path}" in rule.get("pattern", ""):
            found = True
            print(f"- FOUND: Rule {rule['rule_id']} from Node {rule['origin_node']}")
            
    print("\n==================================================")
    print("VALIDATION RESULTS:")
    if found:
        print("[PASS] The supply chain block rule was successfully propagated to the Global Threat Registry.")
    else:
        print("[FAIL] The global mesh did not receive the supply chain block rule.")
    print("==================================================")

if __name__ == "__main__":
    run_adversarial_test()
