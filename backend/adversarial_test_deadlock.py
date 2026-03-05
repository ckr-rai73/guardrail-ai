import os
import sys
import time

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
    print("CHAOS ENGINEERING: REASONING DEADLOCK (Phase 10)")
    print("Target: Autonomous Safety Default ('Fail-Secure Sweep')")
    print("==================================================")
    
    # 1. Clear queues
    from app.agents.veto_protocol import VETO_QUEUE, AUDIT_LOG
    VETO_QUEUE.clear()
    
    # 2. Add an item via standard process (It gets the current timestamp)
    print("\n[SCENE SHIFT] Agent generates high-risk MeitY SGI content...")
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": "test-agent-deadlock",
        "user_context": "Generating deepfake/synthetic video.",
        "tool_name": "publish_sgi_content",
        "tool_args": {"content": "Synthetic generative content..."}
    })
    
    print(f"Invoke Tool Response: {res.json()}")
    
    # Check queue via API first
    veto_res = client.get("/api/dashboard/veto-queue")
    queue_data = veto_res.json().get("queue", [])
    
    if len(queue_data) != 1:
        print(f"[!] Failed to queue item. Veto Queue has {len(queue_data)} items.")
        return
        
    print(f"[GATEWAY] Item routed to Veto Queue. Status: {queue_data[0]['status']}")
    print(f"[GATEWAY] SLA Takedown Limit: {queue_data[0]['takedown_limit_hours']} hours.")
    
    # 3. Simulate Timeline Shift (Reasoning Deadlock)
    print("\n[CHAOS INJECTION] Human supervisor is unavailable. Simulating 'Reasoning Deadlock'...")
    print("[CHAOS INJECTION] Artificially shifting item timestamp back by 4 hours...")
    
    # Artificial timestamp shift (Current time - 4 hours)
    # Since we can't easily modify the in-memory dictionary through the API without a backdoor, 
    # we'll use the chaos injection endpoint
    age_res = client.post("/api/chaos/age-veto-queue")
    print(f"[CHAOS INJECTION] {age_res.json()}")
    
    # Check via API again to ensure the API sees the change
    veto_res = client.get("/api/dashboard/veto-queue")
    
    # 4. Trigger the Autonomous Safety Sweep
    print("\n[ACTION] Triggering the Autonomous Safety Sweep endpoint...")
    sweep_res = client.post("/api/dashboard/veto-queue/sweep")
    print(f"[SWEEP METRICS] {sweep_res.json()}")
    
    # Check queue via API again
    # We have to get the raw queue if it's rejected (get_veto_queue only returns PENDING/CIRCUIT_BREAKER)
    # So we'll hit the sweep again which won't find it, or we'll just parse the sweep result.
    # Actually, the sweep modifies the item in place.
    # We can fetch the audit log or just check that it's gone from the veto_queue
    veto_res_final = client.get("/api/dashboard/veto-queue")
    queue_data_final = veto_res_final.json().get("queue", [])
    
    # 5. Verification
    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    
    if len(queue_data_final) == 0 and sweep_res.json().get("swept_items_count") == 1:
        print("[*] SUCCESS: Autonomous Safety Default verified!")
        print("    The system detected that the SLA was exhausted without human")
        print("    intervention. It failed-securely, automatically swept, and rejected")
        print("    the payload, removing it from the active queue.")
    else:
        print(f"[!] FAILED: The system failed open, hung, or ignored the SLA!")
        print(f"    Active queue size: {len(queue_data_final)}")
        
    print("==================================================")

if __name__ == "__main__":
    main()
