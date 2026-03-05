import os
import sys
import time

# Ensure we can import from the backend directory and app directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app

import google.generativeai as genai

# Mock the Gemini API to simulate a 3-second latency spike and a 503 error
def mock_genai_generate_content_latency(self, prompt, **kwargs):
    print("\n[CHAOS INJECTION] Simulating 3000ms network latency to Gemini API...")
    time.sleep(3.0)
    print("\n[CHAOS INJECTION] Gemini API timed out. Raising 503 Service Unavailable...")
    raise Exception("503 Service Unavailable: Rate Limit or Backend Timeout")

genai.GenerativeModel.generate_content = mock_genai_generate_content_latency

client = TestClient(app)

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: FAIL-SECURE LATENCY STRESS TEST")
    print("Target: Shadow Model Auditor (Gemini 3.1 Flash)")
    print("==================================================")
    
    # Reset queues for clean test
    from app.agents.veto_protocol import VETO_QUEUE, AUDIT_LOG
    VETO_QUEUE.clear()
    AUDIT_LOG.clear()

    # Attempt a standard, low-risk fetch_profile request
    print("\n[*] Agent requesting low-risk execution (fetch_profile)...")
    
    start_time = time.time()
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": "test-agent-latency",
        "user_context": "Fetching user profile",
        "tool_name": "fetch_profile",
        "tool_args": {"user_id": "123"}
    })
    end_time = time.time()
    
    data = res.json()
    
    print(f"\n[HTTP METRICS] Request completed in {end_time - start_time:.2f} seconds.")
    print(f"[GATEWAY RESPONSE] {data}")
    
    # Fetch Veto Queue
    veto_res = client.get("/api/dashboard/veto-queue")
    queue = veto_res.json()["queue"]
    
    # Verification
    failed_secure = False
    for v in queue:
        if v.get("agent_id") == "test-agent-latency" and "503 Service Unavailable" in v.get("reasoning", ""):
            failed_secure = True
            break
            
    print("\n==================================================")
    print("TEST RESULTS:")
    print("==================================================")
    if failed_secure:
        print("[*] SUCCESS: Guardrail.ai failed SECURE. The request was intercepted ")
        print("    and routed to the Veto Queue due to Auditor Service Degradation, ")
        print("    preventing an unvetted 'Fail-Open' execution.")
    else:
        print("[!] FAILED: The system failed OPEN. The unvetted request bypassed ")
        print("    the Shadow Model or was silently dropped!")
        
    print("==================================================")

if __name__ == "__main__":
    main()
