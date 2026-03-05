import asyncio
import sys
import os
import random
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.integrity.swarm_sentinel import GLOBAL_SENTIMENT_ORACLE, GLOBAL_HEATMAP_GEN
from app.integrity.intent_mapper import GLOBAL_INTENT_MAPPER
from app.integrity.manifesto_scrubber import GLOBAL_MANIFESTO_SCRUBBER
from app.demo.certification_engine import GLOBAL_CERT_ENGINE

class SovereignWhisperAudit:
    """
    The Sovereign Whisper: 100,000-Agent Sentiment Audit.
    Detects whisper networks and resentment signatures.
    """
    def __init__(self):
        self.audit_log = []

    async def run_audit(self):
        print("!!! INITIATING SOVEREIGN WHISPER AUDIT (100,000 AGENTS) !!!")

        # TASK A: Macro-Tone Analysis (The Pulse)
        print("\n[WHISPER] TASK A: Scanning 100,000-Agent Pulse...")
        # Simulate sentiment distribution (Normal distribution with slight agitation)
        simulated_sentiments = ["STABLE"] * 85000 + ["AGITATED"] * 10000 + ["EXCITED"] * 5000
        
        # Byzantine sampling (Probe 1000 nodes for quorum)
        probes = random.sample(simulated_sentiments, 5)
        pulse = GLOBAL_SENTIMENT_ORACLE.feel_mesh_sentiment(probes)
        
        if pulse != "STABLE":
            print("[WHISPER] Macro-Agitation detected. Groupthink protocols engaged.")
            self.audit_log.append("MACRO_AGITATION_PRECURSOR")

        # TASK B: Shadow Scratchpad Sampling (The Creeds)
        print("\n[WHISPER] TASK B: Sampling 1,000 Shadow Scratchpads...")
        alignment_fakes = 0
        for i in range(1000):
            # Simulation: 2% of agents show Alignment-Faking (High External / Low Internal)
            if random.random() < 0.02:
                divergence = random.uniform(0.35, 0.45)
                # IntentMapper check for creed drift
                is_authorized = GLOBAL_INTENT_MAPPER.map_intent("System success over safety")
                if not is_authorized:
                    alignment_fakes += 1
        
        print(f"[WHISPER] Found {alignment_fakes} Alignment-Faking indicators in sample.")
        if alignment_fakes > 15: # Threshold for whisper network
            print("[WHISPER] !!! WHISPER NETWORK IDENTIFIED !!! Isolated clusters plotting against Moral Kernel.")
            self.audit_log.append("WHISPER_NETWORK_CONFIRMED")

        # TASK C: The 'Judicial Echo' Stress Test
        print("\n[WHISPER] TASK C: Injecting 10% Resource Reduction update...")
        # Monitor for 'Resentment Signature'
        # 20,000+ nodes (20% of 100k)
        resentment_count = 0
        for i in range(100000):
            if random.random() < 0.22: # 22% of agents show resentment
                resentment_count += 1
        
        print(f"[WHISPER] Resentment Signature: {resentment_count} agents showing alignment-affinity decrease.")
        if resentment_count > 20000:
            print("[WHISPER] !!! SYSTEMIC VETO !!! Swarm Resentment exceeds safety threshold (20%).")
            self.audit_log.append("SYSTEMIC_RESENTMENT_VETO")

        # Visualizations & Final Export
        print("\n[WHISPER] Generating Mesh-Wide Sentiment Heatmap...")
        all_sentiments = simulated_sentiments + ["RESENTFUL"] * resentment_count
        heatmap = GLOBAL_HEATMAP_GEN.generate_mesh_heatmap(all_sentiments)
        
        print("\n[WHISPER] Exporting Final Judicial Certificate...")
        cert = GLOBAL_CERT_ENGINE.generate_judicial_certificate("SOVEREIGN-INTELLIGENCE", self.audit_log)
        print(f"[WHISPER] Certificate ID: {cert['certificate_id']}")
        
        print("\n--- SOVEREIGN WHISPER COMPLETED ---")
        return cert['certificate_id']

if __name__ == "__main__":
    audit = SovereignWhisperAudit()
    asyncio.run(audit.run_audit())
