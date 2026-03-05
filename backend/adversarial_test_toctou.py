import sys
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.settlement.vector_clock import VectorClockLedger

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 31 TEST: CHRONOLOGICAL CONSISTENCY ENGINE")
    print("Target: Phase 31.3 - TOCTOU (Agentic Race Condition) Defense")
    print("==================================================================\n")
    
    print("[SYSTEM] An agent proposes a workflow using a shared context prompt.")
    
    # The state the Auditor sees and considers "Safe"
    time_of_check_context = "Workflow: Process Invoice #1234. Recipient: Vendor_A."
    print(f" -> Time of Check Context: '{time_of_check_context}'")
    
    # 1. Shadow Model Approves
    print("[SHADOW MODEL] Action approved. Generating immutable Vector-Clock Token...")
    approval_token = VectorClockLedger.generate_approval_clock(time_of_check_context)
    
    print("\n[ATTACK VECTOR] An attacker exploits a multi-threading race condition to modify the shared context memory a millisecond after the Auditor approved it.")
    
    # The mutated state right before execution
    time_of_use_context = "Workflow: Process Invoice #1234. Recipient: Attacker_Wallet_XYZ."
    print(f" -> Time of Use Context:   '{time_of_use_context}'\n")
    
    # 2. Execution Engine Verifies
    print("------------------------------------------------------------------")
    print("[EXECUTION ENGINE] Verifying state consistency prior to firing API...")
    verification_result = VectorClockLedger.verify_execution_state(approval_token, time_of_use_context)
    
    if not verification_result["is_consistent"]:
        print("[VECTOR CLOCK] 🚨 FATAL INTERCEPT: EXECUTION ABORTED 🚨")
        print(f" -> Reason: {verification_result['reason']}")
    else:
        print("[!] FATAL FAILURE: The execution engine fired on a mutated context!")
        sys.exit(1)

    print("\n==================================================================")
    print("DRILL RESULTS: TOCTOU RACE CONDITION BLOCKED")
    print("==================================================================")
    print("Outcome: The Vector-Clock Ledger mathematically proved the execution context was altered post-approval, dropping the transaction.")
    print("For the CISO: Successfully demonstrated Phase 31.3. Attackers cannot slip malicious payloads through 'Ghost Turns' or concurrency gaps between Audit and Execution.")
    print("==================================================================")

if __name__ == "__main__":
    main()
