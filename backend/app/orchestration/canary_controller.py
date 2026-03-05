import time
import random
from typing import Dict, Any, List


class CanaryController:
    """
    Phase 100: Canary Deployment Controller.
    Simulates gradual rollout of scheduler changes by splitting traffic
    and monitoring P99 latency and error rates before full promotion.
    """

    def __init__(self):
        self.canary_percentage = 10  # Start with 10% traffic
        self.is_active = False
        self.canary_metrics: Dict[str, List[float]] = {"latencies": [], "errors": []}
        self.baseline_metrics: Dict[str, List[float]] = {"latencies": [], "errors": []}
        self.promotion_threshold_p99_ms = 150.0
        self.max_error_rate_delta = 0.02  # 2% tolerance
        self._decision_log: List[Dict[str, Any]] = []

    def start_canary(self, canary_pct: int = 10):
        """Initializes a canary deployment with the given traffic percentage."""
        self.canary_percentage = canary_pct
        self.is_active = True
        self.canary_metrics = {"latencies": [], "errors": []}
        self.baseline_metrics = {"latencies": [], "errors": []}
        print(f"[CANARY] Started canary deployment with {canary_pct}% traffic split.")

    def route_request(self) -> str:
        """Determines whether a request should go to CANARY or BASELINE."""
        if not self.is_active:
            return "BASELINE"
        return "CANARY" if random.randint(1, 100) <= self.canary_percentage else "BASELINE"

    def record_result(self, route: str, latency_ms: float, is_error: bool):
        """Records the result of a routed request."""
        target = self.canary_metrics if route == "CANARY" else self.baseline_metrics
        target["latencies"].append(latency_ms)
        if is_error:
            target["errors"].append(1.0)
        else:
            target["errors"].append(0.0)

    def evaluate_canary(self) -> Dict[str, Any]:
        """
        Analyzes canary vs baseline metrics and decides PROMOTE or ROLLBACK.
        Requires at least 20 samples in each group.
        """
        canary_lats = self.canary_metrics["latencies"]
        baseline_lats = self.baseline_metrics["latencies"]

        if len(canary_lats) < 20 or len(baseline_lats) < 20:
            return {"decision": "WAITING", "reason": "Insufficient samples for evaluation."}

        # Calculate P99 for both
        canary_lats_sorted = sorted(canary_lats)
        baseline_lats_sorted = sorted(baseline_lats)
        canary_p99 = canary_lats_sorted[int(len(canary_lats_sorted) * 0.99)]
        baseline_p99 = baseline_lats_sorted[int(len(baseline_lats_sorted) * 0.99)]

        # Error rates
        canary_error_rate = sum(self.canary_metrics["errors"]) / len(self.canary_metrics["errors"])
        baseline_error_rate = sum(self.baseline_metrics["errors"]) / max(len(self.baseline_metrics["errors"]), 1)
        error_rate_delta = canary_error_rate - baseline_error_rate

        # Decision logic
        p99_ok = canary_p99 <= self.promotion_threshold_p99_ms
        error_ok = error_rate_delta <= self.max_error_rate_delta

        if p99_ok and error_ok:
            # Phase 106: Autonomously trigger a Chaos Drill before full promotion
            try:
                from app.chaos.chaos_orchestrator import GLOBAL_CHAOS_ORCHESTRATOR
                print("[CANARY] Metrics OK. Triggering pre-promotion Chaos Drill...")
                scenario = GLOBAL_CHAOS_ORCHESTRATOR.generate_chaos_scenario()
                drill = GLOBAL_CHAOS_ORCHESTRATOR.translate_to_drill(scenario)
                drill_result = GLOBAL_CHAOS_ORCHESTRATOR.execute_staging_drill(drill)
                
                if drill_result.get("execution_status") == "SUCCESS":
                    decision = "PROMOTE"
                    reason = f"Canary P99={canary_p99:.1f}ms (<={self.promotion_threshold_p99_ms}ms), Error delta={error_rate_delta:.3f} (<={self.max_error_rate_delta}). Chaos Drill PASSED. Safe to promote."
                else:
                    decision = "ROLLBACK"
                    reason = f"ROLLBACK: Metrics OK, but Pre-Promotion Chaos Drill FAILED: {drill_result}"
            except Exception as e:
                decision = "ROLLBACK"
                reason = f"ROLLBACK: Chaos Drill Exception: {e}"
        else:
            decision = "ROLLBACK"
            reasons = []
            if not p99_ok:
                reasons.append(f"P99={canary_p99:.1f}ms exceeds {self.promotion_threshold_p99_ms}ms")
            if not error_ok:
                reasons.append(f"Error delta={error_rate_delta:.3f} exceeds {self.max_error_rate_delta}")
            reason = "ROLLBACK: " + "; ".join(reasons)

        result = {
            "decision": decision,
            "reason": reason,
            "canary_p99_ms": round(canary_p99, 2),
            "baseline_p99_ms": round(baseline_p99, 2),
            "canary_error_rate": round(canary_error_rate, 4),
            "baseline_error_rate": round(baseline_error_rate, 4),
            "canary_samples": len(canary_lats),
            "baseline_samples": len(baseline_lats),
        }
        self._decision_log.append(result)
        print(f"[CANARY] Evaluation: {decision} - {reason}")

        if decision == "PROMOTE":
            self.is_active = False
            print("[CANARY] Full rollout complete. Canary deactivated.")
        elif decision == "ROLLBACK":
            self.is_active = False
            print("[CANARY] Rolled back to baseline. Canary deactivated.")

        return result

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_active,
            "canary_percentage": self.canary_percentage,
            "canary_samples": len(self.canary_metrics["latencies"]),
            "baseline_samples": len(self.baseline_metrics["latencies"]),
            "decision_log": self._decision_log[-3:],
        }


# Singleton
GLOBAL_CANARY_CONTROLLER = CanaryController()
