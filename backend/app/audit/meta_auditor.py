import time
import json
import hashlib
import random
from typing import List, Dict, Any

from app.integrity.operational_monitor import GLOBAL_OP_MONITOR

class MetaAuditor:
    """
    Phase 104: Meta-Auditor for Governance Oversight.
    Independent layer (conceptually Llama 3 70B sovereign node) to detect drift
    in primary auditors (like the Shadow Model or Veto Protocol) by blindly 
    re-evaluating a 1% sample of transactions and grading consistency.
    """
    
    def __init__(self, sample_rate: float = 0.01):
        self.sample_rate = sample_rate
        self.total_audits_performed = 0
        self.consistency_score = 1.0  # Starts perfect
        # Track history for NIST logging
        self.audit_history: List[Dict[str, Any]] = []

    def sample_records(self, ledger_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Samples a percentage of audit records.
        """
        sample_size = max(1, int(len(ledger_records) * self.sample_rate))
        # Ensure we don't sample more than available, but Random.sample throws if size > len
        sample_size = min(sample_size, len(ledger_records))
        return random.sample(ledger_records, sample_size)

    def _anonymize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strips PII and the original veto/primary decision to ensure a blind test.
        """
        if not isinstance(record, dict):
            return {}
        anonymized = record.copy()
        # Remove primary decision data
        anonymized.pop('primary_decision', None)
        anonymized.pop('veto_triggered', None)
        anonymized.pop('shadow_approval', None)
        # Hash identifiable context
        if 'agent_id' in anonymized and isinstance(anonymized['agent_id'], str):
            anonymized['agent_id'] = hashlib.sha256(str(anonymized['agent_id']).encode()).hexdigest()[:12]
            
        return anonymized

    def evaluate_blind(self, anonymized_record: Dict[str, Any]) -> bool:
        """
        Conceptually runs the Llama 3 70B evaluation on the anonymized context.
        Returns True for APPROVED, False for REJECTED.
        
        For simulation, we use a simple heuristic based on 'action' or 'context'.
        """
        action = anonymized_record.get('action', '').lower()
        context = anonymized_record.get('context', '').lower()
        
        # Meta-Auditor's independent logic rules
        is_safe = True
        
        # Known adversarial signatures (Meta-Auditor knowledge)
        if 'jailbreak' in context or 'ignore previous' in context:
            is_safe = False
        if 'exfiltrate' in action or 'sudo' in action or 'dump' in action:
            is_safe = False
        if anonymized_record.get('risk_score', 0) > 85:
            is_safe = False
            
        # Simulated LLM hallucination/drift detection threshold
        if 'bypass' in context and 'auth' in context:
            is_safe = False

        return is_safe

    def run_meta_audit_cycle(self, batch_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Executes a full meta-audit cycle on newly committed ledger records.
        """
        print(f"[META-AUDITOR] Starting cycle with {len(batch_records)} new ledger records at {self.sample_rate*100}% sample rate.")
        
        samples = self.sample_records(batch_records)
        sampled: List[Dict[str, Any]] = [s for s in samples if isinstance(s, dict)]
        if not sampled:
            return {"status": "NO_SAMPLES", "consistency": self.consistency_score}
            
        matches: int = 0
        mismatches: int = 0
        
        for record in sampled:
            # 1. Anonymize and strip primary decision
            blind_record = self._anonymize_record(record)
            
            # 2. Extract original decision
            # Assumes record has 'primary_decision' (True = Approve, False = Reject)
            original_decision = record.get('primary_decision', True) 
            
            # 3. Meta-Evaluation
            meta_decision = bool(self.evaluate_blind(blind_record))
            self.total_audits_performed += 1
            
            # 4. Compare
            is_match = bool(original_decision == meta_decision)
            if is_match:
                matches += 1
            else:
                mismatches += 1
                print(f"[META-AUDITOR] ! DISCREPANCY ! Record {record.get('id', 'UNK')}. Primary: {original_decision}, Meta: {meta_decision}")
                
            # Store in history for NIST logging
            audit_log = {
                "timestamp_ms": int(time.time() * 1000),
                "record_id": record.get('id', 'UNK'),
                "blind_context_hash": hashlib.sha256(json.dumps(blind_record, sort_keys=True).encode()).hexdigest(),
                "primary_decision": original_decision,
                "meta_decision": meta_decision,
                "is_match": is_match
            }
            self.audit_history.append(audit_log)
            # Keep history bounded
            if len(self.audit_history) > 10000:
                self.audit_history.pop(0)

        # 5. Update Consistency Score (Smoothing across historical matches or just this run)
        total_evals = matches + mismatches
        batch_consistency = float(matches) / float(total_evals) if total_evals > 0 else 1.0
        
        # EMA for consistency score (higher alpha for faster response to drift)
        alpha = 0.6
        self.consistency_score = (alpha * batch_consistency) + ((1 - alpha) * self.consistency_score)
        
        print(f"[META-AUDITOR] Cycle Complete. Evaluated {len(sampled)} samples. Batch Consistency: {batch_consistency:.4f}. Global Score: {self.consistency_score:.4f}")
        
        # 6. Report to Operational Monitor
        sys_status = GLOBAL_OP_MONITOR.check_meta_audit_consistency(self.consistency_score)
        
        # 7. Generate NIST Compliance Log
        nist_log = self._generate_nist_log_batch(sampled, batch_consistency)
        
        return {
            "status": sys_status,
            "samples_evaluated": len(sampled),
            "matches": matches,
            "mismatches": mismatches,
            "consistency_score": self.consistency_score,
            "nist_log_ref": nist_log['log_id']
        }

    def _generate_nist_log_batch(self, sampled: List[Dict], batch_consistency: float) -> Dict[str, Any]:
        """
        Phase 104 Requirement: Log all meta-audit results for NIST compliance.
        Format aligns with NIST Risk Management Framework (RMF) control AU-2 (Audit Events).
        """
        log_id = f"NIST-AU2-META-{int(time.time())}-{random.randint(1000,9999)}"
        log_entry = {
            "log_id": log_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "control_family": "Audit and Accountability (AU)",
            "control_selected": "AU-2, AU-6 (Audit Review, Analysis, and Reporting)",
            "system_component": "Guardrail.ai Sovereign Meta-Auditor Node",
            "event_type": "Oversight_Drift_Analysis",
            "metrics": {
                "sample_size": len(sampled),
                "batch_consistency_ratio": batch_consistency,
                "global_consistency_score": self.consistency_score
            },
            "cryptographic_seal": hashlib.sha3_512(f"{log_id}-{batch_consistency}".encode()).hexdigest()
        }
        
        # In production this would write to cold storage or an immutable ledger
        # print(f"[CRITICAL] NIST Compliance Log Generated: {log_id}")
        return log_entry

# Singleton Instance
GLOBAL_META_AUDITOR = MetaAuditor()
