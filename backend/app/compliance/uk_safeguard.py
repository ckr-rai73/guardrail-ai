import time
import uuid
from typing import Dict, Any

from app.agents.veto_protocol import VETO_QUEUE, AUDIT_LOG
from app.forensics.forensic_replay import ReplayEngine

class UKContestabilityGateway:
    """
    Phase 23: UK Data Act 2025 "Safeguard & Contestability"
    Provides the legally mandated "Right to Explanation" for Automated Decision Making (ADM).
    Allows end-users to halt and contest an autonomous agent's decision, forcing a human review.
    """
    
    @classmethod
    def contest_adm_decision(cls, trace_id_or_hash: str, user_reason: str) -> Dict[str, Any]:
        """
        Receives a contestation request from the end-user.
        1. Locates the specific agent decision in the Audit Log or active Veto Queue.
        2. Preserves the forensic state.
        3. Escalates it to a human reviewer with a 'CONTESTED_BY_USER' flag.
        """
        
        # Search the immutable audit log first (for completed actions)
        target_log = next((log for log in AUDIT_LOG if log.get("merkle_hash") == trace_id_or_hash or log.get("finra_telemetry_dump", {}).get("trace_id") == trace_id_or_hash), None)
        
        target_item = None
        
        if target_log:
             # Create a new VETO_QUEUE item derived from the completed log to trigger a retroactive review
             target_item = {
                 "id": str(uuid.uuid4()),
                 "agent_id": target_log["agent_id"],
                 "action": target_log["action"],
                 "args": target_log["args"],
                 "status": "CONTESTED_BY_USER",
                 "reasoning": f"Retroactive Contestation: {user_reason}",
                 "timestamp_added": time.time(),
                 "takedown_limit_hours": 24, # 24 hour SLA for human response
                 "original_merkle_hash": target_log.get("merkle_hash"),
                 "forensic_replay": None
             }
             
             # Attempt to generate a deterministic replay immediately for the reviewer
             try:
                 if target_log.get("merkle_hash"):
                     target_item["forensic_replay"] = ReplayEngine.generate_replay_attestation(target_log["merkle_hash"])
             except Exception:
                 pass
                 
             VETO_QUEUE.append(target_item)
             
        else:
             # Search active veto queue
             target_item = next((v for v in VETO_QUEUE if v.get("id") == trace_id_or_hash or v.get("action_merkle_hash") == trace_id_or_hash), None)
             if target_item:
                  target_item["status"] = "CONTESTED_BY_USER"
                  target_item["contestation_reason"] = user_reason
             
        if not target_item:
             return {"status": "error", "message": "Transaction or Trace ID not found."}
             
        return {
            "status": "success",
            "message": "UK ADM Contestation Filed Successfully. Execution paused. Human Audit required.",
            "queue_id": target_item.get("id"),
            "sla": "24 Hours"
        }
