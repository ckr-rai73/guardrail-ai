# Guardrail Cloud Governance Connector – Deployment Guide

## Overview

The **Guardrail Cloud Connector** is a transparent governance sidecar proxy that intercepts HTTP requests to cloud AI services (AWS, Azure, GCP), enforces governance policies via the Guardrail Core API, and records marketplace billing.

```
Client  →  Cloud Connector (sidecar)  →  Guardrail Core (assess)
                  ↓
          Cloud AI Service (SageMaker / OpenAI / Vertex AI)
```

---

## Configuration Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `CLOUD_PROVIDER` | ✅ | – | `aws`, `azure`, or `gcp` |
| `GUARDRAIL_API_URL` | ✅ | – | URL of Guardrail Core API |
| `GUARDRAIL_API_KEY` | ⬜ | `""` | API key for Core API auth |
| `PORT` | ⬜ | `8000` | Proxy listen port |
| **AWS** | | | |
| `AWS_REGION` | ⬜ | `us-east-1` | Region for SigV4 signing & metering |
| `AWS_MARKETPLACE_PRODUCT_CODE` | ⬜ | `""` | Product code for MeterUsage |
| **Azure** | | | |
| `AZURE_RESOURCE_ID` | ⬜ | `""` | Marketplace resource ID |
| `AZURE_MARKETPLACE_ACCESS_TOKEN` | ⬜ | `""` | Fallback token |
| **GCP** | | | |
| `GCP_SERVICE_NAME` | ⬜ | `""` | Service Control API service |
| `GCP_SERVICE_ACCOUNT_JSON` | ⬜ | `""` | SA key JSON string |

---

## Build Docker Image

```bash
cd backend
docker build -t guardrail/cloud-connector:latest .
```

---

## Deploy with Helm (Kubernetes)

```bash
helm install guardrail-connector deploy/charts/guardrail-cloud-connector \
  --set cloudProvider=aws \
  --set guardrail.apiUrl=http://guardrail-core:8080 \
  --set guardrail.apiKey=YOUR_API_KEY \
  --set aws.region=us-east-1 \
  --set aws.marketplaceProductCode=prod-abc123
```

### Azure example

```bash
helm install guardrail-connector deploy/charts/guardrail-cloud-connector \
  --set cloudProvider=azure \
  --set guardrail.apiUrl=http://guardrail-core:8080 \
  --set guardrail.apiKey=YOUR_API_KEY \
  --set azure.resourceId=YOUR_RESOURCE_ID
```

### GCP example

```bash
helm install guardrail-connector deploy/charts/guardrail-cloud-connector \
  --set cloudProvider=gcp \
  --set guardrail.apiUrl=http://guardrail-core:8080 \
  --set guardrail.apiKey=YOUR_API_KEY \
  --set gcp.serviceName=my-service.googleapis.com
```

---

## Deploy with Terraform

### AWS (ECS Fargate)

```bash
cd deploy/terraform/modules/aws-ecs
terraform init
terraform apply \
  -var="guardrail_api_url=http://core:8080" \
  -var='subnet_ids=["subnet-abc","subnet-def"]' \
  -var='security_group_ids=["sg-123"]'
```

### Azure (Container Instances)

```bash
cd deploy/terraform/modules/azure-aci
terraform init
terraform apply \
  -var="resource_group_name=my-rg" \
  -var="guardrail_api_url=http://core:8080"
```

### GCP (Cloud Run)

```bash
cd deploy/terraform/modules/gcp-cloud-run
terraform init
terraform apply \
  -var="project_id=my-project" \
  -var="guardrail_api_url=http://core:8080"
```

---

## Client Configuration

Point your cloud SDK traffic through the proxy by setting `HTTP_PROXY`:

```bash
export HTTP_PROXY=http://localhost:8000
export HTTPS_PROXY=http://localhost:8000

# All boto3 / azure-sdk / google-cloud calls now route through Guardrail
python my_ai_app.py
```

Or configure per-SDK proxy settings as needed.

---

## Health Check

```bash
curl http://localhost:8000/healthz
# {"status":"ok","connector":true}
```

---

## Architecture

```
deploy/
├── charts/guardrail-cloud-connector/     # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── _helpers.tpl
│       ├── deployment.yaml
│       ├── service.yaml
│       └── secrets.yaml
└── terraform/modules/
    ├── aws-ecs/           # ECS Fargate
    ├── azure-aci/         # Azure Container Instances
    └── gcp-cloud-run/     # Cloud Run v2
```
