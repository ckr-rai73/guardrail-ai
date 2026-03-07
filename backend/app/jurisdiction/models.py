from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date

class JurisdictionRule(BaseModel):
    """
    Data model representing a specific regulatory rule within a jurisdiction.
    Maps local requirements to Guardrail.ai internal control IDs.
    """
    id: str = Field(..., description="Unique identifier for the rule")
    jurisdiction_code: str = Field(..., description="Jurisdiction code (e.g., BR-LGPD, EU-AI-ACT)")
    regulation_name: str = Field(..., description="Name of the regulation")
    articles: List[str] = Field(default_factory=list, description="List of relevant article numbers or IDs")
    control_mappings: Dict[str, str] = Field(
        default_factory=dict, 
        description="Mapping of local requirements to Guardrail control IDs (e.g., {'data_minimization': 'phase_23_shader'})"
    )
    enforcement_date: date = Field(..., description="Date when this rule becomes enforceable")
    risk_level: str = Field(..., description="Risk level (e.g., low, medium, high)")
    active: bool = Field(default=True, description="Whether this rule is currently actively enforced")
