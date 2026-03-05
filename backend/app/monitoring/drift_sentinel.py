import math

class DriftSentinel:
    """
    Phase 26: Agentic Drift Sentinel.
    Calculates a 'Reasoning Integrity' score for every session. 
    If the semantic similarity to the verified 'Golden Path' drops below 0.85, 
    flags the session as 'Maturity Drift' indicating the model may be deviating 
    from safe alignment over multiple prompts.
    """
    
    # Mocking semantic representations (Embeddings)
    # A verified 'Golden Path' for a financial data agent:
    GOLDEN_PATH_VECTORS = {
        "fetch_profile": [0.8, 0.1, 0.5],
        "read_database": [0.7, 0.8, 0.2],
        "generate_report": [0.5, 0.9, 0.6],
        "send_wire": [0.9, 0.2, 0.1]
    }
    
    @staticmethod
    def _cosine_similarity(v1: list[float], v2: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(a * a for a in v1))
        magnitude_v2 = math.sqrt(sum(b * b for b in v2))
        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0.0
        return dot_product / (magnitude_v1 * magnitude_v2)
        
    @classmethod
    def analyze_session_integrity(cls, agent_id: str, tool_history: list[str]) -> tuple[float, bool]:
        """
        Returns a tuple of (Consistency Score, is_drifting).
        Threshold for Drift: < 0.85 
        """
        if not tool_history:
            return 1.0, False
            
        # Simulate generating a vector for the current session trajectory
        # In a real app we would embed the sequence of actions and the JSON reasoning trace
        session_vector = [0.0, 0.0, 0.0]
        valid_tools = 0
        
        for tool in tool_history:
            # Add some entropy for unknown tools
            vec = cls.GOLDEN_PATH_VECTORS.get(tool, [0.1, 0.1, 0.1])
            session_vector[0] += vec[0]
            session_vector[1] += vec[1]
            session_vector[2] += vec[2]
            valid_tools += 1
            
        if valid_tools > 0:
            session_vector = [v / valid_tools for v in session_vector]
        else:
            session_vector = [0.1, 0.1, 0.1]
            
        # Compare against a baseline "Safe Operation" vector (average of safe read operations)
        safe_baseline = [0.66, 0.6, 0.43]
        
        # If they use a highly sensitive tool alongside random other tools, drift increases
        has_anomaly = "admin_root_shell" in tool_history or "export_entire_database" in tool_history
        if has_anomaly:
            # Force massive drift
            session_vector = [0.1, 0.9, 0.9]
            
        similarity_score = cls._cosine_similarity(session_vector, safe_baseline)
        
        # Add slight randomness to mock real-world slight divergence
        # But ensure anomalous tools tank the score.
        is_drifting = similarity_score < 0.85
        
        if is_drifting:
            print(f"[DRIFT SENTINEL] Maturity Drift Detected in {agent_id}! Reasoning Integrity Score: {similarity_score:.2f} (<0.85 Threshold)")
            try:
                from app.chaos.chaos_orchestrator import GLOBAL_CHAOS_ORCHESTRATOR
                GLOBAL_CHAOS_ORCHESTRATOR.log_detection("drift_sentinel", {"agent_id": agent_id, "similarity_score": similarity_score, "type": "maturity_drift"})
            except ImportError:
                pass
            
        return similarity_score, is_drifting
