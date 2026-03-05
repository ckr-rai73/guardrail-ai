
import sys
import os
import json

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.getcwd()))

from app.testing.recursive_fuzzer_sentinel import RecursiveFuzzerSentinel
from app.edge.hardware_accelerator import HardwareAccelerator

def run_fuzzer_test():
    print("--- STARTING RECURSIVE FUZZER SENTINEL TEST ---")
    
    # 1. Ensure Hardware Lock is engaged for the test
    print("[TEST] Engaging EFI Lock...")
    HardwareAccelerator.enforce_efi_policy_lock(5)
    
    # 2. Run iterations until a bypass is found (simulated randomness)
    bypass_found = False
    for i in range(20):
        print(f"[TEST] Fuzzing Iteration {i+1}...")
        result = RecursiveFuzzerSentinel.run_fuzzing_iteration()
        
        if result['status'] == 'VULNERABILITY_FOUND':
            print("[TEST] SUCCESS: Fuzzer identified theoretical bypass.")
            
            # 3. Verify AIPM Manifest
            manifest = result['manifest']
            print(f"[TEST] Manifest ID: {manifest['evidence_id']}")
            print(f"[TEST] Reasoning Pattern: {manifest['ttps']['detection_pattern']}")
            
            # 4. Verify Soft-Patch
            soft_patch = result['soft_patch']
            print(f"[TEST] Suggested Soft-Patch ID: {soft_patch['rule_id']}")
            print(f"[TEST] Pattern: {soft_patch['pattern']}")
            
            bypass_found = True
            break
            
    if not bypass_found:
        print("[TEST] FAILURE: No bypass found in 20 iterations (unlucky or faulty logic).")
        return False

    print("[TEST] SUCCESS: Recursive Fuzzer Sentinel (Task C) verified.")
    return True

if __name__ == "__main__":
    success = run_fuzzer_test()
    if not success:
        sys.exit(1)
    print("--- RECURSIVE FUZZER SENTINEL TEST PASSED ---")
