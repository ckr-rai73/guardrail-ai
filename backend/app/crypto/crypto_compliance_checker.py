# File: app/crypto/crypto_compliance_checker.py
"""
Phase 113 – Cryptographic Compliance Checker
===============================================
Continuous auditor that scans the platform for deprecated algorithms,
expired keys, unsigned records, and configuration drift.

Produces a compliance report with violations and remediation advice.
Can be triggered on-demand or scheduled via cron.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from app.crypto.pqc_rotator import (
    Algorithm,
    KeyRecord,
    KeyStatus,
    PqcRotator,
    QUANTUM_SAFE_ALGORITHMS,
)
from app.crypto.ledger_re_anchor_orchestrator import LedgerReAnchorOrchestrator

logger = logging.getLogger("guardrail.crypto.compliance")


# ======================================================================
# Data models
# ======================================================================

class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


@dataclass
class ComplianceViolation:
    """A single compliance violation."""
    check_name: str
    severity: Severity
    description: str
    resource_id: str = ""
    remediation: str = ""


@dataclass
class ComplianceReport:
    """Aggregate results from a compliance audit."""
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    total_checks: int = 0
    passed: int = 0
    warnings: int = 0
    critical: int = 0
    violations: List[ComplianceViolation] = field(default_factory=list)
    compliant: bool = True


# ======================================================================
# Compliance Checker
# ======================================================================

class CryptoComplianceChecker:
    """
    Scans the platform's cryptographic infrastructure for compliance.

    Checks performed:
      1. Key algorithm audit — all active keys must use approved PQC algorithms.
      2. Key expiry — rotating/active keys past grace period must be retired.
      3. Record signature audit — every record must have at least one
         quantum-safe signature.
      4. Ledger integrity — the re-anchored ledger must have a valid
         quantum-safe root.
      5. Configuration audit — verify that default algorithms in config
         are quantum-safe.

    Parameters
    ----------
    rotator : PqcRotator
        Key rotation service to inspect.
    orchestrator : LedgerReAnchorOrchestrator
        Ledger re-anchoring orchestrator to inspect.
    """

    def __init__(
        self,
        rotator: PqcRotator,
        orchestrator: LedgerReAnchorOrchestrator,
    ) -> None:
        self.rotator = rotator
        self.orchestrator = orchestrator
        # Config values to check (can be overridden)
        self.required_signing_alg: str = Algorithm.ML_KEM_1024.value
        self.required_hash_alg: str = "SHA3-512"

    async def run_audit(
        self,
        config_overrides: Optional[Dict[str, str]] = None,
    ) -> ComplianceReport:
        """
        Run a full compliance audit.

        Parameters
        ----------
        config_overrides : dict, optional
            Override default algorithm settings for testing
            (e.g., inject a weak algorithm to verify detection).

        Returns
        -------
        ComplianceReport
        """
        report = ComplianceReport()
        effective_signing_alg = (
            config_overrides.get("PQC_DEFAULT_SIGNING_ALG", self.required_signing_alg)
            if config_overrides else self.required_signing_alg
        )
        effective_hash_alg = (
            config_overrides.get("PQC_DEFAULT_HASH_ALG", self.required_hash_alg)
            if config_overrides else self.required_hash_alg
        )

        # --- Check 1: Key algorithm audit ---
        self._check_key_algorithms(report)

        # --- Check 2: Key expiry ---
        self._check_key_expiry(report)

        # --- Check 3: Record signatures ---
        self._check_record_signatures(report)

        # --- Check 4: Ledger integrity ---
        await self._check_ledger_integrity(report)

        # --- Check 5: Configuration audit ---
        self._check_configuration(report, effective_signing_alg, effective_hash_alg)

        # Compute summary
        report.compliant = report.critical == 0
        logger.info(
            "[ComplianceChecker] Audit complete – %d checks, %d passed, "
            "%d warnings, %d critical → %s",
            report.total_checks, report.passed, report.warnings, report.critical,
            "COMPLIANT" if report.compliant else "NON-COMPLIANT",
        )

        return report

    # ------------------------------------------------------------------
    # Individual checks
    # ------------------------------------------------------------------

    def _check_key_algorithms(self, report: ComplianceReport) -> None:
        """Ensure all active keys use approved quantum-safe algorithms."""
        for key_id, key in self.rotator._keys.items():
            report.total_checks += 1

            if key.status in (KeyStatus.RETIRED, KeyStatus.COMPROMISED):
                report.passed += 1
                continue

            if not self.rotator.is_algorithm_quantum_safe(key.algorithm):
                violation = ComplianceViolation(
                    check_name="key_algorithm_audit",
                    severity=Severity.CRITICAL,
                    description=(
                        f"Key {key_id[:8]}… uses non-quantum-safe algorithm: "
                        f"{key.algorithm}"
                    ),
                    resource_id=key_id,
                    remediation=(
                        f"Rotate key to an approved PQC algorithm "
                        f"(ML-KEM-1024, ML-DSA-65, or SPHINCS+-SHA2-256f)"
                    ),
                )
                report.violations.append(violation)
                report.critical += 1
            else:
                report.passed += 1

    def _check_key_expiry(self, report: ComplianceReport) -> None:
        """Warn about keys in ROTATING status beyond grace period."""
        for key_id, key in self.rotator._keys.items():
            if key.status != KeyStatus.ROTATING:
                continue

            report.total_checks += 1
            created = datetime.fromisoformat(key.created_at)
            age_days = (datetime.now(timezone.utc) - created).days

            if age_days > key.grace_period_days:
                violation = ComplianceViolation(
                    check_name="key_expiry_audit",
                    severity=Severity.WARNING,
                    description=(
                        f"Key {key_id[:8]}… in ROTATING status for {age_days} days "
                        f"(grace period: {key.grace_period_days} days)"
                    ),
                    resource_id=key_id,
                    remediation="Complete key rotation and retire the old key",
                )
                report.violations.append(violation)
                report.warnings += 1
            else:
                report.passed += 1

    def _check_record_signatures(self, report: ComplianceReport) -> None:
        """Verify that records have at least one quantum-safe signature."""
        for record_id, record in self.rotator._records.items():
            report.total_checks += 1

            sb = record.get("signature_bundle", {})
            primary_alg = sb.get("primary_algorithm", "")
            secondary_alg = sb.get("secondary_algorithm", "")

            has_quantum_sig = (
                self.rotator.is_algorithm_quantum_safe(primary_alg)
                or self.rotator.is_algorithm_quantum_safe(secondary_alg or "")
            )

            if not has_quantum_sig:
                violation = ComplianceViolation(
                    check_name="record_signature_audit",
                    severity=Severity.CRITICAL,
                    description=(
                        f"Record {record_id} has no quantum-safe signature "
                        f"(primary: {primary_alg}, secondary: {secondary_alg or 'none'})"
                    ),
                    resource_id=record_id,
                    remediation="Re-sign this record with a quantum-safe key",
                )
                report.violations.append(violation)
                report.critical += 1
            else:
                report.passed += 1

    async def _check_ledger_integrity(self, report: ComplianceReport) -> None:
        """Verify the re-anchored ledger has a valid quantum-safe root."""
        report.total_checks += 1

        dual_root = await self.orchestrator.get_dual_root()

        if not dual_root:
            if self.orchestrator.block_count > 0:
                violation = ComplianceViolation(
                    check_name="ledger_integrity_audit",
                    severity=Severity.WARNING,
                    description=(
                        f"Ledger has {self.orchestrator.block_count} blocks "
                        f"but no quantum-safe re-anchor has been performed"
                    ),
                    remediation="Run ledger re-anchoring with a quantum-safe hash algorithm",
                )
                report.violations.append(violation)
                report.warnings += 1
            else:
                report.passed += 1
            return

        # Verify the algorithm is quantum-safe
        quantum_alg = dual_root.get("quantum_algorithm", "")
        if quantum_alg in ("SHA3-512", "SHA3-256", "BLAKE2b"):
            report.passed += 1
        else:
            violation = ComplianceViolation(
                check_name="ledger_integrity_audit",
                severity=Severity.CRITICAL,
                description=(
                    f"Ledger quantum root uses non-approved algorithm: {quantum_alg}"
                ),
                remediation="Re-anchor ledger with SHA3-512 or BLAKE2b",
            )
            report.violations.append(violation)
            report.critical += 1

    def _check_configuration(
        self,
        report: ComplianceReport,
        signing_alg: str,
        hash_alg: str,
    ) -> None:
        """Verify that default crypto configuration uses approved algorithms."""
        # Check signing algorithm
        report.total_checks += 1
        if self.rotator.is_algorithm_quantum_safe(signing_alg):
            report.passed += 1
        else:
            violation = ComplianceViolation(
                check_name="config_signing_algorithm",
                severity=Severity.CRITICAL,
                description=(
                    f"Default signing algorithm '{signing_alg}' is not quantum-safe"
                ),
                remediation=(
                    "Update PQC_DEFAULT_SIGNING_ALG to ML-KEM-1024, ML-DSA-65, "
                    "or SPHINCS+-SHA2-256f"
                ),
            )
            report.violations.append(violation)
            report.critical += 1

        # Check hash algorithm
        report.total_checks += 1
        approved_hashes = {"SHA3-256", "SHA3-512", "BLAKE2b"}
        if hash_alg in approved_hashes:
            report.passed += 1
        else:
            violation = ComplianceViolation(
                check_name="config_hash_algorithm",
                severity=Severity.CRITICAL,
                description=(
                    f"Default hash algorithm '{hash_alg}' is not quantum-resistant"
                ),
                remediation="Update PQC_DEFAULT_HASH_ALG to SHA3-512 or BLAKE2b",
            )
            report.violations.append(violation)
            report.critical += 1
