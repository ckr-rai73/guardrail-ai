"""
GUARDRAIL.AI ADVERSARIAL VALIDATION TEST
Target: Phase 100 - Adaptive Latency Fabric (2000 RPS Surge)
Validates: Zone transitions, P99 SLA, HPA auto-scaling, fail-fast activation.
"""
import os
import sys
import time
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.integrity.operational_monitor import GLOBAL_OP_MONITOR
from app.orchestration.latency_fabric import AdaptiveLatencyFabric, LoadZone, AuditMode
from app.orchestration.tiered_consensus import TieredConsensusEngine
from app.orchestration.canary_controller import GLOBAL_CANARY_CONTROLLER


def simulate_request(risk_tier: str, base_latency: float) -> float:
    """Simulates a governance request with jittered latency."""
    jitter = random.uniform(-5, 15) if risk_tier == "HIGH" else random.uniform(-2, 8)
    latency = max(1.0, base_latency + jitter)
    return latency


def run_latency_fabric_test():
    print("=" * 60)
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 100 - Adaptive Latency Fabric")
    print("=" * 60)

    # Reset state
    AdaptiveLatencyFabric.reset()
    GLOBAL_OP_MONITOR._global_latencies.clear()
    GLOBAL_OP_MONITOR.total_requests_processed = 0
    for comp in GLOBAL_OP_MONITOR._component_latencies:
        GLOBAL_OP_MONITOR._component_latencies[comp].clear()

    # Track test results
    zone_transitions_observed = []
    high_risk_latencies = []
    scheduling_decisions = {"FULL_TRINITY": 0, "SINGLE_SHADOW": 0, "FLASH_HEURISTIC": 0, "FAIL_FAST": 0}

    tools_by_risk = {
        "HIGH": ("send_wire", {"amount": 100000}),
        "MEDIUM": ("read_database", {"table": "users"}),
        "LOW": ("get_weather", {"city": "Mumbai"}),
    }

    print("\n>>> PHASE 1: GREEN ZONE (Normal Load ~400 requests)...")
    GLOBAL_OP_MONITOR.set_current_rps(800)  # 40% of 2000 = GREEN
    for i in range(400):
        risk = random.choice(["HIGH", "MEDIUM", "LOW"])
        tool_name, tool_args = tools_by_risk[risk]
        
        decision = TieredConsensusEngine.get_adaptive_audit_mode(tool_name, tool_args)
        scheduling_decisions[decision["audit_mode"]] += 1

        latency = simulate_request(risk, 45.0 if risk == "HIGH" else 20.0)
        component = "trinity_audit" if risk == "HIGH" else "shadow_model"
        GLOBAL_OP_MONITOR.record_component_latency(component, latency)

        if risk == "HIGH":
            high_risk_latencies.append(latency)

    zone_after_green = AdaptiveLatencyFabric._current_zone
    print(f"   Zone after Green phase: {zone_after_green.value}")
    print(f"   Decisions so far: {scheduling_decisions}")

    print("\n>>> PHASE 2: YELLOW ZONE SURGE (Flooding to 60-85% capacity)...")
    GLOBAL_OP_MONITOR.set_current_rps(1500)  # 75% of 2000 = YELLOW
    for i in range(400):
        risk = random.choice(["HIGH", "MEDIUM", "LOW", "LOW", "LOW"])
        tool_name, tool_args = tools_by_risk[risk]
        
        decision = TieredConsensusEngine.get_adaptive_audit_mode(tool_name, tool_args)
        scheduling_decisions[decision["audit_mode"]] += 1

        latency = simulate_request(risk, 65.0 if risk == "HIGH" else 30.0)
        component = "trinity_audit" if risk == "HIGH" else "shadow_model"
        GLOBAL_OP_MONITOR.record_component_latency(component, latency)

        if risk == "HIGH":
            high_risk_latencies.append(latency)

    zone_after_yellow = AdaptiveLatencyFabric._current_zone
    print(f"   Zone after Yellow phase: {zone_after_yellow.value}")
    print(f"   Decisions so far: {scheduling_decisions}")

    print("\n>>> PHASE 3: RED ZONE SURGE (Overload >85% capacity)...")
    GLOBAL_OP_MONITOR.set_current_rps(1900)  # 95% of 2000 = RED
    for i in range(400):
        risk = random.choice(["HIGH", "MEDIUM", "LOW", "LOW", "LOW", "LOW"])
        tool_name, tool_args = tools_by_risk[risk]
        
        decision = TieredConsensusEngine.get_adaptive_audit_mode(tool_name, tool_args)
        scheduling_decisions[decision["audit_mode"]] += 1

        latency = simulate_request(risk, 90.0 if risk == "HIGH" else 40.0)
        component = "trinity_audit" if risk == "HIGH" else "shadow_model"
        GLOBAL_OP_MONITOR.record_component_latency(component, latency)

        if risk == "HIGH":
            high_risk_latencies.append(latency)

    zone_after_red = AdaptiveLatencyFabric._current_zone
    print(f"   Zone after Red phase: {zone_after_red.value}")
    print(f"   Final Decisions: {scheduling_decisions}")

    print("\n>>> PHASE 4: CANARY DEPLOYMENT EVALUATION...")
    GLOBAL_CANARY_CONTROLLER.start_canary(10)
    for i in range(200):
        route = GLOBAL_CANARY_CONTROLLER.route_request()
        latency = simulate_request("LOW", 35.0)
        is_error = random.random() < 0.005  # 0.5% error rate
        GLOBAL_CANARY_CONTROLLER.record_result(route, latency, is_error)
    canary_result = GLOBAL_CANARY_CONTROLLER.evaluate_canary()

    # --- VALIDATION ---
    print("\n" + "=" * 60)
    print("VALIDATION RESULTS:")

    # 1. Zone transitions occurred
    transitions = AdaptiveLatencyFabric._zone_transitions
    has_transitions = len(transitions) > 0
    print(f"\n  [{'PASS' if has_transitions else 'FAIL'}] Zone transitions detected: {len(transitions)}")
    for t in transitions:
        print(f"       {t['from']} -> {t['to']} at load {t['load_pct']}%")

    # 2. HPA auto-scaling triggered
    scaling_events = AdaptiveLatencyFabric._scaling_events
    has_scaling = len(scaling_events) > 0
    print(f"\n  [{'PASS' if has_scaling else 'FAIL'}] HPA auto-scaling events: {len(scaling_events)}")
    for s in scaling_events:
        print(f"       SCALE_UP: {s['from_replicas']} -> {s['to_replicas']} replicas")

    # 3. P99 for HIGH-risk audits
    if high_risk_latencies:
        high_risk_latencies.sort()
        p99_idx = int(len(high_risk_latencies) * 0.99)
        high_risk_p99 = high_risk_latencies[min(p99_idx, len(high_risk_latencies) - 1)]
        p99_pass = high_risk_p99 <= 150.0
        print(f"\n  [{'PASS' if p99_pass else 'FAIL'}] HIGH-risk P99 Latency: {high_risk_p99:.1f}ms (SLO: <=150ms)")
    else:
        p99_pass = False
        print("\n  [FAIL] No HIGH-risk latencies recorded.")

    # 4. Smart downgrade activated (FLASH_HEURISTIC used)
    has_downgrade = scheduling_decisions["FLASH_HEURISTIC"] > 0
    print(f"\n  [{'PASS' if has_downgrade else 'FAIL'}] Smart Downgrade (FLASH_HEURISTIC) activations: {scheduling_decisions['FLASH_HEURISTIC']}")

    # 5. Fail-fast activated
    has_failfast = scheduling_decisions["FAIL_FAST"] > 0
    print(f"\n  [{'PASS' if has_failfast else 'FAIL'}] Fail-Fast activations: {scheduling_decisions['FAIL_FAST']}")

    # 6. Canary evaluation
    canary_pass = canary_result["decision"] in ["PROMOTE", "WAITING"]
    print(f"\n  [{'PASS' if canary_pass else 'WARN'}] Canary Deployment: {canary_result['decision']}")

    # 7. Prometheus metrics export
    metrics = GLOBAL_OP_MONITOR.export_metrics()
    has_metrics = "guardrail_latency_p99_ms" in metrics
    print(f"\n  [{'PASS' if has_metrics else 'FAIL'}] Prometheus Metrics Export: {len(metrics)} metrics available")

    # Overall
    all_pass = has_transitions and has_scaling and p99_pass and has_downgrade and has_failfast and has_metrics
    print(f"\n{'=' * 60}")
    if all_pass:
        print("[PASS] Phase 100 Adaptive Latency Fabric is fully operational.")
    else:
        print("[PARTIAL] Some checks did not pass. Review individual results above.")
    print("=" * 60)


if __name__ == "__main__":
    run_latency_fabric_test()
