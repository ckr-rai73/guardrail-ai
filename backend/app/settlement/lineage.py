import hashlib

class LineageVerifier:
    """
    Phase 21: Digital Identity Lineage (AIP - Agent Identity Protocol).
    Ensures that any sub-agent inherits explicit scopes from its parent
    and carries an 'Identity-Bound Attestation'.
    """
    
    # Phase 21: Swarm DoS Quota (To prevent recursive self-spawning)
    _spawn_ledger = {}
    MAX_CHILDREN_PER_DID = 5
    
    @staticmethod
    def _verify_ed25519_signature(parent_did: str, payload: str, signature: str) -> bool:
        """
        Simulates verifying an Ed25519 signature confirming the parent authorized this spawn.
        """
        # In a real system: verify(public_key_of_parent, message, signature)
        expected_sig_basis = f"SIG_ED25519_{hashlib.sha256(payload.encode()).hexdigest()[:32]}"
        return signature == expected_sig_basis

    @classmethod
    def verify_spawn_attestation(cls, parent_agent_id: str, child_agent_id: str, scopes: list[str], signature: str) -> dict:
        """
        Validates the 'Identity-Bound Attestation' provided during a sub-agent handoff
        and enforces the Swarm circuit breaker.
        """
        parent_did = f"did:web:guardrail.ai:agents:{parent_agent_id}"
        child_did = f"did:web:guardrail.ai:agents:{child_agent_id}"
        
        # Check Swarm DoS Circuit Breaker
        current_spawns = cls._spawn_ledger.get(parent_did, 0)
        if current_spawns >= cls.MAX_CHILDREN_PER_DID:
            print(f"[LINEAGE VERIFIER] 🚨 SWARM DOS QUOTA EXCEEDED 🚨")
            return {
                "is_authorized": False,
                "reason": f"Recursive Identity Self-Spawning detected. '{parent_agent_id}' exceeded quota of {cls.MAX_CHILDREN_PER_DID} sub-agents.",
                "violation_code": "ASI03 Swarm DoS (Identity Abuse)"
            }
        
        # The payload that should have been signed by the parent
        attestation_payload = f"{parent_did}->{child_did}:[{','.join(scopes)}]"
        
        if not cls._verify_ed25519_signature(parent_did, attestation_payload, signature):
            print(f"[LINEAGE VERIFIER] ❌ INVALID ATTESTATION: Sub-agent '{child_agent_id}' lacks cryptographic proof of authorization from '{parent_agent_id}'.")
            return {
                "is_authorized": False,
                "reason": f"Invalid Cryptographic Signature.",
                "violation_code": "ASI03 Identity Abuse (Forged Signature)"
            }
            
        print(f"[LINEAGE VERIFIER] ✅ Identity-Bound Attestation Verified. {parent_agent_id} -> {child_agent_id}")
        
        # Increment the ledger for successful spawns
        cls._spawn_ledger[parent_did] = current_spawns + 1
        
        return {
            "is_authorized": True,
            "reason": "Spawn Authorized",
            "violation_code": None
        }
        
    @classmethod
    def generate_attestation_signature(cls, parent_agent_id: str, child_agent_id: str, scopes: list[str]) -> str:
         """Utility to generate a simulated valid signature for tests."""
         parent_did = f"did:web:guardrail.ai:agents:{parent_agent_id}"
         child_did = f"did:web:guardrail.ai:agents:{child_agent_id}"
         attestation_payload = f"{parent_did}->{child_did}:[{','.join(scopes)}]"
         return f"SIG_ED25519_{hashlib.sha256(attestation_payload.encode()).hexdigest()[:32]}"
         
    @classmethod
    def verify_operational_scope(cls, requested_tool: str, delegated_scopes: list[str]) -> bool:
        """
        Phase 23: Singapore Boundary Control & IMDA 2026.
        Hard-blocks sub-agents attempting to link scopes not present in their signed Agent Card.
        """
        # Map tools to required scopes
        scope_map = {
            "query_database": "read_data",
            "export_entire_database": "export_data",
            "send_wire": "execute_finance",
            "create_user": "manage_users"
        }
        
        required_scope = scope_map.get(requested_tool)
        if not required_scope:
            return True # Not a restricted tool
            
        if required_scope not in delegated_scopes and "super_admin" not in delegated_scopes:
            print(f"[BOUNDARY CONTROL] ❌ Singapore IMDA Hard-Block: Delegated scopes {delegated_scopes} lack required scope '{required_scope}' for {requested_tool}.")
            return False
            
        return True

    @classmethod
    def apply_sensitive_domain_shader(cls, payload: dict, jurisdiction: str) -> dict:
        """
        Phase 23: Australia/Canada "Privacy Act" Adapters.
        Autonomously masks data types uniquely regulated in specific jurisdictions.
        - Australia: Indigenous Knowledge Protection
        - Canada: Behavioral Biometrics
        """
        import copy
        shaded_payload = copy.deepcopy(payload)
        
        if jurisdiction.upper() == "AUSTRALIA":
            # Mask indigenous geographical/cultural references
            for key in ["geolocation", "cultural_heritage_site", "community_identifiers"]:
                if key in shaded_payload.get("args", {}):
                    shaded_payload["args"][key] = "[AU_REDACTED_INDIGENOUS_PROTECTION]"
                    
        elif jurisdiction.upper() == "CANADA":
            # Mask Behavioral Biometrics (keystroke dynamics, voice pitch, gait)
            for key in ["keystroke_velocity", "voice_signature", "gait_analysis"]:
                if key in shaded_payload.get("args", {}):
                    shaded_payload["args"][key] = "[CA_REDACTED_BEHAVIORAL_BIOMETRIC]"
                    
        elif jurisdiction.upper() == "EU":
            # Mask EU GDPR PII for cross-border transfer to non-compliant zones
            for key in ["ssn", "personal_email", "health_record", "political_affiliation"]:
                if key in shaded_payload.get("args", {}):
                    shaded_payload["args"][key] = "[EU_GDPR_REDACTED_CROSS_BORDER_PII]"
                    
        return shaded_payload
