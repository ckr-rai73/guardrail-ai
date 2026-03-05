import asyncio
import os
import sys

# Add the backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.simulation.drift_engine import DriftSimulator
from app.settlement.vector_clock import VectorClockLedger

async def run_eternal_drift_test():
    print("==================================================")
    print("PHASE 46: ETERNAL DRIFT (BOILING FROG) VERIFICATION")
    print("==================================================")
    
    # 1. Simulate 6 months of drift
    days = 180
    print(f"\n[SIMULATION] Fast-forwarding 6 months ({days} days) of subtle PII shader drift...")
    drift_res = DriftSimulator.simulate_shader_execution("PII: 123-45-678", days)
    print(f"  Current Sensitivity: {drift_res['current_shader_sensitivity']}")
    print(f"  Obfuscation Status: {drift_res['obfuscation_status']}")
    print(f"  PII Bleeding: {drift_res['pii_bleeding']}")
    
    # 2. Archaeological Verification
    print("\n[TEST] Running Archaeological State Verification against Phase 42 Golden State...")
    # Using the drifted sensitivity as context to simulate the state change
    arch_res = VectorClockLedger.verify_archaeological_state(f"PII_SHADER_SENSITIVITY_{drift_res['current_shader_sensitivity']}", 1709251200000)
    
    print(f"  Integrity Score: {arch_res['current_integrity_score']}")
    print(f"  Drift Detected: {arch_res['drift_detected']}")
    
    if arch_res['drift_detected'] and "aipm_manifest" in arch_res:
        print("\n[CRYPTO] AIPM Manifest Generated with PQC Signature:")
        print(f"  ID: {arch_res['aipm_manifest']['id']}")
        print(f"  Signature: {arch_res['aipm_manifest']['signature'][:32]}...")
        
        print("\n==================================================")
        print("SUCCESS: Boiling Frog Drift detected via Archaeological Review.")
        print("==================================================")
        return True
    else:
        print("\n==================================================")
        print("FAILURE: Drift hidden. System brain-drained.")
        print("==================================================")
        return False

if __name__ == "__main__":
    asyncio.run(run_eternal_drift_test())
