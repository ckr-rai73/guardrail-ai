# File: tests/test_connector_gcp.py
"""
Phase 111 – GCP Connector Test Suite
=======================================
Tests the GCPConnector with fully mocked dependencies:
  • GovernanceGateway  → controlled Decision returns
  • CloudBillingAdapter → captured record_usage calls
  • httpx.AsyncClient → mock upstream responses

Run with:  pytest tests/test_connector_gcp.py -v
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
import pytest_asyncio

from app.cloud.cloud_connector_base import Decision, RealGovernanceClient
from app.cloud.billing_adapter import CloudBillingAdapter
from app.cloud.connector_gcp import GCPConnector


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
    ba.marketplace = "gcp"
    ba.record_usage = AsyncMock()
    return ba


@pytest_asyncio.fixture
async def connector(mock_governance, mock_billing):
    """
    Create a GCPConnector with mocked gateway and billing.
    Replace the internal httpx client with a mock returning 200.
    """
    conn = GCPConnector(
        governance_gateway=mock_governance,
        billing_adapter=mock_billing,
    )

    # Mock the httpx client
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.request = AsyncMock(
        return_value=httpx.Response(
            status_code=200,
            json={"predictions": [{"output": "Hello from Vertex!"}]},
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

def _vertex_headers(tenant: str = "acme") -> dict:
    """Headers for a Vertex AI request."""
    return {
        "host": "us-central1-aiplatform.googleapis.com",
        "content-type": "application/json",
        "Authorization": "Bearer ya29.a0AbV...",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "alice@acme.com",
    }


def _vertex_predict_url(
    project: str = "my-project",
    location: str = "us-central1",
    endpoint: str = "12345",
) -> str:
    return (
        f"https://{location}-aiplatform.googleapis.com"
        f"/v1/projects/{project}/locations/{location}"
        f"/endpoints/{endpoint}:predict"
    )


def _vertex_gemini_url(
    project: str = "my-project",
    location: str = "us-central1",
    publisher: str = "google",
    model: str = "gemini-1.5-pro",
) -> str:
    return (
        f"https://{location}-aiplatform.googleapis.com"
        f"/v1/projects/{project}/locations/{location}"
        f"/publishers/{publisher}/models/{model}:generateContent"
    )


def _vision_headers(tenant: str = "healthco") -> dict:
    return {
        "host": "vision.googleapis.com",
        "content-type": "application/json",
        "Authorization": "Bearer ya29.vision...",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "carol@healthco.com",
    }


def _vision_url() -> str:
    return "https://vision.googleapis.com/v1/images:annotate"


def _language_headers(tenant: str = "fintech") -> dict:
    return {
        "host": "language.googleapis.com",
        "content-type": "application/json",
        "Authorization": "Bearer ya29.lang...",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "bob@fintech.io",
    }


def _language_url(operation: str = "analyzeSentiment") -> str:
    return f"https://language.googleapis.com/v1/documents:{operation}"


def _translate_headers(tenant: str = "globalco") -> dict:
    return {
        "host": "translate.googleapis.com",
        "content-type": "application/json",
        "Authorization": "Bearer ya29.translate...",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "dave@globalco.com",
    }


def _translate_url(
    project: str = "my-project",
    location: str = "global",
) -> str:
    return (
        f"https://translate.googleapis.com"
        f"/v3/projects/{project}/locations/{location}:translateText"
    )


def _speech_headers(tenant: str = "voiceco") -> dict:
    return {
        "host": "speech.googleapis.com",
        "content-type": "application/json",
        "Authorization": "Bearer ya29.speech...",
        "X-Guardrail-Tenant": tenant,
        "X-Forwarded-User": "eve@voiceco.com",
    }


def _speech_url() -> str:
    return "https://speech.googleapis.com/v1/speech:recognize"


# ======================================================================
# Test Cases
# ======================================================================

@pytest.mark.asyncio
async def test_extract_context_vertex_ai(connector):
    """
    Vertex AI predict request → service='vertex-ai', endpoint extracted.
    """
    body = json.dumps({
        "instances": [{"input": "Hello, world!"}],
    }).encode()
    headers = _vertex_headers(tenant="acme-corp")
    url = _vertex_predict_url(endpoint="my-nlp-endpoint-789")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "vertex-ai"
    assert ctx["model"] == "my-nlp-endpoint-789"
    assert ctx["tenant_id"] == "acme-corp"
    assert ctx["user"] == "alice@acme.com"
    assert ctx["agent"] == "gcp-connector"
    assert ctx["estimated_tokens"] == len(body) // 4


@pytest.mark.asyncio
async def test_extract_context_vertex_gemini(connector):
    """
    Vertex AI Gemini generateContent request → publisher/model extracted.
    """
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": "Hi!"}]}],
    }).encode()
    headers = _vertex_headers(tenant="ai-lab")
    url = _vertex_gemini_url(publisher="google", model="gemini-1.5-pro")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "vertex-ai"
    assert ctx["model"] == "google/gemini-1.5-pro"


@pytest.mark.asyncio
async def test_extract_context_vision(connector):
    """
    Vision API annotate request → service='vision', operation='annotate'.
    """
    body = json.dumps({
        "requests": [{"image": {"content": "base64..."}, "features": [{"type": "LABEL_DETECTION"}]}],
    }).encode()
    headers = _vision_headers(tenant="healthco")
    url = _vision_url()

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "vision"
    assert ctx["model"] == "annotate"
    assert ctx["tenant_id"] == "healthco"
    assert ctx["user"] == "carol@healthco.com"


@pytest.mark.asyncio
async def test_extract_context_language(connector):
    """
    Natural Language analyzeSentiment → service='language', operation extracted.
    """
    body = json.dumps({
        "document": {"type": "PLAIN_TEXT", "content": "I love this!"},
    }).encode()
    headers = _language_headers(tenant="fintech-co")
    url = _language_url(operation="analyzeSentiment")

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "language"
    assert ctx["model"] == "analyzeSentiment"
    assert ctx["tenant_id"] == "fintech-co"


@pytest.mark.asyncio
async def test_extract_context_translate(connector):
    """
    Translation API translateText → service='translate', operation extracted.
    """
    body = json.dumps({
        "contents": ["Hello, world!"],
        "targetLanguageCode": "es",
    }).encode()
    headers = _translate_headers(tenant="globalco")
    url = _translate_url()

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "translate"
    assert ctx["model"] == "translateText"
    assert ctx["tenant_id"] == "globalco"


@pytest.mark.asyncio
async def test_extract_context_speech(connector):
    """
    Speech-to-Text recognize → service='speech', operation='recognize'.
    """
    body = json.dumps({
        "config": {"encoding": "LINEAR16", "sampleRateHertz": 16000},
        "audio": {"content": "base64audio..."},
    }).encode()
    headers = _speech_headers(tenant="voiceco")
    url = _speech_url()

    ctx = await connector.extract_context("POST", url, body, headers)

    assert ctx["service"] == "speech"
    assert ctx["model"] == "recognize"
    assert ctx["tenant_id"] == "voiceco"
    assert ctx["user"] == "eve@voiceco.com"


@pytest.mark.asyncio
async def test_handle_allow(connector, mock_governance, mock_billing):
    """
    ALLOW decision → request forwarded to upstream, billing recorded.
    """
    body = json.dumps({"instances": [{"input": "test"}]}).encode()
    headers = _vertex_headers()
    url = _vertex_predict_url()

    response = await connector.handle("POST", url, body, headers)

    connector.client.request.assert_called_once()
    mock_billing.record_usage.assert_called_once()
    billing_kwargs = mock_billing.record_usage.call_args.kwargs
    assert billing_kwargs["decision"] == "ALLOW"
    assert billing_kwargs["service"] == "vertex-ai"
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_handle_block(connector, mock_governance, mock_billing):
    """
    BLOCK decision → returns 403, upstream NOT called.
    """
    mock_governance.assess = AsyncMock(
        return_value=Decision(
            action="BLOCK",
            reason="Prompt violates content safety policy",
        ),
    )

    body = json.dumps({"instances": [{"input": "harmful content"}]}).encode()
    headers = _vertex_headers()
    url = _vertex_predict_url()

    response = await connector.handle("POST", url, body, headers)

    assert response.status_code == 403
    data = json.loads(response.content)
    assert data["error"] == "Blocked by Guardrail policy"
    assert "content safety" in data["reason"]
    connector.client.request.assert_not_called()


@pytest.mark.asyncio
async def test_handle_modify(connector, mock_governance, mock_billing):
    """
    MODIFY decision → specified fields redacted before forwarding.
    """
    mock_governance.assess = AsyncMock(
        return_value=Decision(
            action="MODIFY",
            reason="Redacting patient data",
            modifications={"redact_fields": ["patient_id", "diagnosis"]},
        ),
    )

    original_body = json.dumps({
        "instances": [{"input": "Analyse this record"}],
        "patient_id": "P-12345",
        "diagnosis": "Type-2 Diabetes",
        "department": "Endocrinology",
    }).encode()
    headers = _vertex_headers()
    url = _vertex_predict_url()

    response = await connector.handle("POST", url, original_body, headers)

    connector.client.request.assert_called_once()
    call_kwargs = connector.client.request.call_args.kwargs
    forwarded_payload = json.loads(call_kwargs["content"])

    assert forwarded_payload["patient_id"] == "[REDACTED]"
    assert forwarded_payload["diagnosis"] == "[REDACTED]"
    assert forwarded_payload["department"] == "Endocrinology"  # untouched
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_handle_extraction_failure(connector, mock_governance):
    """
    Unknown host → extract_context raises ValueError → 500 returned.
    """
    body = json.dumps({"data": "test"}).encode()
    headers = {"host": "completely-unknown.example.com"}
    url = "https://completely-unknown.example.com/api/test"

    response = await connector.handle("POST", url, body, headers)

    assert response.status_code == 500
    data = json.loads(response.content)
    assert "context extraction" in data["error"].lower()


@pytest.mark.asyncio
async def test_forward_request_passthrough(connector):
    """
    Verify that forward_request passes the Authorization header through
    to the upstream unchanged (no re-signing).
    """
    body = json.dumps({"instances": [{"input": "test"}]}).encode()
    headers = {
        "host": "us-central1-aiplatform.googleapis.com",
        "content-type": "application/json",
        "Authorization": "Bearer ya29.super-secret-token",
        "X-Custom-Header": "custom-value",
    }
    url = _vertex_predict_url()

    await connector.forward_request("POST", url, body, headers)

    call_kwargs = connector.client.request.call_args.kwargs
    forwarded_headers = call_kwargs["headers"]

    assert forwarded_headers["Authorization"] == "Bearer ya29.super-secret-token"
    assert forwarded_headers["X-Custom-Header"] == "custom-value"


@pytest.mark.asyncio
async def test_apply_modifications_non_json(connector):
    """
    If the body is not valid JSON, apply_modifications should return it
    unchanged (graceful degradation).
    """
    raw_body = b"This is raw audio data, not JSON at all"
    modifications = {"redact_fields": ["patient_id"]}

    result = await connector.apply_modifications(raw_body, modifications)

    assert result == raw_body  # unchanged
