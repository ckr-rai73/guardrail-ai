"""Phase 116 adversarial tests for hallucination mitigation."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.hallucination.grounding_engine import GroundingEngine, GroundingResult
from app.hallucination.knowledge_source import KnowledgeSource
from app.hallucination.hallucination_mitigator import HallucinationMitigator
from app.settlement.vector_clock import VectorClockLedger


class MockKnowledgeSource(KnowledgeSource):
    def __init__(self, name: str, responses: dict):
        super().__init__(name)
        self.responses = responses

    async def verify(self, claim: str, context=None):
        return self.responses.get(claim, False)


@pytest.fixture
def grounding_engine():
    sources = [
        MockKnowledgeSource("source1", {"Paris is capital of France": True, "2+2=5": False}),
        MockKnowledgeSource("source2", {"Paris is capital of France": True}),
    ]
    return GroundingEngine(sources, cache_ttl=1)


@pytest.fixture
def ledger():
    return AsyncMock(spec=VectorClockLedger)


@pytest.fixture
def mitigator(grounding_engine, ledger):
    return HallucinationMitigator(grounding_engine, ledger)


@pytest.mark.asyncio
async def test_grounding_engine_verifies_claims(grounding_engine):
    claims = ["Paris is capital of France", "2+2=5"]
    result = await grounding_engine.ground_claims(claims)
    assert isinstance(result, GroundingResult)
    assert "Paris is capital of France" in result.verified_claims
    assert "2+2=5" in result.unverified_claims
    assert result.confidence_score == 0.5
    assert result.latency_ms >= 0
    assert result.grounding_id


@pytest.mark.asyncio
async def test_grounding_engine_cache(grounding_engine):
    claims = ["Paris is capital of France"]
    result1 = await grounding_engine.ground_claims(claims)
    # Second call should hit cache
    result2 = await grounding_engine.ground_claims(claims)
    assert result1.verified_claims == result2.verified_claims
    assert result1.grounding_id != result2.grounding_id  # different timestamps


@pytest.mark.asyncio
async def test_mitigator_high_confidence_allows(mitigator):
    output = "Paris is capital of France."
    result = await mitigator.mitigate(output)
    assert result["action"] == "ALLOW"
    assert result["confidence"] >= 0.85
    assert result["grounding_result"] is not None


@pytest.mark.asyncio
async def test_mitigator_low_confidence_blocks(mitigator):
    output = "2+2=5."
    result = await mitigator.mitigate(output)
    assert result["action"] == "BLOCK"
    assert result["confidence"] < 0.85


@pytest.mark.asyncio
async def test_mitigator_logs_to_ledger(mitigator, ledger):
    output = "Paris is capital of France."
    await mitigator.mitigate(output)
    ledger.append.assert_called_once()


@pytest.mark.asyncio
async def test_performance_below_50ms(grounding_engine):
    claims = ["fact 1", "fact 2", "fact 3"] * 10  # 30 claims
    result = await grounding_engine.ground_claims(claims)
    assert result.latency_ms < 50, f"Latency too high: {result.latency_ms}ms"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
