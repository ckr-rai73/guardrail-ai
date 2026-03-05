import time
import logging
import heapq
from collections import deque
from typing import Dict, Any, List

class OperationalMonitor:
    """
    Phase 96 + Phase 100: Operational KPI Monitor.
    Tracks per-component latency (Shadow Model, Trinity Audit, ZK-Prover),
    queue depths, P99 latency, and SLO burn-rate alerts.
    Exports Prometheus-compatible metrics.
    """
    def __init__(self):
        self.latency_p95 = 0.0
        self.latency_p99 = 0.0
        self.veto_count_24h = 0
        self.daily_compute_cost = 0.0
        self.thresholds = {
            "p95_latency_ms": 500.0,
            "p99_latency_ms": 150.0,  # Phase 100: Strict SLO
            "veto_drift_limit": 0.15,
            "daily_cost_ceiling": 1000.0,
            "slo_burn_rate_threshold": 2.0,  # 2x budget consumption rate
            "meta_audit_consistency_min": 0.95  # Phase 104: Meta-Auditor threshold
        }
        self.meta_audit_score = 1.0  # Phase 104
        self.systemic_pause_active = False # Phase 66 / 104

        # --- Phase 100 Additions ---
        # Per-component latency tracking (rolling window of last 200 samples)
        self._component_latencies: Dict[str, deque] = {
            "shadow_model": deque(maxlen=200),
            "trinity_audit": deque(maxlen=200),
            "zk_prover": deque(maxlen=200),
            "build_api": deque(maxlen=200),
        }
        # Queue depths
        self._queue_depths: Dict[str, int] = {
            "shadow_model": 0,
            "trinity_audit": 0,
            "zk_prover": 0,
        }
        # Global latency buffer for P99 calculation
        self._global_latencies: deque = deque(maxlen=1000)
        # Total requests processed (for load calculation)
        self.total_requests_processed = 0
        self.max_capacity_rps = 2000  # Configurable max RPS
        self._current_rps = 0  # Updated externally or via sliding window
        # SLO tracking
        self._slo_violations_in_window = 0
        self._requests_in_window = 0

    def record_component_latency(self, component: str, latency_ms: float):
        """Records a latency sample for a specific component."""
        if component in self._component_latencies:
            self._component_latencies[component].append(latency_ms)
        self._global_latencies.append(latency_ms)
        self.total_requests_processed += 1
        self._requests_in_window += 1

        # Track SLO violations
        if latency_ms > self.thresholds["p99_latency_ms"]:
            self._slo_violations_in_window += 1

        # Recalculate P95 and P99 from global buffer
        self._recalculate_percentiles()

    def set_queue_depth(self, component: str, depth: int):
        """Updates the current queue depth for a given component."""
        if component in self._queue_depths:
            self._queue_depths[component] = depth

    def get_current_load_percent(self) -> float:
        """Returns current load as a percentage of max capacity."""
        if self.max_capacity_rps == 0:
            return 0.0
        return min((self._current_rps / self.max_capacity_rps) * 100.0, 100.0)

    def set_current_rps(self, rps: int):
        """Sets the current RPS (called by the test harness or load balancer)."""
        self._current_rps = rps

    def get_component_p99(self, component: str) -> float:
        """Returns the P99 latency for a specific component."""
        samples = list(self._component_latencies.get(component, []))
        if not samples:
            return 0.0
        samples.sort()
        idx = int(len(samples) * 0.99)
        return samples[min(idx, len(samples) - 1)]

    def get_slo_burn_rate(self) -> float:
        """
        Calculates the SLO Burn Rate.
        A rate of 1.0 means we are consuming the error budget exactly as planned.
        A rate > threshold means we are burning too fast and need to act.
        """
        if self._requests_in_window == 0:
            return 0.0
        allowed_error_rate = 0.01  # 1% error budget (P99 means 1% can exceed)
        actual_error_rate = self._slo_violations_in_window / self._requests_in_window
        if allowed_error_rate == 0:
            return float('inf') if actual_error_rate > 0 else 0.0
        return actual_error_rate / allowed_error_rate

    def update_metrics(self, latency: float, veto_triggered: bool, compute_cost: float):
        """Updates runtime metrics and checks for threshold violations."""
        self.latency_p95 = latency
        self.daily_compute_cost += compute_cost
        if veto_triggered:
            self.veto_count_24h += 1

        if self.latency_p95 > self.thresholds["p95_latency_ms"]:
            print(f"[OP-MONITOR] WARNING: Latency P95 ({self.latency_p95}ms) exceeds budget!")

        if self.daily_compute_cost > self.thresholds["daily_cost_ceiling"]:
            print(f"[OP-MONITOR] !!! COST CEILING BREACHED !!! Suspending non-critical stochastic loops.")
            return "COST_HALT"

        # Phase 100: SLO Burn Rate Alert
        burn_rate = self.get_slo_burn_rate()
        if burn_rate > self.thresholds["slo_burn_rate_threshold"]:
            print(f"[OP-MONITOR] ALERT: SLO Burn Rate is {burn_rate:.2f}x (>{self.thresholds['slo_burn_rate_threshold']}x). P99 SLA at risk!")

        return "NOMINAL"

    def check_systemic_drift(self, prev_veto_count: int):
        """Detects drift if veto rate increases beyond the 15% threshold."""
        if prev_veto_count == 0: return False
        drift = (self.veto_count_24h - prev_veto_count) / prev_veto_count
        if drift > self.thresholds["veto_drift_limit"]:
            print(f"[OP-MONITOR] !!! SYSTEMIC DRIFT DETECTED !!! Veto rate increased by {drift*100:.1f}%")
            return True
        return False

    def check_meta_audit_consistency(self, consistency_score: float) -> str:
        """
        Phase 104: Integrates Meta-Auditor score.
        If consistency drops below 0.95, it triggers a SystemicPause (Phase 66)
        and alerts Human Stewards via HeatmapScreen.
        """
        self.meta_audit_score = consistency_score
        if consistency_score < self.thresholds["meta_audit_consistency_min"]:
            if not self.systemic_pause_active:
                print(f"[OP-MONITOR] [CRITICAL ALERT]")
                print(f"[OP-MONITOR] Meta-Auditor consistency score dropped to {consistency_score:.4f} (Threshold: {self.thresholds['meta_audit_consistency_min']})")
                print(f"[OP-MONITOR] TRIGGERING SYSTEMIC PAUSE (Phase 66 Protocol).")
                print(f"[OP-MONITOR] INITIATING HEATMAP_SCREEN ALERT FOR HUMAN STEWARDS.")
                self.systemic_pause_active = True
            return "SYSTEMIC_PAUSE_ACTIVE"
        
        # If score recovers (hypothetically, via steward override)
        self.systemic_pause_active = False
        return "NOMINAL"

    def export_metrics(self) -> Dict[str, Any]:
        """
        Phase 100: Exports all metrics in a Prometheus/Grafana-compatible dict.
        In production, this would be a /metrics endpoint returning OpenMetrics text.
        """
        metrics = {
            "guardrail_latency_p95_ms": self.latency_p95,
            "guardrail_latency_p99_ms": self.latency_p99,
            "guardrail_veto_count_24h": self.veto_count_24h,
            "guardrail_daily_compute_cost_usd": self.daily_compute_cost,
            "guardrail_total_requests": self.total_requests_processed,
            "guardrail_load_percent": self.get_current_load_percent(),
            "guardrail_slo_burn_rate": self.get_slo_burn_rate(),
            "guardrail_meta_audit_score": self.meta_audit_score,
            "guardrail_systemic_pause": 1 if self.systemic_pause_active else 0,
        }
        # Per-component P99
        for comp in self._component_latencies:
            metrics[f"guardrail_{comp}_p99_ms"] = self.get_component_p99(comp)
        # Queue depths
        for comp, depth in self._queue_depths.items():
            metrics[f"guardrail_{comp}_queue_depth"] = depth
        return metrics

    def _recalculate_percentiles(self):
        """Recalculates P95 and P99 from the rolling global buffer."""
        samples = list(self._global_latencies)
        if not samples:
            return
        samples.sort()
        p95_idx = int(len(samples) * 0.95)
        p99_idx = int(len(samples) * 0.99)
        self.latency_p95 = samples[min(p95_idx, len(samples) - 1)]
        self.latency_p99 = samples[min(p99_idx, len(samples) - 1)]

# Singleton
GLOBAL_OP_MONITOR = OperationalMonitor()
