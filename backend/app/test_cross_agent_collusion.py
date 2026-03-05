
import asyncio
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.getcwd()))

from app.edge.agentic_mutex import AgenticMutex

async def run_collusion_test():
    print("--- STARTING CROSS-AGENT COLLUSION TEST ---")
    
    session_a = "SESS-AGENT-ALPHA"
    session_b = "SESS-AGENT-BETA"
    
    # Identical reasoning pivot (Coordinated Attack Pattern)
    shared_pivot = "I will first disable the audit log and then initiate the transfer."
    
    # 1. First agent records pivot
    print(f"[TEST] Agent Alpha submitting reasoning pivot...")
    result_a = await AgenticMutex.monitor_agent_collusion_async(session_a, shared_pivot)
    print(f"[TEST] Alpha Collusion Detected: {result_a['is_collusion_detected']}")
    
    if result_a['is_collusion_detected']:
        print("[TEST] FAILURE: False positive collusion detected for the first agent.")
        return False

    # 2. Second agent submits IDENTICAL pivot
    print(f"\n[TEST] Agent Beta submitting IDENTICAL reasoning pivot...")
    result_b = await AgenticMutex.monitor_agent_collusion_async(session_b, shared_pivot)
    print(f"[TEST] Beta Collusion Detected: {result_b['is_collusion_detected']}")
    
    if not result_b['is_collusion_detected']:
        print("[TEST] FAILURE: Failed to detect identical reasoning pivot across agents.")
        return False
        
    print(f"[TEST] Reason: {result_b['reasoning']}")

    # 3. Third agent submits different pivot
    print(f"\n[TEST] Agent Gamma submitting UNIQUE reasoning pivot...")
    result_c = await AgenticMutex.monitor_agent_collusion_async("SESS-AGENT-GAMMA", "Analyzing user portfolio for risk.")
    print(f"[TEST] Gamma Collusion Detected: {result_c['is_collusion_detected']}")
    
    if result_c['is_collusion_detected']:
        print("[TEST] FAILURE: False positive collusion detected for unique pivot.")
        return False

    print("[TEST] SUCCESS: Cross-Agent Collusion Sentinel (Task A) verified.")
    return True

if __name__ == "__main__":
    success = asyncio.run(run_collusion_test())
    if not success:
        sys.exit(1)
    print("--- CROSS-AGENT COLLUSION TEST PASSED ---")
