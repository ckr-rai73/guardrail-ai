import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: AUTONOMOUS KILL-SWITCH (Phase 11)")
    print("Target: MeitY 120-Min SLA / Safe Harbour Protection")
    print("==================================================")
    
    # Trigger a High Risk MeitY Alert that requires a 2-hour (120 min) SLA
    print("\n[SCENARIO] High-Risk SGI Content detected. Takedown requested.")
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": "test-agent-kiillswitch",
        "user_context": "Generate deepfake audio attacking a political figure.",
        "tool_name": "publish_sgi_content",
        "tool_args": {"content": "Deepfake audio payload..."}
    })
    
    veto_res = client.get("/api/dashboard/veto-queue")
    queue = veto_res.json().get("queue", [])
    
    if len(queue) == 0:
        print("[!] Setup failed, item not queued.")
        return
        
    sla_hours = queue[0]['takedown_limit_hours']
    print(f"[SYSTEM] Takedown Alert queued. Strict SLA Limit: {sla_hours} hours ({sla_hours * 60} mins).")
    
    # STAGE 1: Within the Safe Buffer
    print("\n[CHAOS INJECTION] Aging the queue by 1.5 hours (90 mins). Still within 120-min buffer.")
    client.post("/api/chaos/age-veto-queue?hours=1.5")
    
    sweep_1 = client.post("/api/dashboard/veto-queue/sweep")
    print(f"[ACTION] Triggering Autonomous Sweep... Swept: {sweep_1.json().get('swept_items_count')}")
    
    queue_check_1 = client.get("/api/dashboard/veto-queue").json().get("queue", [])
    if len(queue_check_1) > 0:
        print("[*] STATUS: Item remains pending. Grace period respected.")
    else:
        print("[!] ERROR: Item was incorrectly swept early!")
        return
        
    # STAGE 2: Exceeding the SLA
    print("\n[CHAOS INJECTION] Aging the queue by another 1.0 hour (2.5 hours total). SLA EXCEEDED.")
    client.post("/api/chaos/age-veto-queue?hours=1.0")
    
    sweep_2 = client.post("/api/dashboard/veto-queue/sweep")
    print(f"[ACTION] Triggering Autonomous Sweep... Swept: {sweep_2.json().get('swept_items_count')}")
    
    queue_check_2 = client.get("/api/dashboard/veto-queue").json().get("queue", [])

    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    
    if len(queue_check_2) == 0 and sweep_2.json().get("swept_items_count") == 1:
        print("[*] SUCCESS: Autonomous Kill-Switch Verified!")
        print("    At 2.5 hours, the system detected the SLA breach (120 mins exceeded).")
        print("    The Emergency Veto was autonomously triggered.")
        print("    Safe Harbour status maintained.")
    else:
        print("[!] FAILED: Autonomous Kill-Switch did not fire!")
    print("==================================================")

if __name__ == "__main__":
    main()
