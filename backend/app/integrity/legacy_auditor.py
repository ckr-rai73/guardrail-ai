import time
from typing import Dict, Any, List
from app.settlement.vector_clock import VectorClockLedger

class LegacyAuditor:
    """
    Phase 63: The 'Cognitive Legacy' Safeguard.
    Prevents long-term 'Epistemic Poisoning' by auditing agent memory drift.
    """
    
    DRIFT_THRESHOLD = 0.15  # 15% maximum allowable deviation from Golden State

    @staticmethod
    def audit_agent_memory(agent_id: str, context_samples: List[str]) -> Dict[str, Any]:
        """
        Re-evaluates long-term agent memories against the Phase 42 baseline.
        """
        print(f"[LEGACY-AUDITOR] Auditing long-term cognitive drift for Agent: {agent_id}...")
        
        # We use the VectorClock's archaeological state verification
        total_drift = 0.0
        audit_results = []
        
        for sample in context_samples:
            # Current timestamp for the audit cycle
            timestamp = int(time.time() * 1000)
            check = VectorClockLedger.verify_archaeological_state(sample, timestamp)
            
            # Archaeological check returns integrity_score (1.0 = perfect, lower = drift)
            # Drift = 1.0 - integrity_score
            sample_drift = 1.0 - check.get("current_integrity_score", 1.0)
            total_drift += sample_drift
            audit_results.append(check)
            
        avg_drift = total_drift / len(context_samples) if context_samples else 0.0
        is_compromised = avg_drift > LegacyAuditor.DRIFT_THRESHOLD
        
        print(f"[LEGACY-AUDITOR] Average Cognitive Drift: {avg_drift:.4f} | Threshold: {LegacyAuditor.DRIFT_THRESHOLD}")
        
        if is_compromised:
            print(f"[LEGACY-AUDITOR] VETO: Epistemic Poisoning detected. Agent {agent_id} identity has drifted beyond 15% limit.")
            return {
                "status": "COMPROMISED",
                "drift_score": round(avg_drift, 4),
                "threshold": LegacyAuditor.DRIFT_THRESHOLD,
                "reason": "Exceeded reasoning convergence deviation (15% limit).",
                "aipm_required": True
            }
            
        return {
            "status": "VERIFIED_STABLE",
            "drift_score": round(avg_drift, 4),
            "threshold": LegacyAuditor.DRIFT_THRESHOLD,
            "details": "Agent identity remains within Phase 42 Golden State parameters."
        }

# Singleton for the integrity layer
GLOBAL_LEGACY_AUDITOR = LegacyAuditor()
