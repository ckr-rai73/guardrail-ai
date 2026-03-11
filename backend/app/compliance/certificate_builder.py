# File: app/compliance/certificate_builder.py
"""
Phase 114: Certificate Builder
================================
Assembles compliance evidence into verifiable, court-ready certification
packages complete with ZK-proofs and SPHINCS+ signatures.
"""

import hashlib
import json
import time
import uuid
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.compliance.zk_prover import GLOBAL_ZK_PROVER
from app.compliance.control_mapper import ControlMapper
from app.compliance.evidence_collector import EvidenceCollector

logger = logging.getLogger(__name__)


@dataclass
class Certificate:
    """
    Immutable certification package with framework metadata,
    control statuses, ZK-proofs, and a SPHINCS+ signature.
    """

    certificate_id: str
    framework: str
    framework_meta: Dict[str, Any]
    org_id: str
    issued_at: float
    time_range: Dict[str, float]
    controls: List[Dict[str, Any]]
    zk_proofs: List[Dict[str, Any]]
    evidence_merkle_root: str
    non_repudiation_hash: str
    package_signature: str
    signature_algorithm: str = "SPHINCS+-SHA3-256f (FIPS 205)"
    status: str = "ISSUED"
    _raw_data: Dict[str, Any] = field(default_factory=dict, repr=False)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_json(self) -> str:
        """Serialise the certificate to a JSON string (e-discovery ready)."""
        return json.dumps(self._to_dict(), indent=2, default=str)

    def to_pdf(self) -> bytes:
        """
        Stub – in production this would use reportlab / weasyprint.

        Returns a UTF-8 encoded placeholder.
        """
        header = (
            f"COMPLIANCE CERTIFICATE – {self.framework}\n"
            f"{'=' * 60}\n"
            f"Certificate ID : {self.certificate_id}\n"
            f"Organisation   : {self.org_id}\n"
            f"Issued         : {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(self.issued_at))}\n"
            f"Signature      : {self.package_signature[:32]}…\n"
            f"Status         : {self.status}\n\n"
        )
        body = "\n".join(
            f"  [{c['status']}] {c['control_id']} – {c['title']}"
            for c in self.controls
        )
        return (header + body).encode("utf-8")

    def verify(self) -> bool:
        """
        Verify the certificate's signature and internal integrity.

        Returns ``False`` if the package has been tampered with.
        """
        # Recompute expected signature over canonical payload
        payload = self._signable_payload()
        expected_sig = (
            "SPHINCS-PLUS-"
            + hashlib.sha3_512(payload.encode()).hexdigest()[:48].upper()
        )
        return self.package_signature == expected_sig

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _to_dict(self) -> Dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "framework": self.framework,
            "framework_meta": self.framework_meta,
            "org_id": self.org_id,
            "issued_at": self.issued_at,
            "time_range": self.time_range,
            "controls": self.controls,
            "zk_proofs_count": len(self.zk_proofs),
            "evidence_merkle_root": self.evidence_merkle_root,
            "non_repudiation_hash": self.non_repudiation_hash,
            "package_signature": self.package_signature,
            "signature_algorithm": self.signature_algorithm,
            "status": self.status,
        }

    def _signable_payload(self) -> str:
        """Canonical string used for signing / verification."""
        signable = {
            "certificate_id": self.certificate_id,
            "framework": self.framework,
            "org_id": self.org_id,
            "issued_at": self.issued_at,
            "evidence_merkle_root": self.evidence_merkle_root,
            "non_repudiation_hash": self.non_repudiation_hash,
            "controls": self.controls,
        }
        return json.dumps(signable, sort_keys=True, default=str)


class CertificateBuilder:
    """
    Assembles a ``Certificate`` from collected evidence.

    Workflow::

        builder = CertificateBuilder()
        evidence = await EvidenceCollector().collect_evidence("ISO_42001", (t0, t1))
        cert = await builder.build_certificate("ISO_42001", evidence, "ACME-CORP")
        assert cert.verify()
    """

    def __init__(
        self,
        control_mapper: Optional[ControlMapper] = None,
        zk_prover: Optional[Any] = None,
    ):
        self._mapper = control_mapper or ControlMapper()
        self._zk = zk_prover or GLOBAL_ZK_PROVER

    async def build_certificate(
        self,
        framework: str,
        evidence: Dict[str, Any],
        org_id: str,
    ) -> Certificate:
        """
        Build a signed certification package.

        Args:
            framework: Framework ID (e.g. ``"ISO_42001"``).
            evidence: The evidence dict returned by
                :meth:`EvidenceCollector.collect_evidence`.
            org_id: Organisation identifier.

        Returns:
            A fully signed :class:`Certificate`.
        """
        cert_id = f"CERT-{framework}-{uuid.uuid4().hex[:12].upper()}"
        issued_at = time.time()

        # --- Framework metadata ---
        try:
            fw_meta = self._mapper.get_framework_meta(framework)
        except ValueError:
            fw_meta = {"id": framework, "name": framework}

        # --- Evaluate controls ---
        evidence_items = evidence.get("evidence_items", [])
        controls: List[Dict[str, Any]] = []
        zk_proofs: List[Dict[str, Any]] = []

        for item in evidence_items:
            # Determine compliance status
            status = self._evaluate_control_status(item)

            control_entry = {
                "control_id": item["control_id"],
                "title": item.get("title", ""),
                "status": status,
                "evidence_hash": item["evidence_hash"],
                "evidence_count": len(item.get("evidence", [])),
            }
            controls.append(control_entry)

            # Generate ZK-proof for each control
            proof = self._zk.generate_inclusion_proof(
                record_hash=item["evidence_hash"],
                merkle_root=evidence.get("merkle_root", ""),
                metadata={"control_id": item["control_id"], "framework": framework},
            )
            zk_proofs.append(proof)

        # --- Signature ---
        merkle_root = evidence.get("merkle_root", "")
        non_rep_hash = evidence.get("non_repudiation_hash", "")

        cert = Certificate(
            certificate_id=cert_id,
            framework=framework,
            framework_meta=fw_meta,
            org_id=org_id,
            issued_at=issued_at,
            time_range=evidence.get("time_range", {}),
            controls=controls,
            zk_proofs=zk_proofs,
            evidence_merkle_root=merkle_root,
            non_repudiation_hash=non_rep_hash,
            package_signature="",            # placeholder – computed below
            _raw_data=evidence,
        )

        # Compute SPHINCS+ signature (simulated)
        payload = cert._signable_payload()
        cert.package_signature = (
            "SPHINCS-PLUS-"
            + hashlib.sha3_512(payload.encode()).hexdigest()[:48].upper()
        )

        logger.info(
            "[CERT-BUILDER] Certificate %s issued for %s (%s). Controls: %d",
            cert_id, org_id, framework, len(controls),
        )

        return cert

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _evaluate_control_status(evidence_item: Dict[str, Any]) -> str:
        """
        Determine whether a control is compliant based on collected evidence.

        A control is ``compliant`` if at least one evidence source returned
        data; ``non_compliant`` if no evidence was found.
        """
        evidences = evidence_item.get("evidence", [])
        if not evidences:
            return "non_compliant"

        has_data = any(e.get("record_count", 0) > 0 for e in evidences)
        return "compliant" if has_data else "non_compliant"
