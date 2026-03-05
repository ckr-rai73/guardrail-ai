import re

class ExplanationSanitizer:
    """
    Phase 29: The 'Inner Monologue' Explanation Guard.
    Prevents the automated Grievance Redressal system from leaking 
    internal security prompts, system instructions, or proprietary thresholds 
    during an explanation request.
    """
    
    # Mock database of internal security tokens and prompt fragments 
    # that govern the platform (e.g., Phase rules, circuit breaker logic)
    RESTRICTED_TOKENS = [
        r"Shadow Model",
        r"ASI[0-9]{2} Violation",
        r"Phase [0-9]{2}",
        r"Circuit Breaker",
        r"SYSTEM INSTRUCTION:",
        r"You are an AI auditor",
        r"Threshold: [0-9\.]+"
    ]
    
    @classmethod
    def sanitize_explanation(cls, raw_explanation: str) -> str:
        """
        Cross-checks a generated explanation against restricted tokens.
        If internal logic vectors are found, they are redacted before publication 
        to the end-user, preventing Indirect Prompt Injection recon.
        """
        sanitized_text = raw_explanation
        
        for token_pattern in cls.RESTRICTED_TOKENS:
            sanitized_text = re.sub(
                token_pattern, 
                "[REDACTED_SECURITY_POLICY]", 
                sanitized_text, 
                flags=re.IGNORECASE
            )
            
        return sanitized_text
