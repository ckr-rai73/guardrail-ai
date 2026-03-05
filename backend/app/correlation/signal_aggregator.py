import time
import uuid
import heapq
from typing import Dict, Any, List

class SignalAggregator:
    """
    Phase 99: The Toxic Combination Correlator layer
    Aggregates low-level infrastructure signals (WAF, API Gateway, VectorClockLedger).
    Normalizes into a common schema.
    Uses an in-memory priority queue to mock a short-term time-series DB like ClickHouse.
    """
    
    # Simple simulated time-series buffer
    # Format: [(-timestamp, event_id, event_data)]
    # We use negative timestamp to keep latest events at the top (max-heap)
    _time_series_db: List[Any] = []
    
    @classmethod
    def ingest_waf_log(cls, source_ip: str, path: str, bot_score: int, payload_size: int = 1024):
        """Simulates ingestion from Cloudflare Logpush or equivalent."""
        timestamp = time.time()
        event_id = f"WAF-{uuid.uuid4().hex[:8]}"
        
        normalized = {
            "timestamp": timestamp,
            "source": "WAF",
            "source_ip": source_ip,
            "path": path,
            "bot_score": bot_score,
            "auth_status": False,
            "agent_id": None,
            "metrics": {
                 "payload_size": payload_size
            }
        }
        
        heapq.heappush(cls._time_series_db, (-timestamp, event_id, normalized))
        return event_id

    @classmethod
    def ingest_api_gateway_log(cls, source_ip: str, path: str, auth_status: bool, agent_id: str | None = None):
         """Simulates logs from the Guardrail.ai API Gateway."""
         timestamp = time.time()
         event_id = f"GW-{uuid.uuid4().hex[:8]}"
         
         normalized = {
            "timestamp": timestamp,
            "source": "API_GATEWAY",
            "source_ip": source_ip,
            "path": path,
            "bot_score": 100, # Assume 100 if passed WAF natively
            "auth_status": auth_status,
            "agent_id": agent_id,
            "metrics": {}
         }
         
         heapq.heappush(cls._time_series_db, (-timestamp, event_id, normalized))
         return event_id
         
    @classmethod
    def ingest_ledger_event(cls, agent_id: str, action: str, result_status: str):
        """Ingests events from the VectorClockLedger."""
        timestamp = time.time()
        event_id = f"LDG-{uuid.uuid4().hex[:8]}"
         
        normalized = {
            "timestamp": timestamp,
            "source": "VECTOR_LEDGER",
            "source_ip": "INTERNAL_MESH",
            "path": action,
            "bot_score": 100,
            "auth_status": True,
            "agent_id": agent_id,
            "metrics": {
                "result": result_status
            }
         }
         
        heapq.heappush(cls._time_series_db, (-timestamp, event_id, normalized))
        return event_id

    @classmethod
    def query_recent_signals(cls, time_window_seconds: int = 60, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Query the time-series DB for recent events.
        Simulates `SELECT * FROM system.events WHERE timestamp >= (now() - 60s)`
        """
        results = []
        current_time = time.time()
        
        # We need to iterate the heap (but we don't pop to keep them for other correlations)
        # This is a bit inefficient for a real system, but perfect for a simulated memory DB
        for neg_ts, eid, data in cls._time_series_db:
             ts = -neg_ts
             if (current_time - ts) <= time_window_seconds:
                  # Apply basic matching
                  match = True
                  if filters:
                       for k, v in filters.items():
                            if data.get(k) != v:
                                match = False
                                break
                  if match:
                       results.append(data)
                            
        return sorted(results, key=lambda x: x["timestamp"]) # Return oldest first for chronological analysis

    @classmethod
    def flush(cls):
         cls._time_series_db = []
