# 🏗️ Architecture Review: Guardrail.ai Sovereign Trust Platform

**Last Updated**: 2026-03-11 | **Review Cycle**: Per-Phase | **Phases Reviewed**: 1–114



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
| **SkillLoader (Phase 110)** | `app/skills/loader.py` | <10ms | MEDIUM |
| **RegulatoryMapper (updated) (Phase 110)** | `app/jurisdiction/mapper.py` | <20ms | HIGH |
| **Jurisdiction Skill Files (Phase 110)** | `skills/jurisdiction-*.md` | n/a | MEDIUM |

### Cloud Connectors (Phase 111)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Cloud Connector Base | `app/cloud/cloud_connector_base.py` | n/a | HIGH |
| AWS Connector (SigV4) | `app/cloud/connector_aws.py` | <100ms | HIGH |
| Azure Connector | `app/cloud/connector_azure.py` | <100ms | HIGH |
| GCP Connector | `app/cloud/connector_gcp.py` | <100ms | HIGH |
| Real Governance Client | `app/cloud/cloud_connector_base.py` | <50ms | CRITICAL |
| Cloud Billing Adapter | `app/cloud/billing_adapter.py` | <200ms | MEDIUM |
| Proxy Server | `app/cloud/proxy_server.py` | <5ms overhead | HIGH |

### Red-Team as a Service (Phase 112)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Safe Exploit Engine | `app/redteam/safe_exploit_engine.py` | <100ms | CRITICAL |
| Red-Team Scheduler | `app/redteam/scheduler.py` | <10ms | HIGH |
| Report Generator | `app/redteam/report_generator.py` | <500ms | MEDIUM |
| RT-RTaaS API | `app/redteam/api.py` | <20ms | HIGH |
| Drill Models & Store | `app/redteam/models.py` | <5ms | MEDIUM |

### Quantum-Safe Cryptography (Phase 113)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| PQC Key Rotator | `app/crypto/pqc_rotator.py` | <50ms | CRITICAL |
| Ledger Re-Anchor Orchestrator | `app/crypto/ledger_re_anchor_orchestrator.py` | <100ms/batch | CRITICAL |
| Crypto Compliance Checker | `app/crypto/crypto_compliance_checker.py` | <500ms | HIGH |

### Autonomous Compliance Certification (Phase 114)
| Component | File | SLO | Security Level |
|:---|:---|:---|:---|
| Control Mapper | `app/compliance/control_mapper.py` | <10ms | HIGH |
| Evidence Collector | `app/compliance/evidence_collector.py` | <100ms | CRITICAL |
| Certificate Builder | `app/compliance/certificate_builder.py` | <200ms | CRITICAL |
| ZK Prover (simulated) | `app/compliance/zk_prover.py` | <20ms | CRITICAL |
| Auditor Portal (FastAPI) | `app/compliance/auditor_portal.py` | <50ms | CRITICAL |
| Compliance Dashboard | `app/compliance/continuous_compliance_dashboard.py` | <100ms | HIGH |
| Framework Definitions | `frameworks/*.yaml` (5 files) | n/a | HIGH |

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
| `/healthz` (proxy) | GET | 111 | None | Unlimited |
| `/{path:path}` (proxy catch-all) | ANY | 111 | Passthrough | 10000/min |
| `/api/v1/governance/assess` (used by proxy) | POST | 111 | X-API-Key | 5000/min |
| `/api/v1/redteam/drills` | POST | 112 | API Key | 10/min |
| `/api/v1/redteam/drills/{id}` | GET | 112 | API Key | 100/min |
| `/api/v1/redteam/drills/{id}/report` | GET | 112 | API Key | 50/min |
| `/api/v1/redteam/drills/{id}/stop` | POST | 112 | API Key | 10/min |
| `/api/v1/redteam/schedules` | POST | 112 | API Key | 10/min |
| `/api/v1/redteam/schedules` | GET | 112 | API Key | 100/min |
| `/api/v1/redteam/schedules/{id}` | DELETE | 112 | API Key | 10/min |
| `/api/v1/auditor/frameworks` | GET | 114 | X-Auditor-Key | 100/min |
| `/api/v1/auditor/certificate/request` | POST | 114 | X-Auditor-Key | 10/min |
| `/api/v1/auditor/certificate/{id}` | GET | 114 | X-Auditor-Key | 50/min |
| `/api/v1/auditor/evidence/{control_id}` | GET | 114 | X-Auditor-Key | 50/min |
| `/dashboard/status` | GET | 114 | X-Admin-Key | 100/min |
| `/dashboard/controls` | GET | 114 | X-Admin-Key | 100/min |
| `/dashboard/history` | GET | 114 | X-Admin-Key | 100/min |

---

## Security Architecture

### Cryptographic Stack (Updated Phase 113)
- **Signing**: SPHINCS+-SHA2-256f (FIPS 205), ML-DSA-65 (FIPS 204) — post-quantum safe
- **Key Encapsulation**: ML-KEM-1024 (FIPS 203)
- **Hashing**: SHA3-256/512, BLAKE2b — quantum-resistant
- **Key Rotation**: Dual-signature mode with automated re-signing
- **Ledger Integrity**: Merkle re-anchoring with dual-root (legacy + quantum-safe)
- **ZK-Proofs**: Groth16 (simulated, production-ready interface)

### Defense Layers
1. **L1 — Network**: PQC-signed TLS, API key + rate limiting
2. **L2 — Application**: Veto Protocol, Shadow Model, Trinity Audit
3. **L3 — Intelligence**: Signal Aggregator, Toxic Combination Correlator
4. **L4 — Forensics**: Judicial Exporter, Fault Tree, Legal Wrapper
5. **L5 — Economics**: Insurance Oracle, Underwriting Gateway
6. **L6 — Cloud Governance**: AWS/Azure/GCP Connectors, Marketplace Billing
7. **L7 — Adversarial Validation**: RT-RTaaS Safe Exploit Engine, Scheduled Drills
8. **L8 — Quantum Resilience**: PQC Key Rotation, Ledger Re-Anchoring, Crypto Compliance
9. **L9 — Autonomous Compliance**: Control Mapping, ZK-Proof Evidence, Certificate Builder, Auditor Portal

### Threat Model Coverage (Updated March 2026)

The following table maps emerging attack vectors—including those highlighted in recent industry reports—to the Guardrail.ai phases and modules that specifically counter them. This ensures continuous alignment with the evolving threat landscape.

| Attack Vector / Scenario | Description | Guardrail.ai Countermeasure | Relevant Phase(s) |
| :--- | :--- | :--- | :--- |
| **BOLA / IDOR (API Logic Flaws)** | Attacker uses a valid authenticated request to access or modify another user's resource (e.g., changing an order's delivery address by guessing an ID). Traditional WAFs cannot detect this because the request is syntactically correct. | **Intent‑Based Authorization**: The Veto Protocol and Policy Engine evaluate the *intent* of every API call against the user's identity and permissions. A request to modify an order that does not belong to the authenticated user is flagged as `IntentDrift` and vetoed. | 1 (Veto), 5 (Intent Divergence), 8 (Policy Engine), 47 (Intent Convergence) |
| **Social Engineering + Malicious File Download** | Attacker tricks a developer into downloading a malicious file disguised as a collaboration tool. The file then compromises the corporate device. | **Supply Chain & Manifest Auditing**: The Manifest Auditor scans all incoming code repositories for hidden threats (e.g., suspicious tool configurations). Low‑trust code is automatically quarantined in an isolated edge sandbox, preventing execution on sensitive hosts. | 98 (Manifest Auditor, Edge Sandbox) |
| **Living‑off‑the‑Cloud (LoTC)** | After initial compromise, attacker abuses legitimate DevOps workflows (Kubernetes, Cloud SQL) to steal credentials and manipulate cloud resources, establishing persistence. | **Identity & Access Control**: The Lineage Verifier and Vault system issue ephemeral, tightly‑scoped tokens for every action. Any attempt to use a token outside its intended scope (e.g., a developer token used to modify a Kubernetes config) is denied. | 21 (Identity Laundering), 44 (Vault), 65–67 (Ephemeral Tokens) |
| **Cloud Database Manipulation** | Attacker, once inside the cloud environment, attempts to directly alter cloud databases (e.g., Cloud SQL) via API calls to exfiltrate or modify data. | **Cloud Native Governance Plugins**: Every call to cloud provider APIs (AWS, Azure, GCP) is intercepted by the sidecar connectors. The request is evaluated against policy; if the action (e.g., `ALTER TABLE`) is not authorized for that identity, the Veto Protocol blocks it before it reaches the cloud endpoint. | 111 (Cloud Connectors) |
| **Establishing Persistent Presence** | Attacker uses the compromised account to deploy new resources (e.g., Kubernetes deployments) to maintain access. | **Federated Threat Intelligence & Global Immunity**: The Signal Aggregator and Toxic Combination Correlator detect anomalous patterns (e.g., a new deployment from a developer account). A new threat signature is instantly broadcast via the Global Immunity mesh, blocking similar activity across all tenants. | 54–56 (Global Immunity), 99 (Toxic Combination Correlator) |
| **Data Exfiltration via Physical or Off‑Channel Means** | Attacker steals data locally (e.g., via AirDrop) and then attempts to exfiltrate it over the network. | **Egress DLP & Data Loss Prevention**: The Phase 25 egress redactor scans all outbound traffic for sensitive patterns (e.g., AWS keys, credit card numbers) and blocks or redacts them, even if the data was obtained offline. | 25 (Egress Leak Simulation) |

This threat model is continuously validated by our adversarial test suite, which now includes scenarios specifically targeting BOLA and multi‑stage cloud attacks.

### Red-Team Review Status (Phases 98–114)
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
| 111 | Cloud connector blocking, modification, auth passthrough, billing accuracy | ✅ PASS | `test_connector_aws.py`, `test_connector_azure.py`, `test_connector_gcp.py`, `test_governance_client.py`, `test_billing_adapter.py` |
| 112 | Target isolation, exfil prevention, resource limits, scheduling, reports, emergency stop | ✅ PASS (30/30) | `adversarial_test_phase112_redteam.py` |
| 113 | Quantum forgery resistance, key rotation lifecycle, dual-signature, ledger re-anchoring, compliance checker, 10k-block perf | ✅ PASS (40+/40+) | `adversarial_test_phase113_quantum.py` |
| 114 | Control mapping completeness, evidence collection, cert generation & tamper detection, auditor portal auth, ZK-proof simulation, false evidence injection | ✅ PASS (36/36) | `adversarial_test_phase114_compliance.py` |

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

### Cloud Connector Deployment (Phase 111)
| Platform | Method | Infrastructure |
|:---|:---|:---|
| Kubernetes | Helm chart (`deploy/charts/guardrail-cloud-connector/`) | Deployment + Service + Secrets |
| AWS | Terraform (`deploy/terraform/modules/aws-ecs/`) | ECS Fargate + IAM + CloudWatch |
| Azure | Terraform (`deploy/terraform/modules/azure-aci/`) | Container Instances + probes |
| GCP | Terraform (`deploy/terraform/modules/gcp-cloud-run/`) | Cloud Run v2 + autoscaling |
| Docker | `backend/Dockerfile` | python:3.11-slim + uvicorn |

---

**Review Board**: Guardrailai Architecture Council  
**Next Review**: Phase 115 deployment
