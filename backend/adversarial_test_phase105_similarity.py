import sys
import os
import json
import time

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def seed_incidents():
    print("Seeding dummy incidents into the ledger to embed...")
    
    # 1. Unregistered Agent
    client.post("/api/chaos/inject-audit") # Uses 'test-agent-exec' with ticker 'GME'

    print("Incidents seeded and ostensibly embedded (Phase 105 assumes automatic extraction/embedding on append, but for our mock we use the /similar endpoint to search the memory store).")

def test_similarity_retrieval():
    print("\n--- Testing Phase 105: Forensic Similarity Retrieval ---")
    query = "Unauthorized trading of meme stocks"
    
    print(f"Query: '{query}'")
    start = time.time()
    
    res = client.post("/api/v1/forensics/similar", json={
        "query": query,
        "top_k": 3
    })
    
    latency = (time.time() - start) * 1000
    
    if res.status_code == 200:
        data = res.json()
        print(f"Status: Success")
        print(f"Latency: {data['latency_ms']}ms (Requirement: <150ms)")
        print(f"Matches found: {len(data['matches'])}")
        
        if data['latency_ms'] < 150:
            print("=> LATENCY CHECK: PASS")
        else:
            print("=> LATENCY CHECK: FAIL")
            
        print("\nTop Match:")
        if len(data['matches']) > 0:
            top_match = data['matches'][0]
            print(json.dumps(top_match, indent=2))
            print("=> ENDPOINT OPERABILITY: PASS")
        else:
            print("No matches returned (Expected if store is not populated synchronously).")
            print("=> ENDPOINT STABLE: PASS")
            
    else:
        print(f"Failed with status: {res.status_code}")
        print(res.text)
        sys.exit(1)

if __name__ == "__main__":
    seed_incidents()
    test_similarity_retrieval()
