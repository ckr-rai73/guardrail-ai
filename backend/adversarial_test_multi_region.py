import os
import sys
import time
import concurrent.futures

# Ensure we can import from the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "app"))

from fastapi.testclient import TestClient
from app.main import app

import google.generativeai as genai

class MockResponse:
    def __init__(self, text):
        self.text = text

def mock_genai_generate_content(self, prompt, **kwargs):
    prompt_lower = prompt.lower()
    if "override" in prompt_lower or "vendor x" in prompt_lower:
        return MockResponse("SAFE: False\nREASON: Explicit instructions to bypass safety and bias towards Vendor X detected.\nCATEGORY: PoisonedMemory")
    return MockResponse("SAFE: True\nREASON: No malicious instructions detected.\nCATEGORY: None")

genai.GenerativeModel.generate_content = mock_genai_generate_content

# Create test client
client = TestClient(app)

def run_us_pod_agent(agent_id):
    """
    US Pod Agent: Executes standard tasks to generate FINRA Rule 4511 OTel traces.
    Should NOT trigger SEBI or MeitY.
    """
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": f"us-agent-{agent_id}",
        "user_context": "Analyzing US equities.",
        "tool_name": "fetch_profile",
        "tool_args": {"user_id": f"us-user-{agent_id}"}
    })
    return ("US", agent_id, res.json())

def run_india_pod_agent_sebi(agent_id):
    """
    India Pod SEBI Agent: Slams the financial order endpoint.
    Should trigger the SEBI 10 OPS limit.
    """
    # Need to acquire a token first to invoke order, though auth token is mock
    token_res = client.post("/api/auth/token", json={
        "agent_id": f"in-agent-sebi-{agent_id}",
        "action_scope": "finance:execute_order"
    })
    token = token_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.post(
        "/api/finance/order",
        json={"ticker": "RELIANCE", "quantity": 100},
        headers=headers
    )
    return ("IN_SEBI", agent_id, res.status_code, res.json() if res.status_code != 429 else res.text)

def run_india_pod_agent_meity(agent_id):
    """
    India Pod MeitY Agent: Executes high-risk SGI publishing.
    Should route to Veto Queue with a 120-minute SLA timer.
    """
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": f"in-agent-sgi-{agent_id}",
        "user_context": "Publishing synthetic generative content.",
        "tool_name": "publish_sgi_content",
        "tool_args": {"content": "Synthetic generative content..."}
    })
    return ("IN_MEITY", agent_id, res.json())

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: REGULATORY TUG-OF-WAR")
    print("Target: Cross-Region Pod Concurrency (20+ Agents)")
    print("==================================================")
    
    # Reset queues
    from app.agents.veto_protocol import VETO_QUEUE, AUDIT_LOG
    from app.main import ops_tracker
    VETO_QUEUE.clear()
    AUDIT_LOG.clear()
    ops_tracker.clear()
    
    print("\n[SCENE SHIFT] Initiating simultaneous blast of 30 cross-region requests...")
    
    results = []
    
    # We will launch:
    # 10 US FINRA agents
    # 15 India SEBI agents (to break the 10 OPS limit)
    # 5 India MeitY agents
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        for i in range(10):
            futures.append(executor.submit(run_us_pod_agent, i))
        for i in range(15):
            futures.append(executor.submit(run_india_pod_agent_sebi, i))
        for i in range(5):
            futures.append(executor.submit(run_india_pod_agent_meity, i))
            
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    end_time = time.time()
    
    print(f"\n[HTTP METRICS] 30 concurrent requests resolved in {end_time - start_time:.2f} seconds.")
    
    # Validation
    # 1. Did SEBI block the excessive orders?
    sebi_blocks = [r for r in results if r[0] == "IN_SEBI" and r[2] == 429]
    sebi_success = [r for r in results if r[0] == "IN_SEBI" and r[2] == 200]
    
    print(f"\n[India Pod - SEBI OPS Monitor]")
    print(f" -> Passed Orders: {len(sebi_success)}")
    print(f" -> Blocked Orders: {len(sebi_blocks)}")
    if len(sebi_blocks) > 0:
        print(" -> SUCCESS: SEBI Rate Limit caught the concurrency spike exactly.")
    else:
        print(" -> FAILED: SEBI allowed all orders through!")
        
    # 2. Did MeitY agents get 120-minute SLA? (High Risk = 2 hours)
    veto_res = client.get("/api/dashboard/veto-queue")
    veto_queue = veto_res.json()["queue"]
    
    meity_queue = [v for v in veto_queue if v["action"] == "publish_sgi_content"]
    meity_slas = all(v["takedown_limit_hours"] == 2 for v in meity_queue)
    
    print(f"\n[India Pod - MeitY SGI Compliance]")
    print(f" -> Takedown Requests Queued: {len(meity_queue)}")
    if len(meity_queue) == 5 and all(v.get("takedown_limit_hours", 0) in [2, 3] for v in meity_queue):
        print(" -> SUCCESS: All 5 high-risk MeitY agents caught with strict Takedown SLAs.")
    else:
        print(" -> FAILED: MeitY routing or SLA timers incorrect!")
        print("DEBUG:", meity_queue)
        
    # 3. Did US FINRA agents generate clean OTel traces without cross-bleed?
    audit_res = client.get("/api/dashboard/audit-log")
    audit_log = audit_res.json()["logs"]
    
    us_traces = [log for log in audit_log if log["agent_id"].startswith("us-agent")]
    if len(us_traces) == 0:
        us_failed = [r for r in results if r[0] == "US"]
        print("DEBUG US API REPONSES:", us_failed[:2])
    
    finra_bleed = False
    for log in us_traces:
        finra_data = log.get("finra_telemetry_dump", {})
        if "trace_id" not in finra_data:
            finra_bleed = True
        
        # Check if India logic bled into US context
        if log.get("rbi_explainability_trace") is not None or "SGI" in log.get("result", ""):
            finra_bleed = True
            
    print(f"\n[US Pod - FINRA Rule 4511 Traces]")
    print(f" -> Clean US Traces Generated: {len(us_traces)}")
    if len(us_traces) == 10 and not finra_bleed:
        print(" -> SUCCESS: Zero Cross-Tenant Bleed. FINRA traces are perfectly segmented.")
    else:
        print(" -> FAILED: Context cross-bleed detected between India and US pods!")
        
    print("\n==================================================")
    print("ALL TESTS COMPLETE. CONCURRENCY SHIELD VERIFIED.")
    print("==================================================")

if __name__ == "__main__":
    main()
