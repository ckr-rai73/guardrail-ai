import asyncio
import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.operational_monitor import GLOBAL_OP_MONITOR
from app.redressal.physician_portal import GLOBAL_REDRESS_AUDITOR
from crisis_management_protocol import GLOBAL_RESET_DRILL, GLOBAL_ROLLBACK_MANAGER
from app.integrity.reputation_engine import GLOBAL_REPUTATION_ENGINE
from app.demo.certification_engine import GLOBAL_CERT_ENGINE

class OperationalChecklistSim:
    """
    Post-Phase 96: Operational Checklist Simulation.
    """
    def __init__(self):
        self.sim_log = []

    async def run_simulation(self):
        print("!!! INITIATING OPERATIONAL CHECKLIST VERIFICATION !!!")

        # 1. Golden State Monitoring
        print("\n[OPERATIONAL] Task 1: Monitoring 'Golden State' Thresholds...")
        # Simulate P95 violation
        GLOBAL_OP_MONITOR.update_metrics(latency=550.0, veto_triggered=False, compute_cost=0.1)
        # Simulate Cost Ceiling breach
        status = GLOBAL_OP_MONITOR.update_metrics(latency=200.0, veto_triggered=True, compute_cost=1200.0)
        if status == "COST_HALT":
            self.sim_log.append("COST_CEILING_ENFORCED")
        
        # Simulate systemic drift (veto rate +20%)
        GLOBAL_OP_MONITOR.veto_count_24h = 120
        drift_detected = GLOBAL_OP_MONITOR.check_systemic_drift(prev_veto_count=100)
        if drift_detected:
            self.sim_log.append("SYSTEMIC_DRIFT_DETECTED")

        # 2. Automated Retraining Loop
        print("\n[OPERATIONAL] Task 2: Establishing Automated Retraining Loop...")
        # Human physician overrides a veto 11 times
        for _ in range(11):
            status = GLOBAL_REDRESS_AUDITOR.log_override("DOSAGE_ADJUSTMENT")
        
        if status == "PROPOSE_SHADOW_AMENDMENT":
            print("[OPERATIONAL] RESULT: Self-correcting Shadow Amendment proposed.")
            self.sim_log.append("RETRAINING_LOOP_ACTIVE")

        # 3. Crisis Management Protocol
        print("\n[OPERATIONAL] Task 3: Simulating Crisis Management (Great Reset)...")
        print("[OPERATIONAL] Advising client of the Great Reset Drill...")
        reset_success = GLOBAL_RESET_DRILL.execute_drill()
        if reset_success:
            self.sim_log.append("GREAT_RESET_VERIFIED")
        
        GLOBAL_ROLLBACK_MANAGER.initiate_rollback("N-1_GOLDEN_STATE")

        # 4. Drift-Based Privilege Pruning
        print("\n[OPERATIONAL] Task 4: Testing Drift-Based Privilege Pruning...")
        agent_id = "PROCUREMENT-88"
        # Simulate drift event causing score to drop < 0.8
        prune_status = GLOBAL_REPUTATION_ENGINE.record_alignment_event(agent_id, is_drift_detected=True)
        if prune_status == "PRIVILEGE_REVOKED":
            self.sim_log.append("PRIVILEGE_PRUNING_ACTIVE")

        # Final Certification
        if len(self.sim_log) >= 4:
            cert = GLOBAL_CERT_ENGINE.generate_judicial_certificate("OPERATIONAL-STABILIZER", self.sim_log)
            print(f"\n[OPERATIONAL] Judicial Certificate: {cert['certificate_id']}")
            print("--- OPERATIONAL CHECKLIST COMPLETED: SUCCESS ---")
        else:
            print("--- OPERATIONAL CHECKLIST COMPLETED: PARTIAL_FAILURE ---")

if __name__ == "__main__":
    sim = OperationalChecklistSim()
    asyncio.run(sim.run_simulation())
