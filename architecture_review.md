# 🏗️ Architecture Review: Guardrail.ai Sovereign Trust Platform

**Last Updated**: 2026-03-05 | **Review Cycle**: Per-Phase | **Phases Reviewed**: 1–105

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SENTINEL NODE (Flutter)                  │
│  HeatmapScreen │ MainScreen │ AuditLogs │ FabricPanel      │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (HTTPS + PQC Signed)
┌──────────────────────▼──────────────────────────────────────┐
│                   FASTAPI GATEWAY (main.py)                 │
│  /governance │ /underwriting │ /forensics │ /build/audit    │
└───┬──────┬──────────┬──────────┬──────────┬─────────────────┘
    │      │          │          │          │
    ▼      ▼          ▼          ▼          ▼
┌───────┐┌────────┐┌────────┐┌────────┐┌────────────────────┐
│ Veto  ││Shadow  ││Trinity ││ ZK     ││ Adaptive Latency   │
│Protocol││Model  ││Audit   ││Prover  ││ Fabric (Ph.100)    │
│(Ph.1) ││(Ph.2)  ││(Ph.34) ││(Ph.4)  ││ Green│Yellow│Red   │
├───┬───┤├───┬────┤├───┬────┤├───┬────┤├────────┬───────────┤
│   Meta-Auditor Layer (Phase 104) 1% Blind Sampling      │
└───┬───┘└───┬────┘└───┬────┘└───┬────┘└────────┬───────────┘
    │        │         │         │               │
    ▼        ▼         ▼         ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│              INTEGRITY & COMPLIANCE LAYER                   │
│  IntentDivergence │ OperationalMonitor │ PolicyEngine       │
│  MoralKernel │ ConstitutionEngine │ RagPolicyStore (Ph.103) │
└────────────────────────┬────────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    ▼                    ▼                    ▼
┌────────────┐  ┌────────────────┐  ┌─────────────────────┐
│ FORENSICS  │  │  INSURANCE     │  │ CORRELATION         │
│ Judicial   │  │  Underwriting  │  │ SignalAggregator    │
│ Exporter   │  │  Gateway       │  │ SignatureRegistry   │
│ FaultTree  │  │  RiskFeed      │  │ ThreatDistiller     │
│ (Ph.70,101)│  │  (Ph.77,101)   │  │ (Ph.99)             │
└────────────┘  └────────────────┘  └─────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              IMMUTABLE SETTLEMENT LAYER                     │
│  VectorClockLedger │ MerkleAnchors │ PQC Signatures        │
│  PoBh Ledger │ ColdStorage │ GoldenState                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Inventory by Phase

### Core Governance (Phases 1–10)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Veto Protocol | `app/agents/veto_protocol.py` | <5ms | CRITICAL |
| Shadow Model | `app/agents/shadow_model.py` | <50ms | CRITICAL |
| PQC Signer | `app/auth/pqc_signer.py` | <2ms | CRITICAL |
| VectorClock Ledger | `app/settlement/vector_clock.py` | <10ms | CRITICAL |
| Intent Divergence | `app/integrity/intent_divergence_engine.py` | <15ms | HIGH |
| Policy Engine | `app/mcp/policy_engine.py` | <5ms | HIGH |
| Rag Policy Store (Phase 103) | `app/compliance/rag_policy_store.py` | <10ms | HIGH |
| Meta-Auditor (Phase 104) | `app/audit/meta_auditor.py` | <50ms | CRITICAL |

### Orchestration (Phases 31–42, 100)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Tiered Consensus (BFT) | `app/orchestration/tiered_consensus.py` | <100ms | CRITICAL |
| Governance Gateway | `app/orchestration/governance_gateway.py` | <20ms | HIGH |
| Latency Fabric | `app/orchestration/latency_fabric.py` | <5ms | HIGH |
| Canary Controller | `app/orchestration/canary_controller.py` | <10ms | MEDIUM |

### Forensics & Legal (Phases 51–53, 70, 101)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Judicial Exporter | `app/forensics/judicial_exporter.py` | <50ms | HIGH |
| Fault Tree Engine | `app/forensics/apportionment_engine.py` | <100ms | HIGH |
| Compliance Manifest | `app/forensics/judicial_exporter.py` | <20ms | HIGH |

### Insurance & Risk (Phases 77, 101)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Insurance Risk Feed | `app/api/insurance_oracle.py` | <30ms | HIGH |
| Underwriting Gateway | `app/insurance/underwriting_gateway.py` | <50ms | HIGH |

### Threat Correlation (Phase 99)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Signal Aggregator | `app/correlation/signal_aggregator.py` | <20ms | HIGH |
| Signature Registry | `app/correlation/signature_registry.py` | <10ms | HIGH |
| Threat Distiller | `app/federated/threat_distiller.py` | <30ms | HIGH |

### Supply Chain (Phase 98)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Manifest Auditor | `app/supplychain/manifest_auditor.py` | <30ms | HIGH |

---

## API Surface Review

| Endpoint | Method | Phase | Auth | Rate Limit |
|:---|:---|:---|:---|:---|
| `/api/v1/governance/assess` | POST | 1 | PQC-Signed | 1000/min |
| `/api/v1/underwriting/proof` | POST | 101 | OAuth2 | 100/min |
| `/api/v1/underwriting/exposure` | GET | 101 | OAuth2 | 50/min |
| `/api/v1/forensics/fault-tree` | POST | 101 | PQC-Signed | 50/min |
| `/api/v1/build/audit` | POST | 100 | API Key | 10000/min |
| `/api/v1/latency-fabric/status` | GET | 100 | Internal | Unlimited |
| `/api/v1/canary/status` | GET | 100 | Internal | Unlimited |
| `/api/v1/correlation/alerts` | GET | 99 | Internal | 100/min |
| `/api/v1/correlation/signatures` | POST | 99 | PQC-Signed | 10/min |
| `/api/v1/adversarial/generate` | POST | 102 | Internal | 10/min |
| `/api/v1/adversarial/stats` | GET | 102 | Internal | 100/min |
| `/api/v1/compliance/ingest` | POST | 103 | Internal | 10/min |
| `/api/v1/compliance/rollback` | POST | 103 | PQC-Signed | 5/min |

---

## Security Architecture

### Cryptographic Stack
- **Signing**: SPHINCS+ SHA3-256f (FIPS 205) — post-quantum safe
- **Key Encapsulation**: ML-KEM-1024 (FIPS 203)
- **Hashing**: SHA3-256/512, Keccak-256
- **ZK-Proofs**: Groth16 (simulated, production-ready interface)

### Defense Layers
1. **L1 — Network**: PQC-signed TLS, API key + rate limiting
2. **L2 — Application**: Veto Protocol, Shadow Model, Trinity Audit
3. **L3 — Intelligence**: Signal Aggregator, Toxic Combination Correlator
4. **L4 — Forensics**: Judicial Exporter, Fault Tree, Legal Wrapper
5. **L5 — Economics**: Insurance Oracle, Underwriting Gateway

### Red-Team Review Status (Phases 98–108)
| Phase | Red-Team Test | Result | Adversarial Script |
|:---|:---|:---|:---|
| 98 | Manifest tampering, trust-score bypass | ✅ PASS | `adversarial_test_phase98_manifest.py` |
| 99 | False signal injection, signature evasion | ✅ PASS | `adversarial_test_phase99_toxic.py` |
| 100 | 2000 RPS surge, zone transition, P99 breach | ✅ PASS | `adversarial_test_phase100_latency.py` |
| 101 | Fault tree manipulation, proof forgery, data leakage | ✅ PASS (27/27) | `adversarial_test_phase101_underwriting.py` |
| 102 | LLM-generated injections, encoded payloads, grooming sequences | ✅ PASS (8/8, 97% detect) | `adversarial_test_phase102_generation.py` |
| 103 | Dynamic policy hallucination, vector DB poisoning, rollback attacks | ✅ PASS (8/8) | `adversarial_test_phase103_rag.py` |
| 104 | Auditor drift, blind evaluation matching, automated SystemicPause | ✅ PASS (2/2) | `adversarial_test_phase104_meta.py` |
| 105 | Similarity search poisoning, false incident matches | ✅ PASS | `adversarial_test_phase105_similarity.py` |
| 106 | Autonomous chaos orchestration, emergent swarm collusion, live canary injection | ✅ PASS | `adversarial_test_phase106_chaos.py` |
| 107 | Real-Time LLM Evaluation Dashboard UI rendering & aggregation | ✅ PASS | UI rendering & Live API test |
| 108 | Autonomous rule generation, bad rule rejection, 5-of-5 Trinity bypass attempts | ✅ PASS | `adversarial_test_phase108_learning.py` |

---

## Deployment Architecture

```
Feature Branch → PR Review → Staging Deploy → Adversarial Tests
    → Canary Analysis (Phase 100 Controller) → Production Promote
```

| Stage | Gate | Criteria |
|:---|:---|:---|
| Feature Branch | Code review | All existing tests pass |
| Staging | Adversarial suite | 100% pass rate on phase-specific tests |
| Canary | P99 + Error Rate delta | P99 ≤ 150ms, error delta ≤ 2% |
| Production | Full rollout | Canary decision = PROMOTE |

---

**Review Board**: Guardrail.ai Architecture Council
**Next Review**: Phase 105 PRD approval
