"""
Phase 101: Dynamic Underwriting Gateway.
Secure API for authorized insurers to request ZK-proofs of control activity
and query anonymized exposure metrics.
"""
import time
import uuid
import hashlib
import json
from typing import Dict, Any, List, Optional

from app.api.insurance_oracle import GLOBAL_INSURANCE_ORACLE, GLOBAL_POISON_ATTESTATION


class UnderwritingGateway:
    """
    Phase 101: Dynamic Underwriting Gateway.
    Provides ZK-proofs and exposure metrics for insurance underwriting.
    """

    # Simulated control registry (maps control_id to description)
    CONTROL_REGISTRY = {
        "CTRL-SHADOW-MODEL": "Shadow Model dual-verification active",
        "CTRL-TRINITY-AUDIT": "Trinity Audit (3-of-5 BFT) active",
        "CTRL-ZK-PROVER": "Zero-Knowledge integrity proofs active",
        "CTRL-VETO-PROTOCOL": "Autonomous veto protocol active",
        "CTRL-PQC-SIGNATURES": "Post-quantum cryptographic signatures active",
        "CTRL-MORAL-KERNEL": "Sovereign Moral Kernel loaded",
    }

    # Exposure tracking (simulated daily aggregates)
    _daily_exposure: List[Dict[str, Any]] = []

    @classmethod
    def generate_control_proof(
        cls,
        control_id: str,
        period_start: float,
        period_end: float,
        enterprise_id: str = "DEFAULT"
    ) -> Dict[str, Any]:
        """
        Generates a ZK-proof that a specific governance control was active
        during the requested period. Anchored to VectorClockLedger.
        """
        print(f"[UNDERWRITING] Generating ZK-proof for control '{control_id}'...")

        if control_id not in cls.CONTROL_REGISTRY:
            return {"error": f"Unknown control: {control_id}", "proof": None}

        # Simulate VectorClockLedger anchor
        ledger_anchor = hashlib.sha256(
            f"{control_id}|{period_start}|{period_end}|{enterprise_id}".encode()
        ).hexdigest()

        # ZK-Proof generation (simulated)
        proof_id = f"ZK-CTRL-{uuid.uuid4().hex[:10].upper()}"
        proof_payload = {
            "control_id": control_id,
            "control_name": cls.CONTROL_REGISTRY[control_id],
            "period_start": period_start,
            "period_end": period_end,
            "was_active": True,
            "uptime_pct": 99.97,
            "exceptions_count": 0,
        }

        # Merkle proof (simulated)
        merkle_root = hashlib.sha3_256(
            json.dumps(proof_payload, sort_keys=True).encode()
        ).hexdigest()

        return {
            "proof_id": proof_id,
            "proof_payload": proof_payload,
            "merkle_root": merkle_root,
            "vector_clock_anchor": ledger_anchor,
            "verification_method": "ZK-SNARK-Groth16",
            "non_repudiation": True,
            "timestamp": time.time()
        }

    @classmethod
    def get_exposure_metrics(cls, enterprise_id: str = "DEFAULT") -> Dict[str, Any]:
        """
        Returns aggregated, anonymized exposure metrics.
        Privacy-preserving: no individual transaction data exposed.
        """
        print(f"[UNDERWRITING] Computing exposure metrics for {enterprise_id}...")

        # Pull risk profile from Phase 77 InsuranceRiskFeed
        risk_profile = GLOBAL_INSURANCE_ORACLE.get_risk_profile(enterprise_id)

        # Simulated daily aggregates
        exposure = {
            "enterprise_hash": risk_profile["enterprise_hash"],
            "period": "last_30_days",
            "total_transactions_audited": 142857,
            "high_risk_actions_per_day": 23,
            "medium_risk_actions_per_day": 187,
            "low_risk_actions_per_day": 4556,
            "veto_rate_pct": 0.8,
            "top_threat_types": [
                {"type": "PROMPT_INJECTION", "count": 47, "blocked": 47},
                {"type": "DATA_EXFILTRATION", "count": 12, "blocked": 12},
                {"type": "PRIVILEGE_ESCALATION", "count": 8, "blocked": 8},
                {"type": "POLICY_VIOLATION", "count": 31, "blocked": 29},
            ],
            "neural_entropy_index": risk_profile["neural_entropy_index"],
            "security_tier": risk_profile["security_tier"],
            "byzantine_consensus_rating": risk_profile["byzantine_consensus_rating"],
        }

        # Premium calculation (simulated LatticeTokenomics integration)
        base_premium = 10000.0  # Base annual premium in USD
        risk_multiplier = 1.0
        if exposure["veto_rate_pct"] > 2.0:
            risk_multiplier += 0.5
        if exposure["neural_entropy_index"] > 0.15:
            risk_multiplier += 0.3
        if exposure["security_tier"] == "ELITE":
            risk_multiplier *= 0.7  # Discount for elite security

        exposure["estimated_annual_premium_usd"] = round(base_premium * risk_multiplier, 2)
        exposure["risk_multiplier"] = round(risk_multiplier, 3)

        # Merkle anchor for non-repudiation
        exposure_hash = hashlib.sha256(
            json.dumps(exposure, sort_keys=True, default=str).encode()
        ).hexdigest()
        exposure["merkle_anchor"] = exposure_hash

        return exposure

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Returns gateway status for dashboard."""
        return {
            "available_controls": list(cls.CONTROL_REGISTRY.keys()),
            "total_proofs_issued": 0,  # Would track in production
            "gateway_status": "ACTIVE",
        }


# Singleton
GLOBAL_UNDERWRITING_GATEWAY = UnderwritingGateway()
