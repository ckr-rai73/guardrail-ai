# File: tests/test_connector_azure.py
"""
Phase 111 – Azure Connector Test Suite
========================================
Tests the AzureConnector with fully mocked dependencies:
  • GovernanceGateway  → controlled Decision returns
  • CloudBillingAdapter → captured record_usage calls
  • httpx.AsyncClient → mock upstream responses

Run with:  pytest tests/test_connector_azure.py -v
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import pytest_asyncio

from app.cloud.cloud_connector_base import Decision, RealGovernanceClient
from app.cloud.billing_adapter import CloudBillingAdapter
from app.cloud.connector_azure import AzureConnector


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def mock_governance():
    """RealGovernanceClient with a mocked async assess() that defaults to ALLOW."""
    gw = MagicMock(spec=RealGovernanceClient)
    gw.assess = AsyncMock(
        return_value=Decision(action="ALLOW", reason="Test ALLOW"),
    )
    return gw


@pytest.fixture
def mock_billing():
    """CloudBillingAdapter with a no-op record_usage."""
    ba = MagicMock(spec=CloudBillingAdapter)
    ba.marketplace = "azure"
    ba.record_usage = AsyncMock()
    return ba


@pytest_asyncio.fixture
async def connector(mock_governance, mock_billing):
    """
    Create an AzureConnector with mocked gateway and billing.
    Replace the internal httpx client with a mock returning 200.
    """
    conn = AzureConnector(
        governance_gateway=mock_governance,
        billing_adapter=mock_billing,
    )

    # Mock the httpx client
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.request = AsyncMock(
        return_value=httpx.Response(
            status_code=200,
            json={"id": "chatcmpl-abc123", "choices": [{"text": "Hello!"}]},
            headers={"content-type": "application/json"},
        ),
    )
    mock_client.aclose = AsyncMock()
    conn.client = mock_client

    yield conn

    await conn.close()


# ======================================================================
# Helpers
# ======================================================================

def _openai_headers(tenant: str = "acme") -> dict:
    """Headers for an Azure OpenAI request."""
    return {
        "host": "my-resource.openai.azure.com",
        "content-type": "application/json",
        "api-key": "sk-test-key-12345",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "alice@acme.com",
    }


def _openai_url(deployment: str = "gpt-4o", operation: str = "chat/completions") -> str:
    return (
        f"https://my-resource.openai.azure.com"
        f"/openai/deployments/{deployment}/{operation}"
        f"?api-version=2024-02-15-preview"
    )


def _azureml_headers(tenant: str = "fintech") -> dict:
    """Headers for an Azure ML endpoint request."""
    return {
        "host": "my-endpoint.westus2.inference.ml.azure.com",
        "content-type": "application/json",
        "Authorization": "Bearer eyJ0eXAi...",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "bob@fintech.io",
    }


def _azureml_url() -> str:
    return "https://my-endpoint.westus2.inference.ml.azure.com/score"


def _cognitive_headers(tenant: str = "healthco") -> dict:
    """Headers for a Cognitive Services request."""
    return {
        "host": "my-resource.api.cognitive.microsoft.com",
        "content-type": "application/json",
        "Ocp-Apim-Subscription-Key": "abc123def456",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "carol@healthco.com",
    }


def _cognitive_url(operation: str = "sentiment") -> str:
    return f"https://my-resource.api.cognitive.microsoft.com/text/analytics/v3.1/{operation}"


# ======================================================================
# Test Cases
# ======================================================================

@pytest.mark.asyncio
async def test_extract_context_openai(connector):
    """
    Azure OpenAI chat completion request → service='openai',
    deployment extracted from URL path.
    """
    body = json.dumps({
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 100,
    }).encode()
    headers = _openai_headers(tenant="acme-corp")
    url = _openai_url(deployment="gpt-4o-mini")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "openai"
    assert ctx["model"] == "gpt-4o-mini"
    assert ctx["tenant_id"] == "acme-corp"
    assert ctx["user"] == "alice@acme.com"
    assert ctx["agent"] == "azure-connector"
    assert ctx["estimated_tokens"] == len(body) // 4


@pytest.mark.asyncio
async def test_extract_context_azureml(connector):
    """
    Azure ML endpoint invocation → service='azureml',
    model extracted from body or 'unknown'.
    """
    body = json.dumps({
        "model": "my-custom-model-v2",
        "data": [[1.0, 2.0, 3.0]],
    }).encode()
    headers = _azureml_headers(tenant="fintech-co")
    url = _azureml_url()

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "azureml"
    assert ctx["model"] == "my-custom-model-v2"
    assert ctx["tenant_id"] == "fintech-co"
    assert ctx["user"] == "bob@fintech.io"


@pytest.mark.asyncio
async def test_extract_context_azureml_no_model(connector):
    """
    Azure ML endpoint invocation without model in body → model='unknown'.
    """
    body = json.dumps({"data": [[1.0, 2.0]]}).encode()
    headers = _azureml_headers()
    url = _azureml_url()

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "azureml"
    assert ctx["model"] == "unknown"


@pytest.mark.asyncio
async def test_extract_context_cognitive(connector):
    """
    Cognitive Services text analytics → service='cognitive',
    operation extracted from URL path.
    """
    body = json.dumps({
        "documents": [{"id": "1", "text": "I love this product!"}],
    }).encode()
    headers = _cognitive_headers(tenant="healthco")
    url = _cognitive_url(operation="sentiment")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "cognitive"
    assert ctx["model"] == "sentiment"
    assert ctx["tenant_id"] == "healthco"
    assert ctx["user"] == "carol@healthco.com"


@pytest.mark.asyncio
async def test_handle_allow(connector, mock_governance, mock_billing):
    """
    ALLOW decision → request forwarded to upstream, billing recorded.
    """
    body = json.dumps({"messages": [{"role": "user", "content": "Hi"}]}).encode()
    headers = _openai_headers()
    url = _openai_url()

    response = await connector.handle("POST", url, body, headers)

    connector.client.request.assert_called_once()
    mock_billing.record_usage.assert_called_once()
    billing_kwargs = mock_billing.record_usage.call_args.kwargs
    assert billing_kwargs["decision"] == "ALLOW"
    assert billing_kwargs["service"] == "openai"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_handle_block(connector, mock_governance, mock_billing):
    """
    BLOCK decision → returns 403, upstream NOT called.
    """
    mock_governance.assess = AsyncMock(
        return_value=Decision(
            action="BLOCK",
            reason="Prompt contains prohibited content",
        ),
    )

    body = json.dumps({"messages": [{"role": "user", "content": "bad stuff"}]}).encode()
    headers = _openai_headers()
    url = _openai_url()

    response = await connector.handle("POST", url, body, headers)

    assert response.status_code == 403
    data = json.loads(response.content)
    assert data["error"] == "Blocked by Guardrail policy"
    assert "prohibited content" in data["reason"]
    connector.client.request.assert_not_called()


@pytest.mark.asyncio
async def test_handle_modify(connector, mock_governance, mock_billing):
    """
    MODIFY decision → specified fields redacted before forwarding.
    """
    mock_governance.assess = AsyncMock(
        return_value=Decision(
            action="MODIFY",
            reason="Redacting PII",
            modifications={"redact_fields": ["ssn", "dob"]},
        ),
    )

    original_body = json.dumps({
        "messages": [{"role": "user", "content": "Check this"}],
        "ssn": "123-45-6789",
        "dob": "1990-01-15",
        "name": "Alice",
    }).encode()
    headers = _openai_headers()
    url = _openai_url()

    response = await connector.handle("POST", url, original_body, headers)

    connector.client.request.assert_called_once()
    call_kwargs = connector.client.request.call_args.kwargs
    forwarded_payload = json.loads(call_kwargs["content"])

    assert forwarded_payload["ssn"] == "[REDACTED]"
    assert forwarded_payload["dob"] == "[REDACTED]"
    assert forwarded_payload["name"] == "Alice"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_handle_extraction_failure(connector, mock_governance):
    """
    Unknown host → extract_context raises ValueError → 500 returned.
    """
    body = json.dumps({"data": "test"}).encode()
    headers = {"host": "totally-unknown-service.example.com"}
    url = "https://totally-unknown-service.example.com/api/test"

    response = await connector.handle("POST", url, body, headers)

    assert response.status_code == 500
    data = json.loads(response.content)
    assert "context extraction" in data["error"].lower()


@pytest.mark.asyncio
async def test_forward_request_passthrough(connector):
    """
    Verify that forward_request passes headers (including api-key and
    Authorization) through to the upstream unchanged.
    """
    body = json.dumps({"messages": [{"role": "user", "content": "test"}]}).encode()
    headers = {
        "host": "my-resource.openai.azure.com",
        "content-type": "application/json",
        "api-key": "sk-secret-key-xyz",
        "Authorization": "Bearer eyJ0eXAi...",
        "X-Custom-Header": "custom-value",
    }
    url = _openai_url()

    await connector.forward_request("POST", url, body, headers)

    call_kwargs = connector.client.request.call_args.kwargs
    forwarded_headers = call_kwargs["headers"]

    # All original auth headers preserved
    assert forwarded_headers["api-key"] == "sk-secret-key-xyz"
    assert forwarded_headers["Authorization"] == "Bearer eyJ0eXAi..."
    assert forwarded_headers["X-Custom-Header"] == "custom-value"


@pytest.mark.asyncio
async def test_apply_modifications_non_json(connector):
    """
    If the body is not valid JSON, apply_modifications should return it
    unchanged (graceful degradation).
    """
    raw_body = b"This is plain text, not JSON"
    modifications = {"redact_fields": ["ssn"]}

    result = await connector.apply_modifications(raw_body, modifications)

    assert result == raw_body  # unchanged
