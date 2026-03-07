import os

# List of all jurisdictions from your mapping
jurisdictions = [
    "BR-LGPD",
    "IN-DPDPA",
    "JP-APPI",
    "EU-AI-ACT",
    "US-DISCOVERY-HOLD",
    "ZA-POPIA"
]

# Template for the skill file
template = """---
name: jurisdiction-{code}
description: Required controls for {name}
version: 1.0.0
---

## Required Controls
- Phase 1 Veto Protocol
- Phase 21 Compliance Traceability
- Phase 23 Jurisdictional Shader
- Phase 101 Evidentiary Bridge

## Compliance Notes
- Data subject rights must be honored within 15 days.
- Consent records must be maintained for the duration of processing.
"""

# Human-readable names for each jurisdiction
names = {
    "BR-LGPD": "Brazil's LGPD (Lei Geral de Proteção de Dados)",
    "IN-DPDPA": "India's DPDPA (Digital Personal Data Protection Act)",
    "JP-APPI": "Japan's APPI (Act on the Protection of Personal Information)",
    "EU-AI-ACT": "EU AI Act",
    "US-DISCOVERY-HOLD": "US Discovery Hold",
    "ZA-POPIA": "South Africa's POPIA (Protection of Personal Information Act)"
}

# Create skills directory if it doesn't exist
os.makedirs("skills", exist_ok=True)

# Generate each file
for code in jurisdictions:
    filename = f"skills/jurisdiction-{code}.md"
    with open(filename, "w") as f:
        f.write(template.format(code=code, name=names.get(code, code)))
    print(f"Created {filename}")

print("All jurisdiction skill files generated successfully!")
