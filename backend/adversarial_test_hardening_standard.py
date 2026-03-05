import asyncio
import os
import sys

# Add the backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.reporting.risk_oracle import RiskScoreAPI
from app.settlement.vector_clock import VectorClockLedger
from app.orchestration.threat_broadcast import FederatedThreatBroadcast

async def run_hardening_suite():
    print("==================================================")
    print("PHASES 54-56: GLOBAL HARDENING VERIFICATION SUITE")
    print("==================================================")

    # 1. PHASE 54: Insurance Oracle
    print("\n[TEST] Phase 54: Insurance Risk Oracle...")
    # Low risk scenario
    low_risk = RiskScoreAPI.generate_actuarial_manifest("TENANT-LOW", 0.05, 0.05)
    # High risk scenario
    high_risk = RiskScoreAPI.generate_actuarial_manifest("TENANT-HIGH", 0.35, 0.45)
    print(f"  Low Risk Category: {low_risk['underwriting_category']}")
    print(f"  High Risk Category: {high_risk['underwriting_category']}")
    assert high_risk['exposure_score'] > low_risk['exposure_score']

    # 2. PHASE 55: Quantum Archival
    print("\n[TEST] Phase 55: Quantum Lattice Archival...")
    retention_artifact = VectorClockLedger.enforce_dpdp_retention_policy()
    print(f"  Archival Status: {retention_artifact['archival_status']}")
    assert retention_artifact['archival_status'] == "LATTICE_SECURE_COLD_STORAGE"

    # 3. PHASE 56: Global Immunity (Cross-Tenant Sync)
    print("\n[TEST] Phase 56: Federated Global Immunity...")
    # Tenant A neutralizes an attack
    FederatedThreatBroadcast.broadcast_anonymized_threat("FINANCE-A", "sql_injection_on_vault_v2")
    
    # Check if a global rule was created
    registry = FederatedThreatBroadcast.sync_global_policies()
    immunity_rules = [r for r in registry if "GLOBAL-IMMUNITY" in r['rule_id']]
    print(f"  Global Immunity Rules Broadcasted: {len(immunity_rules)}")
    assert len(immunity_rules) > 0

    print("\n==================================================")
    print("HARDENING VERIFIED. STANDARD SECURED.")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_hardening_suite())
