# File: tests/test_connector_aws.py
"""
Phase 111 – AWS Connector Test Suite
======================================
Tests the AWSConnector with fully mocked dependencies:
  • GovernanceGateway  → controlled Decision returns
  • CloudBillingAdapter → captured record_usage calls
  • httpx.AsyncClient → mock upstream responses
  • boto3 / botocore   → mock credential chain

Run with:  pytest tests/test_connector_aws.py -v
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import pytest_asyncio

from app.cloud.cloud_connector_base import Decision, GovernanceGateway
from app.cloud.billing_adapter import CloudBillingAdapter
from app.cloud.connector_aws import AWSConnector


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture
def mock_governance():
    """GovernanceGateway with an async assess() that defaults to ALLOW."""
    gw = MagicMock(spec=GovernanceGateway)
    gw.assess = AsyncMock(
        return_value=Decision(action="ALLOW", reason="Test ALLOW"),
    )
    return gw


@pytest.fixture
def mock_billing():
    """CloudBillingAdapter with a no-op record_usage."""
    ba = MagicMock(spec=CloudBillingAdapter)
    ba.marketplace = "aws"
    ba.record_usage = AsyncMock()
    return ba


@pytest.fixture
def mock_credentials():
    """Patch boto3 session to provide fake frozen credentials."""
    frozen = MagicMock()
    frozen.access_key = "AKIAIOSFODNN7EXAMPLE"
    frozen.secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    frozen.token = None

    session = MagicMock()
    creds = MagicMock()
    creds.get_frozen_credentials.return_value = frozen
    session.get_credentials.return_value = creds

    return session, frozen


@pytest_asyncio.fixture
async def connector(mock_governance, mock_billing, mock_credentials):
    """
    Create an AWSConnector with mocked gateway, billing, and credentials.
    Also mock the internal httpx.AsyncClient to capture forwarded requests.
    """
    session_mock, _ = mock_credentials

    with patch("app.cloud.connector_aws.boto3.Session", return_value=session_mock):
        conn = AWSConnector(
            governance_gateway=mock_governance,
            billing_adapter=mock_billing,
            region="us-east-1",
        )

    # Replace the httpx client with a mock that returns a dummy 200
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.request = AsyncMock(
        return_value=httpx.Response(
            status_code=200,
            json={"result": "ok"},
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

def _sagemaker_headers(endpoint: str = "my-endpoint", tenant: str = "acme") -> dict:
    """Build headers for a typical SageMaker InvokeEndpoint request."""
    return {
        "host": f"runtime.sagemaker.us-east-1.amazonaws.com",
        "content-type": "application/json",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "alice@acme.com",
    }


def _sagemaker_url(endpoint: str = "my-endpoint") -> str:
    return f"https://runtime.sagemaker.us-east-1.amazonaws.com/endpoints/{endpoint}/invocations"


def _bedrock_headers(tenant: str = "acme") -> dict:
    return {
        "host": "bedrock-runtime.us-east-1.amazonaws.com",
        "content-type": "application/json",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "bob@acme.com",
    }


def _bedrock_url(model_id: str = "anthropic.claude-v2") -> str:
    return f"https://bedrock-runtime.us-east-1.amazonaws.com/model/{model_id}/invoke"


# ======================================================================
# Test Cases
# ======================================================================

@pytest.mark.asyncio
async def test_extract_context_sagemaker(connector):
    """
    Verify context extraction for a SageMaker InvokeEndpoint request.
    Should pull out service, endpoint (model), tenant, user, and tokens.
    """
    body = json.dumps({"inputs": "Hello, world!"}).encode()
    headers = _sagemaker_headers(endpoint="my-nlp-endpoint", tenant="acme-corp")
    url = _sagemaker_url(endpoint="my-nlp-endpoint")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "sagemaker"
    assert ctx["model"] == "my-nlp-endpoint"
    assert ctx["tenant_id"] == "acme-corp"
    assert ctx["user"] == "alice@acme.com"
    assert ctx["agent"] == "aws-connector"
    assert ctx["estimated_tokens"] == len(body) // 4
    assert "Hello, world!" in ctx["payload"]


@pytest.mark.asyncio
async def test_extract_context_bedrock(connector):
    """
    Verify context extraction for a Bedrock InvokeModel request.
    Should detect bedrock service and model ID from the URL path.
    """
    body = json.dumps({
        "prompt": "Summarise this document.",
        "max_tokens": 512,
    }).encode()
    headers = _bedrock_headers(tenant="fintech-co")
    url = _bedrock_url(model_id="amazon.titan-text-express-v1")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "bedrock"
    assert ctx["model"] == "amazon.titan-text-express-v1"
    assert ctx["tenant_id"] == "fintech-co"
    assert ctx["user"] == "bob@acme.com"


@pytest.mark.asyncio
async def test_handle_allow(connector, mock_governance, mock_billing):
    """
    ALLOW decision → request forwarded to upstream, billing recorded.
    """
    body = json.dumps({"inputs": "test"}).encode()
    headers = _sagemaker_headers()
    url = _sagemaker_url()

    response = await connector.handle("POST", url, body, headers)

    # Upstream was called
    connector.client.request.assert_called_once()
    # Billing was recorded
    mock_billing.record_usage.assert_called_once()
    billing_kwargs = mock_billing.record_usage.call_args.kwargs
    assert billing_kwargs["decision"] == "ALLOW"
    assert billing_kwargs["tenant_id"] == "acme"
    assert billing_kwargs["service"] == "sagemaker"
    # Response is the 200 from the mock upstream
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_handle_block(connector, mock_governance, mock_billing):
    """
    BLOCK decision → returns 403 with reason, upstream NOT called.
    """
    mock_governance.assess = AsyncMock(
        return_value=Decision(
            action="BLOCK",
            reason="PII detected in prompt – policy violation",
        ),
    )

    body = json.dumps({"inputs": "SSN: 123-45-6789"}).encode()
    headers = _sagemaker_headers()
    url = _sagemaker_url()

    response = await connector.handle("POST", url, body, headers)

    assert response.status_code == 403
    data = json.loads(response.content)
    assert data["error"] == "Blocked by Guardrail policy"
    assert "PII detected" in data["reason"]

    # Upstream should NOT have been called
    connector.client.request.assert_not_called()


@pytest.mark.asyncio
async def test_handle_modify(connector, mock_governance, mock_billing):
    """
    MODIFY decision → body is modified (fields redacted) before forwarding.
    """
    mock_governance.assess = AsyncMock(
        return_value=Decision(
            action="MODIFY",
            reason="Redacting SSN field",
            modifications={"redact_fields": ["ssn", "credit_card"]},
        ),
    )

    original_body = json.dumps({
        "inputs": "Analyse this user",
        "ssn": "123-45-6789",
        "credit_card": "4111-1111-1111-1111",
        "name": "Alice",
    }).encode()
    headers = _sagemaker_headers()
    url = _sagemaker_url()

    response = await connector.handle("POST", url, original_body, headers)

    # The upstream was called
    connector.client.request.assert_called_once()

    # Verify the body sent to upstream has redacted fields
    call_kwargs = connector.client.request.call_args.kwargs
    forwarded_body = call_kwargs.get("content", b"")
    forwarded_payload = json.loads(forwarded_body)

    assert forwarded_payload["ssn"] == "[REDACTED]"
    assert forwarded_payload["credit_card"] == "[REDACTED]"
    assert forwarded_payload["name"] == "Alice"  # untouched
    assert forwarded_payload["inputs"] == "Analyse this user"  # untouched

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_handle_extraction_failure(connector, mock_governance):
    """
    If extract_context raises an exception, the connector should return 500.
    """
    # Force extract_context to fail by sending un-parseable data
    # We'll monkey-patch extract_context to raise
    connector.extract_context = AsyncMock(
        side_effect=ValueError("Simulated extraction failure"),
    )

    response = await connector.handle("POST", "https://bad-url", b"garbage", {})

    assert response.status_code == 500
    data = json.loads(response.content)
    assert "context extraction" in data["error"].lower()


@pytest.mark.asyncio
async def test_sigv4_signing(connector, mock_credentials):
    """
    Verify that forward_request creates an AWSRequest and signs it
    with SigV4Auth for the correct service and region.
    """
    body = json.dumps({"inputs": "test"}).encode()
    headers = {
        "host": "runtime.sagemaker.us-east-1.amazonaws.com",
        "content-type": "application/json",
    }
    url = _sagemaker_url()

    with patch("app.cloud.connector_aws.botocore.auth.SigV4Auth") as mock_sigv4_cls:
        mock_signer = MagicMock()
        mock_sigv4_cls.return_value = mock_signer

        await connector.forward_request("POST", url, body, headers)

        # SigV4Auth was instantiated with correct service and region
        mock_sigv4_cls.assert_called_once()
        call_args = mock_sigv4_cls.call_args
        assert call_args[0][1] == "sagemaker"   # service name
        assert call_args[0][2] == "us-east-1"   # region

        # add_auth was called to sign the request
        mock_signer.add_auth.assert_called_once()
