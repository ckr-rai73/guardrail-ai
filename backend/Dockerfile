# Phase 111 – Guardrail Cloud Governance Proxy
# Multi-stage build for minimal production image

FROM python:3.11-slim AS base

LABEL maintainer="Guardrail.ai <ops@guardrail.ai>"
LABEL description="Cloud Governance Proxy – transparent sidecar for AWS, Azure, GCP AI services"

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# ---- Dependencies ----
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ---- Application code ----
COPY backend/app/ app/

# ---- Runtime ----
EXPOSE 8000

# Health check for orchestrators
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import httpx; r = httpx.get('http://127.0.0.1:8000/healthz'); r.raise_for_status()" || exit 1

# Default entrypoint
CMD ["uvicorn", "app.cloud.proxy_server:app", "--host", "0.0.0.0", "--port", "8000"]
