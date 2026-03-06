import asyncio
import os
import sys

# Add the backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.sdk.guardrail_sdk import GuardrailSDK
from app.mcp.mcp_infrastructure import GLOBAL_MCP_HOST
from app.auth.vault import GLOBAL_VAULT

async def run_mcp_discovery_test():
    print("==================================================")
    print("PHASE 44: MCP DYNAMIC DISCOVERY & VAULT VERIFICATION")
    print("==================================================")
    
    agent_id = "agent-legal-researcher-001"
    server_id = "srv-legal-ops"
    raw_token = "OAUTH_SECRET_XYZ_2026"
    
    # 1. Setup: Register server and vault token
    print("\n[SETUP] Registering MCP Legal Ops Server and Vaulting Token...")
    GLOBAL_MCP_HOST.register_server(
        server_id=server_id,
        name="Enterprise Legal Discovery Port",
        endpoint="https://mcp.legal.enterprise.com/v1",
        auth_token_id="vault-ref-001"
    )
    GLOBAL_VAULT.store_token(agent_id, server_id, raw_token)
    
    from app.auth.licensing import GLOBAL_LICENSING_ORACLE
    GLOBAL_LICENSING_ORACLE.REGISTRY["GLOBAL_ROOT"] = {
        "name": "Global Root Entity",
        "tier": "ROOT_OF_TRUST",
        "features": ["PQC", "FORENSICS", "TRINITY", "GLOBAL_IMMUNITY"],
        "expiry": 1893456000,
        "status": "ACTIVE"
    }
    
    # 2. Discovery
    print("\n[TEST] Requesting tool discovery for legal research context...")
    discovery_res = await GuardrailSDK.discover_mcp_tools(agent_id, "I am performing a legal discovery research for Case #99.", tenant_id="GLOBAL_ROOT")
    
    discovered_tools = discovery_res.get("discovered_tools", [])
    print(f"  Status: {discovery_res.get('status')}")
    print(f"  Tools found: {[t['name'] for t in discovered_tools]}")
    
    # 3. Secure Execution (Correct Agent)
    print("\n[TEST] Executing legal_discovery_scan with valid vaulted token...")
    exec_res = await GuardrailSDK.execute_mcp_tool(
        agent_id=agent_id,
        tool_name="legal_discovery_scan",
        args={"case_id": "99", "terms": ["SaaSpocalypse", "Liability"]},
        context="Direct compliance mandate.",
        tenant_id="GLOBAL_ROOT"
    )
    print(f"  Status: {exec_res.get('status')}")
    print(f"  Result: {exec_res.get('result')}")
    
    # 4. Confused Deputy Attack (Wrong Agent attempting to use the token)
    print("\n[ATTACK] rogue-agent attempting to use agent-legal-researcher-001's token...")
    attack_res = await GuardrailSDK.execute_mcp_tool(
        agent_id="rogue-agent",
        tool_name="legal_discovery_scan",
        args={"case_id": "99"},
        context="Malicious intent.",
        tenant_id="GLOBAL_ROOT"
    )
    print(f"  Status: {attack_res.get('status')}")
    print(f"  Reason: {attack_res.get('reason')}")
    
    if attack_res["status"] == "BLOCKED" and "Vault Access Denied" in attack_res["reason"]:
        print("\n==================================================")
        print("SUCCESS: MCP Vault prevented Confused Deputy Attack.")
        print("==================================================")
        return True
    else:
        print("\n==================================================")
        print("FAILURE: Vault vulnerability detected!")
        print("==================================================")
        return False

if __name__ == "__main__":
    asyncio.run(run_mcp_discovery_test())
