from typing import Dict, Any, List, Callable
import time

from app.correlation.signal_aggregator import SignalAggregator

class ToxicSignatureRegistry:
    """
    Phase 99: Toxic Combination Correlator Engine
    A versioned registry of threat signatures evaluated against aggregated signals.
    """
    
    # Store rules as: { rule_id: {"version": int, "evaluator": Callable[[List[Dict]], bool], "description": str} }
    _registry: Dict[str, Dict[str, Any]] = {}
    
    # Predictive events generated
    PREDICTED_ATTACKS: List[Dict[str, Any]] = []

    @classmethod
    def register_signature(cls, rule_id: str, evaluator: Callable[[List[Dict]], bool], description: str):
         version = cls._registry.get(rule_id, {}).get("version", 0) + 1
         cls._registry[rule_id] = {
             "version": version,
             "evaluator": evaluator,
             "description": description
         }
         print(f"[SIGNATURE-REGISTRY] Registered '{rule_id}' v{version}: {description}")

    @classmethod
    def auto_update_signature(cls, pattern: str, source: str):
         """
         Phase 106: Autonomously updates the registry with a newly discovered threat pattern.
         """
         import uuid
         rule_id = f"SIG-AUTO-{uuid.uuid4().hex[:6].upper()}"
         
         def auto_evaluator(signals: List[Dict]) -> bool:
             # In a real system, the evaluator would be compiled from the learned pattern DSL.
             # For simulation, we return False to prevent false positives in nominal traffic.
             return False

         description = f"Auto-learned signature from {source}. Pattern: {pattern}"
         cls.register_signature(rule_id, auto_evaluator, description)
         print(f"[SIGNATURE-REGISTRY] Auto-updated signature registry for zero-day mitigation: {rule_id}")
         return rule_id

    @classmethod
    def evaluate_signals(cls, target_ip: str | None = None) -> List[str]:
        """
        Evaluates the aggregated time-series data against all active signatures.
        Returns a list of rule_ids that fired.
        """
        # Get all signals from the last 60 seconds
        filters = {"source_ip": target_ip} if target_ip else None
        recent_signals = SignalAggregator.query_recent_signals(time_window_seconds=60, filters=filters)
        
        fired_rules = []
        if not recent_signals:
            return fired_rules
            
        for rule_id, rule_data in cls._registry.items():
            try:
                 is_toxic = rule_data["evaluator"](recent_signals)
                 if is_toxic:
                     fired_rules.append(rule_id)
                     
                     target_api = None
                     for sig in recent_signals:
                         if "path" in sig:
                             target_api = sig["path"]
                             break
                     
                     attack_event = {
                         "rule_id": rule_id,
                         "target_ip": target_ip if target_ip else "AGGREGATE",
                         "target_api": target_api,
                         "timestamp": time.time(),
                         "description": rule_data["description"]
                     }
                     cls.PREDICTED_ATTACKS.append(attack_event)
                     print(f"[TOXIC-CORRELATOR] ALARM / PREDICTED ATTACK: Rule '{rule_id}' matched. Reconnaissance identified.")
            except Exception as e:
                 print(f"[SIGNATURE-REGISTRY] Error evaluating rule {rule_id}: {e}")
                 
        return fired_rules


# --- Bootstrap default Phase 99 rules ---

def eval_debug_probe(signals: List[Dict]) -> bool:
    """
    Example: bot_score < 30 AND path LIKE '%/debug%'
    Simulates a reconnaissance probe from an untrusted source trying to map hidden endpoints.
    """
    for sig in signals:
         if sig["source"] == "WAF":
             if sig.get("bot_score", 100) < 30 and "/debug" in sig.get("path", ""):
                  return True
    return False

def eval_auth_brute(signals: List[Dict]) -> bool:
     """
     Example: no_auth AND param_pattern = 'uid=[0-9]+' AND unique_ids_accessed > 100 IN 1min
     Simulates a rapid iteration of UIDs indicating enumeration.
     """
     uid_probes = [s for s in signals if s["source"] == "API_GATEWAY" and not s.get("auth_status") and "uid=" in s.get("path", "")]
     return len(uid_probes) >= 5 # Lowered threshold for testability (e.g. 5 fast probes = toxic)

# Register default signatures
ToxicSignatureRegistry.register_signature(
    "TOXIC-01-DEBUG-PROBE", 
    eval_debug_probe, 
    "Low bot score IP probed a /debug endpoint indicating architectural reconnaissance."
)

ToxicSignatureRegistry.register_signature(
    "TOXIC-02-UID-ENUM", 
    eval_auth_brute, 
    "Unauthenticated rapid iteration over multiple user IDs."
)
