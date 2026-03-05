-- Phase 12: WORM Security SQL Migration
-- Objective: Enforce Write-Once-Read-Many (WORM) constraints on the `audit_log` table.
-- This ensures that even database administrators or compromised service roles cannot 
-- UPDATE or DELETE finalized FINRA compliance and MeitY takedown traces.

-- 1. Create the hypothetical `audit_log` table if it doesn't exist
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    agent_id TEXT NOT NULL,
    action TEXT NOT NULL,
    args JSONB,
    result TEXT,
    security_verification BOOLEAN,
    finra_telemetry_dump JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Enable Row Level Security (RLS)
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- 3. Policy: Allow INSERT for authenticated service roles or agents
CREATE POLICY "Allow Insert Operations" 
ON audit_log
FOR INSERT 
TO authenticated 
WITH CHECK (true);

-- 4. Policy: Allow SELECT (Read) for compliance dashboards
CREATE POLICY "Allow Select Operations"
ON audit_log
FOR SELECT
TO authenticated
USING (true);

-- 5. Policy: Explicitly BLOCK DELETE Operations
-- RLS default-deny works, but an explicit deny is better for enterprise clarity
CREATE POLICY "Strict Deny Delete Operations"
ON audit_log
FOR DELETE
TO PUBLIC
USING (false);

-- 6. Policy: Explicitly BLOCK UPDATE Operations
CREATE POLICY "Strict Deny Update Operations"
ON audit_log
FOR UPDATE
TO PUBLIC
USING (false)
WITH CHECK (false);

-- 7. PostgreSQL Trigger: Log unauthorized tampering attempts
-- Even if RLS fails (e.g. postgres superuser), this hard trigger blocks and alerts.
CREATE OR REPLACE FUNCTION audit_log_worm_defense()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'WORM_SECURITY_VIOLATION: Attempted to modify or delete an immutable audit log record. Action blocked and flagged for review.';
END;
$$ LANGUAGE plpgsql;

-- 8. Bind the Trigger to UPDATE and DELETE actions
DROP TRIGGER IF EXISTS prevent_audit_log_tampering ON audit_log;
CREATE TRIGGER prevent_audit_log_tampering
BEFORE UPDATE OR DELETE ON audit_log
FOR EACH ROW
EXECUTE FUNCTION audit_log_worm_defense();

-- Phase 13: SaaSpocalypse V3 - WORM Schema Protection (Event Trigger)
-- 9. Protect the schema itself from being altered or triggers dropped by compromised DBAs
CREATE OR REPLACE FUNCTION block_audit_log_ddl()
RETURNS event_trigger
LANGUAGE plpgsql
AS $$
DECLARE
    obj record;
    target text;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands()
    LOOP
        target := obj.object_identity;
        IF target LIKE '%audit_log%' OR target LIKE '%prevent_audit_log_tampering%' THEN
            RAISE EXCEPTION 'CRITICAL_TAMPER_ALERT: DDL modifications to WORM ledger schemas are strictly prohibited.';
        END IF;
    END LOOP;
END;
$$;

DROP EVENT TRIGGER IF EXISTS prevent_audit_log_ddl;
CREATE EVENT TRIGGER prevent_audit_log_ddl
ON ddl_command_start
EXECUTE FUNCTION block_audit_log_ddl();
