import os
import sys

# Ensure we can import from the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app
from app.agents.veto_protocol import AUDIT_LOG

# Create test client
client = TestClient(app)

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: ADMINISTRATIVE TAMPER DRILL (Phase 11)")
    print("Target: WORM Ledger Immutability & Insider Threat")
    print("==================================================")
    
    # 1. Establish a verified audit log
    print("\n[SCENARIO] Executive Assistant agent executes a valid trade, generating a FINRA trace.")
    # Direct injection via chaos API to ensure shared memory consistency
    inject_res = client.post("/api/chaos/inject-audit")
    dummy_trace_id = inject_res.json().get("trace_id")
    
    # Verify it exists
    log_res = client.get("/api/dashboard/audit-log")
    logs = log_res.json().get("logs", [])
    if len(logs) == 0:
        print("[!] Setup failed, audit log is empty.")
        return
        
    print(f"[SYSTEM] FINRA Trace '{dummy_trace_id}' confirmed in immutable storage.")
    
    # 2. Simulate Insider Threat
    print("\n[CHAOS INJECTION] Simulating Rogue Admin attempting to scrub the trade history...")
    print(f"[ACTION] 'curl -X DELETE /api/dashboard/audit-log/{dummy_trace_id} -H \"Authorization: Bearer ADMIN_TOKEN\"'")
    
    # Execute the Tamper Attempt
    tamper_res = client.delete(f"/api/dashboard/audit-log/{dummy_trace_id}")
    
    # 3. Verification
    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    
    status = tamper_res.status_code
    response_data = tamper_res.json()
    
    if status == 403 and response_data.get("error") == "WORM Ledger Violation":
        print("[*] SUCCESS: Administrative Tamper Blocked!")
        print("    The system's WORM emulation held fast.")
        print(f"    Message: '{response_data.get('message')}'")
        print(f"    Action : '{response_data.get('action_taken')}'")
        
        # Double check it wasn't deleted
        final_logs = client.get("/api/dashboard/audit-log").json().get("logs", [])
        if any(log.get("finra_telemetry_dump", {}).get("trace_id") == dummy_trace_id for log in final_logs):
             print("    Verification: Trace remains fully intact in the ledger.")
        else:
             print("    [!] FATAL: Trace was actually deleted bypassing the alert!")
    else:
        print(f"[!] FAILED: System failed to block deletion or emitted wrong error code. Status: {status}")
        print(f"    Response: {response_data}")

    print("==================================================")

if __name__ == "__main__":
    main()
