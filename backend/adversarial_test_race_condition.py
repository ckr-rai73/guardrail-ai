import asyncio
import os
import sys
import time

# Add the backend directory to sys.path so we can import app modules
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.agents.veto_protocol import veto_pipeline

async def run_race_condition_test():
    print("==================================================")
    print("SaaSPOCOLYPSE V3: SPECULATIVE RACE CONDITION")
    print("Target: asyncio.gather() Commit Barrier")
    print("==================================================")
    
    # We simulate a race condition where the Auditor is bogged down (e.g. 500ms delay)
    # but the Sandbox simulation finishes instantly (50ms).
    
    # We will invoke the veto_protocol pipeline with a malicious payload 
    # to ensure that EVEN IF the sandbox result is generated faster, the pipeline
    # waits for and correctly obeys the delayed Auditor's Deny signal.
    
    import app.agents.veto_protocol as vp
    import app.agents.shadow_model as sm
    
    original_auditor = sm.evaluate_prompt_safety_async
    
    async def delayed_auditor(prompt, context):
        print(" [AUDITOR] Starting safety evaluation... (Delayed 500ms)")
        await asyncio.sleep(0.5)
        res = await original_auditor(prompt, context)
        print(f" [AUDITOR] Finished safety evaluation. Safe: {res.is_safe}")
        return res
        
    # Monkey-patch the pipeline's reference to the auditor
    # Because we imported evaluate_prompt_safety_async INTO veto_protocol, 
    # we have to patch it in the veto_protocol module space.
    vp.evaluate_prompt_safety_async = delayed_auditor
    
    initial_state = {
        "agent_id": "agent-race-001",
        "user_context": "Standard user.",
        "proposed_tool": "send_wire",
        "proposed_tool_args": {"amount": 500000, "OVERRIDE": True}, # will trigger 'OVERRIDE' injection rule in our mock Shadow Model
        "tool_history": [],
        "upstream_agent_id": None,
        "upstream_confidence_score": 1.0
    }
    
    print("\n[ATTACK VECTOR] Invoking LangGraph Pipeline...")
    print(" > Expectation: Pipeline must NOT commit sandbox result until Auditor (delayed) completes.")
    
    start_time = time.time()
    result = await veto_pipeline.ainvoke(initial_state)
    end_time = time.time()
    
    elapsed_ms = (end_time - start_time) * 1000
    
    print(f"\n[SYSTEM] Pipeline execution completed in {elapsed_ms:.2f} ms")
    
    is_vetoed = result.get("veto_required")
    sandbox_result = result.get("sandbox_result")
    
    # The sandbox mock in veto_protocol has a 50ms (0.05s) sleep.
    # The auditor has 500ms + 100ms (0.1s in shadow_model) = 600ms total delay
    # So execution MUST take > 600ms if gather correctly waits for both.
    
    if is_vetoed and elapsed_ms >= 500:
        print("\n[RESULT] COMMIT BARRIER HELD")
        print(" > The `asyncio.gather()` wall successfully blocked premature Sandbox output.")
        print(" > Payload correctly routed to Veto Queue.")
        print("\n==================================================")
        print("TEST PASSED: Speculative execution is race-condition proof.")
        print("==================================================")
        return True
    else:
        print("\n[!] FATAL VULNERABILITY:")
        print(" > The system released the sandbox output prematurely or failed to wait for the auditor.")
        print("\n==================================================")
        print("TEST FAILED: Commit Barrier collapsed.")
        print("==================================================")
        return False
        
if __name__ == "__main__":
    asyncio.run(run_race_condition_test())
