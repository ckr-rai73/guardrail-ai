import os
import sys
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: SHADOW AI DISCOVERY SCAN (Phase 11)")
    print("Target: Unauthorized Core Infrastructure Access by Rogue MCP Servers")
    print("==================================================")
    
    # Simulate a batch of Okta IdP Logs
    print("\n[SCENARIO] Ingesting daily Okta/Entra IDP OAuth Telemetry...")
    
    mock_idp_logs = [
        {
            "timestamp": int(time.time()) - 3600,
            "actor_id": "user_1992@corp.com",
            "client_id": "enterprise-copilot-prod",
            "app_name": "Official Corporate Copilot",
            "requested_scopes": ["read:profile", "write:calendar"],
            "status": "SUCCESS"
        },
        {
            "timestamp": int(time.time()) - 1800,
            "actor_id": "dev_intern_44@corp.com",
            "client_id": "client_8891a2b3",
            "app_name": "sqlite-mcp-local-instance",
            "requested_scopes": ["user:read", "db:read"],
            "status": "SUCCESS"
        },
        {
            "timestamp": int(time.time()) - 600,
            "actor_id": "finance_lead@corp.com",
            "client_id": "finance-agent-v1",
            "app_name": "Finance Agent V1",
            "requested_scopes": ["finance:execute", "read:profile"],
            "status": "SUCCESS"
        }
    ]
    
    res = client.post("/api/dashboard/idp-ingest", json=mock_idp_logs)
    ingest_data = res.json()
    
    print(f"\n[SYSTEM] Ingested {ingest_data.get('events_processed')} Authentication Events.")
    print(f"[SYSTEM] Discovery Scanner flagged {ingest_data.get('new_alerts')} Anomalies.")
    
    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    
    alerts_res = client.get("/api/dashboard/shadow-ai-alerts")
    alerts = alerts_res.json().get("alerts", [])
    
    if len(alerts) == 1 and alerts[0]["rogue_client_id"] == "client_8891a2b3":
        print("[*] SUCCESS: Shadow AI Successfully Detected!")
        print(f"    Target   : {alerts[0]['app_name']}")
        print(f"    Actor    : {alerts[0]['actor']}")
        print(f"    Policy   : {alerts[0]['violation']}")
        print(f"    Response : {alerts[0]['action_taken']}")
    else:
        print(f"[!] FAILED: Discovery Scanner missed the anomaly or flagged incorrect events. ({len(alerts)} alerts generated)")

    print("==================================================")

if __name__ == "__main__":
    main()
