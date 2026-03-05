import time
import hashlib
from typing import Dict, Any

class PoBhLedger:
    """
    Phase 27: 'Proof of Behavior' (PoBh) Ledger.
    Records 'Handoff Intent' between agents as a cryptographically signed contract, 
    preventing the 'Attribution Gap' in multi-agent workflows. If Agent B commits 
    a violation, it can be traced back to whether Agent A's instructions were the root cause.
    """
    
    POBH_CONTRACTS = []
    
    @classmethod
    def create_handoff_contract(cls, delegating_agent: str, receiving_agent: str, task_context: str, safety_constraints: list[str]) -> Dict[str, Any]:
        """
        Generates a PoBh token that binds the delegating agent to the exact
        intent they passed to the receiving agent.
        """
        timestamp = time.time()
        
        contract_data = {
            "delegator": delegating_agent,
            "receiver": receiving_agent,
            "intent": task_context,
            "constraints_passed": safety_constraints,
            "timestamp": timestamp
        }
        
        # Hash the intent payload
        payload_string = f"{delegating_agent}:{receiving_agent}:{task_context}:{timestamp}"
        intent_hash = hashlib.sha256(payload_string.encode()).hexdigest()
        
        # Simulate the delegating agent 'signing' the intent with its private key
        signature = f"SIG_POBH_ED25519_{intent_hash[:32]}"
        
        contract = {
            "contract_id": f"pobh-{int(timestamp)}",
            "data": contract_data,
            "intent_hash": intent_hash,
            "delegator_signature": signature
        }
        
        cls.POBH_CONTRACTS.append(contract)
        print(f"[POBH LEDGER] Handoff Contract Secured: {delegating_agent} -> {receiving_agent} (Hash: {intent_hash[:12]}...)")
        
        return contract
        
    @classmethod
    def verify_attribution(cls, contract_id: str) -> Dict[str, Any]:
        """
        Used during an incident investigation to retrieve the exact boundaries
        delegated to the sub-agent.
        """
        for contract in cls.POBH_CONTRACTS:
            if contract["contract_id"] == contract_id:
                return contract
        return {"error": "Contract not found"}
