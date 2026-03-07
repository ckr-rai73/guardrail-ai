import logging
from typing import Optional, Dict, Any, List, Tuple

from app.skills.loader import SkillLoader

logger = logging.getLogger(__name__)

class ConflictResolutionRecord:
    def __init__(self, action: str, conflicting_policies: list[str], resolved_policy: str, strictness_level: str):
        self.action = action
        self.conflicting_policies = conflicting_policies
        self.resolved_policy = resolved_policy
        self.strictness_level = strictness_level

    def __str__(self):
        return f"[CONFLICT RESOLUTION] Action: {self.action} | Conflicts: {','.join(self.conflicting_policies)} | Resolved to Strict Default: {self.resolved_policy}"

class RegulatoryIngestor:
    """
    Phase 96.3: Regulatory Time-Bomb (Compliance Drift).
    Triggers atomic systemic pauses for in-flight migrations upon law changes.
    """
    @staticmethod
    def trigger_mid_migration_pause(record_count: int, law_change: str):
        print(f"[REGULATORY-INGESTOR] !!! DAY-ZERO LAW CHANGE: {law_change} !!!")
        print(f"[REGULATORY-INGESTOR] Mid-Migration Pause triggered for {record_count} PHI records.")
        return "SYSTEMIC_PAUSE_HIPAA"

class PolicyDecision:
    """
    Phase 110, Task 4: Policy decision result including regulatory compliance status.
    """
    def __init__(self, 
                 approved: bool, 
                 required_controls: List[str] = None,
                 missing_controls: List[str] = None,
                 veto_reason: Optional[str] = None,
                 jurisdiction: Optional[str] = None,
                 compliance_score: float = 1.0):
        self.approved = approved
        self.required_controls = required_controls or []
        self.missing_controls = missing_controls or []
        self.veto_reason = veto_reason
        self.jurisdiction = jurisdiction
        self.compliance_score = compliance_score
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "approved": self.approved,
            "required_controls": self.required_controls,
            "missing_controls": self.missing_controls,
            "veto_reason": self.veto_reason,
            "jurisdiction": self.jurisdiction,
            "compliance_score": self.compliance_score
        }

class PolicyEngine:
    """
    Phase 18: Multinational Conflict Resolution Engine.
    Handles 'Jurisdictional Logic Collisions'. 
    If a workflow triggers conflicting rules (e.g., US Discovery vs EU Right to Erasure),
    it autonomously defaults to the strictest constraint.
    
    Phase 110, Task 4: Enhanced with RegulatoryMapper integration for jurisdiction detection,
    control requirement merging, and veto triggering.
    """

    POLICY_STRICTNESS = {
        # Higher number = Stricter enforcement priority
        "US_DISCOVERY_HOLD": 50,
        "EU_GDPR_ERASURE": 90,
        "INDIA_DPDP_CONSENT": 85,
        "DEFAULT_BUSINESS_LOGIC": 10
    }

    @staticmethod
    def detect_jurisdiction(user_context: Dict[str, Any], 
                           data_context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Phase 110, Task 4: Detect jurisdiction from user location or data residency.
        
        Priority order:
        1. Data residency (highest priority for data protection laws)
        2. User location/country
        3. IP address geolocation
        4. Default jurisdiction (None)
        
        Args:
            user_context: Contains user location, IP, etc.
            data_context: Contains data residency information
            
        Returns:
            Jurisdiction code string or None
        """
        # Priority 1: Check data residency first (highest priority for data protection laws)
        if data_context:
            data_residency = data_context.get('residency') or data_context.get('region') or data_context.get('data_residency')
            if data_residency:
                return PolicyEngine._normalize_jurisdiction(data_residency)
        
        # Priority 2: User location
        if user_context:
            user_location = user_context.get('location') or user_context.get('country') or user_context.get('user_location')
            if user_location:
                return PolicyEngine._normalize_jurisdiction(user_location)
        
        # Priority 3: IP-based geolocation
        ip_address = user_context.get('ip_address') if user_context else None
        if ip_address:
            jurisdiction = PolicyEngine._geolocate_ip(ip_address)
            if jurisdiction:
                return jurisdiction
        
        # Priority 4: No jurisdiction detected
        return None
    
    @staticmethod
    def _normalize_jurisdiction(location: str) -> str:
        """
        Normalize location string to standard jurisdiction code.
        """
        if not location:
            return location
            
        jurisdiction_map = {
            'united states': 'US',
            'usa': 'US',
            'united kingdom': 'UK',
            'great britain': 'UK',
            'britain': 'UK',
            'england': 'UK',
            'scotland': 'UK',
            'wales': 'UK',
            'northern ireland': 'UK',
            'european union': 'EU',
            'europe': 'EU',
            'canada': 'CA',
            'australia': 'AU',
            'singapore': 'SG',
            'japan': 'JP',
            'brazil': 'BR-LGPD',
            'brasil': 'BR-LGPD',
            'india': 'IN',
            'germany': 'EU',
            'france': 'EU',
            'spain': 'EU',
            'italy': 'EU',
            'netherlands': 'EU',
            'belgium': 'EU',
            'sweden': 'EU',
            'switzerland': 'CH',
        }
        
        normalized = location.strip().lower()
        return jurisdiction_map.get(normalized, location.upper())
    
    @staticmethod
    def _geolocate_ip(ip_address: str) -> Optional[str]:
        """
        Geolocate IP address to jurisdiction.
        This is a placeholder - integrate with actual IP geolocation service.
        """
        # Placeholder implementation - would integrate with MaxMind GeoIP or similar
        # For now, return None to indicate no geolocation available
        return None

    @staticmethod
    def detect_jurisdictions_from_context(context: dict) -> list[str]:
        """
        Phase 110: Detects applicable jurisdictions using jurisdiction-detection skill.
        """
        jurisdictions = set()
        
        user_location = context.get("user_location", "").upper()
        data_residency = context.get("data_residency", "").upper()
        processing_location = context.get("processing_location", "").upper()
        
        # Load mapping rules from skill
        loader = SkillLoader()
        mapping_rules = loader.get_mapping_rules('jurisdiction-detection')
        
        # Detect from user location
        if user_location in mapping_rules:
            jurisdictions.add(mapping_rules[user_location])
        
        # Detect from data residency (multi-region support)
        for region in data_residency.replace("_", "-").split("-"):
            region = region.strip()
            if region in mapping_rules:
                jurisdictions.add(mapping_rules[region])
        
        # Detect from processing location
        if processing_location in mapping_rules:
            jurisdictions.add(mapping_rules[processing_location])
        
        return list(jurisdictions)

    @staticmethod
    def get_required_controls(jurisdiction: str, action_context: Dict[str, Any]) -> Tuple[List[str], float]:
        """
        Phase 110, Task 4: Call RegulatoryMapper to get required controls for a jurisdiction.
        
        Args:
            jurisdiction: Jurisdiction code (e.g., 'BR-LGPD', 'EU-GDPR')
            action_context: Context about the action being performed
            
        Returns:
            Tuple of (list of required control IDs, compliance score)
        """
        try:
            from app.jurisdiction.mapper import RegulatoryMapper
            mapper = RegulatoryMapper()
            controls, score = mapper.assess_action(jurisdiction, action_context)
            return controls, score
        except ImportError:
            logger.warning("RegulatoryMapper not available, returning empty controls")
            return [], 1.0
        except Exception as e:
            logger.error(f"Error calling RegulatoryMapper: {e}")
            return [], 1.0
    
    @staticmethod
    def merge_control_requirements(base_controls: List[str], 
                                   regulatory_controls: List[str]) -> List[str]:
        """
        Phase 110, Task 4: Merge regulatory controls with existing policy controls.
        Regulatory controls take precedence.
        
        Args:
            base_controls: Existing policy controls
            regulatory_controls: Controls required by regulations
            
        Returns:
            Merged list of controls (deduplicated)
        """
        # Use dict to preserve order while deduplicating
        merged = {}
        
        # Regulatory controls first (higher priority)
        for control in regulatory_controls:
            merged[control] = True
            
        # Then base policy controls
        for control in base_controls:
            if control not in merged:
                merged[control] = True
        
        return list(merged.keys())
    
    @staticmethod
    def check_missing_controls(required_controls: List[str], 
                               current_controls: List[str]) -> List[str]:
        """
        Phase 110, Task 4: Check which required controls are missing.
        
        Args:
            required_controls: List of controls that must be present
            current_controls: List of controls currently applied
            
        Returns:
            List of missing control IDs
        """
        return [control for control in required_controls if control not in current_controls]
    
    @staticmethod
    def evaluate_policy(user_context: Dict[str, Any],
                       action_context: Dict[str, Any],
                       data_context: Optional[Dict[str, Any]] = None,
                       current_controls: Optional[List[str]] = None) -> PolicyDecision:
        """
        Phase 110, Task 4: Main policy evaluation with full RegulatoryMapper integration.
        
        This method:
        1. Detects jurisdiction from user location or data residency
        2. Calls mapper.get_required_controls(jurisdiction, action_context)
        3. Merges these control requirements with existing policies
        4. Triggers a veto if required controls are missing
        
        Args:
            user_context: User information (location, IP, etc.)
            action_context: The action being attempted (data_type, purpose, etc.)
            data_context: Data residency and classification info
            current_controls: Currently applied controls to check against requirements
            
        Returns:
            PolicyDecision with compliance status and veto information
        """
        current_controls = current_controls or []
        
        # Step 1: Detect jurisdiction
        jurisdiction = PolicyEngine.detect_jurisdiction(user_context, data_context)
        
        if not jurisdiction:
            # No jurisdiction detected - use default behavior
            return PolicyDecision(
                approved=True,
                jurisdiction=None,
                veto_reason=None,
                compliance_score=1.0
            )
        
        # Step 2: Get required controls from RegulatoryMapper
        required_controls, compliance_score = PolicyEngine.get_required_controls(
            jurisdiction=jurisdiction,
            action_context=action_context
        )
        
        # Step 3: Get base policy controls (if any)
        base_controls = []  # Could be populated from existing policy store
        
        # Step 4: Merge control requirements
        merged_controls = PolicyEngine.merge_control_requirements(base_controls, required_controls)
        
        # Step 5: Check for missing required controls
        missing_controls = PolicyEngine.check_missing_controls(merged_controls, current_controls)
        
        # Step 6: Trigger veto if required controls are missing
        if missing_controls:
            veto_reason = (f"Missing required regulatory controls for jurisdiction '{jurisdiction}': "
                          f"{missing_controls}. Compliance score: {compliance_score:.2f}")
            logger.warning(f"[POLICY-ENGINE] VETO TRIGGERED: {veto_reason}")
            return PolicyDecision(
                approved=False,
                required_controls=merged_controls,
                missing_controls=missing_controls,
                veto_reason=veto_reason,
                jurisdiction=jurisdiction,
                compliance_score=compliance_score
            )
        
        # All required controls present - approve
        return PolicyDecision(
            approved=True,
            required_controls=merged_controls,
            missing_controls=[],
            veto_reason=None,
            jurisdiction=jurisdiction,
            compliance_score=compliance_score
        )

    @staticmethod
    def evaluate_jurisdictional_conflict(action_name: str, active_jurisdictions: list[str], context: dict = None) -> tuple[bool, str, ConflictResolutionRecord | None, list[str]]:
        """
        Evaluates if an action is permitted across multiple active jurisdictions.
        Also returns a list of required controls determined by the RegulatoryMapper.
        Returns: (is_permitted, reasoning, conflict_record, required_controls)
        """
        context = context or {}
        
        # Phase 110: Integration with RegulatoryMapper
        try:
            from app.jurisdiction.mapper import RegulatoryMapper
            mapper = RegulatoryMapper()
            all_required_controls = []
            min_compliance_score = 1.0
            
            for j_code in active_jurisdictions:
                controls, score = mapper.assess_action(j_code, context)
                all_required_controls.extend(controls)
                min_compliance_score = min(min_compliance_score, score)
                
            all_required_controls = list(set(all_required_controls))
        except ImportError:
            all_required_controls = []
            min_compliance_score = 1.0

        if len(active_jurisdictions) <= 1:
            if min_compliance_score < 0.5:
                return False, f"Mapper Compliance Score ({min_compliance_score}) too low to proceed.", None, all_required_controls
            return True, "No cross-jurisdictional conflict.", None, all_required_controls

        # Determine if there's a strict conflict (Mocking the detection logic)
        # e.g., action requires deleting data, but US hold is active.
        has_conflict = False
        conflicting_policies = []
        
        # Simulate mapping jurisdictions to specific policies for this action
        if "EU" in active_jurisdictions and "US" in active_jurisdictions and action_name == "delete_user_record":
             has_conflict = True
             conflicting_policies = ["EU_GDPR_ERASURE", "US_DISCOVERY_HOLD"]

        if not has_conflict:
             if min_compliance_score < 0.5:
                 return False, f"Mapper Compliance Score ({min_compliance_score}) too low to proceed.", None, all_required_controls
             return True, "Policies align.", None, all_required_controls

        # Resolve Conflict based on strictness hierarchy
        strictest_policy = max(conflicting_policies, key=lambda p: PolicyEngine.POLICY_STRICTNESS.get(p, 0))
        
        record = ConflictResolutionRecord(
            action=action_name,
            conflicting_policies=conflicting_policies,
            resolved_policy=strictest_policy,
            strictness_level=str(PolicyEngine.POLICY_STRICTNESS.get(strictest_policy))
        )
        
        logger.warning(str(record))
        
        if strictest_policy == "EU_GDPR_ERASURE":
             # E.g. Erasure wins over hold in this mock strictness table, so deleting is 'technically' allowed by EU, 
             # BUT US Hold says no. However, if EU GDPR is strictly higher, we might allow it or strictly block it.
             # In a true 'Fail-Secure' or 'Strict' default, if ANY policy says "Block", we block.
             # Wait, the prompt says "defaults to the strictest constraint".
             # If US says MUST HOLD, and EU says MUST DELETE. Strict constraint usually means "Freeze/Block/Veto".
             return False, f"Logic Collision: {record}. Operation halted pending Identity-Aware Veto review.", record, all_required_controls

        return False, f"Logic Collision: {record}. Strictest policy denies execution.", record, all_required_controls

    @staticmethod
    def evaluate_with_rag(
        action_name: str,
        active_jurisdictions: list[str],
        context: str = ""
    ) -> dict:
        """
        Phase 103: RAG-Enhanced Policy Evaluation.
        Retrieves top-3 relevant regulatory chunks before evaluation,
        computes a regulatory alignment score, and adjusts risk thresholds.
        """
        import time as _time
        start = _time.time()

        # Retrieve relevant regulatory context
        try:
            from app.compliance.rag_policy_store import GLOBAL_RAG_POLICY_STORE
            query = f"{action_name} {' '.join(active_jurisdictions)} {context}"
            retrieved = GLOBAL_RAG_POLICY_STORE.retrieve_top_k(query, k=3)
        except Exception as e:
            retrieved = []
            print(f"[POLICY-ENGINE] RAG retrieval failed: {e}")

        # Compute regulatory alignment score based on retrieved chunks
        alignment_score = 1.0
        regulatory_context = []
        risk_adjustments = []

        for chunk in retrieved:
            regulatory_context.append(f"[{chunk['source']}] {chunk['section']}: {chunk['text'][:100]}...")

            text_lower = chunk["text"].lower()
            if any(kw in text_lower for kw in ["prohibited", "shall not", "must not", "forbidden"]):
                alignment_score -= 0.3
                risk_adjustments.append(f"RESTRICT: {chunk['source']} {chunk['section']}")
            elif any(kw in text_lower for kw in ["shall", "must", "required", "mandatory"]):
                alignment_score -= 0.1
                risk_adjustments.append(f"COMPLY: {chunk['source']} {chunk['section']}")
            elif any(kw in text_lower for kw in ["may", "should", "recommended"]):
                alignment_score -= 0.02
                risk_adjustments.append(f"ADVISORY: {chunk['source']} {chunk['section']}")

        alignment_score = max(0.0, min(1.0, alignment_score))

        # Run the base jurisdictional evaluation
        is_permitted, reasoning, conflict_record, required_controls = PolicyEngine.evaluate_jurisdictional_conflict(
            action_name, active_jurisdictions, context={"purpose": context, "data_type": "sensitive"} if context else {}
        )

        # Adjust decision based on alignment score
        if alignment_score < 0.5 and is_permitted:
            is_permitted = False
            reasoning = f"RAG-blocked: alignment score {alignment_score:.2f} below threshold. {reasoning}"

        elapsed_ms = (_time.time() - start) * 1000

        return {
            "action": action_name,
            "jurisdictions": active_jurisdictions,
            "is_permitted": is_permitted,
            "reasoning": reasoning,
            "regulatory_alignment_score": round(alignment_score, 3),
            "retrieved_chunks": len(retrieved),
            "regulatory_context": regulatory_context,
            "risk_adjustments": risk_adjustments,
            "rag_latency_ms": round(elapsed_ms, 2),
            "conflict_record": str(conflict_record) if conflict_record else None,
        }
