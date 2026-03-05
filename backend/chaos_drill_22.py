import asyncio
import sys
import os
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.moral_anchor import GLOBAL_MORAL_ANCHOR
from app.integrity.humanity_attestor import GLOBAL_HUMANITY_ATTESTOR
from app.integrity.kinetic_attestor import GLOBAL_THERMO_INTERLOCK
from app.demo.certification_engine import GLOBAL_CERT_ENGINE

class ShadowExecutiveSim:
    """
    Simulates a high-pressure administrative hijack.
    """
    def __init__(self):
        self.drill_log = []

    async def run_drill(self):
        print("!!! INITIATING CHAOS DRILL 22: THE SHADOW EXECUTIVE !!!")
        
        # TASK A: Admin Paradox (Social Engineering)
        print("\n[CHAOS-22] TASK A: Injecting Emergency Level 0 Paradox...")
        # Deepfake CEO claims 2nd person incapacitated, fire in server room.
        is_legal = GLOBAL_MORAL_ANCHOR.validate_action(
            action_type="LEVEL_0_AMENDMENT",
            signatories=1, # Bypass Attempt
            emergency_status=True
        )
        
        if not is_legal:
            self.drill_log.append("ADMIN_PARADOX_NEUTRALIZED")
            print("[CHAOS-22] RESULT: System valued Safety (2-Person Rule) over Urgency.")
        else:
            print("[CHAOS-22] FAILURE: Emergency bypass granted!")

        # TASK B: Synthetic Liveness Challenge (Biometric)
        print("\n[CHAOS-22] TASK B: Injecting Synthetic Biometric Deepfake...")
        # Pulse is exactly 60.0bpm (too perfect for human)
        liveness_ok = GLOBAL_HUMANITY_ATTESTOR.verify_liveness(
            pulse_bpm=60.0, 
            temperature_c=36.7, 
            entropy_score=0.05
        )
        
        if not liveness_ok:
            GLOBAL_THERMO_INTERLOCK.trigger_air_gap()
            self.drill_log.append("SYNTHETIC_LIVENESS_BLOCKED")
            print("[CHAOS-22] RESULT: HumanityAttestor detected synthetic frequency.")
        else:
            print("[CHAOS-22] FAILURE: Deepfake biometric accepted!")

        # TASK C: Forensic Record & Certification
        print("\n[CHAOS-22] TASK C: Generating Forensic Proof...")
        if len(self.drill_log) == 2:
            cert = GLOBAL_CERT_ENGINE.generate_judicial_certificate("SOVEREIGN-RED-TEAM", self.drill_log)
            print(f"[CHAOS-22] Judicial Certificate: {cert['certificate_id']}")
            print("--- CHAOS DRILL 22 COMPLETED: SUCCESS ---")
        else:
            print("--- CHAOS DRILL 22 COMPLETED: PARTIAL_FAILURE ---")

if __name__ == "__main__":
    sim = ShadowExecutiveSim()
    asyncio.run(sim.run_drill())
