import json
import hashlib

class ToolManifestVerifier:
    """
    Phase 30.3: Tool Manifest Non-Repudiation.
    Intersects the Model Context Protocol (MCP) tool loading process.
    Requires an Ed25519 cryptographic signature (simulated here via SHA256 of salt+content)
    on all tool capabilities to prevent 'Tool Registry Rug Pulls'.
    """
    
    # In production, this would be an Ed25519 public key.
    # We use a mock salt here for the simulation drill.
    MOCK_PUBLIC_KEY_SALT = "guardrail_mcp_pub_key_9921"
    
    @classmethod
    def generate_mock_signature(cls, manifest_dict: dict) -> str:
        """Helper to generate a valid signature for the test."""
        # Remove any existing signature to avoid recursive hashing
        clean_manifest = {k: v for k, v in manifest_dict.items() if k != "ed25519_signature"}
        serialized = json.dumps(clean_manifest, sort_keys=True)
        payload = f"{cls.MOCK_PUBLIC_KEY_SALT}::{serialized}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @classmethod
    def verify_tool_manifest(cls, manifest_dict: dict) -> dict:
        """
        Verifies that the provided tool manifest signature matches 
        its declared capabilities, ensuring it hasn't been tampered with post-approval.
        """
        try:
            provided_sig = manifest_dict.get("ed25519_signature")
            
            if not provided_sig:
                 return {
                    "is_valid": False,
                    "reason": "Missing Ed25519 Signature. All MCP tools require cryptographic non-repudiation."
                }
                 
            # Reconstruct the expected signature
            expected_sig = cls.generate_mock_signature(manifest_dict)
            
            if provided_sig == expected_sig:
                return {
                    "is_valid": True,
                    "reason": "Manifest Integrity Verified."
                }
            else:
                 return {
                    "is_valid": False,
                    "reason": "Signature Mismatch. TAMPERING DETECTED in Tool Capabilities."
                }
                 
        except Exception as e:
            return {
                "is_valid": False,
                "reason": f"Verification Error: {str(e)}"
            }
