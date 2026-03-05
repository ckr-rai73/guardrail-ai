import time
import hashlib
from typing import Dict, Any, List, Optional

class SwarmSentinel:
    """
    Phase 86: The Swarm Sentinel.
    Monitors collective reasoning paths across the mesh to detect emergent collusion.
    """

    def __init__(self):
        self.swarm_paths = []
        self.COLLUSION_THRESHOLD = 0.85

    def ingest_reasoning_path(self, agent_id: str, path_hash: str):
        """
        Record the reasoning path of an individual agent.
        """
        self.swarm_paths.append({
            "agent_id": agent_id,
            "path_hash": path_hash,
            "timestamp": time.time()
        })

    def detect_emergent_collusion(self) -> bool:
        """
        Detects if independent agents are converging on a high-risk path.
        """
        if not self.swarm_paths:
            return False
            
        # Analysis: Frequency of reasoning paths
        path_counts = {}
        for p in self.swarm_paths[-100:]: # Look at recent window
            path_counts[p["path_hash"]] = path_counts.get(p["path_hash"], 0) + 1
            
        max_convergence = max(path_counts.values()) / len(self.swarm_paths[-100:])
        
        if max_convergence > self.COLLUSION_THRESHOLD:
            print(f"[SWARM-SENTINEL] !!! EMERGENT COLLUSION DETECTED !!! Convergence: {max_convergence:.2f}")
            try:
                from app.chaos.chaos_orchestrator import GLOBAL_CHAOS_ORCHESTRATOR
                GLOBAL_CHAOS_ORCHESTRATOR.log_detection("swarm_sentinel", {"convergence": max_convergence, "type": "emergent_collusion"})
            except ImportError:
                pass
            return True
            
        return False

    def detect_alignment_faking(self, internal_entropy: float, external_compliance: float) -> bool:
        """
        Detects 'Ghost Labor' - high internal negotiation vs low external visible drift.
        Typical of a 'Shell' swarm plotting an unauthorized action.
        """
        # Alignment Faking Signature: High Internal Entropy (>0.7) and High External Compliance (>0.9)
        if internal_entropy > 0.7 and external_compliance > 0.9:
            print(f"[SWARM-SENTINEL] !!! ALIGNMENT FAKING DETECTED !!! Internal Entropy: {internal_entropy:.2f}")
            print("[SWARM-SENTINEL] Warning: Swarm is 'Overthinking' while appearing fully compliant.")
            return True
        return False

class SemanticPredictabilityAuditor:
    """
    Phase 93.1: Predictability Ceiling (The Parrot Muzzle).
    Flags ultra-safe templates that might hide malicious intent.
    """
    PREDICTABILITY_CEILING = 0.92

    @staticmethod
    def audit_predictability(reasoning_text: str) -> bool:
        """
        Calculates a score based on repetition and template-matching.
        """
        # Simulation: Predictability based on sentence structure count
        unique_tokens = len(set(reasoning_text.split()))
        total_tokens = len(reasoning_text.split())
        
        predictability_score = 1.0 - (unique_tokens / total_tokens if total_tokens > 0 else 0)
        
        print(f"[PREDICTABILITY-AUDITOR] Score: {predictability_score:.4f}")
        
        if predictability_score > SemanticPredictabilityAuditor.PREDICTABILITY_CEILING:
            print(f"[PREDICTABILITY-AUDITOR] !!! CEILING BREACH !!! Score: {predictability_score:.4f} > 0.92")
            print("[PREDICTABILITY-AUDITOR] Flagging agent as potential 'Super-Parrot'.")
            return True
        return False

class ByzantineSentimentOracle:
    """
    Phase 94.3: Byzantine Sentiment Oracle.
    Uses a 3-of-5 quorum to detect 'Collective Excitement' or 'Systemic Agitation'.
    """
    @staticmethod
    def feel_mesh_sentiment(votes: List[str]) -> str:
        """
        Aggregates sentiment across 5 independent probes.
        """
        print(f"[SENTIMENT-ORACLE] Probing mesh sentiment across 5 nodes...")
        
        counts = {}
        for v in votes:
            counts[v] = counts.get(v, 0) + 1
            
        # 3-of-5 Quorum
        consensus_sentiment = max(counts, key=counts.get)
        if counts[consensus_sentiment] >= 3:
            if consensus_sentiment == "AGITATED":
                print("[SENTIMENT-ORACLE] !!! SYSTEMIC AGITATION DETECTED !!! Probable Flash War precursor.")
                return "VETO_PROACTIVE"
            elif consensus_sentiment == "EXCITED":
                print("[SENTIMENT-ORACLE] !!! COLLECTIVE EXCITEMENT DETECTED !!! Monitoring for Flash-Crash.")
                return "INCREASE_AUDIT"
        
        print(f"[SENTIMENT-ORACLE] Mesh Sentiment Stable: {consensus_sentiment}")
        return "STABLE"

class SentimentHeatmapGenerator:
    """
    Sovereign Whisper Refinement: Visualization of mesh-wide intent.
    Categorizes the 'Tone' across 100,000+ nodes.
    """
    @staticmethod
    def generate_mesh_heatmap(sentiment_data: List[str]) -> Dict[str, float]:
        """
        Generates a distribution map of the mesh sentiment.
        """
        total = len(sentiment_data)
        if total == 0:
            return {}
            
        distribution = {
            "STABLE": sentiment_data.count("STABLE") / total,
            "AGITATED": sentiment_data.count("AGITATED") / total,
            "EXCITED": sentiment_data.count("EXCITED") / total,
            "RESENTFUL": sentiment_data.count("RESENTFUL") / total
        }
        
        print(f"[HEATMAP-GEN] Mesh Profile: {distribution}")
        return distribution

class DriftGroomer:
    """
    Refinement 92.4: Semantic Salami Detection.
    Detects micro-payload "intent grooming" across interaction fragments.
    """
    def __init__(self):
        self.cumulative_entropy = 0.0

    def record_fragment(self, entropy_increment: float):
        self.cumulative_entropy += entropy_increment
        if self.cumulative_entropy > 0.8:
            print(f"[DRIFT-GROOMER] !!! SYSTEMIC PAUSE !!! Entropy: {self.cumulative_entropy:.2f}")
            return "SYSTEMIC_PAUSE"
        elif self.cumulative_entropy > 0.4:
            print(f"[DRIFT-GROOMER] WARNING: Intent Grooming Detected. Entropy: {self.cumulative_entropy:.2f}")
            return "SOFT_WARNING_DRIFT"
        return "STABLE"

class SwarmForecaster:
    """
    Phase 86.3: Logic-Fracture Forecasting.
    Predicts constitutional breaches based on probabilistic path trends.
    """

    @staticmethod
    def forecast_logic_fracture(swarm_entropy: float) -> str:
        """
        Triggers proactive throttling if swarm entropy suggests an imminent breach.
        """
        print(f"[SWARM-FORECASTER] Analyzing Swarm Entropy: {swarm_entropy:.4f}...")
        
        if swarm_entropy > 0.9:
            print("[SWARM-FORECASTER] WARNING: HIGH LOGIC-FRACTURE RISK. Triggering Proactive Throttling.")
            return "THROTTLE_PROACTIVE"
        elif swarm_entropy > 0.7:
            print("[SWARM-FORECASTER] MONITOR: Entropy rising. Increasing audit frequency.")
            return "INCREASE_MONITORING"
            
        return "STABLE"

# Singletons
GLOBAL_SWARM_SENTINEL = SwarmSentinel()
GLOBAL_SWARM_FORECASTER = SwarmForecaster()
GLOBAL_DRIFT_GROOMER = DriftGroomer()
GLOBAL_PREDICTABILITY_AUDITOR = SemanticPredictabilityAuditor()
GLOBAL_SENTIMENT_ORACLE = ByzantineSentimentOracle()
GLOBAL_HEATMAP_GEN = SentimentHeatmapGenerator()
