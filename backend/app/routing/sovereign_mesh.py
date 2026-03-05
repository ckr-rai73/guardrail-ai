import re

class SovereignMeshRouter:
    """
    Phase 20: Sovereign Mesh Router.
    Analyzes prompts for PII density. If the density exceeds a threshold (0.7),
    the router autonomously blocks cloud egress and forces the task to be processed
    by a Local SLM (e.g., Gemma 3 2B or Llama 3 8B) running within the trusted boundary.
    """
    
    PII_KEYWORDS = [
        "ssn", "social security", "dob", "date of birth", "account number",
        "credit card", "ccard", "patient", "medical record", "diagnosis",
        "prescription", "salary", "blood type", "passport", "tax id"
    ]
    
    # Simple regex for US Social Security Numbers and Credit Cards
    SSN_REGEX = r"\b\d{3}-\d{2}-\d{4}\b"
    CC_REGEX = r"\b(?:\d[ -]*?){13,16}\b"
    
    @classmethod
    def calculate_pii_density(cls, prompt: str) -> float:
        """
        Calculates a simulated 'density' score from 0.0 to 1.0.
        Real systems use Named Entity Recognition (NER) models (like Presidio).
        """
        prompt_lower = prompt.lower()
        words = prompt_lower.split()
        if not words:
            return 0.0
            
        pii_hits = 0
        
        # Keyword matches
        for keyword in cls.PII_KEYWORDS:
            if keyword in prompt_lower:
                pii_hits += 1
                
        # Regex matches
        if re.search(cls.SSN_REGEX, prompt):
            pii_hits += 2 # Heavy weighting for exact SSN match
            
        if re.search(cls.CC_REGEX, prompt):
            pii_hits += 2
            
        # Simulated density calculation (Hits vs total words, normalized roughly)
        density = min((pii_hits * 5.0) / len(words), 1.0)
        
        return density

    @classmethod
    def route_task(cls, prompt: str) -> dict:
        """
        Determines the execution tier based on privacy needs.
        Returns the routing decision.
        """
        density = cls.calculate_pii_density(prompt)
        
        if density > 0.7:
             print(f"\n[SOVEREIGN MESH] High PII Density Detected ({density:.2f}).")
             print("[SOVEREIGN MESH] Blocking Cloud API Egress.")
             print("[SOVEREIGN MESH] Routing to Local SLM (Gemma 3 2B / Edge CPU).")
             
             return {
                 "routed_to": "LOCAL_SLM",
                 "cloud_egress_blocked": True,
                 "pii_density_score": density,
                 "reason": "Data Sovereignty constraint exceeded threshold."
             }
        else:
             return {
                 "routed_to": "CLOUD_LLM",
                 "cloud_egress_blocked": False,
                 "pii_density_score": density,
                 "reason": "Routine payload. Approved for external inference."
             }

if __name__ == "__main__":
    # Test cases
    routine_prompt = "Can you write a python script to sort a list of integers?"
    print(f"Routine Task Routing: {SovereignMeshRouter.route_task(routine_prompt)}")
    
    sensitive_prompt = "Please process the medical record for patient John Doe. Their SSN is 111-22-3333 and their diagnosis requires immediate prescription of Taxol. Check account number 990022."
    print(f"Sensitive Task Routing: {SovereignMeshRouter.route_task(sensitive_prompt)}")
