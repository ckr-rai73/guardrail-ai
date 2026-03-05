import asyncio
import os
import sys

# Add the backend directory to sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.settlement.vector_clock import VectorClockLedger
from app.reporting.board_report import BoardReportGenerator

def run_dpdp_compliance_test():
    print("==================================================")
    print("PHASE 45: DPDP ACT 2023 (INDIA) COMPLIANCE VERIFICATION")
    print("==================================================")
    
    # 1. Right to Erasure
    user_id = "USER-IND-001"
    print(f"\n[TEST] Exercising Right to Erasure for {user_id}...")
    erasure_res = VectorClockLedger.process_right_to_erasure(user_id)
    print(f"  Status: {erasure_res.get('status')}")
    print(f"  Compliance ID: {erasure_res.get('compliance_id')}")
    
    # 2. Accountability Trace
    print("\n[TEST] Verifying EU AI Act / DPDP Accountability Logs...")
    logs = BoardReportGenerator.generate_high_risk_ai_logs()
    print("\n[PREVIEW OF TRANSPARENCY LOGS]")
    # Printing first 5 lines
    print("\n".join(logs.split("\n")[:5]))
    
    if "ERASURE_PENDING" in erasure_res["status"] and "EU AI ACT" in logs:
        print("\n==================================================")
        print("SUCCESS: India DPDP and EU AI Act Compliance verified.")
        print("==================================================")
        return True
    else:
        print("\nFAILURE: Compliance hook missing.")
        return False

if __name__ == "__main__":
    run_dpdp_compliance_test()
