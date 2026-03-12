"""Grounding Engine for fact verification against trusted knowledge sources."""

import asyncio
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel


class GroundingResult(BaseModel):
    """Result of grounding a set of claims."""
    verified_claims: List[str]
    unverified_claims: List[str]
    confidence_score: float
    grounding_sources: List[str]
    latency_ms: float
    grounding_id: str  # unique hash for audit trail


class GroundingEngine:
    """
    Verifies claims against configured knowledge sources.
    """

    def __init__(self, sources: List["KnowledgeSource"], cache_ttl: int = 3600):
        self.sources = sources
        self.cache_ttl = cache_ttl
        self._cache = {}

    async def ground_claims(self, claims: List[str], context: Optional[Dict] = None) -> GroundingResult:
        """
        Verify a list of claims against all knowledge sources.
        Returns a GroundingResult with verified/unverified claims and confidence.
        """
        start = time.time()
        verified: Set[str] = set()
        unverified: Set[str] = set()
        used_sources: Set[str] = set()

        # Deduplicate claims
        unique_claims = set(claims)

        for claim in unique_claims:
            # Check cache first
            if claim in self._cache:
                cached = self._cache[claim]
                if time.time() - cached["timestamp"] < self.cache_ttl:
                    if cached["verified"]:
                        verified.add(claim)
                        used_sources.update(cached["sources"])
                    else:
                        unverified.add(claim)
                    continue

            # Query each source in parallel
            tasks = [source.verify(claim, context) for source in self.sources]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            claim_verified = False
            for source, result in zip(self.sources, results):
                if isinstance(result, Exception):
                    # Log error but continue
                    continue
                if result:  # True means source supports the claim
                    claim_verified = True
                    used_sources.add(source.name)

            if claim_verified:
                verified.add(claim)
                self._cache[claim] = {
                    "verified": True,
                    "sources": list(used_sources),
                    "timestamp": time.time()
                }
            else:
                unverified.add(claim)
                self._cache[claim] = {
                    "verified": False,
                    "sources": [],
                    "timestamp": time.time()
                }

        confidence = len(verified) / (len(verified) + len(unverified)) if (verified or unverified) else 0.0
        latency = (time.time() - start) * 1000  # ms

        # Generate a unique grounding ID for audit
        grounding_id = hashlib.sha256(
            json.dumps({
                "verified": sorted(list(verified)),
                "unverified": sorted(list(unverified)),
                "timestamp": time.time()
            }).encode()
        ).hexdigest()

        return GroundingResult(
            verified_claims=list(verified),
            unverified_claims=list(unverified),
            confidence_score=confidence,
            grounding_sources=list(used_sources),
            latency_ms=latency,
            grounding_id=grounding_id
        )
