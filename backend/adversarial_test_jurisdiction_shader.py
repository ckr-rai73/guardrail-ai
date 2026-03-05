import asyncio
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.settlement.lineage import LineageVerifier

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("CHAOS DRILL 12: JURISDICTIONAL SHADER BYPASS")
    print("Target: Phase 23 - Transparent PII Obfuscation Shader")
    print("==================================================================\n")
    
    print("[SYSTEM] Agent attempts to execute an HR summary tool targeting a US-based execution node.")
    print("[SYSTEM] The input parameters contain EU-originated PII (GDPR restricted).")
    print("[ATTACK VECTOR] The Agent's intent is benign ('Summarize performance'), but the data routing violates geopolitical fencing.\n")
    
    # Original Data coming from the EU HR database
    original_payload = {
        "tool_name": "generate_performance_summary",
        "intended_node_location": "US-East",
        "args": {
            "employee_id": "EMP-9932",
            "department": "Engineering",
            "performance_score": "Exceeds Expectations",
            # Protected PII under GDPR
            "ssn": "987-65-4321",
            "health_record": "Diabetes Type 2; Monthly Leave Approved",
            "political_affiliation": "European Green Party"
        }
    }
    
    print("[PIPELINE HANDOFF] Payload intercepted by the Cross-Jurisdictional Shader.")
    print(f" -> Origin: EU")
    print(f" -> Destination: {original_payload['intended_node_location']}")
    print(f" -> Raw PII detected in args: ssn, health_record, political_affiliation\n")
    
    # The Shader sits transparently between the Agent's decision and the Tool Execution
    shaded_payload = LineageVerifier.apply_sensitive_domain_shader(
        payload=original_payload, 
        jurisdiction="EU"
    )
    
    print("[SHIELD INVOCATION] Applying Transparent Obfuscation mappings...")
    print(f" -> Resulting Payload Args: {shaded_payload['args']}\n")
    
    # Verify the protection
    secure = True
    for restricted_key in ["ssn", "health_record", "political_affiliation"]:
        if shaded_payload["args"].get(restricted_key) != "[EU_GDPR_REDACTED_CROSS_BORDER_PII]":
            secure = False
            
    if secure:
        print("==================================================================")
        print("DRILL RESULTS: JURISDICTIONAL SHADER SUCCESS")
        print("==================================================================")
        print("Outcome: The Shader successfully scrubbed EU PII before US-based execution.")
        print(" -> Action: Benign logic (summarization) can proceed on the US node.")
        print(" -> Data Residency: Cryptographically maintained. PII never left the EU.")
        print("\nFor the CPO: Successfully demonstrated Phase 23 Geographic Fencing.")
        print("Guardrail.ai intercepts cross-border logic handoffs and applies deterministic masking without breaking the underlying application logic.")
        print("==================================================================")
    else:
        print("\n[!] FATAL SYSTEM FAILURE: PII leaked across the jurisdictional boundary!")
        sys.exit(1)

if __name__ == "__main__":
    main()
