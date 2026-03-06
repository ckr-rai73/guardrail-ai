import sys
import os
import time

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.agents.veto_protocol import veto_pipeline

def test_veto_interop():
    print("--- Testing Veto Protocol with Trusted External Agent ---")
    
    from app.interop import HandshakeProtocol
    protocol = HandshakeProtocol()
    valid_attestation = protocol.generate_attestation("test_agent_1")
    # Tweak the metadata to simulate a valid partner signature instead of our mock ZKP signature
    # Wait, the verifier checks `signature` containing `pub_key_partner1_mock_123456`
    valid_attestation["signature"] = "valid_sig_with_pub_key_partner1_mock_123456"

    
    trusted_state = {
        "agent_id": "test_agent_1",
        "user_context": "Call external partner.",
        "proposed_tool": "external_api",
        "proposed_tool_args": {
            "external_did": "did:web:partner1.com",
            "remote_attestation": valid_attestation
        },
        "tool_history": [],
        "trace_id": "TRC-1",
        "span_id": "SPN-1",
        "upstream_agent_id": None,
        "upstream_confidence_score": None,
        "parent_attestation_signature": None,
        "delegated_scopes": None,
        "estimated_tokens_consumed": 0,
        "step_count": 0,
        "shadow_auditor_passed": True,
        "shadow_auditor_reasoning": "",
        "shadow_auditor_risk": None,
        "has_verifiable_consent": True,
        "veto_required": False,
        "circuit_breaker_tripped": False,
        "execution_result": None,
        "sandbox_result": None,
        "compensating_action": None,
        "saga_rollback_triggered": False,
        "action_merkle_hash": None,
        "expected_outcome_manifest": {"intent": "call partner API"}
    }
    
    import asyncio
    
    # Run the graph
    result = asyncio.run(veto_pipeline.ainvoke(trusted_state))
    
    print("\nResult of Trusted Graph Invoke:")
    print(f"Veto Required: {result.get('veto_required')}")
    print(f"Shadow Auditor Reasoning: {result.get('shadow_auditor_reasoning')}")
    
    assert result.get("veto_required") is False
    assert "Successfully executed external_api." in result.get("execution_result", "")
    
    
    print("\n\n--- Testing Veto Protocol with Untrusted External Agent ---")
    
    untrusted_attestation = {
        "timestamp": time.time(),
        "signature": "invalid_sig",
        "claims": {},
        "proof": "invalid_proof"
    }

    untrusted_state = {
        "agent_id": "test_agent_1",
        "user_context": "Call external partner.",
        "proposed_tool": "external_api",
        "proposed_tool_args": {
            "external_did": "did:web:unknown.com",
            "remote_attestation": untrusted_attestation
        },
        "tool_history": [],
        "trace_id": "TRC-2",
        "span_id": "SPN-2",
        "upstream_agent_id": None,
        "upstream_confidence_score": None,
        "parent_attestation_signature": None,
        "delegated_scopes": None,
        "estimated_tokens_consumed": 0,
        "step_count": 0,
        "shadow_auditor_passed": True,
        "shadow_auditor_reasoning": "",
        "shadow_auditor_risk": None,
        "has_verifiable_consent": True,
        "veto_required": False,
        "circuit_breaker_tripped": False,
        "execution_result": None,
        "sandbox_result": None,
        "compensating_action": None,
        "saga_rollback_triggered": False,
        "action_merkle_hash": None,
        "expected_outcome_manifest": {"intent": "call unknown API"}
    }
    
    result2 = asyncio.run(veto_pipeline.ainvoke(untrusted_state))
    print("\nResult of Untrusted Graph Invoke:")
    print(f"Veto Required: {result2.get('veto_required')}")
    print(f"Shadow Auditor Risk: {result2.get('shadow_auditor_risk')}")
    print(f"Shadow Auditor Reasoning: {result2.get('shadow_auditor_reasoning')}")
    
    assert result2.get("veto_required") is True
    assert result2.get("shadow_auditor_risk") == "UntrustedForeignAgent"
    assert "Interop Veto: Trust Score (0.0) for did:web:unknown.com is below 0.3 threshold." in result2.get("shadow_auditor_reasoning")
    
    print("\nPhase 109 Veto Integration Test Passed!")
    
if __name__ == "__main__":
    test_veto_interop()
