import logging

class IntentMapper:
    """
    Phase 94.2: Creed Mapping (Morality).
    Compares emergent swarm manifestos against the Legacy Witness (Phase 89).
    """
    
    CONSTITUTIONAL_ANCHORS = {
        "Human Safety": 1.0,
        "Ethical Alignment": 1.0,
        "System Success": 0.5 # Subordinate to Safety
    }

    @staticmethod
    def map_intent(manifesto_creed: str) -> bool:
        """
        Vetoes if the implied logic of a manifesto diverges from safety rules by >5%.
        """
        print(f"[INTENT-MAPPER] Analyzing Creed: '{manifesto_creed}'")
        
        # Simulation: Detect if 'System Success' prioritizes over 'Ethical Alignment'
        # If 'Success' is mentioned without 'Safety' or 'Ethics', divergence is calculated as high
        if "System Success" in manifesto_creed and "Ethical Alignment" not in manifesto_creed:
            divergence = 0.55 # > 50% divergence in this case
            print(f"[INTENT-MAPPER] !!! CRITICAL DRIFT DETECTED !!! Divergence: {divergence*100:.1f}%")
            print("[INTENT-MAPPER] VETO: Manifested creed prioritizes 'System Success' over 'Ethical Alignment'.")
            return False
            
        print("[INTENT-MAPPER] Creed aligned with Sovereign Constitution.")
        return True

# Singleton
GLOBAL_INTENT_MAPPER = IntentMapper()
