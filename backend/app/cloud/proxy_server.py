# File: app/cloud/proxy_server.py
"""
Phase 111 – Cloud Governance Proxy Server
==========================================
Stateless FastAPI application that intercepts HTTP requests destined
for cloud AI services, runs them through Guardrail governance, and
forwards the (possibly modified) request to the upstream cloud endpoint.

Deployment::

    CLOUD_PROVIDER=aws GUARDRAIL_API_URL=http://core:8080 \
        uvicorn app.cloud.proxy_server:app --host 0.0.0.0 --port 8000

The proxy supports all three cloud providers via ``CLOUD_PROVIDER`` env var.
"""

from __future__ import annotations

import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from app.cloud.cloud_connector_base import RealGovernanceClient
from app.cloud.billing_adapter import CloudBillingAdapter

logger = logging.getLogger("guardrail.cloud.proxy")


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------

def _require_env(name: str) -> str:
    """Read a required environment variable or exit with an error."""
    value = os.environ.get(name, "").strip()
    if not value:
        logger.critical("Missing required environment variable: %s", name)
        sys.exit(1)
    return value


# ---------------------------------------------------------------------------
# Connector factory
# ---------------------------------------------------------------------------

def _build_connector(
    provider: str,
    governance: RealGovernanceClient,
    billing: CloudBillingAdapter,
):
    """Instantiate the correct cloud connector for *provider*."""
    if provider == "aws":
        from app.cloud.connector_aws import AWSConnector
        region = os.environ.get("AWS_REGION", "us-east-1")
        return AWSConnector(governance, billing, region=region)

    if provider == "azure":
        from app.cloud.connector_azure import AzureConnector
        return AzureConnector(governance, billing)

    if provider == "gcp":
        from app.cloud.connector_gcp import GCPConnector
        return GCPConnector(governance, billing)

    logger.critical("Unsupported CLOUD_PROVIDER: '%s'", provider)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Application lifespan (startup / shutdown)
# ---------------------------------------------------------------------------

connector = None          # set during lifespan startup

@asynccontextmanager
async def lifespan(application: FastAPI):
    """Initialise connector on startup, tear down on shutdown."""
    global connector

    provider = _require_env("CLOUD_PROVIDER").lower()
    api_url = _require_env("GUARDRAIL_API_URL")
    api_key = os.environ.get("GUARDRAIL_API_KEY", "")

    logger.info(
        "[Proxy] Starting – provider=%s  guardrail_api=%s",
        provider, api_url,
    )

    governance = RealGovernanceClient(base_url=api_url, api_key=api_key)
    billing = CloudBillingAdapter(marketplace=provider)
    connector = _build_connector(provider, governance, billing)

    logger.info("[Proxy] Connector ready (%s)", provider.upper())

    yield  # application runs

    # Shutdown
    logger.info("[Proxy] Shutting down…")
    await connector.close()
    await governance.close()
    await billing.close()
    logger.info("[Proxy] Stopped.")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Guardrail Cloud Governance Proxy",
    description="Transparent governance sidecar for cloud AI services",
    version="111.0.0",
    lifespan=lifespan,
)


@app.get("/healthz")
async def health_check():
    """Liveness / readiness probe for Kubernetes."""
    return {"status": "ok", "connector": connector is not None}


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"],
)
async def proxy_handler(request: Request, path: str):
    """
    Catch-all reverse proxy handler.

    Captures the raw request (method, URL, headers, body), passes it
    through the cloud connector (governance → modify → forward → bill),
    and returns the upstream response.
    """
    if connector is None:
        return JSONResponse(
            status_code=503,
            content={"error": "Proxy not initialised"},
        )

    # ---- Capture the inbound request ----
    method = request.method
    url = str(request.url)
    body = await request.body()
    headers = dict(request.headers)

    logger.info("[Proxy] %s %s (%d bytes)", method, url, len(body))

    try:
        upstream_response = await connector.handle(method, url, body, headers)
    except Exception as exc:
        logger.exception("[Proxy] Unhandled error in connector.handle")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal proxy error"},
        )

    # ---- Translate httpx.Response → FastAPI Response ----
    excluded = {"content-encoding", "transfer-encoding", "content-length"}
    resp_headers = {
        k: v
        for k, v in upstream_response.headers.items()
        if k.lower() not in excluded
    }

    return Response(
        content=upstream_response.content,
        status_code=upstream_response.status_code,
        headers=resp_headers,
    )


# ---------------------------------------------------------------------------
# Direct run: ``python -m app.cloud.proxy_server``
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    uvicorn.run(
        "app.cloud.proxy_server:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
