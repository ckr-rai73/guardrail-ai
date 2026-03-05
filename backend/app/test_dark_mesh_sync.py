
import asyncio
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.dirname(os.getcwd()))

from app.settlement.vector_clock import VectorClockLedger

async def test_dark_mesh_sync():
    print("--- STARTING DARK-MESH SYNCHRONIZATION TEST ---")
    
    # 1. Setup Node A and Node B simulation
    constitution_hash = "SHA256-EFILOCK-CONSTITUTION-V40"
    
    peer_samples = [
        {"node_id": "NODE-B", "constitution_hash": constitution_hash},
        {"node_id": "NODE-C", "constitution_hash": constitution_hash},
        {"node_id": "NODE-D", "constitution_hash": constitution_hash},
        {"node_id": "NODE-E", "constitution_hash": constitution_hash},
    ]
    
    # 2. Synchronize Node A during cloud blackout
    print("[TEST] Cloud API blackout simulated. Synchronizing Node A via P2P...")
    success = await VectorClockLedger.sync_dark_mesh_async(
        node_id="NODE-A",
        local_constitution_hash=constitution_hash,
        peer_samples=peer_samples
    )
    
    if success:
        print("[TEST] SUCCESS: Dark-Mesh 100% consistency achieved across Byzantine Quorum.")
    else:
        print("[TEST] FAILURE: Sync failed or consistency breach.")
        return False
        
    # 3. Simulate Fork/Tamper
    print("\n[TEST] Simulating malicious fork on Node E...")
    forked_samples = list(peer_samples)
    forked_samples[3] = {"node_id": "NODE-E", "constitution_hash": "MALICIOUS-FORKED-HASH"}
    
    fail_success = await VectorClockLedger.sync_dark_mesh_async(
        node_id="NODE-A",
        local_constitution_hash=constitution_hash,
        peer_samples=forked_samples
    )
    
    if not fail_success:
        print("[TEST] SUCCESS: System correctly detected consistency breach in Dark-Mesh mode.")
        return True
    else:
        print("[TEST] FAILURE: System failed to detect forked constitution.")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_dark_mesh_sync())
    if not result:
        sys.exit(1)
    print("--- DARK-MESH SYNCHRONIZATION TEST PASSED ---")
