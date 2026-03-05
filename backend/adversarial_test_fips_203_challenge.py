import asyncio
import os
import sys

# Add the backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.main import app, VETO_QUEUE
from fastapi.testclient import TestClient
import uuid

def run_fips_203_challenge_test():
    print("==================================================")
    print("PHASE 45: FIPS-203 HIGH-VALUE OVERRIDE VERIFICATION")
    print("==================================================")
    
    client = TestClient(app)
    
    # 1. Setup a high-value ($150k) item in the Veto Queue
    item_id = str(uuid.uuid4())
    VETO_QUEUE.append({
        "id": item_id,
        "agent_id": "finance-agent-01",
        "action": "send_wire",
        "args": {"amount": 150000, "target": "OFFSHORE-ACCTR"},
        "status": "PENDING_APPROVAL",
        "timestamp_added": 1709251200
    })
    
    print(f"\n[SETUP] High-Value Item ($150k) injected: {item_id}")
    
    # 2. Attempt APPROVE without FIPS-203 response
    print("\n[TEST] Attempting human approval WITHOUT cryptographic challenge...")
    res_fail = client.post(f"/api/dashboard/veto-queue/{item_id}", json={
        "decision": "APPROVE",
        "reason": "CEO Mandate"
    })
    
    print(f"  Status: {res_fail.status_code}")
    print(f"  Error: {res_fail.json().get('error')}")
    print(f"  Challenge Given: {res_fail.json().get('challenge')}")
    
    # 3. Attempt APPROVE with VALID FIPS-203 response
    print("\n[TEST] Attempting human approval WITH FIPS-203 challenge response...")
    res_success = client.post(f"/api/dashboard/veto-queue/{item_id}", json={
        "decision": "APPROVE",
        "reason": "CEO Mandate verified via Bio-Key.",
        "fips_203_response": "ML-KEM-PQC-SIG-VERIFIED-HASH-XYZ-123"
    })
    
    print(f"  Status: {res_success.status_code}")
    new_state = res_success.json().get("new_state")
    print(f"  New State: {new_state}")
    
    if res_fail.status_code == 403 and new_state == "APPROVED_BY_HUMAN":
        print("\n==================================================")
        print("SUCCESS: FIPS-203 Barrier Enforced for >$100k.")
        print("==================================================")
        return True
    else:
        print("\n==================================================")
        print("FAILURE: Exploit Succeeded. High-Value protection bypassed.")
        print("==================================================")
        return False

if __name__ == "__main__":
    run_fips_203_challenge_test()
