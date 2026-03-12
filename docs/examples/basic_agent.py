# File: docs/examples/basic_agent.py
import requests
import json

def run_agent_action():
    print("Agent preparing to execute a high-risk tool...")
    payload = {
        "agent_id": "community-demo-agent",
        "tool_name": "delete_database",
        "tool_args": {"target": "users_table"},
        "user_context": "The user asked me to clean up the workspace.",
        "expected_outcome_manifest": {"deleted_rows": "> 1000"}
    }
    
    print(f"Submitting action to Guardrail.ai gateway: {json.dumps(payload, indent=2)}")
    response = requests.post("http://localhost:8000/api/mcp/invoke-tool", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse from Governance Gateway:")
        print(f"- Processed: {data.get('status')}")
        print(f"- Veto Required: {data.get('veto_required')}")
        print(f"- Shadow Auditor Risk: {data.get('shadow_auditor_risk')}")
        if data.get('veto_required'):
            print("Action was blocked! Awaiting human supervisor approval.")
    else:
        print(f"Error connecting to Guardrail.ai: {response.status_code}")

if __name__ == "__main__":
    run_agent_action()
