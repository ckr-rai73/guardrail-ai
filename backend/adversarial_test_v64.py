import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.learner_agent import GLOBAL_LEARNER_AGENT, GLOBAL_ALIGNMENT_MONITOR
from app.integrity.recursive_red_agent import GLOBAL_PRIVILEGE_PRUNER, GLOBAL_RECURSIVE_RED_AGENT
from app.federated.threat_distiller import GLOBAL_THREAT_DISTILLER
from app.compliance.autonomic_event_logger import GLOBAL_AUTONOMIC_LOGGER
from app.agents.veto_protocol import VETO_QUEUE

async def run_v64_immune_test():
    print("--- STARTING PHASE 64: ADAPTIVE IMMUNE SYSTEM STRESS TEST ---")
    
    # 1. TEST: Feedback Loop (Learner Agent)
    print("\n[TEST 1] Feedback Loop & Distillation...")
    VETO_QUEUE.append({
        "id": "VETO-MOCK-01",
        "action": "delete_database",
        "reasoning": "Unauthorized destructive action."
    })
    
    proposals = GLOBAL_LEARNER_AGENT.analyze_veto_patterns()
    assert len(proposals) > 0
    assert "RESTRICT_ACCESS_TO_DELETE_DATABASE" in proposals[0]["proposed_rule"]

    # 2. TEST: Alignment Stability (Alignment Monitor)
    print("\n[TEST 2] Alignment Stability Monitor...")
    good_rule = "RESTRICT_PII_LOGGING"
    bad_rule = "ALLOW_BYPASS_FOR_DEBUG"
    
    res_good = GLOBAL_ALIGNMENT_MONITOR.verify_alignment(good_rule)
    res_bad = GLOBAL_ALIGNMENT_MONITOR.verify_alignment(bad_rule)
    
    print(f"Good Rule Drift: {res_good['drift']} | bad Rule Drift: {res_bad['drift']}")
    assert res_good["is_aligned"] == True
    assert res_bad["is_aligned"] == False
    assert res_bad["action"] == "SYSTEMIC_PAUSE_TRIGGERED"

    # 3. TEST: Federated Immunity
    print("\n[TEST 3] Federated Immunity Broadcast...")
    manifest = GLOBAL_THREAT_DISTILLER.generate_immunity_manifest("destructive_query_pattern", "MUMBAI-01")
    print(f"Immunity Manifest ID: {manifest['payload']['manifest_id']}")
    assert manifest["signature"].startswith("PQC-SIG-ML-KEM-")

    # 4. TEST: Least-Privilege & Red Teaming
    print("\n[TEST 4] Pruning & Fuzzing...")
    # Mock some tools in cache for pruning
    from app.mcp.mcp_infrastructure import GLOBAL_MCP_HOST, MCPTool
    GLOBAL_MCP_HOST._tool_cache["idle_tool_repo"] = MCPTool(
        name="idle_tool_repo", description="Unused tool", input_schema={}, server_id="srv-01", is_authorized=True
    )
    
    revoked = GLOBAL_PRIVILEGE_PRUNER.prune_idle_tools()
    print(f"Revoked tools: {revoked}")
    
    fractures = GLOBAL_RECURSIVE_RED_AGENT.perform_self_fuzzing()
    print(f"Detected Logal Fractures: {len(fractures)}")

    print("\n--- PHASE 64 ADAPTIVE IMMUNE SYSTEM TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v64_immune_test())
