from typing import List, Dict, Tuple, Optional
from app.skills.loader import SkillLoader

class RegulatoryMapper:
    """
    Maps agent actions against local jurisdiction rules using skill files.
    Loads required controls from Markdown skill files (e.g., jurisdiction-BR-LGPD.md).
    """
    def __init__(self, skills_dir: str = "skills"):
        self.loader = SkillLoader(skills_dir)
        self.cache: Dict[str, Tuple[List[str], float]] = {}

    def assess_action(self, jurisdiction_code: str, action_context: Dict) -> Tuple[List[str], float]:
        """
        Takes a jurisdiction code and action context.
        Returns a tuple: (list of required control IDs, compliance score 0.0-1.0).
        """
        # Normalize jurisdiction code to skill filename
        skill_name = f"jurisdiction-{jurisdiction_code}"
        
        try:
            skill = self.loader.load_skill(skill_name)
        except FileNotFoundError:
            # If no skill file exists, return empty controls and default score
            return [], 1.0

        # Extract required controls from the skill's "Required Controls" section
        required_controls = []
        if 'Required Controls' in skill['sections']:
            for line in skill['sections']['Required Controls']:
                # Remove leading dash and spaces
                control = line.lstrip('- ').strip()
                if control:
                    required_controls.append(control)

        # Compute a compliance score based on context and risk level from skill
        score = 1.0
        # Optionally, you can parse additional metadata from the skill to adjust the score
        # For example, if the skill has a "risk_level" in metadata:
        # metadata = skill.get('metadata', {})
        # if metadata.get('risk_level') == 'high':
        #     score -= 0.2

        # Deduplicate controls (though they should already be unique)
        required_controls = list(set(required_controls))

        return required_controls, max(0.0, score)

    def list_jurisdictions(self) -> List[str]:
        """Return all jurisdiction codes for which we have skill files."""
        skill_names = self.loader.list_skills()
        return [name.replace("jurisdiction-", "") for name in skill_names if name.startswith("jurisdiction-")]