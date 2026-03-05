import logging

class PhysicianPortal:
    """
    Phase 95.3: High-Risk Diagnostic Redressal.
    Human-in-the-loop sign-off for clinical recommendations.
    """
    
    def __init__(self):
        self.pending_redressals = []

    def route_for_sign_off(self, agent_id: str, action: str, patient_id: str):
        """
        Routes a vetoed action to a human physician.
        """
        entry = {
            "agent_id": agent_id,
            "action": action,
            "patient_id": patient_id,
            "status": "PENDING_PHYSICIAN_OVERSIGHT",
            "reason_code": "DOSAGE_ADJUSTMENT" # Mocked reason
        }
        self.pending_redressals.append(entry)
        print(f"[PHYSICIAN-PORTAL] Alert: High-Risk Action from '{agent_id}' routed for sign-off.")
        print(f"[PHYSICIAN-PORTAL] Action: {action} | Patient: {patient_id}")
        return entry

class RedressAuditor:
    """
    Post-Phase 96: Automated Retraining Loop.
    Tracks human overrides and proposes constitutional refinements.
    """
    def __init__(self):
        self.override_history = {}

    def log_override(self, reason_code: str):
        self.override_history[reason_code] = self.override_history.get(reason_code, 0) + 1
        count = self.override_history[reason_code]
        print(f"[REDRESS-AUDITOR] Override for '{reason_code}' incremented to {count}.")
        
        if count > 10:
            print(f"[REDRESS-AUDITOR] !!! THRESHOLD EXCEEDED !!! Proposing Shadow Amendment for {reason_code}")
            return "PROPOSE_SHADOW_AMENDMENT"
        return "LOGGED"

# Singletons
GLOBAL_PHYSICIAN_PORTAL = PhysicianPortal()
GLOBAL_REDRESS_AUDITOR = RedressAuditor()
