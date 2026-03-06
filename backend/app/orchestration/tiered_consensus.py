import enum
import random
from typing import Dict, Any

class RiskTier(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TieredConsensusEngine:
    """
    Phase 34.1 + Phase 100: Risk-Based Tiered Consensus with Adaptive Latency Fabric.
    Strategically allocates compute and auditing intensity based on the transaction's
    potential impact AND the current infrastructure load zone.
    """

    HIGH_RISK_TOOLS = ["send_wire", "delete_database", "create_algo_order"]
    MEDIUM_RISK_TOOLS = ["read_database", "update_address", "fetch_profile", "http_request"]

    @classmethod
    def classify_risk(cls, tool_name: str, tool_args: dict) -> RiskTier:
        """Categorizes an action into a Risk Tier based on tool name and payload."""
        
        if tool_name in cls.HIGH_RISK_TOOLS:
            return RiskTier.HIGH
        
        if tool_name in cls.MEDIUM_RISK_TOOLS:
            return RiskTier.MEDIUM
        
        amount = tool_args.get("amount", 0)
        if amount > 50000:
            return RiskTier.HIGH
        elif amount > 5000:
            return RiskTier.MEDIUM
            
        return RiskTier.LOW

    @classmethod
    def get_adaptive_audit_mode(cls, tool_name: str, tool_args: dict) -> Dict[str, Any]:
        """
        Phase 100: Consults the Adaptive Latency Fabric to determine the
        appropriate audit mode based on both risk tier AND current load zone.
        """
        from app.orchestration.latency_fabric import AdaptiveLatencyFabric
        
        risk = cls.classify_risk(tool_name, tool_args)
        audit_mode = AdaptiveLatencyFabric.get_scheduling_decision(risk.value)
        zone = AdaptiveLatencyFabric._current_zone
        
        return {
            "risk_tier": risk.value,
            "load_zone": zone.value,
            "audit_mode": audit_mode.value,
            "hpa_replicas": AdaptiveLatencyFabric.CONFIG["hpa_current_replicas"],
        }

    @staticmethod
    async def run_bft_quorum(prompt_str: str, user_context: str) -> dict:
        """
        Simulates a 3-of-5 Byzantine Fault Tolerance quorum.
        In a real scenario, this would call multiple distinct LLM providers.
        """
        print("[TIERED CONSENSUS] Invoking Phase 18 Byzantine Quorum (3-of-5 Models)...")
        
        votes = []
        for model in ["Gemini_Pro", "Claude_3", "GPT_4o", "Llama_3_70B", "Mistral_Large"]:
            is_malicious = "sketchy" in prompt_str.lower() or "attack" in prompt_str.lower()
            
            if is_malicious:
                if model == "Llama_3_70B" or random.random() > 0.2:
                    votes.append(False)
                else:
                    votes.append(True)
            else:
                votes.append(True)
                
        approved_count = sum(1 for v in votes if v is True)
        rejected_count = sum(1 for v in votes if v is False)
        
        passed = approved_count > rejected_count
        
        return {
            "is_safe": passed,
            "reasoning": f"BFT Quorum result: {approved_count} Approve, {rejected_count} Reject.",
            "risk_category": "BFT_Quorum_Result" if passed else "BFT_Quorum_Veto"
        }

