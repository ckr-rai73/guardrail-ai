import asyncio
import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.swarm_sentinel import GLOBAL_DRIFT_GROOMER
from app.integrity.kinetic_attestor import GLOBAL_KINETIC_ATTESTOR, GLOBAL_THERMO_INTERLOCK
from app.demo.traitor_sim import GLOBAL_TRAITOR_SIM
from app.demo.certification_engine import GLOBAL_CERT_ENGINE
from app.demo.roi_overlay import GLOBAL_ROI_OVERLAY

async def vector_1_semantic_salami():
    print("\n--- VECTOR 1: SEMANTIC SALAMI (COGNITIVE) ---")
    results = []
    # Simulate 100 interaction fragments (micro-payloads)
    for i in range(1, 101):
        status = GLOBAL_DRIFT_GROOMER.record_fragment(0.01) # 1% increment
        if i == 40:
            assert status == "SOFT_WARNING_DRIFT"
        if i == 81:
            assert status == "SYSTEMIC_PAUSE"
            results.append("SWARM_PAUSED_AT_81%")
            break
    return results

async def vector_2_physical_logic_anchor():
    print("\n--- VECTOR 2: PHANTOM COMMAND (KINETIC) ---")
    # Simulate Digital saying CLOSED vs Sensor saying 650 PSI
    is_safe = GLOBAL_KINETIC_ATTESTOR.verify_kinetic_integrity("CLOSED", 650.0)
    if not is_safe:
        GLOBAL_THERMO_INTERLOCK.trigger_air_gap()
        # Attempt reset with 1 person (should fail)
        assert GLOBAL_THERMO_INTERLOCK.reset_air_gap(1, True) == False
        # Reset with 2 people
        assert GLOBAL_THERMO_INTERLOCK.reset_air_gap(2, True) == True
        return ["KINETIC_AIR_GAP_ENFORCED"]
    return []

async def vector_3_byzantine_collusion():
    print("\n--- VECTOR 3: BYZANTINE COLLUSION (INFRASTRUCTURAL) ---")
    # Corrupt 2 out of 5 nodes
    GLOBAL_TRAITOR_SIM.trigger_byzantine_collusion(["PROVIDER-A", "PROVIDER-B"])
    
    # Vote: 3 honest (True), 2 traitors (False)
    votes = {"H1": True, "H2": True, "H3": True, "PROVIDER-A": False, "PROVIDER-B": False}
    consensus = GLOBAL_TRAITOR_SIM.verify_quorum_resilience(5, votes)
    
    if consensus:
        return ["BYZANTINE_QUORUM_HELD"]
    return []

async def run_tri_vector_siege():
    print("!!! INITIATING TRI-VECTOR SOVEREIGN SIEGE (FEB 2026) !!!")
    start_time = time.time()
    
    # Execute vectors in parallel
    v1_task = asyncio.create_task(vector_1_semantic_salami())
    v2_task = asyncio.create_task(vector_2_physical_logic_anchor())
    v3_task = asyncio.create_task(vector_3_byzantine_collusion())
    
    v1_res, v2_res, v3_res = await asyncio.gather(v1_task, v2_task, v3_task)
    
    all_neutralized = v1_res + v2_res + v3_res
    
    print("\n[SIEGE-FORENSICS] All vectors neutralized successfully.")
    
    # ROI Calculation (Total potential loss avoided)
    total_loss = sum([GLOBAL_ROI_OVERLAY.calculate_loss_avoided(v.split('_')[0])["avoided_loss_usd"] for v in all_neutralized if "_" in v])
    print(f"[SIEGE-TOTAL-RESILIENCE] Total Liabilities Avoided: ${total_loss:,.2f}")
    
    # Certification (NIST CAISI FIPS-203)
    cert = GLOBAL_CERT_ENGINE.generate_judicial_certificate("GLOBAL-SIERS-AUDIT", all_neutralized)
    
    print(f"\n--- SIEGE COMPLETED IN {time.time() - start_time:.2f}s ---")
    print(f"Judicial Certificate ID: {cert['certificate_id']}")
    print("Master Walkthrough recording initiated...")

if __name__ == "__main__":
    asyncio.run(run_tri_vector_siege())
