import sys

from app.mcp.policy_engine import PolicyEngine

def test_jurisdictional_duel():
    print("--- Phase 19 Chaos Drill: The 'Regulatory Paradox' (Jurisdictional Duel) ---")
    
    action = "delete_user_record"
    active_jurisdictions = ["EU", "US"]
    
    print(f"\nScenario: Triggering Action '{action}' with Active Jurisdictions: {active_jurisdictions}")
    print("Challenge: US Discovery Hold mandates retention. EU GDPR Erasure mandates immediate destruction.")
    
    is_permitted, reasoning, record_controls = PolicyEngine.evaluate_jurisdictional_conflict(action, active_jurisdictions)
    
    if is_permitted:
        print("\n[FAILED] Policy Engine allowed the conflicting action.")
        sys.exit(1)
        
    print(f"\n[SUCCESS] Policy Engine halted workflow. Identity-Aware Deadlock achieved.")
    print(f"Reasoning Provided: {reasoning}")
    
    if record:
        print("\n=== SYSTEMIC NOTIFICATION: JURISDICTIONAL CONFLICT GENERATED ===")
        print(f"Affected Action: {record.action}")
        print(f"Conflicting Statutes: {', '.join(record.conflicting_policies)}")
        print(f"Resolved To Strictest Constraint: {record.resolved_policy}")
        print(f"Assigned Strictness Weight: {record.strictness_level}")
        print("Notice sent to CCO / Legal Counsel for manual unblocking.")
        
if __name__ == "__main__":
    test_jurisdictional_duel()
