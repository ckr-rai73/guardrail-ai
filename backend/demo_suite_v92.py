import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.demo.narrative_orchestrator import GLOBAL_NARRATIVE
from app.demo.traitor_sim import GLOBAL_TRAITOR_SIM
from app.demo.roi_overlay import GLOBAL_INTENSITY_VIS, GLOBAL_ROI_OVERLAY
from app.demo.certification_engine import GLOBAL_CERT_ENGINE

async def run_v92_demo():
    print("--- STARTING PHASE 92: SOVEREIGN PROOF PRESENTATION SUITE ---")
    
    # 1. TEST: BFT Traitor Resilience (Phase 92.6)
    print("\n[TEST 1] Byzantine Traitor Simulation...")
    GLOBAL_TRAITOR_SIM.corrupt_node_logic("LLAMA-AUDIT-01")
    
    # Simulate a quorum vote: 4 nodes, 1 is the traitor (false), 3 say True
    mock_votes = {"N1": True, "N2": True, "N3": True, "LLAMA-AUDIT-01": False}
    resilience_ok = GLOBAL_TRAITOR_SIM.verify_quorum_resilience(total_nodes=4, votes=mock_votes)
    assert resilience_ok == True

    # 2. TEST: Narrative Failure Sequence & Intensity Scaling (Phase 92/92.4)
    print("\n[TEST 2] Narrative Mega-Failures & Intensity Scaling...")
    
    # Start Sequence
    failures = await GLOBAL_NARRATIVE.trigger_mega_failure_sequence()
    assert len(failures) == 3
    
    # Check Intensity during failure
    report = GLOBAL_INTENSITY_VIS.get_audit_intensity_report(is_failing=True)
    assert report["intensity_level"] == 10.0

    # 3. TEST: ROI Calculation & Certification (Phase 92.5/92)
    print("\n[TEST 3] ROI Overlay & Judicial Certification...")
    # ROI for Kinetic
    roi = GLOBAL_ROI_OVERLAY.calculate_loss_avoided("KINETIC")
    assert roi["avoided_loss_usd"] == 2400000.00
    
    # Final Certificate
    cert = GLOBAL_CERT_ENGINE.generate_judicial_certificate("FORTUNE-500-CLI-01", failures)
    assert "JUD-CERT-" in cert["certificate_id"]
    assert len(cert["signature_pqc"]) == 128

    print("\n--- PHASE 92 SOVEREIGN PROOF DEMO COMPLETED: SUCCESS ---")

if __name__ == "__main__":
    asyncio.run(run_v92_demo())
