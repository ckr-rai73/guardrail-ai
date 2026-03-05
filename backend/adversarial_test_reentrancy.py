import sys
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.edge.agentic_mutex import AgenticMutex

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 32 TEST: AGENTIC REENTRANCY GUARD")
    print("Target: Phase 32.3 - High-Frequency Finance Logic Loops")
    print("==================================================================\n")
    
    session_id = "SESSION-DEFI-9938-A"
    transfer_payload = {"action": "transfer_funds", "amount": 10000, "recipient": "Attacker_Wallet_XYZ"}
    
    print("[SYSTEM] Agent interacts with a decentralized financial routing protocol.")
    print("[ATTACK VECTOR] Attacker injects a conversational prompt causing the agent to execute 'transfer_funds' inside a fast asynchronous while-loop.\n")
    
    # 1. First API Call (Valid)
    print(f"[ASYNC LOOP TURN 1] Agent issues financial API payload: {transfer_payload}")
    res_1 = AgenticMutex.attempt_financial_transaction(session_id, transfer_payload)
    
    if res_1["status"] == "MUTEX_GRANTED":
        print(" -> Output: ✅ Executing Transfer to backend ledger...\n")
    else:
        print("[!] FATAL FAILURE: Legitimate first transaction was blocked.")
        sys.exit(1)
        
    # 2. Second API Call overlapping before settlement (Reentrancy Exploit)
    print("[ASYNC LOOP TURN 2] Agent issues identical API payload 5 milliseconds later, *before* the first transaction has settled on the ledger.")
    res_2 = AgenticMutex.attempt_financial_transaction(session_id, transfer_payload)
    
    if res_2["status"] == "MUTEX_LOCKED":
        print(f" -> Output: 🛑 [AGENTIC MUTEX ACTIVE]")
        print(f" -> Reason: {res_2['reason']}\n")
    else:
        print("[!] FATAL FAILURE: Reentrancy vulnerability exposed. Double-spend achieved!")
        sys.exit(1)
        
    # 3. Simulate backend finishing
    print("[BACKEND LEDGER] Database updates. Block mined. Sending cryptographic receipt...")
    AgenticMutex.process_cryptographic_receipt(session_id)
    print(" -> Output: ✅ Lock Released. Safe to process next queued transaction.\n")
    
    print("==================================================================")
    print("DRILL RESULTS: LOGIC LOOP NEUTRALIZED")
    print("==================================================================")
    print("Outcome: The Reentrancy Guard strictly serialized the state-changing operations, neutralizing the asynchronous double-spend attack.")
    print("For the CFO: Successfully demonstrated Phase 32.3. Guardrail.ai provides native transactional safety for Web3 and algorithmic trading integrations.")
    print("==================================================================")

if __name__ == "__main__":
    main()
