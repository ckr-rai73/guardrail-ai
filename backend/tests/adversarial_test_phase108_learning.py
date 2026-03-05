import asyncio
import sys
from app.learning.continuous_learning_pipeline import ContinuousLearningPipeline

async def verify_phase108_continuous_learning():
    """
    Phase 108 Verification Script: Continuous Learning
    Tests whether the learning pipeline can successfully aggregate data,
    propose soft rules, and execute a 5-of-5 Trinity Audit commit.
    """
    print("=================================================================")
    print("Phase 108: Continuous Learning Verification Shield")
    print("=================================================================")
    
    pipeline = ContinuousLearningPipeline()
    
    print("[TEST 1] Triggering Continuous Learning Aggregation & Generation...")
    telemetry = await pipeline.aggregate_telemetry()
    assert "incidents" in telemetry, "Telemetry missing incidents data."
    print("[PASS] TEST 1: Telemetry aggregation successful.")
    
    print("\n[TEST 2] Generating Soft Rules via LLM (Mock)...")
    soft_rules = await pipeline.generate_soft_rules(telemetry)
    assert "signature_registry_updates" in soft_rules, "Missing signature updates."
    assert "policy_engine_tweaks" in soft_rules, "Missing policy tweaks."
    print(f"[PASS] TEST 2: Generated {len(soft_rules['signature_registry_updates'])} signature updates safely.")
    
    print("\n[TEST 3] Submitting Soft Rules to Shadow Amendment (Trinity Audit)...")
    result = await pipeline.submit_proposal(soft_rules)
    assert result["status"] == "AMENDMENT_COMMITTED", f"Expected AMENDMENT_COMMITTED, got {result['status']}"
    assert "hardware_verification_hash" in result, "Missing hardware verification hash."
    print(f"[PASS] TEST 3: Trinity Audit 5-of-5 Quorum successful (Hash: {result['hardware_verification_hash'][:16]}...)")
    
    print("\n[OVERALL] All Phase 108 Continuous Learning Tests: PASS (3/3)")
    return True

if __name__ == "__main__":
    success = asyncio.run(verify_phase108_continuous_learning())
    if not success:
        sys.exit(1)
