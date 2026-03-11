# File: app/compliance/__init__.py
"""
Compliance Module
==================
Guardrail.ai compliance subsystem spanning multiple phases.

Phase 114 additions:
- ControlMapper      – maps internal controls to framework requirements
- EvidenceCollector   – collects Merkle-anchored evidence from live system
- CertificateBuilder  – assembles signed certification packages
- Certificate         – immutable certification package dataclass
- ZKProver            – simulated zero-knowledge proof generator
- auditor_portal      – FastAPI router for external auditors
- continuous_compliance_dashboard – FastAPI router for internal teams
"""

from app.compliance.zk_prover import ZKProver, GLOBAL_ZK_PROVER
from app.compliance.control_mapper import ControlMapper
from app.compliance.evidence_collector import EvidenceCollector
from app.compliance.certificate_builder import CertificateBuilder, Certificate
from app.compliance.auditor_portal import router as auditor_router
from app.compliance.continuous_compliance_dashboard import router as dashboard_router

__all__ = [
    # Phase 114
    "ZKProver",
    "GLOBAL_ZK_PROVER",
    "ControlMapper",
    "EvidenceCollector",
    "CertificateBuilder",
    "Certificate",
    "auditor_router",
    "dashboard_router",
]
