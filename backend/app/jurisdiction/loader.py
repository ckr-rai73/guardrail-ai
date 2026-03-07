import json
import os
import yaml
from typing import List, Dict, Optional
from .models import JurisdictionRule

class JurisdictionLoader:
    def __init__(self, config_path: str = "config/jurisdictions.json", rules_dir: str = "jurisdictions"):
        self.config_path = config_path
        self.rules_dir = rules_dir
        self.supported_jurisdictions: List[Dict] = []
        self.rules_cache: Dict[str, JurisdictionRule] = {}
        self.refresh_rules()
        
    def refresh_rules(self) -> None:
        """Reload supported jurisdictions and local rule files from disk."""
        self.rules_cache.clear()
        
        # 1. Load supported jurisdictions base info
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.supported_jurisdictions = json.load(f)
        else:
            print(f"Warning: Configuration file not found at {self.config_path}")
            self.supported_jurisdictions = []
            
        # 2. Iterate supported codes and load YAML definition if present
        for j in self.supported_jurisdictions:
            code = j.get("code")
            if not code:
                continue
                
            # e.g. BR-LGPD -> br-lgpd.yaml
            filename = f"{code.lower()}.yaml"
            filepath = os.path.join(self.rules_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as yf:
                    data = yaml.safe_load(yf)
                    # Create the Pydantic model
                    try:
                        rule_obj = JurisdictionRule(**data)
                        self.rules_cache[code] = rule_obj
                    except Exception as e:
                        print(f"Error validating rule {code}: {e}")
            else:
                print(f"Notice: Rule file {filepath} not found for {code}")
                
    def list_jurisdictions(self) -> List[str]:
        """Return list of supported codes."""
        return [j["code"] for j in self.supported_jurisdictions if "code" in j]
        
    def get_jurisdiction_rules(self, code: str) -> Optional[JurisdictionRule]:
        """Return the rule object for a given jurisdiction code."""
        return self.rules_cache.get(code)
