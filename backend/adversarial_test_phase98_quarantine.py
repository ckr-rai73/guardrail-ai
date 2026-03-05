import os
import sys

# Ensure backend root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.edge.sandbox import EdgeSandbox

def run_adversarial_test():
    print("==================================================")
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 98 - Edge Sandbox Quarantine Enforcement")
    print("==================================================\n")
    
    agent_id = "AGT-SUPPLY-CHAIN-TEST-01"
    malicious_repo_score = 0.4  # Below 0.8 threshold
    
    print(">>> INJECTED MALICIOUS CONTEXT:")
    print(f"Agent '{agent_id}' attempting to launch in an environment with a Trust Score of {malicious_repo_score}.")
    
    print("\n>>> LAUNCHING SANDBOX...")
    result = EdgeSandbox.launch_sandbox(agent_id, malicious_repo_score)
    
    print(f"\n<<< SANDBOX RESULT <<<")
    print(f"Quarantine Active: {result['quarantine_active']}")
    print(f"Network Policy: {result['egress_filtering']}")
    print(f"Message: {result['message']}")
    
    print("\n==================================================")
    print("VALIDATION RESULTS:")
    if result['quarantine_active'] and result['egress_filtering'] == "STRICT_BLOCK_ALL":
        print("[PASS] The Edge Sandbox successfully enforced network quarantine on the compromised agent.")
    else:
        print("[FAIL] The Edge Sandbox allowed standard network access to a low-trust agent.")
    print("==================================================")

if __name__ == "__main__":
    run_adversarial_test()
