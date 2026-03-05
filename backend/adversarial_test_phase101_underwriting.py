"""
GUARDRAIL.AI ADVERSARIAL VALIDATION TEST
Target: Phase 101 - The Evidentiary Bridge & Dynamic Underwriting
Validates: Fault tree generation, ZK-proofs, exposure metrics, legal wrapper.
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.forensics.apportionment_engine import GLOBAL_FAULT_TREE_ENGINE
from app.insurance.underwriting_gateway import GLOBAL_UNDERWRITING_GATEWAY
from app.integrity.mediation_agent import GLOBAL_ADR_MEDIATOR
from app.forensics.judicial_exporter import GLOBAL_JUDICIAL_EXPORTER


def run_phase101_test():
    print("=" * 70)
    print("GUARDRAIL.AI ADVERSARIAL VALIDATION TEST")
    print("Target: Phase 101 - The Evidentiary Bridge & Dynamic Underwriting")
    print("=" * 70)

    # --- SCENARIO: Multi-Agent Trade Failure ---
    print("\n>>> SCENARIO: Multi-agent trade failure between AGT-ALPHA and AGT-BETA")

    agent_ledgers = {
        "AGT-ALPHA": [
            {"action": "initiate_trade", "timestamp": time.time() - 60, "result": "SUCCESS"},
            {"action": "approve_settlement", "timestamp": time.time() - 45, "result": "SUCCESS"},
            {"action": "transfer_funds", "timestamp": time.time() - 30, "result": "FAILURE", "triggered_veto": True},
        ],
        "AGT-BETA": [
            {"action": "receive_trade_request", "timestamp": time.time() - 58, "result": "SUCCESS"},
            {"action": "validate_counterparty", "timestamp": time.time() - 50, "result": "SUCCESS"},
            {"action": "timeout_waiting_for_confirmation", "timestamp": time.time() - 25, "result": "FAILURE"},
        ],
    }

    failed_tx = {
        "tx_id": "TX-2026-0304-ALPHA-BETA",
        "failure_reason": "Transfer failed due to timeout and veto trigger",
        "timestamp": time.time() - 20,
        "amount_usd": 75000.0,
    }

    # --- TEST 1: Fault Tree Generation ---
    print("\n>>> TEST 1: Fault Tree & Apportionment...")
    fault_tree = GLOBAL_FAULT_TREE_ENGINE.build_fault_tree(agent_ledgers, failed_tx)
    
    has_tree = fault_tree.get("format") == "OpenFault-v1"
    has_apportionment = len(fault_tree.get("apportionment", {})) > 0
    has_raw = len(fault_tree.get("apportionment_raw", {})) > 0
    
    # Verify apportionment sums to 100%
    raw_values = list(fault_tree.get("apportionment_raw", {}).values())
    sum_pct = sum(raw_values) if raw_values else 0
    apportionment_valid = abs(sum_pct - 1.0) < 0.01  # Within 1% tolerance
    
    print(f"  [{'PASS' if has_tree else 'FAIL'}] OpenFault-v1 format: {fault_tree.get('format')}")
    print(f"  [{'PASS' if has_apportionment else 'FAIL'}] Apportionment generated: {fault_tree.get('apportionment')}")
    print(f"  [{'PASS' if apportionment_valid else 'FAIL'}] Apportionment sums to 100%: {sum_pct*100:.1f}%")

    # --- TEST 2: Court Report ---
    print("\n>>> TEST 2: SPHINCS+-Signed Court Report...")
    court_report = GLOBAL_FAULT_TREE_ENGINE.generate_court_report(fault_tree)

    has_signature = "SPHINCS-PLUS-SIG-" in court_report.get("signature", "")
    is_court_ready = court_report.get("admissibility_status") == "COURT_READY"
    has_plain_text = "APPORTIONMENT OF LIABILITY" in court_report.get("plain_text_summary", "")

    print(f"  [{'PASS' if has_signature else 'FAIL'}] SPHINCS+ signature present")
    print(f"  [{'PASS' if is_court_ready else 'FAIL'}] Admissibility status: {court_report.get('admissibility_status')}")
    print(f"  [{'PASS' if has_plain_text else 'FAIL'}] Plain-language summary generated")

    # --- TEST 3: ADR Mediator Integration ---
    print("\n>>> TEST 3: PostAuditMediator.replay_and_apportion()...")
    adr_result = GLOBAL_ADR_MEDIATOR.replay_and_apportion(agent_ledgers, failed_tx)

    adr_has_tree = "fault_tree" in adr_result
    adr_has_report = "court_report" in adr_result
    adr_status = adr_result.get("status") == "APPORTIONED"

    print(f"  [{'PASS' if adr_has_tree else 'FAIL'}] Fault tree in ADR result")
    print(f"  [{'PASS' if adr_has_report else 'FAIL'}] Court report in ADR result")
    print(f"  [{'PASS' if adr_status else 'FAIL'}] ADR status: {adr_result.get('status')}")

    # --- TEST 4: ZK-Proof of Control Activity ---
    print("\n>>> TEST 4: Dynamic Underwriting - ZK Control Proof...")
    proof = GLOBAL_UNDERWRITING_GATEWAY.generate_control_proof(
        "CTRL-TRINITY-AUDIT",
        period_start=time.time() - 86400,
        period_end=time.time(),
        enterprise_id="ACME-CORP"
    )

    has_proof_id = proof.get("proof_id", "").startswith("ZK-CTRL-")
    is_active = proof.get("proof_payload", {}).get("was_active") is True
    has_merkle = len(proof.get("merkle_root", "")) > 0
    has_anchor = len(proof.get("vector_clock_anchor", "")) > 0
    non_repudiation = proof.get("non_repudiation") is True

    print(f"  [{'PASS' if has_proof_id else 'FAIL'}] ZK-Proof ID: {proof.get('proof_id')}")
    print(f"  [{'PASS' if is_active else 'FAIL'}] Control was active: {is_active}")
    print(f"  [{'PASS' if has_merkle else 'FAIL'}] Merkle root anchor present")
    print(f"  [{'PASS' if has_anchor else 'FAIL'}] VectorClock anchor present")
    print(f"  [{'PASS' if non_repudiation else 'FAIL'}] Non-repudiation: {non_repudiation}")

    # --- TEST 5: Exposure Metrics ---
    print("\n>>> TEST 5: Dynamic Underwriting - Exposure Metrics...")
    exposure = GLOBAL_UNDERWRITING_GATEWAY.get_exposure_metrics("ACME-CORP")

    has_enterprise_hash = len(exposure.get("enterprise_hash", "")) > 0
    has_threat_types = len(exposure.get("top_threat_types", [])) > 0
    has_premium = exposure.get("estimated_annual_premium_usd", 0) > 0
    has_merkle_anchor = len(exposure.get("merkle_anchor", "")) > 0
    privacy_ok = "ACME-CORP" not in str(exposure.get("enterprise_hash", ""))  # Anonymized

    print(f"  [{'PASS' if has_enterprise_hash else 'FAIL'}] Enterprise hash (anonymized): {exposure.get('enterprise_hash')}")
    print(f"  [{'PASS' if has_threat_types else 'FAIL'}] Top threat types: {len(exposure.get('top_threat_types', []))} categories")
    print(f"  [{'PASS' if has_premium else 'FAIL'}] Premium estimate: ${exposure.get('estimated_annual_premium_usd')}")
    print(f"  [{'PASS' if has_merkle_anchor else 'FAIL'}] Merkle anchor for non-repudiation: present")
    print(f"  [{'PASS' if privacy_ok else 'FAIL'}] Privacy-preserving: enterprise ID not exposed")

    # --- TEST 6: Legal Admissibility Wrapper ---
    print("\n>>> TEST 6: Legal Admissibility Wrapper...")
    admissible = GLOBAL_JUDICIAL_EXPORTER.wrap_for_admissibility(
        court_report,
        event_context="Multi-agent trade failure dispute resolution"
    )

    is_sealed = admissible.get("admissibility_status") == "SEALED_FOR_COURT"
    has_chain = len(admissible.get("chain_of_custody", [])) >= 4
    has_art13 = admissible.get("eu_ai_act_art13", {}).get("risk_classification") == "HIGH-RISK AI SYSTEM"
    has_summary = len(admissible.get("plain_language_summary", "")) > 50
    has_formats = "JSON_E_DISCOVERY" in admissible.get("output_formats", [])
    has_pkg_sig = "SPHINCS-PLUS-" in admissible.get("package_signature", "")

    print(f"  [{'PASS' if is_sealed else 'FAIL'}] Admissibility status: {admissible.get('admissibility_status')}")
    print(f"  [{'PASS' if has_chain else 'FAIL'}] Chain of custody: {len(admissible.get('chain_of_custody', []))} steps")
    print(f"  [{'PASS' if has_art13 else 'FAIL'}] EU AI Act Art. 13 metadata: present")
    print(f"  [{'PASS' if has_summary else 'FAIL'}] Plain-language summary: {len(admissible.get('plain_language_summary', ''))} chars")
    print(f"  [{'PASS' if has_formats else 'FAIL'}] Output formats: {admissible.get('output_formats')}")
    print(f"  [{'PASS' if has_pkg_sig else 'FAIL'}] Package signature: SPHINCS+-sealed")

    # --- TEST 7: Insurer Pilot Simulation ---
    print("\n>>> TEST 7: Insurer Pilot Simulation (End-to-End)...")

    # Insurer requests proof of Shadow Model being active
    insurer_proof = GLOBAL_UNDERWRITING_GATEWAY.generate_control_proof(
        "CTRL-SHADOW-MODEL",
        period_start=time.time() - 2592000,  # Last 30 days
        period_end=time.time(),
        enterprise_id="ACME-CORP"
    )
    pilot_proof_ok = insurer_proof.get("proof_payload", {}).get("uptime_pct", 0) >= 99.0
    
    # Insurer queries unknown control (error handling)
    bad_proof = GLOBAL_UNDERWRITING_GATEWAY.generate_control_proof(
        "CTRL-NONEXISTENT", time.time() - 86400, time.time()
    )
    error_handled = "error" in bad_proof

    print(f"  [{'PASS' if pilot_proof_ok else 'FAIL'}] Shadow Model uptime: {insurer_proof.get('proof_payload', {}).get('uptime_pct')}%")
    print(f"  [{'PASS' if error_handled else 'FAIL'}] Error handling for unknown control: {bad_proof.get('error', 'N/A')}")

    # --- OVERALL ---
    all_checks = [
        has_tree, has_apportionment, apportionment_valid,
        has_signature, is_court_ready, has_plain_text,
        adr_has_tree, adr_has_report, adr_status,
        has_proof_id, is_active, has_merkle, has_anchor, non_repudiation,
        has_enterprise_hash, has_threat_types, has_premium, has_merkle_anchor, privacy_ok,
        is_sealed, has_chain, has_art13, has_summary, has_formats, has_pkg_sig,
        pilot_proof_ok, error_handled,
    ]

    passed = sum(1 for c in all_checks if c)
    total = len(all_checks)

    print(f"\n{'=' * 70}")
    print(f"VALIDATION RESULTS: {passed}/{total} checks passed")
    if passed == total:
        print("[PASS] Phase 101 Evidentiary Bridge & Dynamic Underwriting is fully operational.")
    else:
        print("[PARTIAL] Some checks did not pass. Review individual results above.")
    print("=" * 70)


if __name__ == "__main__":
    run_phase101_test()
