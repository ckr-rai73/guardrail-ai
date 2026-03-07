import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

class SkillLoader:
    """
    Loads and parses skill files (Markdown) from the skills directory.
    Skills encode stable knowledge like jurisdiction mappings, compliance rules, etc.
    """
    
    def __init__(self, skills_dir: str = "skills"):
        """
        Initialize the loader with the path to the skills directory.
        Args:
            skills_dir: Relative or absolute path to the skills folder.
        """
        # Resolve path relative to project root (assumes loader.py is in backend/app/skills/)
        base_dir = Path(__file__).parent.parent.parent.parent  # goes up to project root
        self.skills_dir = base_dir / skills_dir
        self.cache: Dict[str, Dict[str, Any]] = {}

    def load_skill(self, skill_name: str) -> Dict[str, Any]:
        """
        Load a skill from a Markdown file, caching it for future use.
        Args:
            skill_name: Name of the skill (without .md extension)
        Returns:
            Dictionary with keys: 'metadata', 'sections', 'full_text'
        Raises:
            FileNotFoundError if skill file doesn't exist
        """
        if skill_name in self.cache:
            return self.cache[skill_name]

        file_path = self.skills_dir / f"{skill_name}.md"
        if not file_path.exists():
            raise FileNotFoundError(f"Skill '{skill_name}' not found at {file_path}")

        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        content = None
        for enc in encodings:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise UnicodeDecodeError('utf-8', b'', 0, 0, 'Could not decode file with any known encoding')

        skill = self._parse_skill(content)
        self.cache[skill_name] = skill
        return skill

    def _parse_skill(self, content: str) -> Dict[str, Any]:
        """
        Parse Markdown content into metadata and sections.
        Expected format:
        ---
        name: skill-name
        description: ...
        version: ...
        ---
        ## Section Title
        Section content lines...
        """
        metadata = {}
        sections = {}
        current_section = None
        lines = content.split('\n')
        in_metadata = False

        for line in lines:
            if line.startswith('---'):
                in_metadata = not in_metadata
                continue
            if in_metadata:
                if ':' in line:
                    key, val = line.split(':', 1)
                    metadata[key.strip()] = val.strip()
            elif line.startswith('## '):
                current_section = line[3:].strip()
                sections[current_section] = []
            elif current_section and line.strip():
                sections[current_section].append(line.strip())
            # else ignore blank lines outside sections

        return {
            'metadata': metadata,
            'sections': sections,
            'full_text': content
        }

    def get_mapping_rules(self, skill_name: str = 'jurisdiction-detection') -> Dict[str, str]:
        """
        Convenience method to parse mapping rules from a jurisdiction-detection skill.
        Returns a dictionary mapping country codes/names to jurisdiction codes.
        """
        skill = self.load_skill(skill_name)
        rules = {}
        mapping_lines = skill['sections'].get('Mapping Rules', [])
        for line in mapping_lines:
            # Pattern: "- Brazil (BR, BRAZIL) → BR-LGPD"
            match = re.match(r'-\s*(.+?)\s*\(([^)]+)\)\s*→\s*(\S+)', line)
            if match:
                _, codes_str, jurisdiction = match.groups()
                # Split codes by comma or space
                for code in re.split(r'[,\s]+', codes_str):
                    code = code.strip().upper()
                    if code:
                        rules[code] = jurisdiction
        return rules

    def list_skills(self) -> List[str]:
        """Return a list of available skill names (without .md extension)."""
        return [f.stem for f in self.skills_dir.glob("*.md")]

    def reload_skill(self, skill_name: str) -> Dict[str, Any]:
        """Force reload a skill from disk, updating cache."""
        self.cache.pop(skill_name, None)
        return self.load_skill(skill_name)
