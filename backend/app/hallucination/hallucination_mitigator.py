"""Hallucination Mitigator wraps Shadow Model and Grounding Engine."""

import logging
from typing import Any, Dict, Optional

from app.core.config import settings
from app.settlement.vector_clock import VectorClockLedger
from .grounding_engine import GroundingEngine, GroundingResult

logger = logging.getLogger(__name__)


class HallucinationMitigator:
    """
    Verifies agent outputs for factual accuracy before final decision.
    """

    def __init__(self, grounding_engine: GroundingEngine, ledger: VectorClockLedger):
        self.grounding_engine = grounding_engine
        self.ledger = ledger
        self.min_confidence = settings.HALLUCINATION_MIN_CONFIDENCE

    async def mitigate(self, agent_output: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Extract claims from output, ground them, and return mitigation result.
        Returns a dict with:
          - confidence: float
          - action: "ALLOW" | "FLAG" | "BLOCK"
          - grounding_result: GroundingResult
          - audit_record: reference to ledger entry
        """
        # Simple claim extraction: split sentences for demo
        claims = [s.strip() for s in agent_output.split('.') if s.strip()]

        grounding_result = await self.grounding_engine.ground_claims(claims, context)

        # Determine action based on confidence
        if grounding_result.confidence_score >= self.min_confidence:
            action = "ALLOW"
        elif grounding_result.confidence_score >= self.min_confidence - 0.2:
            action = "FLAG"  # human review
        else:
            action = "BLOCK"

        # Log to immutable ledger
        audit_entry = {
            "event": "hallucination_mitigation",
            "grounding_id": grounding_result.grounding_id,
            "confidence": grounding_result.confidence_score,
            "action": action,
            "verified_count": len(grounding_result.verified_claims),
            "unverified_count": len(grounding_result.unverified_claims),
            "timestamp": context.get("timestamp") if context else None
        }
        await self.ledger.append(audit_entry)

        return {
            "confidence": grounding_result.confidence_score,
            "action": action,
            "grounding_result": grounding_result,
            "audit_record": audit_entry
        }
