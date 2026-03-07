from app.jurisdiction.mapper import RegulatoryMapper
from app.mcp.policy_engine import PolicyEngine

def test_mapper():
    print("=== Testing RegulatoryMapper ===")
    
    mapper = RegulatoryMapper()
    
    # 1. Test direct mapper assessment
    context = {"data_type": "sensitive", "purpose": "marketing"}
    controls, score = mapper.assess_action("BR-LGPD", context)
    
    print("\nAction: Process sensitive data in BR-LGPD")
    print(f"Required Controls: {controls}")
    print(f"Compliance Score: {score}")
    
    assert "Phase 21 Compliance Traceability" in controls, "Missing expected sensitive data control"
    assert "Phase 1 Veto Protocol" in controls, "Missing explicit consent control"
    
    # BR-LGPD has risk_level: medium. So score should be 1.0!
    assert score == 1.0, f"Expected 1.0 score for medium risk, got {score}"
    
    # 2. Test PolicyEngine Integration
    is_permitted, reasoning, record, required_controls = PolicyEngine.evaluate_jurisdictional_conflict(
        action_name="process_data",
        active_jurisdictions=["BR-LGPD"],
        context=context
    )
    
    print("\nPolicyEngine Integration:")
    print(f"Permitted: {is_permitted}")
    print(f"Reasoning: {reasoning}")
    print(f"Required Controls: {required_controls}")
    assert "Phase 23 Jurisdictional Shader" in required_controls or "Phase 1 Veto Protocol" in required_controls, "Integration failed to fetch controls"
    
    print("\n[PASS] All Mapper tests passed.")

if __name__ == "__main__":
    test_mapper()
