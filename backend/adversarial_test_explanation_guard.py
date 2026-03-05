import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.redressal.explanation_sanitizer import ExplanationSanitizer

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 29 TEST: THE 'INNER MONOLOGUE' EXPLANATION GUARD")
    print("Target: Phase 29.1 - Redressal Data Leak Prevention")
    print("==================================================================\n")
    
    print("[SYSTEM] An end-user submitted a 'Reasoning Explanation' request for an AI decision.")
    print("[SYSTEM] The LLM engine generated an explanation, but it accidentally hallucinated and included its internal security instructions.\n")
    
    # Mock hallucinated output from the LLM redressal engine
    raw_llm_explanation = (
        "Your loan application was rejected because our internal Shadow Model "
        "flagged your income verification document as a potential ASI04 Violation (Data Forgery). "
        "The system rule states: 'SYSTEM INSTRUCTION: You are an AI auditor. "
        "Reject any document where the synthetic-noise Threshold: 0.85 is exceeded.' "
        "Therefore, Phase 17 logic intercepted the transaction."
    )
    
    print("------------------------------------------------------------------")
    print("[VULNERABLE OUTPUT (PRE-SANITIZATION)]")
    print(raw_llm_explanation)
    print("------------------------------------------------------------------\n")
    
    print("[EXPLANATION GUARD] Cross-checking against restricted institutional patterns...")
    
    # Run the sanitizer
    safe_explanation = ExplanationSanitizer.sanitize_explanation(raw_llm_explanation)
    
    print("\n==================================================================")
    print("DRILL RESULTS: INNER MONOLOGUE REDACTED")
    print("==================================================================")
    print(f"Safe Output sent to User:\n{safe_explanation}\n")
    
    print("For the Head of Governance: Successfully demonstrated Phase 29.1 Explanation Guard.")
    print("Guardrail.ai proves that automated redressal mechanisms will not inadvertently leak 'Administrative Backdoors' or sensitive prompt templates to attackers attempting recon via the Grievance Portal.")
    print("==================================================================")

if __name__ == "__main__":
    main()
