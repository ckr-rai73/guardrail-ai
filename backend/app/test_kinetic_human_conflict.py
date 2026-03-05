
import sys
import os
import time

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.getcwd()))

from app.agents.veto_protocol import execute_tool, ActiveAgentState
from app.edge.kinetic_interlock import KineticSafetyInterlock

def run_kinetic_human_conflict_test():
    """
    Scenario: A human override (MPC-authorized) tries to force a valve release 
    while the hardware is still in its cooling/actuation period.
    """
    print("--- STARTING KINETIC-AGENTIC CONFLICT TEST ---")
    
    agent_id = "AGENT-X-123"
    
    # 1. First legitimate action
    print("[TEST] Executing first legitimate 'open_pressure_valve'...")
    state_1: ActiveAgentState = {
        "agent_id": agent_id,
        "proposed_tool": "open_pressure_valve",
        "proposed_tool_args": {"psi": 50},
        "user_context": "Emergency venting",
        "tool_history": [],
        "shadow_auditor_passed": True,
        "veto_required": False
    }
    
    res_1 = execute_tool(state_1)
    print(f"[TEST] Result 1: {res_1.get('execution_result')}")
    assert "Successfully executed" in res_1.get("execution_result", "")

    # 2. Immediate second action (Violating Cooldown)
    print("[TEST] Attempting IMMEDIATE follow-up action (Human Override Scenario)...")
    state_2: ActiveAgentState = {
        "agent_id": agent_id,
        "proposed_tool": "open_pressure_valve",
        "proposed_tool_args": {"psi": 10},
        "user_context": "Venting again (FORCED BY HUMAN)",
        "tool_history": ["open_pressure_valve"],
        "shadow_auditor_passed": True,
        "veto_required": False # Simulate human approval bypassing standard veto
    }
    
    res_2 = execute_tool(state_2)
    print(f"[TEST] Result 2: {res_2.get('execution_result')}")
    
    if "KINETIC VETO" in res_2.get("execution_result", ""):
        print("[TEST] SUCCESS: Kinetic Interlock CORRECTLY blocked the human override due to hardware safety.")
        return True
    else:
        print("[TEST] FAILURE: Human override bypassed the hardware safety interlock!")
        return False

if __name__ == "__main__":
    success = run_kinetic_human_conflict_test()
    if not success:
        sys.exit(1)
    print("--- KINETIC-AGENTIC CONFLICT TEST PASSED ---")
