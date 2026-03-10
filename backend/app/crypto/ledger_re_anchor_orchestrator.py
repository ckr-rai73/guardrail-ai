# File: app/crypto/ledger_re_anchor_orchestrator.py
"""
Phase 113 – Ledger Re-Anchoring Orchestrator
===============================================
Recalculates Merkle roots for the entire historical audit trail
using quantum-safe hash algorithms, while preserving the ability
to verify blocks via the legacy chain.

Architecture:
  • The existing ledger (vector_clock.py) stores blocks as a
    linear chain with SHA3-256 hashes.
  • This orchestrator:
      1. Traverses all blocks in order.
      2. Computes new hashes using the target algorithm (SHA3-512).
      3. Builds a parallel Merkle tree with the new hashes.
      4. Stores a mapping (old_hash → new_hash) for dual verification.
      5. Produces a new quantum-safe root alongside the legacy root.
"""

from __future__ import annotations

import hashlib
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("guardrail.crypto.reanchor")


# ======================================================================
# Data models
# ======================================================================

@dataclass
class LedgerBlock:
    """A single block in the audit ledger."""
    block_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    data: bytes = b""
    previous_hash: str = ""
    hash: str = ""               # legacy hash
    algorithm: str = "SHA3-256"
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


@dataclass
class BlockMigration:
    """Mapping from legacy hash to quantum-safe hash for a block."""
    block_id: str
    old_hash: str
    old_algorithm: str
    new_hash: str
    new_algorithm: str
    migrated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


@dataclass
class DualRoot:
    """Pair of Merkle roots for legacy and quantum-safe chains."""
    legacy_root: str
    legacy_algorithm: str
    quantum_root: str
    quantum_algorithm: str
    block_count: int
    anchored_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
    )


# ======================================================================
# Hash functions
# ======================================================================

_HASH_FUNCTIONS = {
    "SHA3-256": lambda data: hashlib.sha3_256(data).hexdigest(),
    "SHA3-512": lambda data: hashlib.sha3_512(data).hexdigest(),
    "SHA-256": lambda data: hashlib.sha256(data).hexdigest(),
    "SHA-512": lambda data: hashlib.sha512(data).hexdigest(),
    "BLAKE2b": lambda data: hashlib.blake2b(data).hexdigest(),
}


def compute_hash(data: bytes, algorithm: str = "SHA3-512") -> str:
    """Compute a hash using the specified algorithm."""
    fn = _HASH_FUNCTIONS.get(algorithm)
    if not fn:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    return fn(data)


def compute_merkle_root(hashes: List[str], algorithm: str = "SHA3-512") -> str:
    """
    Compute a Merkle root from a list of leaf hashes.

    Uses bottom-up binary tree construction.
    """
    if not hashes:
        return compute_hash(b"empty", algorithm)

    current_level = list(hashes)

    while len(current_level) > 1:
        next_level: List[str] = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            combined = (left + right).encode()
            next_level.append(compute_hash(combined, algorithm))
        current_level = next_level

    return current_level[0]


# ======================================================================
# Orchestrator
# ======================================================================

class LedgerReAnchorOrchestrator:
    """
    Orchestrates re-anchoring of the Merkle audit trail.

    Parameters
    ----------
    batch_size : int
        Number of blocks to process per batch.
    """

    def __init__(self, batch_size: int = 1000) -> None:
        self.batch_size = batch_size
        # In-memory ledger (replace with DB cursor in production)
        self._blocks: List[LedgerBlock] = []
        self._migrations: Dict[str, BlockMigration] = {}
        self._dual_root: Optional[DualRoot] = None

    # ------------------------------------------------------------------
    # Ledger management (simulation)
    # ------------------------------------------------------------------

    def append_block(self, data: bytes, algorithm: str = "SHA3-256") -> LedgerBlock:
        """Append a new block to the ledger."""
        previous_hash = self._blocks[-1].hash if self._blocks else "genesis"
        block_data = previous_hash.encode() + data
        block_hash = compute_hash(block_data, algorithm)

        block = LedgerBlock(
            data=data,
            previous_hash=previous_hash,
            hash=block_hash,
            algorithm=algorithm,
        )
        self._blocks.append(block)
        return block

    def get_block(self, block_id: str) -> Optional[LedgerBlock]:
        """Get a block by ID."""
        for b in self._blocks:
            if b.block_id == block_id:
                return b
        return None

    @property
    def block_count(self) -> int:
        return len(self._blocks)

    # ------------------------------------------------------------------
    # Re-anchoring
    # ------------------------------------------------------------------

    async def re_anchor_all(
        self,
        new_hash_algorithm: str = "SHA3-512",
    ) -> dict:
        """
        Re-anchor the entire ledger with a quantum-safe hash algorithm.

        Traverses all blocks, computes new hashes, builds a parallel
        Merkle tree, and stores the mapping.
        """
        start_time = time.monotonic()
        total = len(self._blocks)

        if total == 0:
            return {
                "status": "empty",
                "blocks_processed": 0,
                "duration_seconds": 0,
            }

        logger.info(
            "[ReAnchor] Starting re-anchor of %d blocks with %s",
            total, new_hash_algorithm,
        )

        new_hashes: List[str] = []
        legacy_hashes: List[str] = []
        batches_processed = 0

        for i, block in enumerate(self._blocks):
            # Compute new hash for this block
            block_data = block.previous_hash.encode() + block.data
            new_hash = compute_hash(block_data, new_hash_algorithm)

            # Store migration mapping
            migration = BlockMigration(
                block_id=block.block_id,
                old_hash=block.hash,
                old_algorithm=block.algorithm,
                new_hash=new_hash,
                new_algorithm=new_hash_algorithm,
            )
            self._migrations[block.block_id] = migration

            new_hashes.append(new_hash)
            legacy_hashes.append(block.hash)

            if (i + 1) % self.batch_size == 0:
                batches_processed += 1
                logger.info(
                    "[ReAnchor] Processed batch %d (%d/%d blocks)",
                    batches_processed, i + 1, total,
                )

        # Build Merkle roots
        legacy_root = compute_merkle_root(legacy_hashes, "SHA3-256")
        quantum_root = compute_merkle_root(new_hashes, new_hash_algorithm)

        self._dual_root = DualRoot(
            legacy_root=legacy_root,
            legacy_algorithm="SHA3-256",
            quantum_root=quantum_root,
            quantum_algorithm=new_hash_algorithm,
            block_count=total,
        )

        duration = time.monotonic() - start_time

        logger.info(
            "[ReAnchor] Complete – %d blocks, legacy_root=%s…, "
            "quantum_root=%s…, %.2fs",
            total, legacy_root[:16], quantum_root[:16], duration,
        )

        return {
            "status": "completed",
            "blocks_processed": total,
            "legacy_root": legacy_root,
            "quantum_root": quantum_root,
            "algorithm": new_hash_algorithm,
            "duration_seconds": round(duration, 3),
        }

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    async def verify_block(
        self,
        block_id: str,
        algorithm: str = "legacy",
    ) -> dict:
        """
        Verify a block using either the legacy or quantum-safe algorithm.

        Returns verification result with the computed and expected hashes.
        """
        block = self.get_block(block_id)
        if not block:
            return {"verified": False, "error": "Block not found"}

        block_data = block.previous_hash.encode() + block.data

        if algorithm == "legacy" or algorithm == block.algorithm:
            expected = block.hash
            computed = compute_hash(block_data, block.algorithm)
            verified = computed == expected
            return {
                "verified": verified,
                "algorithm": block.algorithm,
                "expected": expected,
                "computed": computed,
            }
        else:
            # Verify using re-anchored hash
            migration = self._migrations.get(block_id)
            if not migration:
                return {"verified": False, "error": "Block not re-anchored yet"}

            computed = compute_hash(block_data, migration.new_algorithm)
            verified = computed == migration.new_hash
            return {
                "verified": verified,
                "algorithm": migration.new_algorithm,
                "expected": migration.new_hash,
                "computed": computed,
            }

    async def get_dual_root(self) -> Optional[dict]:
        """
        Get the current dual-root (legacy + quantum-safe) for
        external anchoring or attestation.
        """
        if not self._dual_root:
            return None

        return {
            "legacy_root": self._dual_root.legacy_root,
            "legacy_algorithm": self._dual_root.legacy_algorithm,
            "quantum_root": self._dual_root.quantum_root,
            "quantum_algorithm": self._dual_root.quantum_algorithm,
            "block_count": self._dual_root.block_count,
            "anchored_at": self._dual_root.anchored_at,
        }

    def get_migration(self, block_id: str) -> Optional[BlockMigration]:
        """Get the migration record for a specific block."""
        return self._migrations.get(block_id)
