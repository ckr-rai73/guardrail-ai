---
name: jurisdiction-detection
description: Maps user location and data residency to applicable jurisdiction codes.
version: 1.0.0
---

## Purpose
This skill determines which regulatory jurisdictions apply based on user location and data residency context.

## Input
- `user_location`: ISO country code (e.g., "BR", "IN", "JP")
- `data_residency`: Where data is stored (e.g., "EU", "US-IN")
- `processing_location`: Where processing occurs (e.g., "US")

## Output
List of jurisdiction codes (e.g., ["BR-LGPD", "IN-DPDPA"])

## Mapping Rules
- Brazil (BR, BRAZIL) → BR-LGPD
- India (IN, INDIA) → IN-DPDPA
- Japan (JP, JAPAN) → JP-APPI
- European Union (EU, EUROPE, DE, FR, GB, UK) → EU-AI-ACT
- United States (US, USA) → US-DISCOVERY-HOLD
- South Africa (ZA, SOUTH_AFRICA) → ZA-POPIA

## Example
Input: {"user_location": "IN", "data_residency": "EU-IN"}
Output: ["IN-DPDPA", "EU-AI-ACT"]
