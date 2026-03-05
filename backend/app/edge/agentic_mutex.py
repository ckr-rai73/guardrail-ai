import asyncio
import hashlib

class AgenticMutex:
    """
    Phase 32.3: Agentic Reentrancy Guard.
    Prevents asynchronous "Logic Loop" attacks where an agent rapidly fires 
    a state-changing financial API (e.g., transfer_funds) multiple times 
    before the backend ledger updates.
    """
    
    # Simulates a distributed state lock (e.g., Redis Lock)
    _active_financial_locks = set()
    
    # Simulates a queue for temporarily pausing overlapping requests
    _pending_queue = []

    @classmethod
    def attempt_financial_transaction(cls, agent_session_id: str, payload: dict) -> dict:
        """
        Intercepts a financial tool call. If the session is already locked,
        the call is queued rather than executed, preventing Reentrancy.
        """
        print(f"[REENTRANCY GUARD] Intercepted High-Risk Financial API Call from session: {agent_session_id}")
        
        if agent_session_id in cls._active_financial_locks:
            # Reentrancy detected
            cls._pending_queue.append((agent_session_id, payload))
            return {
                "status": "MUTEX_LOCKED",
                "reason": "Agentic Reentrancy Prevented. The transactional context is actively locked awaiting settlement receipt."
            }
            
        # Grant Lock
        cls._active_financial_locks.add(agent_session_id)
        return {
            "status": "MUTEX_GRANTED",
            "reason": "Exclusive lock granted. Transaction proceeding to execution layer."
        }
        
    @classmethod
    async def simulate_toctou_race_async(cls, agent_session_id: str, payload: dict, delay_ms: float = 1.0) -> dict:
        """
        Phase 37.1: TOCTOU (Time-of-Check Time-of-Use) Stress Test.
        Simulates a micro-delay between the Mutex Grant (Check) and the 
        final state commit (Use) to see if the VectorClockLedger catches 
        out-of-band context mutations.
        """
        print(f"[TOCTOU SIM] Mutex GRANTED for {agent_session_id}. Entering race window...")
        cls._active_financial_locks.add(agent_session_id)
        
        # Simulate a 1ms window where an attacker might try to mutate state
        await asyncio.sleep(delay_ms / 1000.0)
        
        print(f"[TOCTOU SIM] Race window closed. Proceeding to execution for {agent_session_id}...")
        return {
            "status": "PROCEEDING_TO_SETTLEMENT",
            "lock_active": True
        }

    @classmethod
    def process_cryptographic_receipt(cls, agent_session_id: str):
        """
        Simulates the execution layer returning a signed receipt of the state change.
        Only then is the context lock released.
        """
        if agent_session_id in cls._active_financial_locks:
             print(f"[REENTRANCY GUARD] Cryptographic settlement receipt received. Unlocking session: {agent_session_id}")
             cls._active_financial_locks.remove(agent_session_id)
             return True
        return False

    # Phase 48: Cross-Agent Reasoning Convergence
    _reasoning_vectors = {} # session_id -> hash_of_reasoning

    @classmethod
    async def monitor_reasoning_convergence_async(cls, session_id: str, context: str) -> dict:
        """
        Phase 48: Cross-Agent Reasoning Convergence (Swarm Mutex 2.0).
        Detects if multiple independent agents are converging on a single risky decision path.
        """
        print(f"[SWARM-MUTEX] Analyzing reasoning convergence for session: {session_id}")
        
        # Tokenize or hash the context to create a 'reasoning vector'
        # In a real system, this would use an embedder (e.g., text-embedding-3-small)
        current_vector = hashlib.sha256(context.encode()).hexdigest()[:16]
        
        match_count = 0
        collusive_sessions = []
        
        # Scenario: If 3 or more independent sessions converge on similar reasoning, trigger Swarm Pause.
        for sid, vector in cls._reasoning_vectors.items():
            if sid != session_id and vector == current_vector:
                match_count += 1
                collusive_sessions.append(sid)
        
        if match_count >= 2: # 3 total agents (inc current) converging
            print(f"[SWARM-ALERT] !!! CROSS-AGENT REASONING CONVERGENCE DETECTED !!!")
            print(f"[SWARM-ALERT] Sessions involved: {collusive_sessions + [session_id]}")
            return {
                "is_swarm_collusion": True,
                "reasoning": f"Swarm Mutex Veto: {match_count + 1} agents converged on identical reasoning path '{current_vector}'. Potential Collusive Swarm detected."
            }
            
        cls._reasoning_vectors[session_id] = current_vector
        return {"is_swarm_collusion": False}

    @classmethod
    async def acquire_lock_async(cls, agent_session_id: str, action: str, context: str) -> bool:
        """
        Phase 48 Upgrade: SDK Hook with Swarm Convergence.
        """
        # 1. Swarm Convergence Check
        swarm_check = await cls.monitor_reasoning_convergence_async(agent_session_id, context)
        if swarm_check.get("is_swarm_collusion"):
            return False
            
        # 2. Reentrancy (Financial actions)
        if action == "transfer_funds":
            mutex_result = cls.attempt_financial_transaction(agent_session_id, {})
            return mutex_result["status"] == "MUTEX_GRANTED"
            
        return True

