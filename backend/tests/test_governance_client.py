# File: tests/test_governance_client.py
"""
Phase 111 – RealGovernanceClient Test Suite
=============================================
Tests the HTTP governance client that replaces the stub facade.

Run with:  pytest tests/test_governance_client.py -v
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import pytest_asyncio

from app.cloud.cloud_connector_base import (
    Decision,
    GovernanceAPIError,
    RealGovernanceClient,
)


# ======================================================================
# Fixtures
# ======================================================================

@pytest_asyncio.fixture
async def client():
    """Create a RealGovernanceClient with a mocked httpx client."""
    gc = RealGovernanceClient(
        base_url="http://guardrail-core:8080",
        api_key="test-api-key-xyz",
    )

    mock_http = AsyncMock(spec=httpx.AsyncClient)
    mock_http.aclose = AsyncMock()
    gc._client = mock_http

    yield gc

    await gc.close()


# ======================================================================
# Test Cases
# ======================================================================

@pytest.mark.asyncio
async def test_assess_success(client):
    """
    200 response with valid decision → returns Decision with correct fields.
    """
    client._client.post = AsyncMock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "action": "ALLOW",
                "reason": "All policies satisfied",
                "modifications": {},
            },
            headers={"content-type": "application/json"},
        ),
    )

    context = {"service": "sagemaker", "tenant_id": "acme", "method": "POST"}
    decision = await client.assess(context)

    assert isinstance(decision, Decision)
    assert decision.action == "ALLOW"
    assert decision.reason == "All policies satisfied"
    assert decision.modifications == {}

    # Verify the request was sent correctly
    call_kwargs = client._client.post.call_args
    assert "/api/v1/governance/assess" in call_kwargs.args[0]
    assert call_kwargs.kwargs["headers"]["X-API-Key"] == "test-api-key-xyz"
    assert call_kwargs.kwargs["json"] == context


@pytest.mark.asyncio
async def test_assess_success_modify(client):
    """
    200 response with MODIFY decision → modifications parsed correctly.
    """
    client._client.post = AsyncMock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "action": "MODIFY",
                "reason": "Redacting PII fields",
                "modifications": {"redact_fields": ["ssn", "dob"]},
            },
            headers={"content-type": "application/json"},
        ),
    )

    decision = await client.assess({"service": "bedrock"})

    assert decision.action == "MODIFY"
    assert decision.modifications == {"redact_fields": ["ssn", "dob"]}


@pytest.mark.asyncio
async def test_assess_error_status(client):
    """
    Non-200 response (e.g. 403 or 500) → raises GovernanceAPIError.
    """
    client._client.post = AsyncMock(
        return_value=httpx.Response(
            status_code=403,
            text="Forbidden: invalid API key",
            headers={"content-type": "text/plain"},
        ),
    )

    with pytest.raises(GovernanceAPIError) as exc_info:
        await client.assess({"service": "bedrock"})

    assert "403" in str(exc_info.value)


@pytest.mark.asyncio
async def test_assess_invalid_json(client):
    """
    200 response with malformed JSON → raises GovernanceAPIError.
    """
    # Create a response with invalid JSON content
    response = httpx.Response(
        status_code=200,
        content=b"not-valid-json{{{",
        headers={"content-type": "application/json"},
    )
    client._client.post = AsyncMock(return_value=response)

    with pytest.raises(GovernanceAPIError) as exc_info:
        await client.assess({"service": "sagemaker"})

    assert "invalid json" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_assess_timeout(client):
    """
    HTTP timeout → raises GovernanceAPIError.
    """
    client._client.post = AsyncMock(
        side_effect=httpx.TimeoutException("Connection timed out"),
    )

    with pytest.raises(GovernanceAPIError) as exc_info:
        await client.assess({"service": "vertex-ai"})

    assert "timed out" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_assess_network_error(client):
    """
    Generic HTTP error → raises GovernanceAPIError.
    """
    client._client.post = AsyncMock(
        side_effect=httpx.ConnectError("Connection refused"),
    )

    with pytest.raises(GovernanceAPIError) as exc_info:
        await client.assess({"service": "vision"})

    assert "request failed" in str(exc_info.value).lower()
