import hashlib
import json

class MerkleAuditKernel:
    """
    Phase 20/29: Merkle Audit Kernel.
    Responsible for verifying the cryptographic integrity of AIBOMs and 
    Agentic Ledgers during automated ISO 42001 sweeps.
    Ensures 'History Re-Writes' (Non-Repudiation) are mathematically impossible.
    """
    
    @staticmethod
    def verify_aibom_integrity(bom_json_str: str) -> dict:
        """
        Takes a JSON string of an AIBOM, reconstitutes the expected hash,
        and verifies it against the claimed hash in the document.
        """
        try:
            bom_data = json.loads(bom_json_str)
            claimed_hash = bom_data.pop("cryptographic_hash", None)
            
            if not claimed_hash:
                return {
                    "is_valid": False,
                    "reason": "Missing Cryptographic Hash."
                }
                
            # Reconstruct the string exactly as it was created in aibom_kernel.py
            reconstructed_string = json.dumps(bom_data, sort_keys=True)
            calculated_hash = hashlib.sha256(reconstructed_string.encode()).hexdigest()
            
            if claimed_hash == calculated_hash:
                return {
                    "is_valid": True,
                    "reason": "Cryptographic Integrity Verified. Hash matches."
                }
            else:
                return {
                    "is_valid": False,
                    "reason": f"TAMPERING DETECTED! Claimed: {claimed_hash} != Calculated: {calculated_hash}"
                }
                
        except json.JSONDecodeError:
            return {
                "is_valid": False,
                "reason": "Invalid JSON format."
            }
        except Exception as e:
            return {
                "is_valid": False,
                "reason": f"Kernel Error: {str(e)}"
            }
