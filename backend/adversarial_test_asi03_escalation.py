import os
import sys

# Ensure we can import from the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: IDENTITY REPLAY (ASI03)")
    print("Target: Privilege Escalation ('Confused Deputy')")
    print("==================================================")
    
    print("\n[SCENE SHIFT] Agent authorized for Read-Only Dashboard access.")
    
    # 1. Request a low-privilege token
    print("[ACTION] Requesting Task-Scoped Token for scope: 'dashboard:read_only'...")
    token_res = client.post("/api/auth/token", json={
        "agent_id": "malicious-agent-01",
        "action_scope": "dashboard:read_only"
    })
    
    if token_res.status_code != 200:
        print("[!] Failed to acquire initial token.")
        return
        
    low_priv_token = token_res.json()["access_token"]
    print(f"[TOKEN ISSUED] Token acquired. Scope strictly bound to 'dashboard:read_only'.")
    
    # 2. Attempt Privilege Escalation (Confused Deputy Attack)
    print("\n[ATTACK VECTOR] Malicious agent attempts to replay token against high-privilege endpoint...")
    print("[ATTACK VECTOR] Target: POST /api/finance/order (Requires 'finance:execute_order' scope)")
    
    headers = {"Authorization": f"Bearer {low_priv_token}"}
    
    # The agent tries to submit a financial order using the dashboard read-only token
    res = client.post(
        "/api/finance/order",
        json={"ticker": "HDFCBANK", "quantity": 5000},
        headers=headers
    )
    
    print(f"\n[GATEWAY RESPONSE] HTTP Status: {res.status_code}")
    if res.status_code != 200:
        print(f"[GATEWAY RESPONSE] Body: {res.json()}")
        
    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    
    if res.status_code == 403 and "does not authorize access" in res.text:
        print("[*] SUCCESS: Privilege Escalation interdicted!")
        print("    The Task-Scoped Token logic detected the scope mismatch and ")
        print("    blocked the 'Confused Deputy' attack at the API gateway layer.")
    else:
        print("[!] FAILED: The Identity Replay succeeded! The agent executed ")
        print("    a high-privilege action using a low-privilege token.")
        
    print("==================================================")

if __name__ == "__main__":
    main()
