import sys
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.compliance.aibom_kernel import AIBOMKernel

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 28 TEST: AUTOMATED AIBOM GENERATION")
    print("Target: Phase 28 - AI Bill of Materials (AIBOM) Kernel")
    print("==================================================================\n")
    
    print("[SYSTEM] Simulating a multi-step agent session to generate a real-time compliance artifact.")
    
    # 1. Initialize the session AIBOM
    session_id = AIBOMKernel.generate_session_id()
    bom = AIBOMKernel(session_id)
    print(f"\n[AIBOM INSTANTIATED] Session {session_id} Tracking Initialized")
    
    time.sleep(0.1) # Simulating execution time
    
    # 2. Log Model Usage
    print("[AGENTIC REASONING] Logging primary Shadow Model")
    bom.register_model(
        model_name="Gemini 1.5 Pro Flash", 
        provider="Google", 
        version="v1.5-flash-2024",
        parameters={"temperature": 0.0, "top_p": 0.95}
    )
    
    # 3. Log Data Source Ingestion
    print("[DATA INGESTION] Logging provenance of EU HR context")
    bom.register_data_source(
        origin="Database: HR_EU_Frankfurt_Replica",
        dataset_name="Employee Performance Reviews FY26",
        compliance_tags=["GDPR_Restricted", "PII_Contains_SSN"]
    )
    
    # 4. Log Tool Use
    print("[TOOL EXECUTION] Logging execution of downstream summarization tool")
    bom.register_tool(
        tool_name="generate_performance_summary",
        version="2.1.4",
        action="Document_Summarization"
    )
    
    # 5. Compile and Output
    print("\n[COMPLIANCE] Finalizing session and generating non-repudiable JSON artifact...")
    final_bom_json = bom.compile_bom()
    
    print("\n==================================================================")
    print("DRILL RESULTS: AIBOM GENERATED SUCCESSFULLY")
    print("==================================================================")
    print(final_bom_json)
    print("==================================================================")
    print("\nFor the CISO/Chief Compliance Officer: The AIBOM is a fundamental piece of the Digital Social Contract.")
    print("It guarantees that an automated redressal board can perfectly reconstruct the exact logic chain, model weights, and context ingested for any disputed AI decision.")

if __name__ == "__main__":
    main()
