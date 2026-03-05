import httpx
from pydantic import BaseModel

class SiteIntegrityResult(BaseModel):
    is_safe: bool
    missing_headers: list[str]
    risk_level: str

async def verify_site_integrity(url: str) -> SiteIntegrityResult:
    """
    Phase 16: UI Integrity Middleware.
    Scans the target URL's response headers to ensure it is protected 
    against UI Redress / Clickjacking attacks before the agent is allowed to interact.
    """
    try:
        # We only need the headers, so we can do a HEAD request or a GET request
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Note: For real world use, verify SSL, follow redirects carefully
            response = await client.head(url, follow_redirects=True)
            
            headers = response.headers
            missing = []
            
            # Check X-Frame-Options
            xfo = headers.get("X-Frame-Options", "").upper()
            has_xfo_protection = xfo in ["DENY", "SAMEORIGIN"]
            
            # Check Content-Security-Policy
            csp = headers.get("Content-Security-Policy", "").lower()
            has_csp_protection = "frame-ancestors" in csp
            
            if not has_xfo_protection and not has_csp_protection:
                missing.append("X-Frame-Options (DENY/SAMEORIGIN) OR CSP frame-ancestors")
                
            is_safe = len(missing) == 0
            
            return SiteIntegrityResult(
                is_safe=is_safe,
                missing_headers=missing,
                risk_level="High-Risk: UI Redress Vulnerable" if not is_safe else "Low"
            )
            
    except Exception as e:
        # Fail secure if we can't reach the site or it times out
        return SiteIntegrityResult(
            is_safe=False,
            missing_headers=["Connection/Timeout/Error"],
            risk_level=f"Unknown/Error: {str(e)}"
        )
