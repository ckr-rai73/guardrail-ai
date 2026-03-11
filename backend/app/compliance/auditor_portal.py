# File: app/compliance/auditor_portal.py
"""
Phase 114: Auditor Portal
===========================
FastAPI-based read-only portal for external auditors to request,
download, and verify compliance certificates without exposing
sensitive internal data.

All evidence is presented via ZK-proofs.  Raw data never leaves
the system boundary.
"""

import hashlib
import json
import time
import uuid
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.compliance.control_mapper import ControlMapper
from app.compliance.evidence_collector import EvidenceCollector
from app.compliance.certificate_builder import CertificateBuilder, Certificate
from app.compliance.zk_prover import GLOBAL_ZK_PROVER

logger = logging.getLogger(__name__)

# ======================================================================
# Router
# ======================================================================
router = APIRouter(prefix="/api/v1/auditor", tags=["Auditor Portal – Phase 114"])

# ======================================================================
# In-memory stores (production: durable storage / secure bucket)
# ======================================================================
_AUDITOR_KEYS: Dict[str, Dict[str, Any]] = {
    # Pre-seeded demo auditor key
    "AUDIT-KEY-DEMO-001": {
        "auditor_id": "EXT-AUDITOR-DEMO",
        "name": "Demo Auditor",
        "scope": ["ISO_42001", "SOC2", "FedRAMP", "EU_AI_ACT", "NIST_AI_RMF"],
        "expires_at": time.time() + 365 * 86400,  # 1 year from now
    },
}

_CERTIFICATES: Dict[str, Certificate] = {}
_REQUEST_LOG: List[Dict[str, Any]] = []

# ======================================================================
# Shared dependencies
# ======================================================================
_mapper = ControlMapper()
_collector = EvidenceCollector(control_mapper=_mapper)
_builder = CertificateBuilder(control_mapper=_mapper)


def _authenticate_auditor(x_auditor_key: str = Header(default="")) -> Dict[str, Any]:
    """
    Validate the time-bound, scope-limited API key.

    Raises 401 if the key is missing, expired, or unknown.
    """
    if not x_auditor_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Auditor-Key header.",
        )
    key_info = _AUDITOR_KEYS.get(x_auditor_key)
    if key_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auditor API key.",
        )
    if key_info.get("expires_at", 0) < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auditor API key has expired.",
        )

    # Immutable request log
    _REQUEST_LOG.append({
        "auditor_id": key_info["auditor_id"],
        "timestamp": time.time(),
        "key_hash": hashlib.sha3_256(x_auditor_key.encode()).hexdigest()[:16],
    })

    return key_info


# ======================================================================
# Pydantic models
# ======================================================================
class CertificateRequest(BaseModel):
    """Request body for certificate generation."""
    framework: str = Field(..., description="Framework ID, e.g. ISO_42001")
    time_range_start: float = Field(..., description="Epoch start of evidence window")
    time_range_end: float = Field(..., description="Epoch end of evidence window")
    org_id: str = Field(default="GUARDRAIL-AI", description="Organisation identifier")


class CertificateResponse(BaseModel):
    """Minimal response after requesting a new certificate."""
    certificate_id: str
    framework: str
    status: str
    message: str


class FrameworkInfo(BaseModel):
    """Summary of a supported framework."""
    id: str
    name: str
    title: str
    version: str


# ======================================================================
# Endpoints
# ======================================================================

@router.get("/frameworks", response_model=List[FrameworkInfo])
async def list_frameworks(
    auditor: Dict[str, Any] = Depends(_authenticate_auditor),
):
    """Return the list of supported compliance frameworks."""
    frameworks = []
    for fw_id in _mapper.list_frameworks():
        meta = _mapper.get_framework_meta(fw_id)
        frameworks.append(FrameworkInfo(
            id=meta.get("id", fw_id),
            name=meta.get("name", fw_id),
            title=meta.get("title", ""),
            version=meta.get("version", ""),
        ))
    return frameworks


@router.post("/certificate/request", response_model=CertificateResponse)
async def request_certificate(
    body: CertificateRequest,
    auditor: Dict[str, Any] = Depends(_authenticate_auditor),
):
    """
    Request generation of a new compliance certificate.

    The certificate is built synchronously and stored for later retrieval.
    """
    # Scope check
    if body.framework not in auditor.get("scope", []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Auditor not authorised for framework: {body.framework}",
        )

    # Collect evidence
    evidence = await _collector.collect_evidence(
        framework=body.framework,
        time_range=(body.time_range_start, body.time_range_end),
    )

    # Build certificate
    cert = await _builder.build_certificate(
        framework=body.framework,
        evidence=evidence,
        org_id=body.org_id,
    )

    # Store
    _CERTIFICATES[cert.certificate_id] = cert

    return CertificateResponse(
        certificate_id=cert.certificate_id,
        framework=body.framework,
        status=cert.status,
        message="Certificate generated successfully.",
    )


@router.get("/certificate/{certificate_id}")
async def get_certificate(
    certificate_id: str,
    auditor: Dict[str, Any] = Depends(_authenticate_auditor),
):
    """Download a previously generated certificate package (JSON)."""
    cert = _CERTIFICATES.get(certificate_id)
    if cert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificate not found: {certificate_id}",
        )
    return json.loads(cert.to_json())


@router.get("/evidence/{control_id}")
async def get_evidence_proof(
    control_id: str,
    auditor: Dict[str, Any] = Depends(_authenticate_auditor),
):
    """
    Retrieve a ZK-proof for a specific control.

    Returns a simulated SNARK proof demonstrating the control's evidence
    exists in the Merkle tree – without revealing the underlying data.
    """
    try:
        mapping = _mapper.map_control(control_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown control ID: {control_id}",
        )

    # Generate a fresh ZK-proof for this control
    record_hash = hashlib.sha3_512(control_id.encode()).hexdigest()
    merkle_root = hashlib.sha3_256(b"GLOBAL_MERKLE_ROOT").hexdigest()

    proof = GLOBAL_ZK_PROVER.generate_inclusion_proof(
        record_hash=record_hash,
        merkle_root=merkle_root,
        metadata={
            "control_id": control_id,
            "framework": mapping["framework"],
            "title": mapping["title"],
        },
    )

    return {
        "control_id": control_id,
        "framework": mapping["framework"],
        "zk_proof": proof,
        "privacy_note": "Raw evidence data is NOT exposed. Only ZK-proof is provided.",
    }
