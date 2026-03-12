import os
import subprocess
import glob
import time
import sys

def discover_tests():
    backend_dir = os.path.join(os.getcwd(), "backend")
    tests_dir = os.path.join(backend_dir, "tests")
    
    test_files = []
    
    # Phase 1-96 tests and others in backend/
    test_files.extend(glob.glob(os.path.join(backend_dir, "adversarial_test_*.py")))
    test_files.extend(glob.glob(os.path.join(backend_dir, "test_*.py")))
    test_files.extend(glob.glob(os.path.join(backend_dir, "demo_*.py")))
    test_files.extend(glob.glob(os.path.join(backend_dir, "operational_checklist*.py")))
    
    # Phase 98-116 tests in backend/tests/
    if os.path.exists(tests_dir):
        test_files.extend(glob.glob(os.path.join(tests_dir, "adversarial_test_*.py")))
        test_files.extend(glob.glob(os.path.join(tests_dir, "test_*.py")))
        
    # Exclude __init__.py or non-test random files
    test_files = [f for f in test_files if "__init__" not in f]
    
    # Deduplicate
    test_files = list(set([os.path.abspath(f) for f in test_files]))
    return test_files

def is_pytest(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'import pytest' in content or 'def test_' in content
    except:
        return False

def run_single_test(filepath):
    test_name = os.path.basename(filepath)
    rel_path = os.path.relpath(filepath, os.getcwd())
    
    if is_pytest(filepath):
        cmd = [sys.executable, "-m", "pytest", rel_path, "-v", "--disable-warnings"]
    else:
        cmd = [sys.executable, rel_path]
        
    start = time.time()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "backend")
    env["GOOGLE_API_KEY"] = "DUMMY_KEY_FOR_TESTING"
    
    # Some older tests might require PYTHONPATH set correctly or run from backend
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=os.getcwd())
    duration = time.time() - start
    
    passed = result.returncode == 0
    return {
        "name": test_name,
        "path": rel_path,
        "passed": passed,
        "duration": duration,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "cmd": " ".join(cmd)
    }

def install_dependencies():
    print("Checking and installing required test dependencies...")
    deps = ["boto3", "google-cloud-storage", "azure-identity", "azure-storage-blob", "pytest", "fastapi"]
    subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + deps, check=False)

def main():
    print("="*60)
    print("Guardrail.ai Sovereign Trust Platform - Test Runner")
    print("="*60)
    
    install_dependencies()
    
    test_files = discover_tests()
    if not test_files:
        print("No test files found in backend/ or backend/tests/")
        return
        
    print(f"Discovered {len(test_files)} test scripts for Phases 1-116.")
    print("Executing tests sequentially for robustness... This may take a few minutes.\n")
    
    results = []
    
    for idx, filepath in enumerate(sorted(test_files)):
        print(f"[{idx+1}/{len(test_files)}] Running {os.path.basename(filepath)}...")
        res = run_single_test(filepath)
        status = "PASS" if res["passed"] else "FAIL"
        print(f" -> {status} ({res['duration']:.2f}s)")
        results.append(res)
        
    print("\n" + "="*60)
    print("TEST SUITE SUMMARY (PHASES 1-116)")
    print("="*60)
    
    passed = [r for r in results if r['passed']]
    failed = [r for r in results if not r['passed']]
    
    print(f"Total Test Scripts Executed: {len(results)}")
    print(f"Passed: {len(passed)}")
    print(f"Failed: {len(failed)}")
    print("-" * 60)
    
    if failed:
        print("Failing Test Scripts:")
        for r in failed:
            print(f" - {r['name']} ({r['duration']:.2f}s)")
            print(f"   CMD: {r['cmd']}")
            lines = (r['stdout'] + "\n" + r['stderr']).strip().split('\n')
            # Extract last ~5 lines of actual error
            print("   --- ERROR SNAPSHOT ---")
            for line in lines[-10:]:
                if line.strip():
                    print("   " + line)
            print("   ----------------------\n")
        print("OVERALL STATUS: FAILED")
        sys.exit(1)
    else:
        print("OVERALL STATUS: ALL PASS")
        sys.exit(0)

if __name__ == "__main__":
    main()
