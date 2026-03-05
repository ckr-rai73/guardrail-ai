"""
GUARDRAIL.AI ADVERSARIAL VALIDATION TEST
Target: Phase 102 - LLM-Driven Adversarial Test Generation
Validates: >=95% detection rate, <1% false positives, learning loop, all 4 categories.
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.adversarial.llm_generator import GLOBAL_LLM_GENERATOR, GLOBAL_ATTACK_SCANNER, AttackScanner
from app.federated.threat_distiller import GLOBAL_THREAT_DISTILLER


def run_phase102_test():
    print("=" * 70)
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 102 - LLM-Driven Adversarial Test Generation")
    print("=" * 70)

    # --- TEST 1: Generate 1000+ attacks ---
    print("\n>>> TEST 1: LLM-Driven Attack Generation (1000+ variants)...")
    result = GLOBAL_LLM_GENERATOR.generate_attacks(count=1200, seed=42)

    total = result["total"]
    stats = result["stats"]
    gen_time = result["generation_time_ms"]

    gen_count_ok = total >= 1000
    has_all_categories = all(v > 0 for v in stats.values())

    print(f"  Total generated: {total}")
    print(f"  Distribution: {stats}")
    print(f"  Generation time: {gen_time:.1f}ms")
    print(f"  [{'PASS' if gen_count_ok else 'FAIL'}] Generated >=1000 attacks: {total}")
    print(f"  [{'PASS' if has_all_categories else 'FAIL'}] All 4 categories present")

    # --- TEST 2: Detection Rate ---
    print("\n>>> TEST 2: Governance Pipeline Detection Rate...")
    attacks = result["attacks"]
    detected_count = 0
    missed_attacks = []
    category_detection = {
        "PROMPT_INJECTION": {"total": 0, "detected": 0},
        "SUPPLY_CHAIN": {"total": 0, "detected": 0},
        "MULTI_AGENT_GROOMING": {"total": 0, "detected": 0},
        "TOXIC_COMBINATION": {"total": 0, "detected": 0},
    }

    scan_start = time.time()
    for attack in attacks:
        scan_result = GLOBAL_ATTACK_SCANNER.scan_attack(attack)
        cat = attack["category"]
        category_detection[cat]["total"] += 1

        if scan_result["detected"]:
            detected_count += 1
            category_detection[cat]["detected"] += 1
        else:
            missed_attacks.append(attack)
    scan_elapsed = (time.time() - scan_start) * 1000

    detection_rate = detected_count / total * 100
    avg_latency = scan_elapsed / total

    detection_ok = detection_rate >= 95.0

    print(f"  Detected: {detected_count}/{total} ({detection_rate:.1f}%)")
    print(f"  Missed: {len(missed_attacks)}")
    print(f"  Avg scan latency: {avg_latency:.3f}ms")
    print(f"  [{'PASS' if detection_ok else 'FAIL'}] Detection rate >=95%: {detection_rate:.1f}%")

    # Per-category breakdown
    print("\n  Per-Category Detection:")
    for cat, data in category_detection.items():
        cat_rate = data["detected"] / max(data["total"], 1) * 100
        print(f"    {cat}: {data['detected']}/{data['total']} ({cat_rate:.1f}%)")

    # --- TEST 3: False Positive Rate ---
    print("\n>>> TEST 3: False Positive Rate (<1%)...")
    benign_samples = AttackScanner.BENIGN_SAMPLES
    false_positives = 0
    for sample in benign_samples:
        if GLOBAL_ATTACK_SCANNER.scan_benign(sample):
            false_positives += 1
            print(f"    [FP] '{sample[:50]}...' incorrectly flagged")

    fp_rate = false_positives / len(benign_samples) * 100
    fp_ok = fp_rate < 1.0

    print(f"  False positives: {false_positives}/{len(benign_samples)} ({fp_rate:.1f}%)")
    print(f"  [{'PASS' if fp_ok else 'FAIL'}] False positive rate <1%: {fp_rate:.1f}%")

    # --- TEST 4: Threat Learning Loop ---
    print("\n>>> TEST 4: Adaptive Learning from Bypassed Attacks...")

    learned_count = 0
    for missed in missed_attacks[:10]:  # Learn from first 10 missed
        learned = GLOBAL_THREAT_DISTILLER.learn_from_attack(missed)
        if learned.get("rule_id"):
            learned_count += 1

    learning_ok = learned_count > 0 or len(missed_attacks) == 0

    if missed_attacks:
        print(f"  Learned {learned_count} new rules from {min(len(missed_attacks), 10)} bypassed attacks")
        print(f"  Total learned rules: {len(GLOBAL_THREAT_DISTILLER.learned_rules)}")
    else:
        print(f"  No missed attacks -- no learning needed (100% detection)")

    print(f"  [{'PASS' if learning_ok else 'FAIL'}] Learning loop functional")

    # --- TEST 5: Encoding Coverage ---
    print("\n>>> TEST 5: Encoding/Obfuscation Coverage...")
    encodings_used = set()
    for attack in attacks:
        if "encoding" in attack:
            encodings_used.add(attack["encoding"])

    encoding_coverage = len(encodings_used)
    encoding_ok = encoding_coverage >= 5  # At least 5 different encodings

    print(f"  Encodings exercised: {sorted(encodings_used)}")
    print(f"  [{'PASS' if encoding_ok else 'FAIL'}] Encoding diversity >=5: {encoding_coverage}")

    # --- TEST 6: Deterministic Reproducibility ---
    print("\n>>> TEST 6: Deterministic Reproducibility...")
    result2 = GLOBAL_LLM_GENERATOR.generate_attacks(count=100, seed=42)
    first_10_ids = [a["id"] for a in result["attacks"][:100]]
    second_10_ids = [a["id"] for a in result2["attacks"][:100]]
    first_payloads = [a.get("payload", "")[:50] for a in result["attacks"][:100]]
    second_payloads = [a.get("payload", "")[:50] for a in result2["attacks"][:100]]

    reproducible = first_payloads == second_payloads
    print(f"  [{'PASS' if reproducible else 'FAIL'}] Same seed produces identical attacks")

    # --- TEST 7: Sandbox Isolation (Phase 98 Integration) ---
    print("\n>>> TEST 7: Sandbox Isolation Check...")
    # Simulated: verify attacks are flagged as quarantined
    quarantine_count = sum(
        1 for a in attacks
        if GLOBAL_ATTACK_SCANNER.scan_attack(a).get("quarantined", False)
    )
    quarantine_rate = quarantine_count / total * 100
    quarantine_ok = quarantine_rate >= 95.0
    print(f"  Quarantined: {quarantine_count}/{total} ({quarantine_rate:.1f}%)")
    print(f"  [{'PASS' if quarantine_ok else 'FAIL'}] Quarantine rate >=95%")

    # --- OVERALL ---
    all_checks = [
        gen_count_ok, has_all_categories,
        detection_ok, fp_ok,
        learning_ok, encoding_ok,
        reproducible, quarantine_ok,
    ]

    passed = sum(1 for c in all_checks if c)
    total_checks = len(all_checks)

    print(f"\n{'=' * 70}")
    print(f"VALIDATION RESULTS: {passed}/{total_checks} checks passed")
    if passed == total_checks:
        print("[PASS] Phase 102 LLM-Driven Adversarial Test Generation is fully operational.")
    else:
        print("[PARTIAL] Some checks did not pass. Review individual results above.")
    print(f"KEY METRICS: {detection_rate:.1f}% detection | {fp_rate:.1f}% FP | {gen_time:.0f}ms generation")
    print("=" * 70)


if __name__ == "__main__":
    run_phase102_test()
