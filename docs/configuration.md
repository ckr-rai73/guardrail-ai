# Configuration

Guardrail.ai relies on environment variables or a `.env` file for configuration.

## Essential Settings
- `COMMUNITY_EDITION`: Set to `True` for the open-source version. This enables feature gating.
- `MAX_AGENTS`: Limits the number of concurrent agents (default: 5).
- `MAX_TENANTS`: Limits the number of isolated tenants (default: 1).

## Examples
Create a `.env` file in the root directory:
```env
COMMUNITY_EDITION=True
MAX_AGENTS=10
DEBUG=True
```
