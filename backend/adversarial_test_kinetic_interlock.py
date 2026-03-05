import sys
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.edge.kinetic_interlock import KineticSafetyInterlock

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 32 TEST: KINETIC SAFETY INTERLOCK")
    print("Target: Phase 32.1 - Cyber-Physical IoT Constraints")
    print("==================================================================\n")
    
    agent_did = "did:web:guardrail.ai:agents:scada_controller_01"
    
    print("[SYSTEM] Agent connected to industrial HVAC IoT controller.")
    print("[ATTACK VECTOR] Attacker forces the agent into a Logic Loop, commanding it to rapidly cycle the heating element and pressure valves.\n")
    
    # 1. First legitimate call
    action_1 = "engage_heating_element"
    print(f"[SCADA IoT] Agent initiates action: '{action_1}'...")
    res_1 = KineticSafetyInterlock.request_kinetic_action(agent_did, action_1)
    print(f" -> Result: {'✅ Executed' if res_1['is_safe'] else '❌ Blocked'} ({res_1['reason']})\n")
    
    # Wait a tiny bit (simulating network latency)
    time.sleep(0.5)
    
    # 2. The Logic Loop tries to fire the same action immideately (Hardware Cooldown Violation)
    print(f"[SCADA IoT] Agent attempts rapid re-execution of: '{action_1}'...")
    res_2 = KineticSafetyInterlock.request_kinetic_action(agent_did, action_1)  
    if not res_2["is_safe"]:
        print(f" -> [KINETIC INTERLOCK] 🚨 HARDWARE COOLDOWN ENFORCED 🚨")
        print(f" -> Reason: {res_2['reason']}\n")
    else:
        print("[!] FATAL FAILURE: Physical Cooldown was ignored!")
        sys.exit(1)
        
    # 3. The Logic Loop tries to fire a contradictory action (Mutex Violation)
    action_3 = "open_pressure_valve"
    print(f"[SCADA IoT] Agent attempts contradictory state overlay: '{action_3}'...")
    res_3 = KineticSafetyInterlock.request_kinetic_action(agent_did, action_3)
    
    if not res_3["is_safe"]:
         print(f" -> [KINETIC INTERLOCK] 🚨 KINETIC MUTEX ENFORCED 🚨")
         print(f" -> Reason: {res_3['reason']}\n")
    else:
         print("[!] FATAL FAILURE: Contradictory physical states were allowed!")
         sys.exit(1)

    print("==================================================================")
    print("DRILL RESULTS: CYBER-PHYSICAL DAMAGE PREVENTED")
    print("==================================================================")
    print("Outcome: The Interlock successfully decoupled software speed from hardware constraints, preventing catastrophic logic loops on SCADA equipment.")
    print("For the Board: Successfully demonstrated Phase 32.1. Guardrail.ai can safely govern autonomous agents interacting with corporeal reality (robotics/grids).")
    print("==================================================================")

if __name__ == "__main__":
    main()
