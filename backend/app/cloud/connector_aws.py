# File: app/cloud/connector_aws.py
"""
Phase 111 – AWS Cloud Governance Connector
============================================
Concrete implementation of ``CloudConnectorBase`` for AWS AI services
(SageMaker, Bedrock, Rekognition, Comprehend, Textract, etc.).

Responsibilities:
  • Parse the AWS service and model from the incoming request.
  • Sign outbound requests with SigV4 using the caller's credentials.
  • Redact fields when the governance engine demands modifications.
  • Forward metering events to the billing adapter.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import httpx

# AWS SDK imports – used for SigV4 request signing
import boto3
import botocore.auth
import botocore.awsrequest
import botocore.credentials

from app.cloud.cloud_connector_base import CloudConnectorBase, GovernanceGateway
from app.cloud.billing_adapter import CloudBillingAdapter

logger = logging.getLogger("guardrail.cloud.aws")

# ---------------------------------------------------------------------------
# Service-detection helpers
# ---------------------------------------------------------------------------

# Maps hostname keywords to canonical AWS service names
_SERVICE_HOST_PATTERNS: Dict[str, str] = {
    "runtime.sagemaker":   "sagemaker",
    "sagemaker":           "sagemaker",
    "bedrock-runtime":     "bedrock",
    "bedrock":             "bedrock",
    "rekognition":         "rekognition",
    "comprehend":          "comprehend",
    "textract":            "textract",
    "translate":           "translate",
}

# SigV4 signing service names (may differ from friendly names)
_SIGV4_SERVICE_NAMES: Dict[str, str] = {
    "sagemaker":    "sagemaker",
    "bedrock":      "bedrock",
    "rekognition":  "rekognition",
    "comprehend":   "comprehend",
    "textract":     "textract",
    "translate":    "translate",
}

# Regex to extract SageMaker endpoint name from path:
#   /endpoints/<endpoint-name>/invocations
_SAGEMAKER_ENDPOINT_RE = re.compile(
    r"/endpoints/(?P<endpoint>[^/]+)/invocations", re.IGNORECASE,
)

# Regex to extract Bedrock model ID from path:
#   /model/<model-id>/invoke  or  /model/<model-id>/invoke-with-response-stream
_BEDROCK_MODEL_PATH_RE = re.compile(
    r"/model/(?P<model>[^/]+)/invoke", re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# AWS Connector
# ---------------------------------------------------------------------------

class AWSConnector(CloudConnectorBase):
    """
    Governance-aware proxy for AWS AI services.

    For every inbound request the connector:

    1. **Extracts** the target AWS service and model from the URL / body.
    2. **Assesses** the request through the ``GovernanceGateway``.
    3. **Signs** the (possibly modified) request with SigV4.
    4. **Forwards** it to the real AWS endpoint.
    5. **Records** usage via the ``CloudBillingAdapter``.
    """

    def __init__(
        self,
        governance_gateway: GovernanceGateway,
        billing_adapter: CloudBillingAdapter,
        region: str = "us-east-1",
        *,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(
            governance_gateway=governance_gateway,
            billing_adapter=billing_adapter,
            timeout=timeout,
        )
        self.region = region

        # Create a boto3 session and extract credentials for SigV4 signing.
        # In production, credentials come from the instance role, env vars,
        # or the shared credentials file (~/.aws/credentials).
        self._session = boto3.Session(region_name=self.region)
        self._credentials = self._session.get_credentials()
        if self._credentials:
            # Resolve returns a ResolvedRefreshableCredentials / frozen set
            self._credentials = self._credentials.get_frozen_credentials()

        logger.info(
            "[AWSConnector] Initialised – region=%s  credentials=%s",
            self.region,
            "present" if self._credentials else "MISSING",
        )

    # ------------------------------------------------------------------
    # Abstract-method implementations
    # ------------------------------------------------------------------

    async def extract_context(
        self,
        method: str,
        url: str,
        body: bytes,
        headers: dict,
    ) -> dict:
        """
        Build a normalised governance context from an AWS-bound request.

        Extracts:
          - **service** from the ``Host`` header (e.g. ``bedrock``, ``sagemaker``).
          - **model** from the URL path or JSON body.
          - **tenant_id** from ``X-Guardrail-Tenant`` header.
          - **user** from ``X-Forwarded-User`` header.
          - **estimated_tokens** as ``len(body) // 4``.
        """
        host = headers.get("host", headers.get("Host", ""))
        service = self._detect_service(host)
        model = self._extract_model(service, url, body)

        tenant_id = headers.get(
            "x-guardrail-tenant",
            headers.get("X-Guardrail-Tenant", "default"),
        )
        user = headers.get(
            "x-forwarded-user",
            headers.get("X-Forwarded-User", "unknown"),
        )

        # Rough token estimation: 1 token ≈ 4 bytes
        estimated_tokens = len(body) // 4 if body else 0

        # Decode body for policy inspection (lossy – safe for logging)
        payload_str = body.decode("utf-8", errors="ignore") if body else ""

        context = {
            "tenant_id":        tenant_id,
            "user":             user,
            "agent":            "aws-connector",
            "service":          service,
            "model":            model,
            "method":           method,
            "url":              url,
            "payload":          payload_str,
            "estimated_tokens": estimated_tokens,
        }

        logger.info(
            "[AWSConnector] Context extracted – service=%s model=%s "
            "tenant=%s tokens≈%d",
            service, model, tenant_id, estimated_tokens,
        )
        return context

    async def forward_request(
        self,
        method: str,
        url: str,
        data: bytes,
        headers: dict,
    ) -> httpx.Response:
        """
        Sign the request with SigV4 and forward to the real AWS endpoint.
        """
        # Ensure data is bytes
        if isinstance(data, dict):
            data = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            data = data.encode("utf-8")

        # Determine the SigV4 service name from the host header
        host = headers.get("host", headers.get("Host", ""))
        service = self._detect_service(host)
        sigv4_service = _SIGV4_SERVICE_NAMES.get(service, service)

        # Build a botocore AWSRequest for signing
        aws_request = botocore.awsrequest.AWSRequest(
            method=method.upper(),
            url=url,
            data=data,
            headers=dict(headers),  # copy to avoid mutation
        )

        # Sign the request (adds Authorization, X-Amz-Date, etc.)
        if self._credentials:
            signer = botocore.auth.SigV4Auth(
                self._credentials,
                sigv4_service,
                self.region,
            )
            signer.add_auth(aws_request)

        # Convert signed headers back for httpx
        signed_headers = dict(aws_request.headers)

        # Forward the request using the async HTTP client
        logger.info(
            "[AWSConnector] Forwarding %s %s (signed for %s/%s)",
            method.upper(), url, sigv4_service, self.region,
        )

        response = await self.client.request(
            method=method.upper(),
            url=url,
            content=data,
            headers=signed_headers,
        )

        logger.info(
            "[AWSConnector] Upstream response: %d (%d bytes)",
            response.status_code, len(response.content),
        )
        return response

    async def apply_modifications(
        self,
        body: bytes,
        modifications: dict,
    ) -> bytes:
        """
        Apply governance-required modifications to the request body.

        Currently supports:
          - ``redact_fields``: list of top-level JSON keys whose values
            will be replaced with ``"[REDACTED]"``.
        """
        try:
            payload = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(
                f"Cannot apply modifications: body is not valid JSON – {exc}"
            ) from exc

        # Redact specified fields
        redact_fields = modifications.get("redact_fields", [])
        for field_name in redact_fields:
            if field_name in payload:
                logger.info(
                    "[AWSConnector] Redacting field '%s'", field_name,
                )
                payload[field_name] = "[REDACTED]"

        modified = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        logger.info(
            "[AWSConnector] Body modified – %d fields redacted, "
            "new size=%d bytes",
            len(redact_fields), len(modified),
        )
        return modified

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_service(host: str) -> str:
        """
        Map an AWS hostname to a canonical service name.

        Examples::

            runtime.sagemaker.us-east-1.amazonaws.com  →  sagemaker
            bedrock-runtime.us-west-2.amazonaws.com    →  bedrock
            rekognition.eu-west-1.amazonaws.com        →  rekognition
        """
        host_lower = host.lower()
        for pattern, svc in _SERVICE_HOST_PATTERNS.items():
            if pattern in host_lower:
                return svc
        return "unknown"

    @staticmethod
    def _extract_model(service: str, url: str, body: bytes) -> str:
        """
        Extract the model / endpoint identifier from the request.

        - **SageMaker**: endpoint name from URL path.
        - **Bedrock**: model ID from URL path, falling back to JSON body.
        - **Others**: ``"default"``.
        """
        parsed_path = urlparse(url).path

        if service == "sagemaker":
            match = _SAGEMAKER_ENDPOINT_RE.search(parsed_path)
            if match:
                return match.group("endpoint")

        if service == "bedrock":
            # Try URL path first (newer invoke API)
            match = _BEDROCK_MODEL_PATH_RE.search(parsed_path)
            if match:
                return match.group("model")
            # Fall back to JSON body
            try:
                payload = json.loads(body)
                return payload.get("modelId", "default")
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        return "default"
