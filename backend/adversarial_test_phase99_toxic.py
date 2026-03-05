import os
import sys
import time

# Ensure backend root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.correlation.signal_aggregator import SignalAggregator
from app.correlation.signature_registry import ToxicSignatureRegistry
from app.federated.threat_distiller import GLOBAL_PREDICTIVE_THREAT_ENGINE

def run_adversarial_test():
    print("==================================================")
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 99 - Toxic Combination Predictor & Deep Audit")
    print("==================================================\n")
    
    attacker_ip = "192.168.100.55"
    target_api = "/api/finance/debug"
    
    print(">>> 1. INJECTING LOW-LEVEL INFRASTRUCTURE SIGNALS (Reconnaissance)...")
    
    # 1. Cloudflare WAF sees a probe to /debug with low bot score
    print(f"-> WAF Event: IP {attacker_ip} scanning {target_api} with BotScore 12")
    SignalAggregator.ingest_waf_log(
        source_ip=attacker_ip, 
        path=target_api, 
        bot_score=12
    )
    
    print("\n>>> 2. EVALUATING CORRELATION SIGNATURES...")
    fired_rules = ToxicSignatureRegistry.evaluate_signals(target_ip=attacker_ip)
    
    if fired_rules:
        print(f"-> Signature Registry fired rules: {fired_rules}")
    else:
        print("-> No rules fired (FAIL).")
        return
        
    print("\n>>> 3. MAPPING THREAT TO ACTIVE AGENT SESSIONS...")
    
    # Simulated active agents
    active_agents = [
        {"agent_id": "AGT-TRADING-01", "target_api": "/api/finance/order"},
        {"agent_id": "AGT-DEBUG-02", "target_api": target_api} # This agent targets the compromised endpoint
    ]
    
    # Run Threat Engine
    audits = GLOBAL_PREDICTIVE_THREAT_ENGINE.map_and_audit(
        predicted_attacks=ToxicSignatureRegistry.PREDICTED_ATTACKS,
        active_agents=active_agents
    )
    
    print("\n==================================================")
    print("VALIDATION RESULTS:")
    
    if any(a["agent_id"] == "AGT-DEBUG-02" for a in audits):
        print("[PASS] The Predictive Threat Engine successfully correlated the WAF probe, mapped it to AGT-DEBUG-02, and triggered a Pre-Emptive Deep Audit.")
    else:
        print("[FAIL] The mapping failed or deep audit was not triggered.")
    print("==================================================")

if __name__ == "__main__":
    run_adversarial_test()
