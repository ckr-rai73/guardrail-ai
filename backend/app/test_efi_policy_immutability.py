
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.getcwd()))

from app.edge.hardware_accelerator import HardwareAccelerator

def run_efi_lock_test():
    print("--- STARTING EFI POLICY IMMUTABILITY TEST ---")
    
    # 1. Verify initial state (Unlocked)
    print(f"[TEST] Initial Lock Status: {HardwareAccelerator.verify_policy_immutability()}")
    
    # 2. Attempt to lock with incomplete quorum
    print("[TEST] Attempting lock with 3/5 quorum...")
    locked_3 = HardwareAccelerator.enforce_efi_policy_lock(3)
    print(f"[TEST] Lock Successful: {locked_3}")
    print(f"[TEST] Current Lock Status: {HardwareAccelerator.verify_policy_immutability()}")
    
    if locked_3 or HardwareAccelerator.verify_policy_immutability():
        print("[TEST] FAILURE: EFI Lock engaged without quorum.")
        return False

    # 3. Lock with full quorum
    print("[TEST] Attempting lock with 5/5 quorum...")
    locked_5 = HardwareAccelerator.enforce_efi_policy_lock(5)
    print(f"[TEST] Lock Successful: {locked_5}")
    print(f"[TEST] Current Lock Status: {HardwareAccelerator.verify_policy_immutability()}")
    
    if not locked_5 or not HardwareAccelerator.verify_policy_immutability():
        print("[TEST] FAILURE: EFI Lock failed to engage with full quorum.")
        return False

    print("[TEST] SUCCESS: Constitutional Immortality achieved and verified.")
    return True

if __name__ == "__main__":
    success = run_efi_lock_test()
    if not success:
        sys.exit(1)
    print("--- EFI POLICY IMMUTABILITY TEST PASSED ---")
