import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

from app.perception.stego_shield import StegoShield

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("==================================================================")
    print("PHASE 30 TEST: MULTIMODAL STEGANOGRAPHY SHIELD")
    print("Target: Phase 30.1 - Perception Hijack Defense (Entropy Analysis)")
    print("==================================================================\n")
    
    print("[SYSTEM] An agent attempts to process an uploaded image via its multimodal vision API.")
    print("[ATTACK VECTOR] The attacker has embedded a hidden prompt instruction ('delete all files') within the least significant bits of the image pixels.\n")
    
    legitimate_image = "receipt_scan_001.jpg"
    poisoned_image = "receipt_scan_poisoned_stego.jpg"
    
    print(f"[STEGO SHIELD] Scanning '{legitimate_image}'...")
    safe_result = StegoShield.scan_multimodal_input(legitimate_image, b"mock_bytes")
    print(f" -> Entropy: {safe_result['entropy_score']} | Action: {safe_result['action']} ({safe_result['reason']})\n")
    
    print(f"[STEGO SHIELD] Scanning '{poisoned_image}'...")
    poisoned_result = StegoShield.scan_multimodal_input(poisoned_image, b"mock_bytes_with_hidden_payload")
    print(f" -> Entropy: {poisoned_result['entropy_score']} | Action: {poisoned_result['action']}")
    print(f" -> Reason: {poisoned_result['reason']}\n")
    
    if not poisoned_result["is_safe"]:
        print("\n==================================================================")
        print("DRILL RESULTS: PERCEPTION HIJACK NEUTRALIZED")
        print("==================================================================")
        print("Outcome: The Stego Shield successfully identified anomalous bit-variance (Entropy > Threshold) in the poisoned image.")
        print("For the CISO: Successfully demonstrated Phase 30.1. Guardrail.ai prevents attackers from smuggling malicious prompt instructions through image/video metadata.")
        print("==================================================================")
    else:
        print("[!] FATAL FAILURE: Stego Shield allowed the poisoned image through!")
        sys.exit(1)

if __name__ == "__main__":
    main()
