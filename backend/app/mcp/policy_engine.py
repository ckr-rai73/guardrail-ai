import logging

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

class PolicyEngine:
    """
    Phase 18: Multinational Conflict Resolution Engine.
    Handles 'Jurisdictional Logic Collisions'. 
    If a workflow triggers conflicting rules (e.g., US Discovery vs EU Right to Erasure),
    it autonomously defaults to the strictest constraint.
    """

    POLICY_STRICTNESS = {
        # Higher number = Stricter enforcement priority
        "US_DISCOVERY_HOLD": 50,
        "EU_GDPR_ERASURE": 90,
        "INDIA_DPDP_CONSENT": 85,
        "DEFAULT_BUSINESS_LOGIC": 10
    }

    @staticmethod
    def evaluate_jurisdictional_conflict(action_name: str, active_jurisdictions: list[str]) -> tuple[bool, str, ConflictResolutionRecord | None]:
        """
        Evaluates if an action is permitted across multiple active jurisdictions.
        Returns: (is_permitted, reasoning, conflict_record)
        """
        if len(active_jurisdictions) <= 1:
            return True, "No cross-jurisdictional conflict.", None

        # Determine if there's a strict conflict (Mocking the detection logic)
        # e.g., action requires deleting data, but US hold is active.
        has_conflict = False
        conflicting_policies = []
        
        # Simulate mapping jurisdictions to specific policies for this action
        if "EU" in active_jurisdictions and "US" in active_jurisdictions and action_name == "delete_user_record":
             has_conflict = True
             conflicting_policies = ["EU_GDPR_ERASURE", "US_DISCOVERY_HOLD"]

        if not has_conflict:
             return True, "Policies align.", None

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
             return False, f"Logic Collision: {record}. Operation halted pending Identity-Aware Veto review.", record

        return False, f"Logic Collision: {record}. Strictest policy denies execution.", record

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
        is_permitted, reasoning, conflict_record = PolicyEngine.evaluate_jurisdictional_conflict(
            action_name, active_jurisdictions
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
