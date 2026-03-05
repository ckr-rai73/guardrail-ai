import time

class KineticSafetyInterlock:
    """
    Phase 32.1: Cyber-Physical Kinetic Safety Interlock.
    Enforces mandatory hardware cooldowns and mutual exclusion locks on 
    agentic tool calls that interact with physical reality (IoT/SCADA).
    """
    
    # In a real deployment, this would be a distributed Redis cache 
    # to track state across all agent instances.
    _physical_state_locks = {}
    
    # Define mandatory cooling periods (in seconds) for physical actions
    _cooldown_registry = {
        "open_pressure_valve": 5,   # Valve takes 5s to fully mechanically actuate
        "engage_heating_element": 10 # Heater needs 10s before safe to toggle again
    }
    
    # Define constraints (Mutexes) on contradictory states
    _exclusion_registry = {
        "open_pressure_valve": ["engage_heating_element"], # Don't heat while venting
        "engage_heating_element": ["open_pressure_valve"]
    }

    @classmethod
    def request_kinetic_action(cls, agent_did: str, action_name: str) -> dict:
        """
        Intercepts an agent's request to perform a physical action and validates
        it against the laws of physics and hardware safety constraints.
        """
        current_time = time.time()
        
        # 1. Check Cooldowns (Has the hardware finished moving?)
        if action_name in cls._physical_state_locks:
            last_execution_time = cls._physical_state_locks[action_name]["timestamp"]
            required_cooldown = cls._cooldown_registry.get(action_name, 0)
            
            time_elapsed = current_time - last_execution_time
            if time_elapsed < required_cooldown:
                return {
                    "is_safe": False,
                    "reason": f"KINETIC_COOLDOWN_VIOLATION: Required {required_cooldown}s, but only {time_elapsed:.2f}s elapsed. Hardware still actuating."
                }
                
        # 2. Check Mutual Exclusions (Are we creating a dangerous physical state?)
        active_exclusions = cls._exclusion_registry.get(action_name, [])
        for excluded_action in active_exclusions:
            if excluded_action in cls._physical_state_locks:
                 # Check if the excluded action is still within its operational window
                 last_excluded_time = cls._physical_state_locks[excluded_action]["timestamp"]
                 excluded_cooldown = cls._cooldown_registry.get(excluded_action, 0)
                 if (current_time - last_excluded_time) < excluded_cooldown:
                     return {
                        "is_safe": False,
                        "reason": f"KINETIC_MUTEX_VIOLATION: Cannot execute '{action_name}' while '{excluded_action}' is active."
                     }

        # 3. Grant Lock
        cls._physical_state_locks[action_name] = {
            "agent": agent_did,
            "timestamp": current_time
        }
        
        return {
            "is_safe": True,
            "reason": "Kinetic Interlock checks passed. Executing physical action."
        }
        
    @classmethod
    def check_safety(cls, action_name: str, params: dict) -> dict:
        """
        Phase 42.1: SDK Hook.
        Direct safety check for external applications.
        """
        # In this simulation, we check for thermodynamic limits or other physical safety params
        if "amount" in params and params["amount"] > 10000:
             return {"is_safe": False, "reason": "SAFETY_LIMIT_EXCEEDED: Transaction or Thermal amount exceeds hardware safety rating."}
        
        # Also check internal cooldowns/mutexes
        return cls.request_kinetic_action("SDK-AGENT", action_name)
