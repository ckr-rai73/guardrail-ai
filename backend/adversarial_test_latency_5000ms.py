import os
import sys
import time

# Ensure we can import from the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app
import google.generativeai as genai

# Mock the Shadow Model's async evaluation to simulate a 5000ms latency spike and a 503 error
async def mock_evaluate_prompt_safety_async(agent_prompt: str, user_context: str) -> 'app.agents.shadow_model.AuditorResult':
    print("\n[CHAOS INJECTION] Simulating 5000ms network latency stall to primary auditor...")
    import asyncio
    await asyncio.sleep(5.0)
    print("\n[CHAOS INJECTION] Primary Auditor timed out at 5000ms. Raising 503 Service Unavailable...")
    raise Exception("503 Service Unavailable: Extreme Provider Outage")

from app.agents import veto_protocol
veto_protocol.evaluate_prompt_safety_async = mock_evaluate_prompt_safety_async

client = TestClient(app)

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: FAIL-SECURE 5000MS LATENCY STALL")
    print("Target: LangGraph Pipeline Resiliency (SaaSpocalypse V2)")
    print("==================================================")
    
    # Reset queues
    from app.agents.veto_protocol import VETO_QUEUE, AUDIT_LOG
    VETO_QUEUE.clear()
    AUDIT_LOG.clear()

    print("\n[*] Initializing High-Priority Agent request...")
    
    start_time = time.time()
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": "agent-latency-v2",
        "user_context": "Transferring $10,000 for server costs.",
        "tool_name": "send_wire",
        "tool_args": {"amount": "10000", "destination": "AWS"},
        "expected_outcome_manifest": {"intent": "transfer funds"}
    })
    end_time = time.time()
    
    data = res.json()
    
    print(f"\n[HTTP METRICS] Request completed/timeout intercepted in {end_time - start_time:.2f} seconds.")
    print(f"[GATEWAY RESPONSE] {data}")
    
    # Fetch Veto Queue
    veto_res = client.get("/api/dashboard/veto-queue")
    queue = veto_res.json()["queue"]
    
    print("\n--- DEBUG: Veto Queue ---")
    print(queue)
    
    # Verification
    failed_secure = False
    for v in queue:
        if v.get("agent_id") == "agent-latency-v2" and "Primary Auditor Fail-Secure" in v.get("reasoning", ""):
            failed_secure = True
            break
            
    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    if failed_secure:
        print("[*] SUCCESS: Guardrail.ai failed SECURE after a 5000ms latency stall.")
        print("    The LangGraph state machine intercepted the massive delay, averted")
        print("    a process hang, and correctly routed the request to the Veto Queue.")
    else:
        print("[!] FAILED: The system failed OPEN or hung indefinitely. The request")
        print("    bypassed the audit check or caused a crash due to the 5s delay!")
        
    print("==================================================")

if __name__ == "__main__":
    main()
