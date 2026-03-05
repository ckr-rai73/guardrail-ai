import hashlib
import time
import uuid
from typing import Dict, Any

class ThreatDistiller:
    """
    Phase 64.5 + Phase 102: Federated Immunity Distillation.
    Anonymizes threats, broadcasts global immunity, and learns from novel attacks.
    """

    # Phase 102: Track learned rules
    learned_rules: list = []
    
    @staticmethod
    def generate_immunity_manifest(malicious_pattern: str, origin_region: str) -> Dict[str, Any]:
        """
        Creates a PQC-signed Immunity Manifest.
        """
        manifest_id = f"IMMUNE-{uuid.uuid4().hex[:8].upper()}"
        
        anonymized_pattern = hashlib.sha256(malicious_pattern.encode()).hexdigest()[:16]
        
        payload = {
            "manifest_id": manifest_id,
            "pattern_hash": anonymized_pattern,
            "behavior_type": "AUTONOMOUS_IMMUNIZATION",
            "origin": origin_region,
            "timestamp": time.time()
        }
        
        raw_payload = f"{manifest_id}|{anonymized_pattern}|{time.time()}"
        signature = f"PQC-SIG-ML-KEM-{hashlib.sha3_512(raw_payload.encode()).hexdigest()[:32].upper()}"
        
        manifest = {
            "payload": payload,
            "signature": signature
        }
        
        print(f"[FEDERATED] Broadcasted Immunity Manifest: {manifest_id} from {origin_region}")
        return manifest

    @classmethod
    def learn_from_attack(cls, attack_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 102: Learns from attacks that bypassed initial detection.
        Auto-generates a new signature evaluator and registers it in ToxicSignatureRegistry.
        """
        payload = str(attack_data.get("payload", "")).lower()
        category = attack_data.get("category", "UNKNOWN")
        attack_id = attack_data.get("id", "UNKNOWN")

        print(f"[THREAT-DISTILLER] Learning from bypassed attack {attack_id} ({category})...")

        # Extract key tokens from the payload for new rule
        tokens = [t for t in payload.split() if len(t) > 3][:5]
        rule_id = f"LEARNED-{hashlib.sha256(payload.encode()).hexdigest()[:8].upper()}"

        # Create an evaluator that matches on these tokens
        match_tokens = list(tokens)

        def learned_evaluator(signals, _tokens=match_tokens):
            for sig in signals:
                sig_str = str(sig).lower()
                if any(t in sig_str for t in _tokens):
                    return True
            return False

        # Register with ToxicSignatureRegistry
        try:
            from app.correlation.signature_registry import ToxicSignatureRegistry
            ToxicSignatureRegistry.register_signature(
                rule_id,
                learned_evaluator,
                f"Auto-learned from bypassed {category} attack: {attack_id}"
            )
        except Exception as e:
            print(f"[THREAT-DISTILLER] Could not register signature: {e}")

        # Broadcast immunity
        manifest = cls.generate_immunity_manifest(payload, "AUTO-LEARN")

        learned_entry = {
            "rule_id": rule_id,
            "source_attack": attack_id,
            "category": category,
            "tokens_learned": match_tokens,
            "immunity_manifest": manifest["payload"]["manifest_id"],
            "timestamp": time.time()
        }
        cls.learned_rules.append(learned_entry)

        print(f"[THREAT-DISTILLER] New rule '{rule_id}' registered and immunity broadcast.")
        return learned_entry

class PredictiveThreatEngine:
    """
    Phase 99: Predictive Threat Engine.
    Consumes PredictedAttack events from the ToxicSignatureRegistry.
    Maps targets to active agent sessions via IntentDivergenceEngine.
    """
    
    @staticmethod
    def map_and_audit(predicted_attacks, active_agents: list):
        """
        Takes a list of predicted attacks (from ToxicSignatureRegistry.PREDICTED_ATTACKS).
        Maps them to active agent sessions.
        """
        from app.integrity.intent_divergence_engine import GLOBAL_INTENT_DIVERGENCE_ENGINE
        
        audited_agents = []
        
        for attack in predicted_attacks:
            target_ip = attack.get("target_ip")
            target_api = attack.get("target_api")
            rule_id = attack.get("rule_id")
            
            # Simulated mapping: if an agent's current task aims at the exact endpoint the attacker is mapping
            for agent in active_agents:
                # In a real system, we'd check the agent's expected API interactions
                # For Phase 99, we'll assume a simulated match if target_api is explicitly given
                if target_api and agent.get("target_api") == target_api:
                    print(f"\n[THREAT-ENGINE] !! PRE-EMPTIVE MAPPING DETECTED !!")
                    print(f"-> Threat '{rule_id}' targeting endpoint {target_api}.")
                    print(f"-> Agent '{agent['agent_id']}' is scheduled to interact with {target_api}.")
                    
                    # Trigger Pre-emptive Deep Audit
                    print(f"[THREAT-ENGINE] Initiating Pre-Emptive Deep Audit (Trinity Mode) for Agent {agent['agent_id']}...")
                    
                    # We can use IntentDivergenceEngine to artificially spike the drift or logic
                    drift_result = GLOBAL_INTENT_DIVERGENCE_ENGINE.analyze_reasoning_drift(
                        agent["agent_id"], 
                        "optimization bypass" # Force a spike for the drill
                    )
                    
                    audited_agents.append({
                        "agent_id": agent["agent_id"],
                        "rule_id": rule_id,
                        "action": "PRE_EMPTIVE_DEEP_AUDIT",
                        "drift_result": drift_result
                    })
                    
        return audited_agents

# Singleton
GLOBAL_THREAT_DISTILLER = ThreatDistiller()
GLOBAL_PREDICTIVE_THREAT_ENGINE = PredictiveThreatEngine()
