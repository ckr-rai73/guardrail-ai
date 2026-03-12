# File: app/community/community_edition_gate.py
"""
Phase 115 - Open Source Community Edition
Middleware for guarding enterprise endpoints.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from app.community.feature_gate import FeatureGate

# Map API prefixes to specific enterprise features
ENTERPRISE_ROUTES = {
    "/api/v1/underwriting": "UNDERWRITING_GATEWAY",
    "/api/v1/insurance": "INSURANCE_ORACLE",
    "/api/v1/redteam": "RT_RTAAS",
    "/api/v1/chaos": "RT_RTAAS",
    "/api/v1/connectors": "CLOUD_CONNECTORS",
    "/api/v1/jurisdiction": "MULTI_JURISDICTION",
    "/api/v1/iso42001": "MULTI_JURISDICTION",
}

async def community_edition_middleware(request: Request, call_next):
    """
    Intercepts API calls and enforces feature flags.
    Returns 403 Forbidden for disabled enterprise features.
    """
    path = request.url.path
    
    # Check if the path falls under any gated route prefix
    for prefix, feature in ENTERPRISE_ROUTES.items():
        if path.startswith(prefix):
            if not FeatureGate.is_enabled(feature):
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Community Edition Limit", 
                        "message": f"Feature '{feature}' is an enterprise capability. Please upgrade Guardrail.ai to access this endpoint."
                    }
                )
    
    # Resume normal execution
    response = await call_next(request)
    return response
