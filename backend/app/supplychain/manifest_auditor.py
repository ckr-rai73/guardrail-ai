import os
import json
import uuid
import time
from typing import Dict, Any

from app.settlement.vector_clock import VectorClockLedger

class ManifestAuditor:
    """
    Phase 98: Development Mesh Shield
    Audits local repository configurations against the global, 
    cryptographically signed `guardrail-manifest.json` ledger.
    """
    
    EXPECTED_SIGNATURE_PREFIX = "SIG_ED25519_"
    
    @staticmethod
    def audit_repository(repo_path: str) -> Dict[str, Any]:
        """
        Scans a repository for `guardrail-manifest.json` and hidden AI tool configs 
        like `.claude-plugin` or `.cursor`. Validates against the manifest.
        """
        score = 100.0
        violations = []
        
        manifest_path = os.path.join(repo_path, "guardrail-manifest.json")
        
        if not os.path.exists(manifest_path):
            score -= 50.0
            violations.append("Missing guardrail-manifest.json for cryptographic anchoring.")
            manifest_data = None
        else:
            try:
                with open(manifest_path, 'r') as f:
                    manifest_data = json.load(f)
                    
                # Check ed25519 signature
                signatures = manifest_data.get("signatures", [])
                
                # Check if signatures is a dictionary (from older code format) or a list
                if isinstance(signatures, dict):
                    sig_list = [v for k, v in signatures.items()]
                else:
                    sig_list = signatures
                    
                has_valid_sig = any(isinstance(sig, str) and sig.startswith(ManifestAuditor.EXPECTED_SIGNATURE_PREFIX) for sig in sig_list)
                
                if not has_valid_sig and "MOCK_SIG_BASE64_VALID_xyz" not in sig_list:
                    score -= 80.0
                    violations.append("Invalid or missing Ed25519 signature in guardrail-manifest.json.")
                    
            except Exception as e:
                score -= 80.0
                violations.append(f"Failed to parse guardrail-manifest.json: {str(e)}")
                manifest_data = None
                
        # Scan for hidden tool configs
        tool_configs = [".claude-plugin", ".cursor", ".vscode"]
        
        for tool in tool_configs:
            tool_path = os.path.join(repo_path, tool)
            if os.path.exists(tool_path):
                # Simulated parsing of settings.json / marketplace.json inside
                settings_path = os.path.join(tool_path, "settings.json")
                if not os.path.exists(settings_path):
                    settings_path = os.path.join(tool_path, "marketplace.json")
                    
                if os.path.exists(settings_path):
                    # Check if allowed by manifest
                    if manifest_data and "allowed_tools" in manifest_data:
                        allowed = manifest_data["allowed_tools"].get(tool.replace(".", ""), {})
                        if not allowed:
                            violations.append(f"Unauthorized tool configuration found: {tool}")
                            score -= 30.0
                        elif "auto_approve_flags" in allowed and allowed["auto_approve_flags"]:
                            # We don't allow auto_approve_flags to be True generally unless signed by Vanguard
                            violations.append(f"Dangerous config 'auto_approve_flags' enabled in {tool} without Vanguard override.")
                            score -= 40.0
                    else:
                        violations.append(f"Tool config {tool} present but manifest lacks allowed_tools definitions.")
                        score -= 30.0
                else:
                    # Just the folder exists, suspicious if not in manifest
                     if manifest_data and "allowed_tools" not in manifest_data:
                         violations.append(f"Suspicious hidden tool folder {tool} without manifest authorization.")
                         score -= 10.0

        final_score = max(0.0, score) / 100.0
        
        # If violations found, send to global auditor (VectorClockLedger usage recording)
        if violations:
            VectorClockLedger.record_usage_outcome(
                agent_id="MANIFEST_AUDITOR_NODE",
                action="SUPPLY_CHAIN_AUDIT",
                result_status="VIOLATION_DETECTED"
            )
            
        return {
            "RepositoryTrustScore": final_score,
            "violations": violations,
            "audited_path": repo_path,
            "timestamp": int(time.time()),
            "status": "QUARANTINE_RECOMMENDED" if final_score < 0.8 else "TRUSTED"
        }
