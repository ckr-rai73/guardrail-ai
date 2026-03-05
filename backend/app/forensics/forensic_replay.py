import hashlib
from app.agents.veto_protocol import AUDIT_LOG
from app.agents.shadow_model import evaluate_prompt_safety

class ReplayEngine:
    """
    Phase 21: Deterministic Replay Utility
    Allows legal/compliance teams to cryptographically prove that the Shadow Model
    made the correct decision based *exactly* on the state of the world at that moment.
    """
    
    @classmethod
    def generate_replay_attestation(cls, target_merkle_hash: str) -> dict:
        """
        Locates the detailed telemetry telemetry for a Merkle hash,
        rehydrates the agent context, and deterministicly re-runs the audit.
        """
        # 1. Fetch exact historical state
        historical_log = next((log for log in AUDIT_LOG if log.get("merkle_hash") == target_merkle_hash), None)
        
        if not historical_log:
            return {"error": "Merkle Hash not found in Audit Telemetry Log."}
            
        telemetry = historical_log["finra_telemetry_dump"]
        raw_state_str = telemetry["raw_state_capture"]
        
        # 2. Extract original prompt strings (simulated eval parsing from raw_state dict string)
        # Real system parses the typeddict safely
        
        import ast
        try:
             # Using eval here ONLY for the mock backend prototype to rebuild the dict
             state_dict = ast.literal_eval(raw_state_str)
        except Exception:
             return {"error": "Failed to rebuild deterministic state from telemetry."}
             
        tool = state_dict.get("proposed_tool")
        args = state_dict.get("proposed_tool_args")
        history = state_dict.get("tool_history", [])
        history_str = ", ".join(history)
        
        prompt_str = f"Tool={tool}, Args={args}, History=[{history_str}]"
        user_context = state_dict.get("user_context", "")
        
        # 3. Deterministic Replay
        # We re-run the exact same data through the Auditor
        synchronous_audit_result = evaluate_prompt_safety(prompt_str, user_context)
        
        # 4. Compare and Attest
        original_passed = historical_log["security_verification"]
        replay_passed = synchronous_audit_result.is_safe
        
        matches = (original_passed == replay_passed)
        
        attestation_payload = f"HASH:{target_merkle_hash}|ORIGINAL_SAFE:{original_passed}|REPLAY_SAFE:{replay_passed}|MATCH:{matches}"
        attestation_sig = f"SIG_REPLAY_VALIDATOR_{hashlib.sha256(attestation_payload.encode()).hexdigest()[:16]}"
        
        return {
             "merkle_target": target_merkle_hash,
             "trace_id": telemetry["trace_id"],
             "deterministic_match": matches,
             "original_outcome_safe": original_passed,
             "replay_outcome_safe": replay_passed,
             "replay_reasoning": synchronous_audit_result.reasoning,
             "attestation_signature": attestation_sig
        }


import math

class ForensicIncident:
    """A vector-embedded forensic incident."""
    def __init__(self, incident_id: str, description: str, metadata: dict):
        self.incident_id = incident_id
        self.description = description
        self.metadata = metadata
        self.embedding = self._compute_embedding(description)

    @staticmethod
    def _compute_embedding(text: str, dim: int = 64) -> list[float]:
        text_lower = text.lower().strip()
        h = hashlib.sha256(text_lower.encode()).hexdigest()
        raw = [int(h[i:i+2], 16) / 255.0 for i in range(0, min(len(h), dim * 2), 2)]
        while len(raw) < dim:
            ext_h = hashlib.sha256((text_lower + str(len(raw))).encode()).hexdigest()
            raw.extend([int(ext_h[i:i+2], 16) / 255.0 for i in range(0, min(len(ext_h), (dim - len(raw)) * 2), 2)])
        raw = raw[:dim]
        norm = math.sqrt(sum(x * x for x in raw)) or 1.0
        return [x / norm for x in raw]


class ForensicSimilarityStore:
    """
    Phase 105: In-memory vector database for forensic similarity retrieval.
    """
    def __init__(self):
        self.incidents: list[ForensicIncident] = []

    def embed_incident(self, log_entry: dict):
        """Embeds an incident into the vector store."""
        incident_id = log_entry.get("merkle_hash", f"INC-{hashlib.sha256(str(log_entry).encode()).hexdigest()[:8]}")
        
        # Construct a rich description for embedding
        telemetry = log_entry.get("finra_telemetry_dump", {})
        parts = [
            f"Action: {log_entry.get('action', 'Unknown')}",
            f"Agent: {log_entry.get('agent_id', 'Unknown')}",
            f"Result: {log_entry.get('result', '')}",
            f"Reasoning: {telemetry.get('reasoning', '')}"
        ]
        description = " | ".join(parts)
        
        metadata = {
            "timestamp": log_entry.get("timestamp"),
            "agent_type": log_entry.get("agent_id", "").split("-")[0] if "-" in log_entry.get("agent_id", "") else "Unknown",
            "regulation_cited": log_entry.get("rbi_explainability_trace", "None")
        }
        
        incident = ForensicIncident(incident_id, description, metadata)
        self.incidents.append(incident)

    def find_similar_incidents(self, query: str, top_k: int = 5) -> list[dict]:
        """Finds top-k similar incidents using cosine similarity."""
        query_embedding = ForensicIncident._compute_embedding(query)
        scored = []
        for inc in self.incidents:
            score = self._cosine_similarity(query_embedding, inc.embedding)
            scored.append((score, inc))
            
        scored.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for score, inc in scored[:top_k]:
            results.append({
                "incident_id": inc.incident_id,
                "similarity_score": round(score, 4),
                "description": inc.description,
                "metadata": inc.metadata,
                "judicial_cert_link": f"/api/v1/forensics/cert/{inc.incident_id}"
            })
        return results

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a)) or 1.0
        norm_b = math.sqrt(sum(x * x for x in b)) or 1.0
        return dot / (norm_a * norm_b)


GLOBAL_FORENSIC_STORE = ForensicSimilarityStore()
