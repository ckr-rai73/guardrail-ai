"""
RegulatoryMapper - Phase 110
Maps jurisdiction codes to required controls using skill files.
"""

import os
import re
from typing import Dict, List, Tuple, Any, Optional
from app.skills.loader import SkillLoader

class RegulatoryMapper:
    """
    Loads jurisdiction-specific control requirements from skill files.
    """

    def __init__(self, skills_dir: str = "skills"):
        self.loader = SkillLoader(skills_dir)
        self.cache: Dict[str, Tuple[List[str], float]] = {}

    def assess_action(self, jurisdiction_code: str, context: Dict[str, Any]) -> Tuple[List[str], float]:
        """
        Determine required controls and compliance score for an action in a given jurisdiction.

        Args:
            jurisdiction_code: e.g., "BR-LGPD", "EU-AI-ACT"
            context: dictionary with action details (data_type, purpose, etc.)

        Returns:
            (list_of_required_controls, compliance_score)
        """
        # Normalize jurisdiction code (replace hyphens with underscores for skill filename)
        skill_name = f"jurisdiction-{jurisdiction_code}"
        try:
            skill = self.loader.load_skill(skill_name)
        except FileNotFoundError:
            # If no specific skill, return empty controls and default score
            return [], 1.0

        # Extract required controls from the skill's "Required Controls" section
        required_controls = []
        if 'Required Controls' in skill['sections']:
            # Each line is a bullet point like "- Phase 1 Veto Protocol"
            for line in skill['sections']['Required Controls']:
                # Remove leading dash and spaces
                control = re.sub(r'^-\s*', '', line).strip()
                if control:
                    required_controls.append(control)

        # Compute a compliance score based on context and skill (simplified for now)
        # You can enhance this later with more sophisticated logic
        score = 1.0  # default full compliance if skill exists

        return required_controls, score

    def list_jurisdictions(self) -> List[str]:
        """Return all jurisdiction codes for which we have skill files."""
        skill_names = self.loader.list_skills()
        # Extract jurisdiction codes from skill names (assuming format "jurisdiction-CODE")
        codes = []
        for name in skill_names:
            if name.startswith("jurisdiction-") and name != "jurisdiction-detection":
                codes.append(name.replace("jurisdiction-", "", 1))
        return codes
