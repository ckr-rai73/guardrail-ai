# File: adversarial_test_phase114_compliance.py
"""
Phase 114 – Adversarial Test Suite: Autonomous Compliance Certification
========================================================================
Validates the entire compliance certification pipeline end-to-end,
including control mapping, evidence collection, certificate generation,
ZK-proof simulation, auditor portal, and tamper-detection.

Run with:
    python -m pytest backend/adversarial_test_phase114_compliance.py -v
"""

import asyncio
import copy
import hashlib
import json
import time
import sys
import os

import pytest

# ---------------------------------------------------------------------------
# Ensure the backend package is importable
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from app.compliance.zk_prover import ZKProver, GLOBAL_ZK_PROVER
from app.compliance.control_mapper import ControlMapper
from app.compliance.evidence_collector import EvidenceCollector
from app.compliance.certificate_builder import CertificateBuilder, Certificate
from app.core.config import settings


# Helper to run async functions in synchronous test context
def _run(coro):
    """Run an async coroutine in a new event loop."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# ======================================================================
# 1. Control Mapping Completeness
# ======================================================================

class TestControlMapping:
    """
    Verify that all frameworks are loaded and every control maps
    to at least one internal evidence source.
    """

    def setup_method(self):
        self.mapper = ControlMapper()

    def test_all_frameworks_loaded(self):
        """All five supported frameworks must be available."""
        frameworks = self.mapper.list_frameworks()
        expected = {"ISO_42001", "SOC2", "FedRAMP", "EU_AI_ACT", "NIST_AI_RMF"}
        loaded = set(frameworks)
        missing = expected - loaded
        assert not missing, f"Missing frameworks: {missing}"
        print(f"[PASS] All {len(expected)} frameworks loaded: {sorted(loaded)}")

    def test_frameworks_match_config(self):
        """Loaded frameworks must match config.COMPLIANCE_SUPPORTED_FRAMEWORKS."""
        configured = set(settings.COMPLIANCE_SUPPORTED_FRAMEWORKS)
        loaded = set(self.mapper.list_frameworks())
        assert configured == loaded, (
            f"Config mismatch. Configured: {configured}, Loaded: {loaded}"
        )
        print("[PASS] Framework list matches config.py settings.")

    @pytest.mark.parametrize("framework", [
        "ISO_42001", "SOC2", "FedRAMP", "EU_AI_ACT", "NIST_AI_RMF",
    ])
    def test_every_control_has_evidence_source(self, framework):
        """Each control in each framework must map to ≥1 evidence source."""
        controls = self.mapper.get_requirements(framework)
        assert len(controls) > 0, f"No controls found for {framework}"

        for ctrl in controls:
            sources = ctrl.get("evidence_sources", [])
            assert len(sources) > 0, (
                f"Control {ctrl['id']} in {framework} has no evidence sources."
            )
        print(f"[PASS] {framework}: {len(controls)} controls, all mapped.")

    def test_map_control_returns_valid_dict(self):
        """map_control() must return a well-formed mapping for known IDs."""
        mapping = self.mapper.map_control("ISO42001-6.1")
        assert mapping["control_id"] == "ISO42001-6.1"
        assert mapping["framework"] == "ISO_42001"
        assert len(mapping["evidence_sources"]) > 0
        print(f"[PASS] map_control('ISO42001-6.1') → {mapping['title']}")

    def test_unknown_control_raises(self):
        """map_control() must raise ValueError for unknown control IDs."""
        with pytest.raises(ValueError, match="Unknown control ID"):
            self.mapper.map_control("NONEXISTENT-999")
        print("[PASS] Unknown control ID correctly raises ValueError.")


# ======================================================================
# 2. Evidence Collection
# ======================================================================

class TestEvidenceCollection:
    """
    Verify that evidence collection queries the right sources and
    produces well-structured, hash-anchored results.
    """

    def setup_method(self):
        self.mapper = ControlMapper()
        self.collector = EvidenceCollector(control_mapper=self.mapper)

    def test_collect_evidence_structure(self):
        """Evidence dict must contain required top-level keys."""
        now = time.time()
        evidence = _run(self.collector.collect_evidence(
            framework="ISO_42001",
            time_range=(now - 86400, now),
        ))

        required_keys = {
            "framework", "time_range", "collection_timestamp",
            "evidence_items", "merkle_root", "non_repudiation_hash",
            "total_controls", "evidence_count",
        }
        assert required_keys.issubset(evidence.keys()), (
            f"Missing keys: {required_keys - evidence.keys()}"
        )
        assert evidence["framework"] == "ISO_42001"
        assert evidence["evidence_count"] > 0
        print(f"[PASS] Evidence structure valid. Items: {evidence['evidence_count']}")

    def test_evidence_items_have_hashes(self):
        """Every evidence item must carry a SHA3-512 evidence_hash."""
        now = time.time()
        evidence = _run(self.collector.collect_evidence(
            framework="SOC2",
            time_range=(now - 3600, now),
        ))

        for item in evidence["evidence_items"]:
            assert "evidence_hash" in item, f"Missing hash for {item['control_id']}"
            assert len(item["evidence_hash"]) == 128  # SHA3-512 hex length
        print(f"[PASS] All {len(evidence['evidence_items'])} items have valid hashes.")

    def test_merkle_root_is_deterministic(self):
        """Same input must produce the same Merkle root."""
        now = time.time()
        tr = (now - 86400, now)
        e1 = _run(self.collector.collect_evidence("FedRAMP", tr))
        e2 = _run(self.collector.collect_evidence("FedRAMP", tr))
        assert e1["merkle_root"] == e2["merkle_root"]
        print("[PASS] Merkle root is deterministic for identical inputs.")

    def test_non_repudiation_hash_present(self):
        """Evidence must include a non-repudiation SHA3-512 hash."""
        now = time.time()
        evidence = _run(self.collector.collect_evidence(
            framework="NIST_AI_RMF",
            time_range=(now - 3600, now),
        ))
        nrh = evidence["non_repudiation_hash"]
        assert len(nrh) == 128  # SHA3-512
        print(f"[PASS] Non-repudiation hash: {nrh[:32]}…")


# ======================================================================
# 3. Certificate Generation & Verification
# ======================================================================

class TestCertificateGeneration:
    """
    Build a certificate and verify its signature, serialisation,
    and structural integrity.
    """

    def setup_method(self):
        self.mapper = ControlMapper()
        self.collector = EvidenceCollector(control_mapper=self.mapper)
        self.builder = CertificateBuilder(control_mapper=self.mapper)

    def _build_cert(self, framework="ISO_42001"):
        now = time.time()
        evidence = _run(self.collector.collect_evidence(
            framework=framework,
            time_range=(now - 86400, now),
        ))
        return _run(self.builder.build_certificate(framework, evidence, "TEST-ORG"))

    def test_certificate_verify_passes(self):
        """A freshly built certificate must pass self-verification."""
        cert = self._build_cert()
        assert cert.verify(), "Certificate verification failed on untampered cert."
        print(f"[PASS] Certificate {cert.certificate_id} passes verify().")

    def test_certificate_has_sphincs_signature(self):
        """Signature must start with the SPHINCS-PLUS prefix."""
        cert = self._build_cert()
        assert cert.package_signature.startswith("SPHINCS-PLUS-"), (
            f"Unexpected signature prefix: {cert.package_signature[:20]}"
        )
        print(f"[PASS] Signature: {cert.package_signature[:40]}…")

    def test_certificate_to_json(self):
        """to_json() must return valid JSON with required fields."""
        cert = self._build_cert()
        data = json.loads(cert.to_json())
        assert data["framework"] == "ISO_42001"
        assert data["org_id"] == "TEST-ORG"
        assert data["status"] == "ISSUED"
        assert "controls" in data
        print(f"[PASS] to_json() valid. Controls: {len(data['controls'])}")

    def test_certificate_to_pdf_stub(self):
        """to_pdf() must return bytes (stub)."""
        cert = self._build_cert()
        pdf = cert.to_pdf()
        assert isinstance(pdf, bytes)
        assert len(pdf) > 0
        print(f"[PASS] to_pdf() returned {len(pdf)} bytes.")

    def test_certificate_controls_all_compliant(self):
        """All controls should be 'compliant' given simulated evidence sources."""
        cert = self._build_cert()
        for ctrl in cert.controls:
            assert ctrl["status"] == "compliant", (
                f"Control {ctrl['control_id']} is {ctrl['status']}"
            )
        print(f"[PASS] All {len(cert.controls)} controls are compliant.")

    def test_certificate_zk_proofs_attached(self):
        """Each control must have an associated ZK-proof."""
        cert = self._build_cert()
        assert len(cert.zk_proofs) == len(cert.controls), (
            f"Proof count ({len(cert.zk_proofs)}) != control count ({len(cert.controls)})"
        )
        for proof in cert.zk_proofs:
            assert proof["status"] == "VALID"
            assert "proof" in proof
        print(f"[PASS] {len(cert.zk_proofs)} ZK-proofs attached and valid.")


# ======================================================================
# 4. Auditor Portal (TestClient)
# ======================================================================

class TestAuditorPortal:
    """
    Simulate an external auditor using the FastAPI auditor portal.
    """

    def setup_method(self):
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from app.compliance.auditor_portal import router

        app = FastAPI()
        app.include_router(router)
        self.client = TestClient(app)
        self.headers = {"X-Auditor-Key": "AUDIT-KEY-DEMO-001"}

    def test_list_frameworks(self):
        """GET /frameworks must return all supported frameworks."""
        resp = self.client.get("/api/v1/auditor/frameworks", headers=self.headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 5
        ids = {fw["id"] for fw in data}
        assert "ISO_42001" in ids
        print(f"[PASS] /frameworks returned {len(data)} frameworks.")

    def test_request_and_download_certificate(self):
        """Full flow: request → download → verify structure."""
        now = time.time()
        # Request
        resp = self.client.post(
            "/api/v1/auditor/certificate/request",
            json={
                "framework": "SOC2",
                "time_range_start": now - 86400,
                "time_range_end": now,
                "org_id": "AUDIT-TEST-ORG",
            },
            headers=self.headers,
        )
        assert resp.status_code == 200
        cert_id = resp.json()["certificate_id"]
        assert cert_id.startswith("CERT-SOC2-")
        print(f"[PASS] Certificate requested: {cert_id}")

        # Download
        resp2 = self.client.get(
            f"/api/v1/auditor/certificate/{cert_id}",
            headers=self.headers,
        )
        assert resp2.status_code == 200
        cert_data = resp2.json()
        assert cert_data["framework"] == "SOC2"
        assert cert_data["status"] == "ISSUED"
        print(f"[PASS] Certificate downloaded and verified.")

    def test_evidence_proof_retrieval(self):
        """GET /evidence/{control_id} must return a ZK-proof."""
        resp = self.client.get(
            "/api/v1/auditor/evidence/SOC2-CC3.1",
            headers=self.headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["control_id"] == "SOC2-CC3.1"
        assert "zk_proof" in data
        assert data["zk_proof"]["status"] == "VALID"
        print(f"[PASS] ZK-proof retrieved for SOC2-CC3.1.")

    def test_missing_key_returns_401(self):
        """Requests without an API key must be rejected."""
        resp = self.client.get("/api/v1/auditor/frameworks")
        assert resp.status_code == 401
        print("[PASS] Missing API key → 401.")

    def test_invalid_key_returns_401(self):
        """Invalid API keys must be rejected."""
        resp = self.client.get(
            "/api/v1/auditor/frameworks",
            headers={"X-Auditor-Key": "BOGUS-KEY"},
        )
        assert resp.status_code == 401
        print("[PASS] Invalid API key → 401.")

    def test_unknown_certificate_returns_404(self):
        """Requesting a non-existent certificate must return 404."""
        resp = self.client.get(
            "/api/v1/auditor/certificate/CERT-DOES-NOT-EXIST",
            headers=self.headers,
        )
        assert resp.status_code == 404
        print("[PASS] Unknown certificate → 404.")


# ======================================================================
# 5. ZK-Proof Simulation
# ======================================================================

class TestZKProofSimulation:
    """
    Validate that simulated ZK-proofs are generated correctly and
    that the verifier accepts valid proofs.
    """

    def setup_method(self):
        self.prover = ZKProver()

    def test_generate_proof_structure(self):
        """Generated proof must contain all required fields."""
        proof = self.prover.generate_inclusion_proof(
            record_hash="abc123" * 10,
            merkle_root="root456" * 8,
        )
        required = {
            "proof_id", "protocol", "curve", "timestamp",
            "public_inputs", "proof", "witness_commitment",
            "merkle_root", "record_hash", "status",
        }
        assert required.issubset(proof.keys()), (
            f"Missing: {required - proof.keys()}"
        )
        assert proof["proof_id"].startswith("ZKP-")
        print(f"[PASS] Proof generated: {proof['proof_id']}")

    def test_verify_valid_proof(self):
        """verify_inclusion_proof() must return True for a valid proof."""
        proof = self.prover.generate_inclusion_proof("hash_a", "root_a")
        assert self.prover.verify_inclusion_proof(proof) is True
        print("[PASS] Valid proof passes verification.")

    def test_verify_tampered_proof_fails(self):
        """A tampered proof must fail verification."""
        proof = self.prover.generate_inclusion_proof("hash_b", "root_b")
        tampered = copy.deepcopy(proof)
        tampered["status"] = "INVALID"
        assert self.prover.verify_inclusion_proof(tampered) is False
        print("[PASS] Tampered proof correctly fails verification.")

    def test_batch_proof_generation(self):
        """Batch generation must produce one proof per record."""
        records = [
            {"hash": f"record_{i}_hash"} for i in range(5)
        ]
        proofs = self.prover.generate_batch_proofs(records, merkle_root="batch_root")
        assert len(proofs) == 5
        for p in proofs:
            assert p["merkle_root"] == "batch_root"
        print(f"[PASS] Batch: {len(proofs)} proofs generated.")


# ======================================================================
# 6. False Evidence Injection (Tamper Detection)
# ======================================================================

class TestFalseEvidenceInjection:
    """
    Attempt to tamper with evidence / certificates and verify that
    integrity checks detect the modification.
    """

    def setup_method(self):
        self.mapper = ControlMapper()
        self.collector = EvidenceCollector(control_mapper=self.mapper)
        self.builder = CertificateBuilder(control_mapper=self.mapper)

    def _build_cert(self):
        now = time.time()
        evidence = _run(self.collector.collect_evidence(
            "ISO_42001", (now - 86400, now),
        ))
        return _run(self.builder.build_certificate("ISO_42001", evidence, "TAMPER-TEST"))

    def test_tampered_control_status_breaks_signature(self):
        """Flipping a control from 'compliant' to 'non_compliant' must break verify()."""
        cert = self._build_cert()
        assert cert.verify(), "Clean cert failed verification."

        # Tamper: flip first control status
        cert.controls[0]["status"] = "non_compliant"
        assert not cert.verify(), (
            "CRITICAL: Certificate verified after control status was tampered!"
        )
        print("[PASS] Control status tamper detected by verify().")

    def test_tampered_merkle_root_breaks_signature(self):
        """Modifying the Merkle root must break verify()."""
        cert = self._build_cert()
        assert cert.verify()

        cert.evidence_merkle_root = "TAMPERED_ROOT_" + "0" * 50
        assert not cert.verify(), (
            "CRITICAL: Certificate verified after Merkle root tamper!"
        )
        print("[PASS] Merkle root tamper detected.")

    def test_tampered_non_repudiation_hash_breaks_signature(self):
        """Modifying the non-repudiation hash must break verify()."""
        cert = self._build_cert()
        assert cert.verify()

        cert.non_repudiation_hash = "INJECTED_HASH_" + "f" * 114
        assert not cert.verify(), (
            "CRITICAL: Certificate verified after NR-hash tamper!"
        )
        print("[PASS] Non-repudiation hash tamper detected.")

    def test_tampered_evidence_hash_breaks_signature(self):
        """Injecting a false evidence hash into a control must break verify()."""
        cert = self._build_cert()
        assert cert.verify()

        cert.controls[0]["evidence_hash"] = "FORGED_" + "a" * 121
        assert not cert.verify(), (
            "CRITICAL: Certificate verified after evidence hash forgery!"
        )
        print("[PASS] Forged evidence hash detected.")

    def test_tampered_org_id_breaks_signature(self):
        """Changing the org_id must break verify()."""
        cert = self._build_cert()
        assert cert.verify()

        cert.org_id = "ATTACKER-ORG"
        assert not cert.verify(), (
            "CRITICAL: Certificate verified after org_id tamper!"
        )
        print("[PASS] org_id tamper detected.")


# ======================================================================
# Integration sanity
# ======================================================================

class TestIntegrationSanity:
    """Quick cross-module integration checks."""

    def test_config_settings_present(self):
        """Phase 114 config settings must be present."""
        assert settings.COMPLIANCE_EVIDENCE_RETENTION_DAYS == 2555
        assert settings.COMPLIANCE_CERTIFICATE_STORAGE_PATH == "/var/guardrail/certificates"
        assert len(settings.COMPLIANCE_SUPPORTED_FRAMEWORKS) == 5
        print("[PASS] Config settings validated.")

    def test_end_to_end_all_frameworks(self):
        """Build and verify a certificate for every supported framework."""
        mapper = ControlMapper()
        collector = EvidenceCollector(control_mapper=mapper)
        builder = CertificateBuilder(control_mapper=mapper)
        now = time.time()

        for fw in settings.COMPLIANCE_SUPPORTED_FRAMEWORKS:
            evidence = _run(collector.collect_evidence(fw, (now - 86400, now)))
            cert = _run(builder.build_certificate(fw, evidence, "E2E-TEST"))
            assert cert.verify(), f"Cert for {fw} failed verification."
            assert cert.status == "ISSUED"
            assert len(cert.zk_proofs) > 0
            print(f"  [PASS] {fw}: {len(cert.controls)} controls, cert verified.")

        print(f"[PASS] End-to-end pipeline validated for all {len(settings.COMPLIANCE_SUPPORTED_FRAMEWORKS)} frameworks.")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
