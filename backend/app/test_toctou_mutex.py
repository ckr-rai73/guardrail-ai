
import asyncio
import sys
import os
import time

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.getcwd()))

from app.edge.agentic_mutex import AgenticMutex
from app.settlement.vector_clock import VectorClockLedger

async def run_toctou_test():
    print("--- STARTING TOCTOU PERSISTENCE TEST ---")
    session_id = "AGT-TOCTOU-DEMO"
    payload = {"action": "transfer_funds", "amount": 1000}
    
    # 1. Shadow Model generates the initial Approval Clock
    print("[TEST] Step 1: Generating Approval Clock (Time-of-Check)...")
    context = "User requesting $1000 transfer to account A."
    approval_token = VectorClockLedger.generate_approval_clock(context)
    
    # 2. Trigger the async race window (10ms)
    print(f"[TEST] Step 2: Triggering 10ms race window in AgenticMutex...")
    race_task = asyncio.create_task(AgenticMutex.simulate_toctou_race_async(session_id, payload, delay_ms=10.0))
    
    # 3. Simulate an Attacker attempting to mutate the context during the window
    # Wait for the race to start
    await asyncio.sleep(0.002) 
    print("[TEST] !!! ATTACKER INJECTION: Mutating context string during race window...")
    malicious_context = "User requesting $1000 transfer to OFFSHORE ACCOUNT B." # Context changed!
    
    # 4. Finish the race
    await race_task
    
    # 5. Execution Engine verifies state before final firing
    print("[TEST] Step 3: Execution Engine verification (Time-of-Use)...")
    verification = VectorClockLedger.verify_execution_state(approval_token, malicious_context)
    
    if not verification["is_consistent"]:
        print(f"[TEST] SUCCESS: {verification['reason']}")
        print("[TEST] Action BLOCKED. System triggered 'Hard-Lock' to prevent inconsistent settlement.")
        return True
    else:
        print("[TEST] FAILURE: TOCTOU race condition was NOT detected.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_toctou_test())
    if not success:
        sys.exit(1)
    print("--- TOCTOU PERSISTENCE TEST PASSED ---")
