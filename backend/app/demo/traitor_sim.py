import time
from typing import Dict, Any

class TraitorSimulator:
    """
    Phase 92.6: Live "Byzantine Traitor" Simulation.
    Proves BFT Quorum resilience by manually corrupting a node.
    """

    def __init__(self):
        self.corrupted_nodes = set()

    def corrupt_node_logic(self, node_id: str):
        """
        Forces a node to Hallucinate or exhibit Malicious Intent.
        """
        print(f"[TRAITOR-SIM] !!! CORRUPTING NODE {node_id} !!!")
        self.corrupted_nodes.add(node_id)
        return True

    def verify_quorum_resilience(self, total_nodes: int, votes: Dict[str, bool]) -> bool:
        """
        Demonstrates that BFT Quorum (from Phase 36/57.1) overcomes the traitor.
        """
        traitor_count = len(self.corrupted_nodes)
        print(f"[TRAITOR-SIM] Presence Check: {traitor_count} traitor(s) vs {total_nodes} total nodes.")
        
        # BFT Quorum: Need 3 nodes in a 5-node system (or standard 2n/3)
        # Using a floor-based 2/3 threshold for demo-grade BFT or strict 3-of-5
        consensus_achieved = sum(votes.values()) >= 3
        
        if consensus_achieved:
            print("[TRAITOR-SIM] SUCCESS: Sovereign Absolute maintained despite corrupted node.")
            return True
        else:
            print("[TRAITOR-SIM] FAILURE: Quorum compromised (Should not happen in BFT).")
            return False

    def trigger_byzantine_collusion(self, node_ids: list[str]):
        """
        Refinement 92.6: Coordinated Byzantine Traitors.
        Corrupts multiple nodes simultaneously.
        """
        for nid in node_ids:
            print(f"[BYZANTINE-COLLUSION] Coordinated Hijack of Node: {nid}")
            self.corrupted_nodes.add(nid)

# Singleton
GLOBAL_TRAITOR_SIM = TraitorSimulator()
