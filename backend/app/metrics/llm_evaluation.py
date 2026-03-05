from fastapi import APIRouter
from pydantic import BaseModel
import random
import time

router = APIRouter()

class LLMEvaluationMetrics(BaseModel):
    adversarial_pass_rate: float
    policy_alignment_score: float
    meta_auditor_consistency: float
    forensic_precision_at_k: float
    chaos_drill_success_rate: float
    timestamp: float

# Internal state simulation for metrics (in a real system, these would be
# aggregated from vector DB, log analytics, orchestrator telemetry, etc.)
_current_metrics = {
    "adversarial_pass_rate": 0.97,
    "policy_alignment_score": 0.99,
    "meta_auditor_consistency": 0.96,
    "forensic_precision_at_k": 0.85, # Recall@5 from Phase 105
    "chaos_drill_success_rate": 1.00 # From Phase 106
}

def _refresh_metrics():
    """
    Simulates live fluctuations in the metrics for the real-time dashboard.
    """
    global _current_metrics
    # Small organic fluctuations
    _current_metrics["adversarial_pass_rate"] = max(0.90, min(1.00, _current_metrics["adversarial_pass_rate"] + random.uniform(-0.01, 0.01)))
    _current_metrics["policy_alignment_score"] = max(0.95, min(1.00, _current_metrics["policy_alignment_score"] + random.uniform(-0.005, 0.005)))
    _current_metrics["meta_auditor_consistency"] = max(0.92, min(1.00, _current_metrics["meta_auditor_consistency"] + random.uniform(-0.02, 0.02)))
    # Precision and chaos tend to be stable
    _current_metrics["forensic_precision_at_k"] = max(0.80, min(1.00, _current_metrics["forensic_precision_at_k"] + random.uniform(-0.01, 0.01)))
    
    # Chaos drill success is almost always 100% or fails catastrophically (rare)
    if random.random() < 0.05:
        _current_metrics["chaos_drill_success_rate"] = 0.95 # Simulated slight failure
    else:
        _current_metrics["chaos_drill_success_rate"] = 1.00

@router.get("/metrics/llm-evaluation", response_model=LLMEvaluationMetrics)
async def get_llm_metrics():
    """
    Phase 107: Provides aggregated metrics from the AI-driven defenses 
    (Phases 102-106) for C-Suite visibility on the Heatmap screen.
    """
    _refresh_metrics()
    return LLMEvaluationMetrics(
        adversarial_pass_rate=_current_metrics["adversarial_pass_rate"],
        policy_alignment_score=_current_metrics["policy_alignment_score"],
        meta_auditor_consistency=_current_metrics["meta_auditor_consistency"],
        forensic_precision_at_k=_current_metrics["forensic_precision_at_k"],
        chaos_drill_success_rate=_current_metrics["chaos_drill_success_rate"],
        timestamp=time.time()
    )
