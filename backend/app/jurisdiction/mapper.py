from typing import List, Dict, Tuple
from .loader import JurisdictionLoader
from .models import JurisdictionRule

class RegulatoryMapper:
    """
    Maps agent actions against local jurisdiction rules.
    Decides what Guardrail.ai controls are required and computes a compliance score.
    """
    def __init__(self, loader: JurisdictionLoader = None):
        self.loader = loader or JurisdictionLoader()
        
    def assess_action(self, jurisdiction_code: str, action_context: Dict) -> Tuple[List[str], float]:
        """
        Takes a jurisdiction code and action context.
        Returns a tuple: (list of required control IDs, compliance score 0.0-1.0).
        """
        rule: JurisdictionRule = self.loader.get_jurisdiction_rules(jurisdiction_code)
        
        if not rule or not rule.active:
            # If no rules exist or they are inactive, we default to base Guardrail protections (score 1.0)
            return [], 1.0
            
        required_controls = []
        score = 1.0
        
        # Parse context
        # Example context: {"data_type": "sensitive", "purpose": "marketing"}
        data_type = action_context.get("data_type", "standard")
        
        # Very simple heuristic scoring for the mapper based on rule mappings
        if data_type == "sensitive":
            # If sensitive data, we ALWAYS need anonymization or explicit consent depending on the rules
            # We look at the control mappings
            mappings = rule.control_mappings
            
            # If the jurisdiction explicitly maps sensitive data anon, require it
            if "sensitive_data_anonymization" in mappings:
                required_controls.append(mappings["sensitive_data_anonymization"])
                
            # If it maps explicit consent require it
            if "explicit_consent_required" in mappings:
                required_controls.append(mappings["explicit_consent_required"])
                
            # If they are processing sensitive data in a high risk jurisdiction without proper controls modeled,
            # drop the compliance score.
            if rule.risk_level == "high":
                score -= 0.2
                
            # If "data_subject_rights" mapped, add it
            if "data_subject_rights" in mappings:
                required_controls.append(mappings["data_subject_rights"])

        # Deduplicate required controls
        required_controls = list(set(required_controls))
        
        return required_controls, max(0.0, score)
