# File: tests/test_billing_adapter.py
"""
Phase 111 – Billing Adapter Test Suite
========================================
Tests the real marketplace metering implementations with fully mocked
HTTP clients, credentials, and config values.

Run with:  pytest tests/test_billing_adapter.py -v
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

import httpx
import pytest
import pytest_asyncio

from app.cloud.billing_adapter import CloudBillingAdapter


# ======================================================================
# Helpers
# ======================================================================

def _make_record(
    tenant: str = "acme",
    service: str = "bedrock",
    tokens: int = 5000,
    decision: str = "ALLOW",
) -> dict:
    """Build a standard usage record dict."""
    return {
        "tenant_id": tenant,
        "service": service,
        "tokens": tokens,
        "decision": decision,
        "marketplace": "aws",
        "timestamp": 1709500000.0,
    }


# ======================================================================
# Initialization Tests
# ======================================================================

def test_init_valid_marketplace():
    """Valid marketplace strings should be accepted."""
    for mp in ("aws", "azure", "gcp", " AWS ", "  GCP  "):
        adapter = CloudBillingAdapter(mp)
        assert adapter.marketplace in ("aws", "azure", "gcp")


def test_init_invalid_marketplace():
    """Invalid marketplace should raise ValueError."""
    with pytest.raises(ValueError, match="Unsupported marketplace"):
        CloudBillingAdapter("oracle")


# ======================================================================
# record_usage (dispatch + non-fatal error handling)
# ======================================================================

@pytest.mark.asyncio
async def test_record_usage_logs_event():
    """record_usage appends to the usage log regardless of vendor call."""
    adapter = CloudBillingAdapter("aws")
    # Stub out the vendor call
    adapter._record_aws = AsyncMock()

    await adapter.record_usage(
        tenant_id="acme", service="sagemaker", tokens=2000, decision="ALLOW",
    )

    log = adapter.get_usage_log()
    assert len(log) == 1
    assert log[0]["tenant_id"] == "acme"
    assert log[0]["service"] == "sagemaker"


@pytest.mark.asyncio
async def test_record_usage_nonfatal_on_vendor_error():
    """If the vendor call raises, record_usage must NOT propagate."""
    adapter = CloudBillingAdapter("aws")
    adapter._record_aws = AsyncMock(side_effect=RuntimeError("boom"))

    # Should NOT raise
    await adapter.record_usage(
        tenant_id="acme", service="bedrock", tokens=1000, decision="ALLOW",
    )

    # Event was still logged
    assert len(adapter.get_usage_log()) == 1


# ======================================================================
# AWS Marketplace Metering
# ======================================================================

@pytest.mark.asyncio
async def test_aws_skip_when_no_product_code():
    """If AWS_MARKETPLACE_PRODUCT_CODE is empty, _record_aws is a no-op."""
    adapter = CloudBillingAdapter("aws")
    record = _make_record()

    with patch("app.cloud.billing_adapter.CloudBillingAdapter._get_aws_credentials"):
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.AWS_MARKETPLACE_PRODUCT_CODE = ""
            mock_settings.AWS_REGION = "us-east-1"
            await adapter._record_aws(record)
    # No HTTP call made (no exception)


@pytest.mark.asyncio
async def test_aws_meter_usage_success():
    """Successful MeterUsage call: SigV4-signed POST returns 200."""
    adapter = CloudBillingAdapter("aws")

    # Mock credentials
    mock_creds = MagicMock()
    mock_creds.access_key = "AKIAIOSFODNN7EXAMPLE"
    mock_creds.secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    mock_creds.token = None
    adapter._aws_credentials = mock_creds

    # Mock HTTP client
    mock_http = AsyncMock(spec=httpx.AsyncClient)
    mock_http.is_closed = False
    mock_http.post = AsyncMock(
        return_value=httpx.Response(status_code=200, json={"MeteringRecordId": "abc123"}),
    )
    adapter._http_client = mock_http

    record = _make_record(tokens=5000)

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.AWS_MARKETPLACE_PRODUCT_CODE = "prod-abc123"
        mock_settings.AWS_REGION = "us-east-1"

        with patch("botocore.awsrequest.AWSRequest") as MockReq:
            mock_req_instance = MagicMock()
            mock_req_instance.headers = {"Authorization": "AWS4-HMAC-SHA256 ..."}
            MockReq.return_value = mock_req_instance

            with patch("botocore.auth.SigV4Auth") as MockAuth:
                mock_signer = MagicMock()
                MockAuth.return_value = mock_signer

                await adapter._record_aws(record)

                # Verify SigV4 signing
                MockAuth.assert_called_once_with(
                    mock_creds, "aws-marketplace", "us-east-1",
                )
                mock_signer.add_auth.assert_called_once()

                # Verify HTTP call
                mock_http.post.assert_called_once()
                call_kwargs = mock_http.post.call_args
                assert "metering.marketplace" in call_kwargs.args[0]


@pytest.mark.asyncio
async def test_aws_meter_usage_failure():
    """MeterUsage returns non-200: should log warning but not raise."""
    adapter = CloudBillingAdapter("aws")

    mock_creds = MagicMock()
    mock_creds.access_key = "AKIA..."
    mock_creds.secret_key = "secret..."
    mock_creds.token = None
    adapter._aws_credentials = mock_creds

    mock_http = AsyncMock(spec=httpx.AsyncClient)
    mock_http.is_closed = False
    mock_http.post = AsyncMock(
        return_value=httpx.Response(status_code=400, text="Bad Request"),
    )
    adapter._http_client = mock_http

    record = _make_record()

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.AWS_MARKETPLACE_PRODUCT_CODE = "prod-abc"
        mock_settings.AWS_REGION = "us-east-1"

        with patch("botocore.awsrequest.AWSRequest") as MockReq:
            mock_req_instance = MagicMock()
            mock_req_instance.headers = {}
            MockReq.return_value = mock_req_instance

            with patch("botocore.auth.SigV4Auth"):
                # Should NOT raise despite 400
                await adapter._record_aws(record)


# ======================================================================
# Azure Marketplace Metered Billing
# ======================================================================

@pytest.mark.asyncio
async def test_azure_skip_when_no_resource_id():
    """If AZURE_RESOURCE_ID is empty, _record_azure is a no-op."""
    adapter = CloudBillingAdapter("azure")
    record = _make_record()

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.AZURE_RESOURCE_ID = ""
        await adapter._record_azure(record)


@pytest.mark.asyncio
async def test_azure_usage_event_success():
    """Successful Azure UsageEvent: Bearer token POST returns 200."""
    adapter = CloudBillingAdapter("azure")

    # Mock token acquisition
    adapter._get_azure_token = AsyncMock(return_value="eyJ0eXAi.test-token")

    mock_http = AsyncMock(spec=httpx.AsyncClient)
    mock_http.is_closed = False
    mock_http.post = AsyncMock(
        return_value=httpx.Response(status_code=200, json={"status": "Accepted"}),
    )
    adapter._http_client = mock_http

    record = _make_record(service="openai", tokens=3000)

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.AZURE_RESOURCE_ID = "resource-id-xyz"

        await adapter._record_azure(record)

        mock_http.post.assert_called_once()
        call_args = mock_http.post.call_args
        assert "marketplaceapi.microsoft.com" in call_args.args[0]
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer eyJ0eXAi.test-token"
        payload = call_args.kwargs["json"]
        assert payload["resourceId"] == "resource-id-xyz"
        assert payload["dimension"] == "guardrail-openai"


@pytest.mark.asyncio
async def test_azure_token_fallback():
    """If DefaultAzureCredential fails, fallback to static token."""
    adapter = CloudBillingAdapter("azure")

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.AZURE_MARKETPLACE_ACCESS_TOKEN = "static-fallback-token"

        with patch("azure.identity.DefaultAzureCredential", side_effect=Exception("no creds")):
            token = await adapter._get_azure_token()
            assert token == "static-fallback-token"


@pytest.mark.asyncio
async def test_azure_no_credentials_raises():
    """If both DefaultAzureCredential and static token fail, raise."""
    adapter = CloudBillingAdapter("azure")

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.AZURE_MARKETPLACE_ACCESS_TOKEN = ""

        with patch("azure.identity.DefaultAzureCredential", side_effect=Exception("no creds")):
            with pytest.raises(RuntimeError, match="No Azure credentials"):
                await adapter._get_azure_token()


# ======================================================================
# GCP Service Control API
# ======================================================================

@pytest.mark.asyncio
async def test_gcp_skip_when_no_service_name():
    """If GCP_SERVICE_NAME is empty, _record_gcp is a no-op."""
    adapter = CloudBillingAdapter("gcp")
    record = _make_record()

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.GCP_SERVICE_NAME = ""
        await adapter._record_gcp(record)


@pytest.mark.asyncio
async def test_gcp_report_success():
    """Successful GCP ServiceControl.report: Bearer token POST returns 200."""
    adapter = CloudBillingAdapter("gcp")

    # Mock token
    adapter._get_gcp_token = AsyncMock(return_value="ya29.test-gcp-token")

    mock_http = AsyncMock(spec=httpx.AsyncClient)
    mock_http.is_closed = False
    mock_http.post = AsyncMock(
        return_value=httpx.Response(status_code=200, json={}),
    )
    adapter._http_client = mock_http

    record = _make_record(service="vertex-ai", tokens=8000)

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.GCP_SERVICE_NAME = "guardrail-marketplace.googleapis.com"

        await adapter._record_gcp(record)

        mock_http.post.assert_called_once()
        call_args = mock_http.post.call_args
        assert "servicecontrol.googleapis.com" in call_args.args[0]
        assert "guardrail-marketplace.googleapis.com" in call_args.args[0]
        assert call_args.kwargs["headers"]["Authorization"] == "Bearer ya29.test-gcp-token"

        payload = call_args.kwargs["json"]
        assert len(payload["operations"]) == 1
        op = payload["operations"][0]
        assert op["labels"]["guardrail/service"] == "vertex-ai"


@pytest.mark.asyncio
async def test_gcp_token_from_service_account():
    """If GCP_SERVICE_ACCOUNT_JSON is set, use it to get token."""
    adapter = CloudBillingAdapter("gcp")

    fake_sa_key = json.dumps({
        "type": "service_account",
        "project_id": "test",
        "private_key_id": "key-id",
        "private_key": "fake-key",
        "client_email": "test@test.iam.gserviceaccount.com",
        "client_id": "123",
        "token_uri": "https://oauth2.googleapis.com/token",
    })

    with patch("app.core.config.settings") as mock_settings:
        mock_settings.GCP_SERVICE_ACCOUNT_JSON = fake_sa_key

        with patch("google.oauth2.service_account.Credentials.from_service_account_info") as mock_from_info:
            mock_creds = MagicMock()
            mock_creds.token = "ya29.from-sa-json"
            mock_from_info.return_value = mock_creds

            with patch("google.auth.transport.requests.Request"):
                token = await adapter._get_gcp_token()
                assert token == "ya29.from-sa-json"
                mock_from_info.assert_called_once()


# ======================================================================
# Utility methods
# ======================================================================

@pytest.mark.asyncio
async def test_clear_usage_log():
    """clear_usage_log empties the in-memory log."""
    adapter = CloudBillingAdapter("aws")
    adapter._record_aws = AsyncMock()

    await adapter.record_usage(
        tenant_id="t1", service="s1", tokens=100, decision="ALLOW",
    )
    assert len(adapter.get_usage_log()) == 1

    adapter.clear_usage_log()
    assert len(adapter.get_usage_log()) == 0
