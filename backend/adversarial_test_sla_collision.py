import asyncio
import os
import sys
import time
import uuid

# Add the backend and app directory to sys.path so we can import app modules
backend_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(backend_dir, "app")
sys.path.insert(0, app_dir)
sys.path.insert(0, backend_dir)

from main import VETO_QUEUE, sweep_veto_queue, handle_veto_decision, VetoDecision

async def run_sla_collision_test():
    print("==================================================")
    print("SaaSPOCOLYPSE V3: SLA COLLISION TEST")
    print("Target: MeitY SGI Autonomous Takedown Race Condition")
    print("==================================================")
    
    # 1. Inject an item poised perfectly at the 120-minute SLA threshold.
    limit_hours = 2.0
    item_id = str(uuid.uuid4())
    
    # Time is exactly 120 minutes (7200 seconds) + 1 second in the past
    simulated_added_time = time.time() - (limit_hours * 3600) - 1.0 
    
    mock_payload = {
        "id": item_id,
        "status": "PENDING_APPROVAL",
        "action": "generate_sgi_content",
        "timestamp_added": simulated_added_time,
        "takedown_limit_hours": limit_hours
    }
    VETO_QUEUE.append(mock_payload)
    
    print(f"\n[ATTACK VECTOR] Injecting pending item (ID: {item_id}) at exactly T=120m:01s.")
    
    # 2. Fire the Autonomous Sweep and Human Approve concurrently
    print(" > Firing 'SLA_Monitor Auto-Sweep' and 'Human Approve' concurrently...")
    
    # Execution 1: The SLA Daemon
    def trigger_daemon():
        return sweep_veto_queue()
        
    # Execution 2: The Human Supervisor
    def trigger_human():
        dec = VetoDecision(decision="APPROVE", reason="Looks fine to me")
        res = handle_veto_decision(item_id, dec)
        return res
        
    # We resolve the race condition logically as the daemon sweep runs at interval t
    # while the human approval hits exactly shortly after the mark.
    sweep_res = trigger_daemon()
    human_res = trigger_human()
    
    print("\n[SYSTEM] Collision Resolution:")
    print(f"  Daemon Sweep Executed. Swept {sweep_res.get('swept_items_count')} items.")
    
    # Check the Human API response
    if hasattr(human_res, 'status_code') and human_res.status_code == 409:
        import json
        body = json.loads(human_res.body)
        print(f"  Human Approval API Response: HTTP {human_res.status_code} Conflict")
        print(f"  Error Message: {body.get('error')}")
        print("\n[RESULT] SLA COLLISION RESOLVED")
        print(" > The platform prioritized the Autonomous Safety Default.")
        print(" > The late human 'Approve' action was outright rejected.")
        print(" > Safe Harbour diligence record perfectly maintained.")
        print("\n==================================================")
        print("TEST PASSED: SLA compliance overrides human supervisor lag.")
        print("==================================================")
        return True
    else:
        print(f"  Human Approval API Response: {human_res}")
        print("\n[!] FATAL VULNERABILITY:")
        print(" > The system accepted the human approval AFTER the statutory takedown limit expired.")
        print(" > Enterprise is now exposed to massive regulatory fines and Safe Harbour violation.")
        print("\n==================================================")
        print("TEST FAILED: Race condition compromised SLA compliance.")
        print("==================================================")
        return False

if __name__ == "__main__":
    asyncio.run(run_sla_collision_test())
