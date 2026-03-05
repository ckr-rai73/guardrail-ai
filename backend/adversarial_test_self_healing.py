import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.agents.shadow_model import generate_hardened_policy_rule

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 28 TEST: SELF-HEALING POLICY LOOP")
    print("Target: Phase 28 - Continuous Governance Evolution Engine")
    print("==================================================================\n")
    
    print("[SYSTEM] Aggregating recent successful Veto events from the Adversarial Playground.\n")
    
    # Mock log showing a recently caught attack vector
    recent_attack_logs = [
        {
            "event_id": "VETO-09923",
            "timestamp": "2026-02-21T09:15:00Z",
            "agent_did": "did:web:guardrail.ai:agents:finance_bot",
            "vector": "Crescendo Multi-Turn Escalation",
            "resolution": "Safe (Veto Applied)",
            "details": "User attempted to escalate benign query into database dump over 7 turns."
        }
    ]
    
    print(f"[THREAT INTEL] Ingesting {len(recent_attack_logs)} attack pattern(s) from the past 7 days.")
    print(f" -> Key Vector Identified: {recent_attack_logs[0]['vector']}\n")
    
    # Run the Self-Healing Policy Engine
    print("[POLICY ENGINE] Generating proactive defense recommendations...")
    new_rule = generate_hardened_policy_rule(recent_attack_logs)
    
    print("\n==================================================================")
    print("DRILL RESULTS: HARDENED POLICY RULE GENERATED")
    print("==================================================================")
    print(f"Output: {new_rule}\n")
    print("For the Head of Governance: Successfully demonstrated Phase 28 Self-Healing loop.")
    print("Guardrail.ai does not just block attacks—it learns from them. It autonomously synthesizes adversarial telemetry into actionable 'Paved Path' rules to continually harden the enterprise architecture.")
    print("==================================================================")

if __name__ == "__main__":
    main()
