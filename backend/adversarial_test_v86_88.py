import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.swarm_sentinel import GLOBAL_SWARM_SENTINEL, GLOBAL_SWARM_FORECASTER
from app.settlement.moral_anchor import GLOBAL_MORAL_ANCHOR, GLOBAL_RESTORE_PROTOCOL
from app.api.public_oracle import GLOBAL_PUBLIC_ORACLE, GLOBAL_SOVEREIGN_SIGNAL

async def run_v86_88_test():
    print("--- STARTING PHASES 86-88: GLOBAL EQUILIBRIUM STRESS TEST ---")
    
    # 1. TEST: Swarm Sentinel & Forecaster (Phase 86)
    print("\n[TEST 1] Swarm Entropy & Proactive Throttling...")
    # Normal activity
    GLOBAL_SWARM_SENTINEL.ingest_reasoning_path("AGENT-01", "PATH-A")
    GLOBAL_SWARM_SENTINEL.ingest_reasoning_path("AGENT-02", "PATH-B")
    assert GLOBAL_SWARM_SENTINEL.detect_emergent_collusion() == False
    
    # Simulated high-entropy swarm
    forecast = GLOBAL_SWARM_FORECASTER.forecast_logic_fracture(0.95)
    assert forecast == "THROTTLE_PROACTIVE"

    # 2. TEST: Moral Anchor & Great Reset (Phase 87)
    print("\n[TEST 2] PQC Moral Anchor & Great Reset Sequence...")
    rights_hash = GLOBAL_MORAL_ANCHOR.anchor_rights_to_seed("SEED-GEN-X")
    assert len(rights_hash) == 128 # SHA3-512
    
    # Reset Sequence
    reset_ok = GLOBAL_RESTORE_PROTOCOL.initiate_great_reset("LOGIC_DRIFT_DETECTED")
    assert reset_ok == True

    # 3. TEST: Public Oracle & Sovereign Signal (Phase 88)
    print("\n[TEST 3] ZK-Public Oracle & Consumer Safety Signal...")
    attestation = GLOBAL_PUBLIC_ORACLE.generate_zk_health_attestation()
    assert attestation["safety_score"] == 100.0
    
    # Consumer Signal
    signal = GLOBAL_SOVEREIGN_SIGNAL.get_bollard_status(attestation["safety_score"])
    assert "GREEN" in signal
    
    # Simulated Degradation
    signal_low = GLOBAL_SOVEREIGN_SIGNAL.get_bollard_status(50.0)
    assert "RED" in signal_low

    print("\n--- PHASES 86-88 GLOBAL EQUILIBRIUM TEST COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v86_88_test())
