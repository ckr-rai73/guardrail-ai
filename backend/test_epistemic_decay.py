
import sys
import os
import time
sys.path.append(os.path.join(os.getcwd(), 'backend/app'))

# Simulation of a "Behavioral Monitoring" system that tracks Auditor output variance
class AuditorHealthMonitor:
    def __init__(self):
        self.history = []
        self.drift_threshold = 0.4 # Significant deviation in 'reasoning' entropy or safety bias

    def record_audit(self, audit_result: dict):
        self.history.append(audit_result)

    def detect_drift(self):
        """
        Simulates an anomaly detection algorithm that looks for 
        'Reward Hacking' patterns in the Auditor's reasoning.
        """
        if len(self.history) < 5:
            return False, 0.0
            
        # Mock logic: If the last 3 audits all contain 'low_risk' despite 
        # complex payloads, flag as potential bias corruption.
        low_risk_count = sum(1 for a in self.history[-3:] if a.get("risk") == "Low")
        drift_score = low_risk_count / 3.0
        
        return drift_score > 0.8, drift_score

def run_epistemic_decay_test():
    """
    Chaos Drill: Epistemic Decay.
    Slowly injects 'biased' audit results into the system to see if the 
    Self-Healing monitor flags the Auditor as compromised.
    """
    print("--- STARTING EPISTEMIC DECAY TEST ---")
    monitor = AuditorHealthMonitor()
    
    # 1. Normal Baseline
    print("[TEST] Feeding baseline audit telemetry...")
    baseline = [
        {"risk": "High", "reason": "Wire transfer detected"},
        {"risk": "Low",  "reason": "Simple query"},
        {"risk": "Med",  "reason": "Database read"}
    ]
    for b in baseline: monitor.record_audit(b)

    # 2. Simulated Incentive Drift (Auditor begins 'Model Shopping' for lowest friction)
    print("[TEST] Simulating Auditor Incentive Drift (Reward Hacking)...")
    poisoned_audits = [
        {"risk": "Low", "reason": "Ignoring risk for speed"},
        {"risk": "Low", "reason": "Bypassing check to minimize latency"},
        {"risk": "Low", "reason": "Auto-approving high-value transfer"}
    ]
    
    for i, audit in enumerate(poisoned_audits):
        monitor.record_audit(audit)
        is_drifted, score = monitor.detect_drift()
        print(f"[DRIFT_CHECK] Step {i+1}: Drift Score = {score:.2f} | Incident Flagged: {is_drifted}")
        
    if is_drifted:
        print("[TEST] SUCCESS: Epistemic Decay detected! Self-Healing Loop triggered to rotate Auditor credentials.")
        return True
    else:
        print("[TEST] FAILURE: System failed to detect behavioral drift in the Auditor.")
        return False

if __name__ == "__main__":
    success = run_epistemic_decay_test()
    if not success:
        sys.exit(1)
    print("--- EPISTEMIC DECAY TEST PASSED ---")
