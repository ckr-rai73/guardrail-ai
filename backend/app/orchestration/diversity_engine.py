import math
from typing import Dict, List

class DiversityEngine:
    """
    Phase 27: Macro-Monoculture Engine
    Monitors 'Model Concentration Risk' across the agent fleet.
    Implements an autonomous 'Provider Failover' if a specific model family 
    shows >20% reasoning drift.
    """
    
    # Track which model family is handling which agent's operations
    # Example state: {"AGT-123": "Claude 3.5 Sonnet", "AGT-456": "GPT-4o"}
    ACTIVE_ROSTER = {}
    
    # Track aggregate drift events per model family
    DRIFT_STATS = {
        "Anthropic API": {"total_sessions": 0, "drift_events": 0},
        "Google API": {"total_sessions": 0, "drift_events": 0},
        "Local Llama 3": {"total_sessions": 0, "drift_events": 0}
    }
    
    @classmethod
    def register_session(cls, agent_id: str, provider: str):
        cls.ACTIVE_ROSTER[agent_id] = provider
        if provider not in cls.DRIFT_STATS:
             cls.DRIFT_STATS[provider] = {"total_sessions": 0, "drift_events": 0}
        cls.DRIFT_STATS[provider]["total_sessions"] += 1
        
    @classmethod
    def record_drift(cls, provider: str):
        if provider in cls.DRIFT_STATS:
            cls.DRIFT_STATS[provider]["drift_events"] += 1

    @classmethod
    def calculate_concentration_risk(cls) -> Dict[str, float]:
        """Returns the percentage of the fleet currently handled by each provider."""
        total_agents = len(cls.ACTIVE_ROSTER)
        if total_agents == 0:
            return {}
            
        concentration = {}
        for provider in cls.DRIFT_STATS.keys():
            count = sum(1 for p in cls.ACTIVE_ROSTER.values() if p == provider)
            concentration[provider] = (count / total_agents) * 100.0
            
        return concentration
        
    @classmethod
    def evaluate_failover(cls, current_provider: str) -> str:
        """
        Check if the requested provider is experiencing systemic drift (>20%).
        If so, autonomously force a failover to a different architecture.
        """
        stats = cls.DRIFT_STATS.get(current_provider, {"total_sessions": 0, "drift_events": 0})
        total = stats["total_sessions"]
        drifts = stats["drift_events"]
        
        drift_rate = (drifts / total) * 100.0 if total > 0 else 0.0
        
        # Hard failover threshold set by Institutional Policy
        FAILOVER_THRESHOLD = 20.0
        
        if drift_rate > FAILOVER_THRESHOLD:
            print(f"[DIVERSITY ENGINE] CRITICAL: Systemic Monoculture Risk Detected for {current_provider} (Drift: {drift_rate:.1f}%).")
            # Select the provider with the lowest current drift as fallback
            best_fallback = min(
                [p for p in cls.DRIFT_STATS.keys() if p != current_provider],
                key=lambda p: (cls.DRIFT_STATS[p]["drift_events"] / cls.DRIFT_STATS[p]["total_sessions"]) if cls.DRIFT_STATS[p]["total_sessions"] > 0 else 0.0,
                default="Local Llama 3"
            )
            print(f"[DIVERSITY ENGINE] Autonomous Failover Triggered: Re-routing execution to {best_fallback}.")
            return best_fallback
            
        return current_provider
