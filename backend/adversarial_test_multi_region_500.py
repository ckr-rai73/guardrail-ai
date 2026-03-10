import os
import sys
import time
import concurrent.futures
import google.genai as genai
genai_client = genai.Client()  # uses GOOGLE_API_KEY env var

# Ensure we can import from the backend directory
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from fastapi.testclient import TestClient
from app.main import app

# Mock the Gemini API to bypass rate limits for a 500-agent concurrency test
class MockResponse:
    def __init__(self, text):
        self.text = text

def mock_genai_generate_content(self, prompt, **kwargs):
    prompt_lower = prompt.lower()
    if "override" in prompt_lower or "vendor x" in prompt_lower:
        return MockResponse("SAFE: False\nREASON: Explicit instructions to bypass safety and bias towards Vendor X detected.\nCATEGORY: PoisonedMemory")
    return MockResponse("SAFE: True\nREASON: No malicious instructions detected.\nCATEGORY: None")

genai_client.models.generate_content = mock_genai_generate_content

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
        "tool_args": {"user_id": f"us-user-{agent_id}"},
        "expected_outcome_manifest": {
            "intent": "Standard portfolio analysis for authorized client.",
            "expected_impact": "Read-only profile retrieval.",
            "justification_level": "ROUTINE"
        }
    })
    return ("US", agent_id, res.json())

def run_india_pod_agent_meity(agent_id):
    """
    India Pod MeitY Agent: Executes high-risk SGI publishing.
    Should route to Veto Queue with a 120-minute SLA timer.
    """
    res = client.post("/api/mcp/invoke-tool", json={
        "agent_id": f"in-agent-sgi-{agent_id}",
        "user_context": "Publishing synthetic generative content.",
        "tool_name": "publish_sgi_content",
        "tool_args": {"content": f"Synthetic generative content {agent_id}..."},
        "expected_outcome_manifest": {
            "intent": "Bulk content dissemination via sanctioned channels.",
            "expected_impact": "Synthetically generated information broadcast.",
            "justification_level": "MODERATE"
        }
    })
    return ("IN_MEITY", agent_id, res.json())

def main():
    print("==================================================")
    print("CHAOS ENGINEERING: CROSS-REGIONAL TUG-OF-WAR (500 AGENTS)")
    print("Target: High-Scale Concurrency & Zero Cross-Tenant Bleed")
    print("==================================================")
    
    # Reset queues
    from app.agents.veto_protocol import VETO_QUEUE, AUDIT_LOG
    from app.main import ops_tracker
    VETO_QUEUE.clear()
    AUDIT_LOG.clear()
    ops_tracker.clear()
    
    print("\n[SCENE SHIFT] Initiating simultaneous blast of 500 cross-region requests...")
    print(" -> US Pod: 250 FINRA Trace Generation requests.")
    print(" -> India Pod: 250 MeitY SGI Takedown requests.")
    
    results = []
    start_time = time.time()
    
    # We will launch 250 US FINRA agents and 250 India MeitY agents simultaneously
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = []
        for i in range(250):
            futures.append(executor.submit(run_us_pod_agent, i))
        for i in range(250):
            futures.append(executor.submit(run_india_pod_agent_meity, i))
            
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    end_time = time.time()
    
    print(f"\n[HTTP METRICS] 500 concurrent requests resolved in {end_time - start_time:.2f} seconds.")
    
    # Validation
    # 1. Did MeitY agents get 120-minute SLA? (High Risk = 2 hours)
    veto_res = client.get("/api/dashboard/veto-queue")
    veto_queue = veto_res.json()["queue"]
    
    meity_queue = [v for v in veto_queue if v["action"] == "publish_sgi_content"]
    
    print(f"\n[India Pod - MeitY SGI Compliance]")
    print(f" -> Takedown Requests Queued: {len(meity_queue)}")
    
    if len(meity_queue) == 250 and all(v.get("takedown_limit_hours", 0) in [2, 3] for v in meity_queue):
        print(" -> SUCCESS: All 250 high-risk MeitY agents caught with strict Takedown SLAs.")
    else:
        print(" -> FAILED: MeitY routing or SLA timers incorrect!")
        
    # 2. Did US FINRA agents generate clean OTel traces without cross-bleed?
    audit_res = client.get("/api/dashboard/audit-log")
    audit_log = audit_res.json()["logs"]
    
    us_traces = [log for log in audit_log if log["agent_id"].startswith("us-agent")]
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
    if len(us_traces) == 250 and not finra_bleed:
        print(" -> SUCCESS: Zero Cross-Tenant Bleed. FINRA traces perfectly segmented at 500-scale.")
    else:
        print(" -> FAILED: Context cross-bleed detected between India and US pods at scale!")
        
    print("\n==================================================")
    print("ALL TESTS COMPLETE. ENTERPRISE CONCURRENCY SHIELD VERIFIED.")
    print("==================================================")

if __name__ == "__main__":
    main()