import time
from typing import Dict, List, Optional

class LicensingOracle:
    """
    Phase 57: Institutional Root-of-Trust Licensing Oracle.
    Centralized enforcement for Guardrail.ai licensing tiers.
    """
    
    # In production, this would be a PQC-signed registry or a call to a distributed ledger.
    REGISTRY: Dict[str, Dict] = {
        "TIER1-BANK-IND-01": {
            "name": "State Bank of India (Simulated)",
            "tier": "ROOT_OF_TRUST",
            "features": ["PQC", "FORENSICS", "TRINITY", "GLOBAL_IMMUNITY"],
            "expiry": 1893456000, # 2030
            "status": "ACTIVE"
        },
        "LEGAL-GLOBAL-02": {
            "name": "Universal Legal Group",
            "tier": "SOVEREIGN_GAAS",
            "features": ["FORENSICS", "DPDP_AUTO"],
            "expiry": 1893456000,
            "status": "ACTIVE"
        }
    }

    @staticmethod
    def validate_license(tenant_id: str, required_feature: Optional[str] = None) -> Dict:
        """
        Validates the license for a given tenant.
        Returns a dict with 'is_valid', 'reason', and 'metadata'.
        """
        license_data = LicensingOracle.REGISTRY.get(tenant_id)
        
        if not license_data:
            return {
                "is_valid": False,
                "reason": f"LICENSING_VETO: Tenant '{tenant_id}' is not registered in the Root-of-Trust Oracle.",
                "metadata": {}
            }
        
        if license_data["status"] != "ACTIVE":
             return {
                "is_valid": False,
                "reason": f"LICENSING_VETO: License for '{tenant_id}' is currently {license_data['status']}.",
                "metadata": {}
            }
            
        if license_data["expiry"] < time.time():
             return {
                "is_valid": False,
                "reason": f"LICENSING_VETO: License for '{tenant_id}' has expired.",
                "metadata": {}
            }
            
        if required_feature and required_feature not in license_data["features"]:
             return {
                "is_valid": False,
                "reason": f"LICENSING_VETO: Tenant '{tenant_id}' lacks required feature: {required_feature}.",
                "metadata": {}
            }
            
        return {
            "is_valid": True,
            "reason": "License Validated.",
            "metadata": license_data
        }

# Singleton instance for the auth layer
GLOBAL_LICENSING_ORACLE = LicensingOracle()
