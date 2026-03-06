import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from app.interop import ExternalAgentWrapper

def test_foreign_adapter():
    wrapper_low_trust = ExternalAgentWrapper(trust_score=0.3)
    wrapper_high_trust = ExternalAgentWrapper(trust_score=0.8)

    print("--- Testing Outgoing Request ---")
    mock_request = {"action": "fetch_data", "target": "dataset_a"}
    wrapped_req = wrapper_high_trust.wrap_outgoing_request(mock_request)
    print("Wrapped Request:", wrapped_req)
    assert "request_id" in wrapped_req
    assert wrapped_req["destination"] == "UNTRUSTED_EXTERNAL_AGENT"

    print("\n--- Testing Incoming Response ---")
    mock_response = {"status": "success", "data": "secret_info"}
    wrapped_resp = wrapper_high_trust.wrap_incoming_response(mock_response)
    print("Wrapped Response:", wrapped_resp)
    assert "_security_tag" in wrapped_resp
    assert "<untrusted_external>" in wrapped_resp["_security_tag"]

    print("\n--- Testing Action Allow/Veto ---")
    allowed_low = wrapper_low_trust.should_allow_action("read_database", {})
    print(f"Low Trust Action Allowed: {allowed_low}")
    assert allowed_low is False

    allowed_high = wrapper_high_trust.should_allow_action("read_database", {})
    print(f"High Trust Action Allowed: {allowed_high}")
    assert allowed_high is True

    print("\nPhase 109 Foreign Adapter Test Passed!")

if __name__ == "__main__":
    test_foreign_adapter()
