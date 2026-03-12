# API Reference

The Community Edition includes access to the core REST API for integrating agents and managing governance workflows.

## Endpoints
* `POST /api/mcp/invoke-tool` - Submit an agent action for Shadow Model and Veto Protocol review.
* `GET /api/dashboard/veto-queue` - Retrieve pending actions requiring approval.
* `POST /api/dashboard/veto-queue/{item_uuid}` - Approve or deny a pending action.
* `GET /api/dashboard/audit-log` - Retrieve immutable execution history.

For a complete interactive API reference, run the application and navigate to `/docs` (Swagger UI).
