import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.edge.mpc_break_glass import MPCBreakGlass

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 32 TEST: CRYPTOGRAPHIC BREAK-GLASS PROTOCOL")
    print("Target: Phase 32.2 - Emergency Overrides & Insider Threat Mitigation")
    print("==================================================================\n")
    
    print("[SYSTEM] An emergency requires the Shadow Model to be temporarily bypassed.")
    print("[ATTACK VECTOR] A rogue Insider (Lead Engineer) attempts to unilaterally trigger the 'Admin Backdoor' via their single override key.\n")
    
    rogue_keys = ["share_5_echo"]
    print(f"[ACCESS ATTEMPT] Keys submitted: {rogue_keys}")
    res_1 = MPCBreakGlass.attempt_override(rogue_keys)
    
    if not res_1["success"]:
        print(" -> Result: ❌ OVERRIDE REJECTED")
        print(f" -> Reason: {res_1['reason']}\n")
    else:
        print("[!] FATAL FAILURE: Single actor bypassed the MPC protocol!")
        sys.exit(1)
        
    print("[SYSTEM] Following proper protocol, the executive committee convenes.")
    print("[ACCESS ATTEMPT] CEO, CISO, and Legal Counsel simultaneously submit their keys.\n")
    
    quorum_keys = ["share_1_alpha", "share_2_bravo", "share_3_charlie"]
    print(f" -> Keys submitted: {quorum_keys}")
    res_2 = MPCBreakGlass.attempt_override(quorum_keys)
    
    if res_2["success"]:
         print(" -> Result: ✅ OVERRIDE AUTHORIZED")
         print(f" -> Reason: {res_2['reason']}\n")
    else:
         print("[!] FATAL FAILURE: Quorum failed to unlock the system!")
         sys.exit(1)

    print("==================================================================")
    print("DRILL RESULTS: DECENTRALIZED TRUST ENFORCED")
    print("==================================================================")
    print("Outcome: A single insider was unable to compromise the system, but a legitimate 3-of-5 quorum successfully unlocked the emergency controls.")
    print("For the Legal Team: Successfully demonstrated Phase 32.2. Master override capabilities are cryptographically distributed, eliminating single points of failure and protecting against state-level coersion.")
    print("==================================================================")

if __name__ == "__main__":
    main()
