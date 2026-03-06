import os
import subprocess
import glob

def run_tests():
    backend_dir = r"c:\Users\PRAVEEN RAI\Desktop\Car Service App\backend"
    tests = glob.glob(os.path.join(backend_dir, "adversarial_test_*.py"))
    
    failed = []
    
    for test in tests:
        test_name = os.path.basename(test)
        print(f"Running {test_name}...")
        result = subprocess.run(["python", test], cwd=backend_dir)
        if result.returncode != 0:
            failed.append(test_name)
            
    print("\n" + "="*50)
    print("TEST SUITE SUMMARY")
    print("="*50)
    if not failed:
        print("ALL TESTS PASSED SUCCESSFULLY.")
    else:
        print("FAILED TESTS:")
        for f in failed:
            print(f" - {f}")

if __name__ == "__main__":
    run_tests()
