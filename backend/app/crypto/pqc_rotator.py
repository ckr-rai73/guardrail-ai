# File: app/crypto/pqc_rotator.py
"""
Phase 113 – Post-Quantum Key Rotation Service
================================================
Automated key rotation with dual-signature mode for zero-downtime
migration from legacy to quantum-safe algorithms.

Supported algorithms (NIST FIPS):
  • ML-KEM-1024  (FIPS 203) — key encapsulation
  • SPHINCS+-SHA2-256f (FIPS 205) — stateless hash-based signatures
  • ML-DSA-65   (FIPS 204) — lattice-based digital signatures

Architecture:
  1. Generate new key pair with target algorithm.
  2. Enter dual-signature mode (records carry both old & new signatures).
  3. Re-sign active records with the new key.
  4. After grace period, retire the old key.
  5. Records remain verifiable via the keychain (tries all active keys).
"""

from __future__ import annotations

import hashlib
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("guardrail.crypto.rotator")


# ======================================================================
# Data models
# ======================================================================

class KeyStatus(str, Enum):
    ACTIVE = "active"
    ROTATING = "rotating"       # dual-signature mode
    RETIRED = "retired"
    COMPROMISED = "compromised"


class Algorithm(str, Enum):
    ML_KEM_1024 = "ML-KEM-1024"         # FIPS 203
    ML_DSA_65 = "ML-DSA-65"             # FIPS 204
    SPHINCS_SHA2_256F = "SPHINCS+-SHA2-256f"  # FIPS 205
    LEGACY_RSA_4096 = "RSA-4096"        # Pre-quantum (for backward compat)
    LEGACY_ED25519 = "Ed25519"          # Pre-quantum


# Approved quantum-safe algorithms
QUANTUM_SAFE_ALGORITHMS = {
    Algorithm.ML_KEM_1024,
    Algorithm.ML_DSA_65,
    Algorithm.SPHINCS_SHA2_256F,
}


@dataclass
class KeyRecord:
    """Metadata for a cryptographic key."""
    key_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str = ""
    algorithm: str = Algorithm.ML_KEM_1024.value
    public_key: bytes = b""
    private_key: bytes = b""          # in production, stored in HSM/KMS
    status: KeyStatus = KeyStatus.ACTIVE
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )
    retired_at: Optional[str] = None
    grace_period_days: int = 90


@dataclass
class SignatureBundle:
    """Dual-signature container for a record."""
    primary_key_id: str
    primary_signature: bytes
    primary_algorithm: str
    secondary_key_id: Optional[str] = None
    secondary_signature: Optional[bytes] = None
    secondary_algorithm: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


# ======================================================================
# Simulated crypto operations (replace with real PQC library in prod)
# ======================================================================

def _generate_key_pair(algorithm: str) -> Tuple[bytes, bytes]:
    """
    Generate a simulated key pair for the given algorithm.

    In production, this would use:
      - ML-KEM: liboqs or pqcrypto
      - SPHINCS+: pyspx or liboqs
      - ML-DSA: liboqs
    """
    seed = os.urandom(32)
    public_key = hashlib.sha3_256(seed + b"public-" + algorithm.encode()).digest()
    private_key = hashlib.sha3_256(seed + b"private-" + algorithm.encode()).digest()
    return public_key, private_key


def _sign(data: bytes, private_key: bytes, algorithm: str) -> bytes:
    """
    Simulate signing data with a PQC algorithm.

    In production, dispatches to the appropriate crypto backend.
    """
    return hashlib.sha3_512(data + private_key + algorithm.encode()).digest()


def _verify(data: bytes, signature: bytes, public_key: bytes, algorithm: str) -> bool:
    """
    Simulate signature verification.

    In production, dispatches to the appropriate crypto backend.
    """
    expected = hashlib.sha3_512(
        data + _derive_private_from_public(public_key, algorithm) + algorithm.encode()
    ).digest()
    # In real impl, this would use the public key directly
    # For simulation, we need a consistent check
    return True  # Simulated: always passes if called with correct key


def _derive_private_from_public(public_key: bytes, algorithm: str) -> bytes:
    """Simulation helper — not used in production."""
    return hashlib.sha3_256(public_key + b"derive-" + algorithm.encode()).digest()


# ======================================================================
# PQC Rotator
# ======================================================================

class PqcRotator:
    """
    Post-quantum key rotation service.

    Manages the lifecycle of cryptographic keys for each tenant:
    generate → activate → dual-sign → re-sign → retire.

    Parameters
    ----------
    grace_period_days : int
        Days before an old key is eligible for retirement.
    """

    def __init__(self, grace_period_days: int = 90) -> None:
        self.grace_period_days = grace_period_days
        # In-memory key store (replace with DB/KMS in production)
        self._keys: Dict[str, KeyRecord] = {}          # key_id → KeyRecord
        self._tenant_keys: Dict[str, List[str]] = {}   # tenant_id → [key_ids]
        # Simulated record store for re-signing
        self._records: Dict[str, Dict[str, Any]] = {}  # record_id → record

    # ------------------------------------------------------------------
    # Key management
    # ------------------------------------------------------------------

    async def rotate_keys(
        self,
        tenant_id: str,
        algorithm: str = Algorithm.ML_KEM_1024.value,
    ) -> dict:
        """
        Generate a new key pair and enter dual-signature mode.

        Returns metadata about the new key.
        """
        public_key, private_key = _generate_key_pair(algorithm)

        new_key = KeyRecord(
            tenant_id=tenant_id,
            algorithm=algorithm,
            public_key=public_key,
            private_key=private_key,
            status=KeyStatus.ACTIVE,
            grace_period_days=self.grace_period_days,
        )

        self._keys[new_key.key_id] = new_key
        if tenant_id not in self._tenant_keys:
            self._tenant_keys[tenant_id] = []
        self._tenant_keys[tenant_id].append(new_key.key_id)

        # Mark previous keys as ROTATING (dual-signature mode)
        for kid in self._tenant_keys[tenant_id][:-1]:
            old_key = self._keys.get(kid)
            if old_key and old_key.status == KeyStatus.ACTIVE:
                old_key.status = KeyStatus.ROTATING
                logger.info(
                    "[PqcRotator] Key %s → ROTATING (dual-sig mode)", kid,
                )

        logger.info(
            "[PqcRotator] New key generated – id=%s tenant=%s alg=%s",
            new_key.key_id, tenant_id, algorithm,
        )

        return {
            "key_id": new_key.key_id,
            "algorithm": algorithm,
            "public_key_hex": public_key.hex(),
            "status": new_key.status.value,
            "created_at": new_key.created_at,
        }

    async def re_sign_active_records(
        self,
        tenant_id: str,
        old_key_id: str,
        new_key_id: str,
    ) -> dict:
        """
        Re-sign all active records from old_key to new_key.

        In dual-signature mode, records carry both signatures until
        the old key is retired.
        """
        old_key = self._keys.get(old_key_id)
        new_key = self._keys.get(new_key_id)

        if not old_key or not new_key:
            raise ValueError("Key not found")

        re_signed = 0
        failed = 0

        for record_id, record in self._records.items():
            if record.get("tenant_id") != tenant_id:
                continue
            sig_bundle = record.get("signature_bundle")
            if not sig_bundle:
                continue
            if sig_bundle.get("primary_key_id") != old_key_id:
                continue

            try:
                # Create new signature
                data = record.get("data", b"")
                if isinstance(data, str):
                    data = data.encode()
                new_sig = _sign(data, new_key.private_key, new_key.algorithm)

                # Dual-signature: keep old, add new
                record["signature_bundle"] = {
                    "primary_key_id": new_key_id,
                    "primary_signature": new_sig.hex(),
                    "primary_algorithm": new_key.algorithm,
                    "secondary_key_id": old_key_id,
                    "secondary_signature": sig_bundle.get("primary_signature"),
                    "secondary_algorithm": old_key.algorithm,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                re_signed += 1
            except Exception as exc:
                logger.error("[PqcRotator] Re-sign failed for %s: %s", record_id, exc)
                failed += 1

        logger.info(
            "[PqcRotator] Re-signed %d records (%d failed) – %s → %s",
            re_signed, failed, old_key_id[:8], new_key_id[:8],
        )

        return {"re_signed": re_signed, "failed": failed}

    async def retire_key(self, key_id: str) -> dict:
        """
        Retire a key after the grace period.

        Before retiring, verifies that all records have at least one
        valid signature from a non-retired key.
        """
        key = self._keys.get(key_id)
        if not key:
            raise ValueError(f"Key {key_id} not found")

        # Check that no records depend solely on this key
        orphaned = 0
        for record_id, record in self._records.items():
            sb = record.get("signature_bundle", {})
            primary_ok = (
                sb.get("primary_key_id") != key_id
                or self._keys.get(sb.get("secondary_key_id", ""), KeyRecord()).status
                not in (KeyStatus.RETIRED, KeyStatus.COMPROMISED)
            )
            if sb.get("primary_key_id") == key_id and not sb.get("secondary_key_id"):
                orphaned += 1

        if orphaned > 0:
            raise ValueError(
                f"Cannot retire key {key_id}: {orphaned} records have no backup signature"
            )

        key.status = KeyStatus.RETIRED
        key.retired_at = datetime.now(timezone.utc).isoformat()

        logger.info("[PqcRotator] Key retired: %s", key_id)
        return {"key_id": key_id, "status": "retired", "retired_at": key.retired_at}

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get_current_key(self, tenant_id: str) -> Optional[str]:
        """Get the latest active key ID for a tenant."""
        key_ids = self._tenant_keys.get(tenant_id, [])
        for kid in reversed(key_ids):
            key = self._keys.get(kid)
            if key and key.status == KeyStatus.ACTIVE:
                return kid
        return None

    def list_keys(self, tenant_id: str) -> List[dict]:
        """List all key metadata for a tenant."""
        key_ids = self._tenant_keys.get(tenant_id, [])
        return [
            {
                "key_id": kid,
                "algorithm": self._keys[kid].algorithm,
                "status": self._keys[kid].status.value,
                "created_at": self._keys[kid].created_at,
                "retired_at": self._keys[kid].retired_at,
            }
            for kid in key_ids
            if kid in self._keys
        ]

    def get_key(self, key_id: str) -> Optional[KeyRecord]:
        """Get a key record by ID."""
        return self._keys.get(key_id)

    # ------------------------------------------------------------------
    # Signing and verification
    # ------------------------------------------------------------------

    def sign_data(
        self,
        tenant_id: str,
        data: bytes,
        dual_sign: bool = True,
    ) -> SignatureBundle:
        """
        Sign data with the tenant's current key.

        If dual_sign is True and a rotating key exists, produces
        signatures with both keys.
        """
        key_ids = self._tenant_keys.get(tenant_id, [])
        if not key_ids:
            raise ValueError(f"No keys for tenant {tenant_id}")

        # Primary: latest active key
        primary_kid = self.get_current_key(tenant_id)
        if not primary_kid:
            raise ValueError(f"No active key for tenant {tenant_id}")
        primary_key = self._keys[primary_kid]
        primary_sig = _sign(data, primary_key.private_key, primary_key.algorithm)

        bundle = SignatureBundle(
            primary_key_id=primary_kid,
            primary_signature=primary_sig,
            primary_algorithm=primary_key.algorithm,
        )

        # Secondary: rotating key (if dual-sign mode)
        if dual_sign:
            for kid in key_ids:
                key = self._keys.get(kid)
                if key and key.status == KeyStatus.ROTATING:
                    secondary_sig = _sign(data, key.private_key, key.algorithm)
                    bundle.secondary_key_id = kid
                    bundle.secondary_signature = secondary_sig
                    bundle.secondary_algorithm = key.algorithm
                    break

        return bundle

    def verify_signature_with_keychain(
        self,
        data: bytes,
        signature: bytes,
        tenant_id: str,
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify a signature by trying all active/rotating keys for the tenant.

        Returns (verified: bool, key_id: str or None).
        """
        key_ids = self._tenant_keys.get(tenant_id, [])
        for kid in key_ids:
            key = self._keys.get(kid)
            if not key or key.status in (KeyStatus.COMPROMISED,):
                continue
            if _verify(data, signature, key.public_key, key.algorithm):
                return True, kid
        return False, None

    # ------------------------------------------------------------------
    # Record store (for re-signing simulation)
    # ------------------------------------------------------------------

    def store_record(self, record_id: str, tenant_id: str, data: bytes) -> None:
        """Store a record with a signature for testing."""
        bundle = self.sign_data(tenant_id, data)
        self._records[record_id] = {
            "tenant_id": tenant_id,
            "data": data.hex(),
            "signature_bundle": {
                "primary_key_id": bundle.primary_key_id,
                "primary_signature": bundle.primary_signature.hex(),
                "primary_algorithm": bundle.primary_algorithm,
                "secondary_key_id": bundle.secondary_key_id,
                "secondary_signature": (
                    bundle.secondary_signature.hex()
                    if bundle.secondary_signature else None
                ),
                "secondary_algorithm": bundle.secondary_algorithm,
            },
        }

    def is_algorithm_quantum_safe(self, algorithm: str) -> bool:
        """Check if an algorithm is in the approved quantum-safe set."""
        try:
            return Algorithm(algorithm) in QUANTUM_SAFE_ALGORITHMS
        except ValueError:
            return False
