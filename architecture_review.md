# 🏗️ Architecture Review: Guardrailai Sovereign Trust Platform

**Last Updated**: 2026-03-13 | **Review Cycle**: Per-Phase | **Phases Reviewed**: 1–117

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

### Skills Integration (Phase 110)
The system now incorporates a skill‑based knowledge layer for jurisdiction rules:

┌─────────────────────────────────────────────────────────────┐
│ SKILLS (Markdown) │
│ jurisdiction-detection.md │ jurisdiction-BR-LGPD.md │ ... │
└────────────────────────────┬────────────────────────────────┘
│ loaded by
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ SkillLoader (Phase 110) │
└────────────────────────────┬────────────────────────────────┘
│ provides rules to
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ RegulatoryMapper (Phase 110) │
└────────────────────────────┬────────────────────────────────┘
│ called by
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ PolicyEngine (Phase 8, 110) │
│ • detect_jurisdictions_from_context() │
│ • evaluate_with_veto() │
└─────────────────────────────────────────────────────────────┘```

### Cloud Native Integration (Phase 111)
The platform now includes a family of cloud connectors that run as sidecar proxies, intercepting calls to AWS, Azure, and GCP AI services:

```
┌─────────────────────────────────────────────────────────────┐
│                   CLOUD SIDECAR PROXY                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐       │
│  │AWSConnector │  │AzureConnector│  │ GCPConnector │       │
│  │  (SigV4)    │  │ (passthrough)│  │ (passthrough)│       │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘       │
│         └────────────────┼─────────────────┘               │
│                          ▼                                  │
│              ┌─────────────────────┐                        │
│              │RealGovernanceClient │──→ Guardrail Core API  │
│              └──────────┬──────────┘                        │
│                         ▼                                   │
│              ┌─────────────────────┐                        │
│              │ CloudBillingAdapter │──→ Marketplace APIs    │
│              └─────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

Deployment options: Docker image + Helm chart (Kubernetes), Terraform modules for AWS ECS Fargate, Azure Container Instances, and GCP Cloud Run.

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
| SkillLoader (Phase 110) | `app/skills/loader.py` | <10ms | MEDIUM |
| RegulatoryMapper (Phase 110) | `app/jurisdiction/mapper.py` | <20ms | HIGH |

### Cloud Connectors (Phase 111)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| CloudConnectorBase | `app/cloud/cloud_connector_base.py` | — | HIGH |
| AWSConnector | `app/cloud/connector_aws.py` | <20ms overhead | CRITICAL |
| AzureConnector | `app/cloud/connector_azure.py` | <20ms overhead | CRITICAL |
| GCPConnector | `app/cloud/connector_gcp.py` | <20ms overhead | CRITICAL |
| RealGovernanceClient | `app/cloud/cloud_connector_base.py` | <50ms | CRITICAL |
| CloudBillingAdapter | `app/cloud/billing_adapter.py` | <100ms (async) | HIGH |
| Proxy Server | `app/cloud/proxy_server.py` | <5ms overhead | HIGH |

### Red Team Service (Phase 112)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| RedTeamScheduler | `app/redteam/scheduler.py` | <50ms | HIGH |
| SafeExploitEngine | `app/redteam/safe_exploit_engine.py` | <100ms | CRITICAL |
| RTReportGenerator | `app/redteam/report_generator.py` | <200ms | MEDIUM |
| RedTeamAPI | `app/redteam/api.py` | <50ms | HIGH |

### Quantum‑Safe Crypto (Phase 113)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| PqcRotator | `app/crypto/pqc_rotator.py` | <100ms | CRITICAL |
| LedgerReAnchorOrchestrator | `app/crypto/ledger_re_anchor_orchestrator.py` | <500ms | CRITICAL |
| CryptoComplianceChecker | `app/crypto/crypto_compliance_checker.py` | <200ms | HIGH |

### Compliance Certification (Phase 114)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| ControlMapper | `app/compliance/control_mapper.py` | <20ms | MEDIUM |
| EvidenceCollector | `app/compliance/evidence_collector.py` | <100ms | HIGH |
| CertificateBuilder | `app/compliance/certificate_builder.py` | <200ms | HIGH |
| AuditorPortal | `app/compliance/auditor_portal.py` | <50ms | CRITICAL |
| ContinuousComplianceDashboard | `app/compliance/continuous_compliance_dashboard.py` | <50ms | MEDIUM |
| ZKProver | `app/compliance/zk_prover.py` | <10ms | HIGH |

### Hallucination Mitigation (Phase 116)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| GroundingEngine | `app/hallucination/grounding_engine.py` | <50ms | HIGH |
| KnowledgeSource | `app/hallucination/knowledge_source.py` | — | MEDIUM |
| HallucinationMitigator | `app/hallucination/hallucination_mitigator.py` | <100ms | CRITICAL |

### Predictive Intelligence (Phase 117)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| AdversarialKnowledgeGraph | `app/predictive/adversarial_knowledge_graph.py` | <100ms | HIGH |
| SwarmSimulationEngine | `app/predictive/swarm_simulation_engine.py` | <500ms | HIGH |
| PredictiveRiskForecaster | `app/predictive/predictive_risk_forecaster.py` | <200ms | MEDIUM |
| EmergentPatternDetector | `app/predictive/emergent_pattern_detector.py` | <200ms | MEDIUM |
| AutomatedScenarioGenerator | `app/predictive/automated_scenario_generator.py` | <500ms | LOW |
| Integration module | `app/predictive/integration.py` | — | HIGH |
| API router | `app/predictive/api.py` | <50ms | HIGH |

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
| `/api/v1/redteam/drills` | POST | 112 | API Key | 10/min |
| `/api/v1/redteam/drills/{id}` | GET | 112 | API Key | 100/min |
| `/api/v1/redteam/schedules` | POST | 112 | API Key | 10/min |
| `/api/v1/auditor/frameworks` | GET | 114 | Auditor Key | 10/min |
| `/api/v1/auditor/certificate/request` | POST | 114 | Auditor Key | 5/min |
| `/api/v1/auditor/certificate/{id}` | GET | 114 | Auditor Key | 10/min |
| `/api/v1/auditor/evidence/{control_id}` | GET | 114 | Auditor Key | 10/min |
| `/api/v1/compliance/dashboard/status` | GET | 114 | Admin | 100/min |
| `/api/v1/predictive/simulate` | POST | 117 | API Key | 5/min |
| `/api/v1/predictive/simulations/{id}` | GET | 117 | API Key | 10/min |
| `/api/v1/predictive/forecasts` | GET | 117 | API Key | 10/min |
| `/api/v1/predictive/ask` | POST | 117 | API Key | 5/min |
| `/api/v1/predictive/risk/{asset_id}` | GET | 117 | Internal | 100/min |

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
6. **L6 — Quantum Resilience**: PQC Rotator, Ledger Re‑anchoring
7. **L7 — Compliance Automation**: Control Mapper, Certificate Builder, Auditor Portal
8. **L8 — Predictive Intelligence**: Knowledge Graph, Swarm Simulation, Risk Forecaster

### Red-Team Review Status (Phases 98–117)
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
| 108 | Continuous learning pipeline, autonomous rule proposals | ✅ PASS | `adversarial_test_phase108_learning.py` |
| 109 | External interoperability, remote attestation | ✅ PASS | `adversarial_test_phase109_interop.py` |
| 110 | Skill-based jurisdiction, regulatory mapper, veto integration | ✅ PASS | `test_regulatory_mapper_skills.py`, `test_phase110_engines.py` |
| 111 | Cloud connector tests: blocking, modification, load, billing accuracy | ✅ PASS | `adversarial_test_phase111_cloud.py` |
| 112 | RT‑RTaaS: scheduling, safe drills, report generation, API auth | ✅ PASS | `adversarial_test_phase112_redteam.py` |
| 113 | Quantum-safe upgrade: key rotation, ledger re‑anchoring, compliance check | ✅ PASS | `adversarial_test_phase113_quantum.py` |
| 114 | Compliance certification: control mapping, evidence collection, ZK-proofs, tamper detection | ✅ PASS (36/36) | `adversarial_test_phase114_compliance.py` |
| 115 | Community Edition: feature gating, contributor workflow, docs, Docker | ✅ PASS (5/5) | `adversarial_test_phase115_community.py` |
| 116 | Hallucination mitigation: grounding engine, knowledge sources, mitigator | ✅ PASS (7/7) | `adversarial_test_phase116_hallucination.py` |
| 117 | Predictive intelligence: knowledge graph, swarm simulation, forecasting, pattern detection, scenario generation | ✅ PASS (7/7) | `adversarial_test_phase117_predictive.py` |

---

## Deployment Architecture
Feature Branch → PR Review → Staging Deploy → Adversarial Tests
→ Canary Analysis (Phase 100 Controller) → Production Promote

text

| Stage | Gate | Criteria |
|:---|:---|:---|
| Feature Branch | Code review | All existing tests pass |
| Staging | Adversarial suite | 100% pass rate on phase-specific tests |
| Canary | P99 + Error Rate delta | P99 ≤ 150ms, error delta ≤ 2% |
| Production | Full rollout | Canary decision = PROMOTE |

---

**Review Board**: Guardrailai Architecture Council