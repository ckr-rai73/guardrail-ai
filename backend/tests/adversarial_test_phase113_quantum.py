# File: tests/adversarial_test_phase113_quantum.py
"""
Phase 113 – Quantum-Safe Upgrade Adversarial Test Suite
=========================================================
Validates PQC key rotation, ledger re-anchoring, dual-signature
mode, compliance checking, and resistance to quantum attacks.

Run with:  pytest tests/adversarial_test_phase113_quantum.py -v
"""

from __future__ import annotations

import asyncio
import time
from datetime import datetime, timezone, timedelta

import pytest

from app.crypto.pqc_rotator import (
    Algorithm,
    KeyRecord,
    KeyStatus,
    PqcRotator,
    QUANTUM_SAFE_ALGORITHMS,
    _sign,
    _verify,
    _generate_key_pair,
    SignatureBundle,
)
from app.crypto.ledger_re_anchor_orchestrator import (
    LedgerReAnchorOrchestrator,
    LedgerBlock,
    compute_hash,
    compute_merkle_root,
)
from app.crypto.crypto_compliance_checker import (
    CryptoComplianceChecker,
    ComplianceReport,
    Severity,
)


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def rotator():
    """PqcRotator with short grace period for testing."""
    return PqcRotator(grace_period_days=90)


@pytest.fixture
def orchestrator():
    """LedgerReAnchorOrchestrator with small batch size."""
    return LedgerReAnchorOrchestrator(batch_size=100)


@pytest.fixture
def checker(rotator, orchestrator):
    """CryptoComplianceChecker wired to test rotator and orchestrator."""
    return CryptoComplianceChecker(rotator=rotator, orchestrator=orchestrator)


# ======================================================================
# 1. Legacy Signature Break (Quantum Resistance)
# ======================================================================

class TestQuantumResistance:
    """Simulate an attacker trying to forge old-style signatures."""

    def test_legacy_forgery_fails(self):
        """Forged signature must not match the genuine signature."""
        pub, priv = _generate_key_pair(Algorithm.ML_KEM_1024.value)
        data = b"critical governance record"
        genuine_sig = _sign(data, priv, Algorithm.ML_KEM_1024.value)

        # Attacker tries to forge with a different key
        _, attacker_priv = _generate_key_pair(Algorithm.ML_KEM_1024.value)
        forged_sig = _sign(data, attacker_priv, Algorithm.ML_KEM_1024.value)

        # Signatures must differ (different keys)
        assert genuine_sig != forged_sig

    def test_tampered_data_changes_signature(self):
        """Changing even one byte of data must produce a different signature."""
        _, priv = _generate_key_pair(Algorithm.SPHINCS_SHA2_256F.value)
        sig1 = _sign(b"original data", priv, Algorithm.SPHINCS_SHA2_256F.value)
        sig2 = _sign(b"original datb", priv, Algorithm.SPHINCS_SHA2_256F.value)
        assert sig1 != sig2

    def test_algorithm_mismatch_changes_signature(self):
        """Same data and key but different algorithm must produce different signature."""
        _, priv = _generate_key_pair(Algorithm.ML_KEM_1024.value)
        sig1 = _sign(b"test", priv, Algorithm.ML_KEM_1024.value)
        sig2 = _sign(b"test", priv, Algorithm.ML_DSA_65.value)
        assert sig1 != sig2


# ======================================================================
# 2. Key Rotation Lifecycle
# ======================================================================

class TestKeyRotation:
    """Full key rotation lifecycle: generate → rotate → re-sign → retire."""

    @pytest.mark.asyncio
    async def test_generate_new_key(self, rotator):
        """Generating a key returns valid metadata."""
        result = await rotator.rotate_keys("tenant-1", Algorithm.ML_KEM_1024.value)
        assert result["key_id"]
        assert result["algorithm"] == Algorithm.ML_KEM_1024.value
        assert result["status"] == "active"

    @pytest.mark.asyncio
    async def test_rotation_marks_old_keys(self, rotator):
        """Second key rotation marks the first key as ROTATING."""
        r1 = await rotator.rotate_keys("tenant-1")
        r2 = await rotator.rotate_keys("tenant-1")

        keys = rotator.list_keys("tenant-1")
        assert len(keys) == 2
        assert keys[0]["status"] == "rotating"
        assert keys[1]["status"] == "active"

    @pytest.mark.asyncio
    async def test_re_sign_active_records(self, rotator):
        """Re-signing produces dual-signature records."""
        r1 = await rotator.rotate_keys("tenant-1")
        kid1 = r1["key_id"]

        # Store some records
        rotator.store_record("rec-1", "tenant-1", b"data-1")
        rotator.store_record("rec-2", "tenant-1", b"data-2")

        # Rotate to new key
        r2 = await rotator.rotate_keys("tenant-1")
        kid2 = r2["key_id"]

        # Re-sign
        result = await rotator.re_sign_active_records("tenant-1", kid1, kid2)
        assert result["re_signed"] == 2
        assert result["failed"] == 0

        # Verify dual signatures
        rec = rotator._records["rec-1"]
        sb = rec["signature_bundle"]
        assert sb["primary_key_id"] == kid2
        assert sb["secondary_key_id"] == kid1

    @pytest.mark.asyncio
    async def test_retire_key_with_backup(self, rotator):
        """Retiring a key succeeds when records have backup signatures."""
        r1 = await rotator.rotate_keys("tenant-1")
        kid1 = r1["key_id"]
        rotator.store_record("rec-1", "tenant-1", b"data-1")

        r2 = await rotator.rotate_keys("tenant-1")
        kid2 = r2["key_id"]
        await rotator.re_sign_active_records("tenant-1", kid1, kid2)

        result = await rotator.retire_key(kid1)
        assert result["status"] == "retired"

    @pytest.mark.asyncio
    async def test_retire_key_blocks_if_no_backup(self, rotator):
        """Retiring a key fails when records have no backup signature."""
        r1 = await rotator.rotate_keys("tenant-1")
        kid1 = r1["key_id"]
        rotator.store_record("rec-1", "tenant-1", b"data-1")

        with pytest.raises(ValueError, match="no backup signature"):
            await rotator.retire_key(kid1)

    @pytest.mark.asyncio
    async def test_get_current_key(self, rotator):
        """get_current_key returns the latest active key."""
        r1 = await rotator.rotate_keys("tenant-1")
        r2 = await rotator.rotate_keys("tenant-1")

        current = rotator.get_current_key("tenant-1")
        assert current == r2["key_id"]

    def test_quantum_safe_algorithm_check(self, rotator):
        """Algorithm classification is correct."""
        assert rotator.is_algorithm_quantum_safe(Algorithm.ML_KEM_1024.value)
        assert rotator.is_algorithm_quantum_safe(Algorithm.ML_DSA_65.value)
        assert rotator.is_algorithm_quantum_safe(Algorithm.SPHINCS_SHA2_256F.value)
        assert not rotator.is_algorithm_quantum_safe(Algorithm.LEGACY_RSA_4096.value)
        assert not rotator.is_algorithm_quantum_safe(Algorithm.LEGACY_ED25519.value)
        assert not rotator.is_algorithm_quantum_safe("AES-128")


# ======================================================================
# 3. Dual-Signature Verification
# ======================================================================

class TestDualSignature:
    """Dual-signature mode: records signed with both old and new keys."""

    @pytest.mark.asyncio
    async def test_dual_sign_produces_two_signatures(self, rotator):
        """In rotating state, sign_data produces both primary and secondary."""
        await rotator.rotate_keys("tenant-1")
        await rotator.rotate_keys("tenant-1")  # first key → ROTATING

        bundle = rotator.sign_data("tenant-1", b"test-data", dual_sign=True)

        assert bundle.primary_key_id is not None
        assert bundle.primary_signature is not None
        assert bundle.secondary_key_id is not None
        assert bundle.secondary_signature is not None

    @pytest.mark.asyncio
    async def test_single_sign_no_secondary(self, rotator):
        """With only one active key, no secondary signature is produced."""
        await rotator.rotate_keys("tenant-1")

        bundle = rotator.sign_data("tenant-1", b"test-data", dual_sign=True)

        assert bundle.primary_key_id is not None
        assert bundle.secondary_key_id is None

    @pytest.mark.asyncio
    async def test_keychain_verification(self, rotator):
        """Keychain verification tries all active keys."""
        r1 = await rotator.rotate_keys("tenant-1")
        kid1 = r1["key_id"]
        key1 = rotator.get_key(kid1)

        data = b"verify-this"
        sig = _sign(data, key1.private_key, key1.algorithm)

        verified, matched_kid = rotator.verify_signature_with_keychain(
            data, sig, "tenant-1",
        )
        assert verified is True
        assert matched_kid == kid1


# ======================================================================
# 4. Ledger Re-Anchoring Integrity
# ======================================================================

class TestLedgerReAnchoring:
    """Re-anchor the ledger and verify historical blocks."""

    @pytest.mark.asyncio
    async def test_re_anchor_empty_ledger(self, orchestrator):
        """Re-anchoring an empty ledger completes without error."""
        result = await orchestrator.re_anchor_all()
        assert result["status"] == "empty"
        assert result["blocks_processed"] == 0

    @pytest.mark.asyncio
    async def test_re_anchor_produces_dual_root(self, orchestrator):
        """Re-anchoring produces both legacy and quantum-safe roots."""
        for i in range(10):
            orchestrator.append_block(f"block-data-{i}".encode())

        result = await orchestrator.re_anchor_all("SHA3-512")

        assert result["status"] == "completed"
        assert result["blocks_processed"] == 10
        assert result["legacy_root"]
        assert result["quantum_root"]
        assert result["legacy_root"] != result["quantum_root"]

    @pytest.mark.asyncio
    async def test_verify_block_legacy(self, orchestrator):
        """Blocks can be verified using the legacy algorithm."""
        orchestrator.append_block(b"test-data")
        block = orchestrator._blocks[0]

        result = await orchestrator.verify_block(block.block_id, "legacy")
        assert result["verified"] is True
        assert result["algorithm"] == "SHA3-256"

    @pytest.mark.asyncio
    async def test_verify_block_quantum(self, orchestrator):
        """After re-anchoring, blocks verify with the new algorithm too."""
        orchestrator.append_block(b"test-data")
        block = orchestrator._blocks[0]

        await orchestrator.re_anchor_all("SHA3-512")

        result = await orchestrator.verify_block(block.block_id, "SHA3-512")
        assert result["verified"] is True
        assert result["algorithm"] == "SHA3-512"

    @pytest.mark.asyncio
    async def test_dual_root_returned(self, orchestrator):
        """get_dual_root returns both roots after re-anchoring."""
        orchestrator.append_block(b"data-1")
        orchestrator.append_block(b"data-2")
        await orchestrator.re_anchor_all("SHA3-512")

        dual = await orchestrator.get_dual_root()
        assert dual is not None
        assert dual["legacy_algorithm"] == "SHA3-256"
        assert dual["quantum_algorithm"] == "SHA3-512"
        assert dual["block_count"] == 2

    @pytest.mark.asyncio
    async def test_migration_mapping_created(self, orchestrator):
        """Each block gets a migration record linking old and new hashes."""
        orchestrator.append_block(b"data")
        block = orchestrator._blocks[0]
        await orchestrator.re_anchor_all("SHA3-512")

        migration = orchestrator.get_migration(block.block_id)
        assert migration is not None
        assert migration.old_hash == block.hash
        assert migration.old_algorithm == "SHA3-256"
        assert migration.new_algorithm == "SHA3-512"
        assert migration.new_hash != migration.old_hash

    def test_merkle_root_deterministic(self):
        """Same inputs produce the same Merkle root."""
        hashes = [compute_hash(f"data-{i}".encode()) for i in range(8)]
        root1 = compute_merkle_root(hashes, "SHA3-512")
        root2 = compute_merkle_root(hashes, "SHA3-512")
        assert root1 == root2

    def test_merkle_root_changes_with_data(self):
        """Different inputs produce different Merkle roots."""
        h1 = [compute_hash(b"a"), compute_hash(b"b")]
        h2 = [compute_hash(b"a"), compute_hash(b"c")]
        assert compute_merkle_root(h1) != compute_merkle_root(h2)


# ======================================================================
# 5. Compliance Checker
# ======================================================================

class TestComplianceChecker:
    """Compliance auditor detects weak algorithms and configuration drift."""

    @pytest.mark.asyncio
    async def test_clean_audit_passes(self, checker, rotator, orchestrator):
        """A properly configured system passes all checks."""
        await rotator.rotate_keys("tenant-1", Algorithm.ML_KEM_1024.value)
        rotator.store_record("rec-1", "tenant-1", b"data")
        orchestrator.append_block(b"block")
        await orchestrator.re_anchor_all("SHA3-512")

        report = await checker.run_audit()
        assert report.compliant is True
        assert report.critical == 0

    @pytest.mark.asyncio
    async def test_detects_weak_signing_algorithm(self, checker):
        """Injecting a weak algorithm into config triggers a CRITICAL violation."""
        report = await checker.run_audit(config_overrides={
            "PQC_DEFAULT_SIGNING_ALG": "RSA-4096",
        })
        assert report.compliant is False
        assert report.critical >= 1

        alg_violations = [
            v for v in report.violations
            if v.check_name == "config_signing_algorithm"
        ]
        assert len(alg_violations) == 1
        assert "RSA-4096" in alg_violations[0].description

    @pytest.mark.asyncio
    async def test_detects_weak_hash_algorithm(self, checker):
        """Injecting a weak hash algorithm triggers a violation."""
        report = await checker.run_audit(config_overrides={
            "PQC_DEFAULT_HASH_ALG": "MD5",
        })
        violations = [v for v in report.violations if v.check_name == "config_hash_algorithm"]
        assert len(violations) == 1
        assert "MD5" in violations[0].description

    @pytest.mark.asyncio
    async def test_detects_legacy_key(self, checker, rotator):
        """A key using a legacy algorithm triggers a CRITICAL violation."""
        await rotator.rotate_keys("tenant-1", Algorithm.LEGACY_RSA_4096.value)

        report = await checker.run_audit()
        key_violations = [v for v in report.violations if v.check_name == "key_algorithm_audit"]
        assert len(key_violations) == 1
        assert key_violations[0].severity == Severity.CRITICAL

    @pytest.mark.asyncio
    async def test_detects_unreanchored_ledger(self, checker, orchestrator):
        """A ledger with blocks but no re-anchor triggers a warning."""
        orchestrator.append_block(b"unanchored-data")

        report = await checker.run_audit()
        ledger_violations = [
            v for v in report.violations if v.check_name == "ledger_integrity_audit"
        ]
        assert len(ledger_violations) == 1
        assert ledger_violations[0].severity == Severity.WARNING


# ======================================================================
# 6. Performance: Large-Scale Re-Anchoring
# ======================================================================

class TestPerformance:
    """Re-anchoring should handle large batches efficiently."""

    @pytest.mark.asyncio
    async def test_reanchor_10k_blocks(self):
        """Re-anchoring 10,000 blocks completes within 30 seconds."""
        orch = LedgerReAnchorOrchestrator(batch_size=1000)

        for i in range(10_000):
            orch.append_block(f"block-{i}-data".encode())

        start = time.monotonic()
        result = await orch.re_anchor_all("SHA3-512")
        duration = time.monotonic() - start

        assert result["status"] == "completed"
        assert result["blocks_processed"] == 10_000
        assert duration < 30, f"Re-anchoring took {duration:.1f}s (max 30s)"

        # Verify a random block
        block = orch._blocks[5_000]
        verify = await orch.verify_block(block.block_id, "SHA3-512")
        assert verify["verified"] is True


# ======================================================================
# 7. Hash Function Correctness
# ======================================================================

class TestHashFunctions:
    """Verify hash function implementations."""

    def test_sha3_256_deterministic(self):
        assert compute_hash(b"test", "SHA3-256") == compute_hash(b"test", "SHA3-256")

    def test_sha3_512_deterministic(self):
        assert compute_hash(b"test", "SHA3-512") == compute_hash(b"test", "SHA3-512")

    def test_different_algorithms_different_output(self):
        h256 = compute_hash(b"test", "SHA3-256")
        h512 = compute_hash(b"test", "SHA3-512")
        assert h256 != h512

    def test_unsupported_algorithm_raises(self):
        with pytest.raises(ValueError, match="Unsupported"):
            compute_hash(b"test", "QUANTUM-MAGIC-9000")

    def test_blake2b_supported(self):
        h = compute_hash(b"test", "BLAKE2b")
        assert len(h) > 0
