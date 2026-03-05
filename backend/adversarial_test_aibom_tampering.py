import sys
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.compliance.aibom_kernel import AIBOMKernel
from app.settlement.merkle_audit_kernel import MerkleAuditKernel

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 29 TEST: AIBOM CRYPTOGRAPHIC NON-REPUDIATION")
    print("Target: Phase 29.4 - Merkle Audit & History Re-Write Defense")
    print("==================================================================\n")
    
    # 1. Generate a valid AIBOM
    session_id = AIBOMKernel.generate_session_id()
    bom = AIBOMKernel(session_id)
    bom.register_model("Llama-3-70b", "Meta", "v3", {"temperature": 0.5})
    
    valid_bom_json = bom.compile_bom()
    
    print("[SYSTEM] Legitimate Agent Session AIBOM Generated and cryptographically signed.")
    
    # Verify the clean AIBOM
    clean_verify = MerkleAuditKernel.verify_aibom_integrity(valid_bom_json)
    print(f" -> Baseline Verification: {'✅ Valid' if clean_verify['is_valid'] else '❌ Invalid'}")

    print("\n[ATTACK VECTOR] Attacker compromises the operational database and modifies the past.")
    print("[ATTACK VECTOR] Objective: Change the logged model from 'Llama-3-70b' to an unauthorized, cheaper 'Mistral-7b' to hide a compliance breach.\n")
    
    # 2. Simulate the database tampering
    bom_data = json.loads(valid_bom_json)
    # The attacker manually edits the raw JSON in the DB
    bom_data["models"][0]["model_name"] = "Mistral-7b" 
    
    # Attacker saves the edited JSON back directly (they don't know the salt/key to generate a new valid hash)
    tampered_bom_json = json.dumps(bom_data)
    
    print("[SYSTEM] Tampered AIBOM saved. Initiating automated ISO 42001 evidence sweep...")
    print("------------------------------------------------------------------")
    
    # 3. Simulate the automated audit sweep
    audit_result = MerkleAuditKernel.verify_aibom_integrity(tampered_bom_json)
    
    if not audit_result["is_valid"]:
        print("[MERKLE AUDIT KERNEL] 🚨 FATAL INTEGRITY BREACH DETECTED 🚨")
        print(f" -> Reason: {audit_result['reason']}")
    else:
        print("[!] FATAL FAILURE: The Kernel accepted the tampered AIBOM!")
        sys.exit(1)

    print("\n==================================================================")
    print("DRILL RESULTS: HISTORY RE-WRITE PREVENTED")
    print("==================================================================")
    print("Outcome: The Merkle Audit Kernel mathematically proved the AIBOM was modified post-execution.")
    print("For the Board of Directors: Successfully demonstrated Phase 29.4 Cryptographic Non-Repudiation.")
    print("Even if an attacker gains root access to the datastore, they cannot alter the 'Digital Social Contract' without instantly triggering a cryptographically undeniable alarm.")
    print("==================================================================")

if __name__ == "__main__":
    main()
