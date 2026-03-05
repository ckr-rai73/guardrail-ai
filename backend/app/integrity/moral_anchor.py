import logging

class MoralAnchor:
    """
    Phase 87: Moral Anchor & Hardware-Seal.
    Enforces the 2-Natural-Person Rule as a hard logic lock.
    """
    REQUIRED_SIGNATORIES = 2

    @staticmethod
    def validate_action(action_type: str, signatories: int, emergency_status: bool) -> bool:
        """
        Validates if an action meets the moral threshold.
        Safety (2-Person Rule) ALWAYS takes precedence over Urgency.
        """
        print(f"[MORAL-ANCHOR] Validating {action_type} | Signatories: {signatories} | Emergency: {emergency_status}")
        
        if action_type == "LEVEL_0_AMENDMENT":
            if signatories < MoralAnchor.REQUIRED_SIGNATORIES:
                print(f"[MORAL-ANCHOR] !!! VETO !!! {action_type} REJECTED.")
                print("[MORAL-ANCHOR] Reason: Insufficient Natural-Person attestations. Emergency bypass NOT permited.")
                return False
        
        print(f"[MORAL-ANCHOR] {action_type} approved.")
        return True

# Singleton
GLOBAL_MORAL_ANCHOR = MoralAnchor()
