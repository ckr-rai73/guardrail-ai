import json
import hashlib
import time
import uuid

class AIBOMKernel:
    """
    Phase 28: Automated AIBOM Generator (AI Bill of Materials).
    Logs every model version, third-party tool, and data chunk provenance
    used in a specific session to satisfy MeitY and UK ADM transparency rules.
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.timestamp = time.time()
        self.bom = {
            "session_id": session_id,
            "timestamp_start": self.timestamp,
            "models": [],
            "tools": [],
            "data_sources": [],
            "cryptographic_hash": None
        }

    def register_model(self, model_name: str, provider: str, version: str, parameters: dict = None):
        """Logs the specific LLM/SLM node used for reasoning."""
        self.bom["models"].append({
            "model_name": model_name,
            "provider": provider,
            "version": version,
            "parameters": parameters or {},
            "timestamp": time.time()
        })
        
    def register_tool(self, tool_name: str, version: str, action: str, developer: str = "Guardrail.ai"):
        """Logs the agentic tool invoked during the session."""
        self.bom["tools"].append({
            "tool_name": tool_name,
            "version": version,
            "action": action,
            "developer": developer,
            "timestamp": time.time()
        })
        
    def register_data_source(self, origin: str, dataset_name: str, compliance_tags: list = None):
        """Logs the provenance of data ingested by the agent."""
        self.bom["data_sources"].append({
            "origin": origin,
            "dataset_name": dataset_name,
            "compliance_tags": compliance_tags or [],
            "timestamp": time.time()
        })
        
    def compile_bom(self) -> str:
        """
        Finalizes the AIBOM, generating a cryptographic hash of the entire lineage 
        for non-repudiation during regulatory audits.
        """
        self.bom["timestamp_end"] = time.time()
        
        # Serialize without the hash field to generate the hash
        bom_string = json.dumps({k: v for k, v in self.bom.items() if k != "cryptographic_hash"}, sort_keys=True)
        self.bom["cryptographic_hash"] = hashlib.sha256(bom_string.encode()).hexdigest()
        
        return json.dumps(self.bom, indent=2)

    @classmethod
    def generate_session_id(cls):
        return f"SESSION_{uuid.uuid4()}"
