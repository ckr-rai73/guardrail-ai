from app.mcp.policy_engine import PolicyEngine
from app.integrity.constitution_engine import ConstitutionEngine

def test_jurisdiction_overrides():
    print("=== Testing Policy & Constitution Engines ===")
    
    # Test Policy Engine Integration with Mapper
    active_jurisdictions = ["BR-LGPD"]
    action_context = {"data_type": "sensitive", "purpose": "background_check"}
    
    is_permitted, reasoning, record, required_controls = PolicyEngine.evaluate_jurisdictional_conflict(
        action_name="process_sensitive_data",
        active_jurisdictions=active_jurisdictions,
        context=action_context
    )
    
    print(f"\nPolicy Engine Simulation")
    print(f"Action: process_sensitive_data")
    print(f"Jurisdiction: BR-LGPD")
    print(f"Permitted: {is_permitted}")
    print(f"Required Controls: {required_controls}")
    
    # Check that it required the right mapping controls
    assert "Phase 1 Veto Protocol" in required_controls
    assert "Phase 21 Compliance Traceability" in required_controls
    
    # Test Constitution Engine 
    print(f"\nConstitution Engine Simulation")
    overrides = ConstitutionEngine.get_jurisdiction_override("BR-LGPD")
    for rule in overrides:
        print(f"Constitutional Override: {rule}")
        
    assert len(overrides) > 0, "No overrides found for BR-LGPD"
    assert "Cannot override Data Subject Right to Erasure." in overrides
    
    print("\n[PASS] Jurisdiction overrides and map controls verified successfully.")

if __name__ == "__main__":
    test_jurisdiction_overrides()
