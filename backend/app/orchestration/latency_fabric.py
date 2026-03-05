import time
import enum
from typing import Dict, Any

from app.integrity.operational_monitor import GLOBAL_OP_MONITOR


class LoadZone(enum.Enum):
    GREEN = "GREEN"    # <60% capacity — full audit
    YELLOW = "YELLOW"  # 60-85% — smart downgrade
    RED = "RED"        # >85% — auto-scale / fail-fast


class AuditMode(enum.Enum):
    FULL_TRINITY = "FULL_TRINITY"          # Full Trinity Audit (Shadow + BFT + ZK)
    SINGLE_SHADOW = "SINGLE_SHADOW"        # Single Shadow Model check
    FLASH_HEURISTIC = "FLASH_HEURISTIC"    # Gemini Flash + heuristic pre-filter
    FAIL_FAST = "FAIL_FAST"                # Blocklist check only, bypass deep audit


class AdaptiveLatencyFabric:
    """
    Phase 100: Adaptive Latency Fabric.
    Dynamically adjusts audit intensity based on real-time infrastructure load
    to maintain <150ms P99 governance overhead.
    """

    # Runtime-tunable ConfigMap (simulates K8s ConfigMap / etcd)
    CONFIG: Dict[str, Any] = {
        "green_threshold": 60.0,   # % capacity
        "yellow_threshold": 85.0,  # % capacity
        "p99_slo_ms": 150.0,
        "hpa_min_replicas": 2,
        "hpa_max_replicas": 10,
        "hpa_current_replicas": 2,
        "fail_fast_blocklist": [
            "rm -rf", "DROP TABLE", "DELETE FROM", "shutdown",
            "eval(", "exec(", "__import__"
        ],
    }

    # State
    _current_zone: LoadZone = LoadZone.GREEN
    _scaling_events: list = []
    _zone_transitions: list = []

    @classmethod
    def determine_load_zone(cls) -> LoadZone:
        """Reads telemetry from GLOBAL_OP_MONITOR and classifies the current Load Zone."""
        load_pct = GLOBAL_OP_MONITOR.get_current_load_percent()

        if load_pct >= cls.CONFIG["yellow_threshold"]:
            new_zone = LoadZone.RED
        elif load_pct >= cls.CONFIG["green_threshold"]:
            new_zone = LoadZone.YELLOW
        else:
            new_zone = LoadZone.GREEN

        # Log zone transitions
        if new_zone != cls._current_zone:
            transition = {
                "timestamp": time.time(),
                "from": cls._current_zone.value,
                "to": new_zone.value,
                "load_pct": round(load_pct, 1)
            }
            cls._zone_transitions.append(transition)
            print(f"[LATENCY-FABRIC] Zone transition: {cls._current_zone.value} -> {new_zone.value} (Load: {load_pct:.1f}%)")
            cls._current_zone = new_zone

            # Trigger auto-scaling in Red Zone
            if new_zone == LoadZone.RED:
                cls._trigger_auto_scale()

        return cls._current_zone

    @classmethod
    def get_scheduling_decision(cls, risk_tier: str) -> AuditMode:
        """
        Returns the appropriate AuditMode based on current Load Zone and risk tier.
        
        Args:
            risk_tier: "HIGH", "MEDIUM", or "LOW"
        """
        zone = cls.determine_load_zone()

        if zone == LoadZone.GREEN:
            # Full capacity: use appropriate audit for risk
            if risk_tier == "HIGH":
                return AuditMode.FULL_TRINITY
            else:
                return AuditMode.SINGLE_SHADOW

        elif zone == LoadZone.YELLOW:
            # Smart downgrade: HIGH still gets full, LOW/MEDIUM get fast path
            if risk_tier == "HIGH":
                return AuditMode.FULL_TRINITY
            else:
                return AuditMode.FLASH_HEURISTIC

        else:  # RED
            # Critical: HIGH gets single shadow, everything else is fail-fast
            if risk_tier == "HIGH":
                return AuditMode.SINGLE_SHADOW
            else:
                return AuditMode.FAIL_FAST

    @classmethod
    def run_fail_fast_check(cls, code_snippet: str) -> Dict[str, Any]:
        """
        Fail-fast blocklist scan for Red Zone non-critical traffic.
        Returns immediately with PASS/FAIL.
        """
        snippet_lower = code_snippet.lower()
        for pattern in cls.CONFIG["fail_fast_blocklist"]:
            if pattern.lower() in snippet_lower:
                return {
                    "result": "FAIL",
                    "reason": f"Blocklist match: '{pattern}'",
                    "mode": "FAIL_FAST",
                    "latency_ms": 1.0  # Near-instant
                }
        return {
            "result": "PASS",
            "reason": "No blocklist matches in fail-fast scan.",
            "mode": "FAIL_FAST",
            "latency_ms": 1.0
        }

    @classmethod
    def _trigger_auto_scale(cls):
        """Simulates Kubernetes HPA auto-scaling of Shadow Model pods."""
        current = cls.CONFIG["hpa_current_replicas"]
        max_r = cls.CONFIG["hpa_max_replicas"]

        if current < max_r:
            new_count = min(current + 2, max_r)
            cls.CONFIG["hpa_current_replicas"] = new_count
            event = {
                "timestamp": time.time(),
                "action": "SCALE_UP",
                "from_replicas": current,
                "to_replicas": new_count,
            }
            cls._scaling_events.append(event)
            print(f"[LATENCY-FABRIC] HPA SCALE-UP: Shadow Model pods {current} -> {new_count}")
        else:
            print(f"[LATENCY-FABRIC] HPA at max capacity ({max_r} replicas). Cannot scale further.")

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Returns full Fabric status for the dashboard."""
        return {
            "current_zone": cls._current_zone.value,
            "load_percent": GLOBAL_OP_MONITOR.get_current_load_percent(),
            "p99_latency_ms": GLOBAL_OP_MONITOR.latency_p99,
            "hpa_replicas": cls.CONFIG["hpa_current_replicas"],
            "scaling_events": cls._scaling_events[-5:],  # Last 5
            "zone_transitions": cls._zone_transitions[-10:],  # Last 10
            "slo_burn_rate": GLOBAL_OP_MONITOR.get_slo_burn_rate(),
        }

    @classmethod
    def reset(cls):
        """Resets fabric state for testing."""
        cls._current_zone = LoadZone.GREEN
        cls._scaling_events = []
        cls._zone_transitions = []
        cls.CONFIG["hpa_current_replicas"] = 2


# Singleton reference
GLOBAL_LATENCY_FABRIC = AdaptiveLatencyFabric()
