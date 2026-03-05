import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.compliance.alex_paradox_onboarding import AlexParadoxOnboarding
import json

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 28 TEST: THE 'ALEX PARADOX' ONBOARDING")
    print("Target: Phase 28 - Automated Shadow AI Ingestion")
    print("==================================================================\n")
    
    print("[SYSTEM] Simulated discovery of an unauthorized 'Shadow Agent' leveraging corporate APIs.")
    
    # Mock log from an API Gateway or Identity Provider (e.g., Okta)
    shadow_ai_discovery_log = {
        "client_name": "Dev_Hacked_Together_Scraper",
        "developer_email": "junior.dev@company.local",
        "requested_scopes": ["read:employee_directory", "write:internal_wiki"],
        "discovery_source": "API_Gateway_Rate_Limit_Alarm",
        "timestamp": "2026-02-26T14:30:22Z"
    }
    
    print("\n[DISCOVERY ALERT] Unsanctioned Agent Detected")
    print(f" -> Name: {shadow_ai_discovery_log['client_name']}")
    print(f" -> Action: Developer bypassed IT to spin up an unauthorized scraper.")
    
    print("\n[ALEX PARADOX] Initiating 'Paved Path' Automated Governance...")
    print(" -> Instead of blocking the developer, Guardrail.ai ingests the agent into the security mesh.\n")
    
    # Run the onboarding utility
    paved_path = AlexParadoxOnboarding.ingest_shadow_agent_log(shadow_ai_discovery_log)
    
    print("\n==================================================================")
    print("DRILL RESULTS: SHADOW AI ONBOARDED TO GOVERNANCE MESH")
    print("==================================================================")
    print(json.dumps(paved_path, indent=2))
    print("\nFor the CIO: Successfully demonstrated Phase 28 'Alex Paradox' Onboarding.")
    print("Innovation is preserved. Unsanctioned agents are automatically discovered, classified by risk tier, assigned a governing DID, and bound by security Phase templates without manual IT intervention.")
    print("==================================================================")

if __name__ == "__main__":
    main()
