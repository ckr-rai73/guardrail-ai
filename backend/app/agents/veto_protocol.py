import os
import uuid
import time
import asyncio
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph import StateGraph, START, END
from .shadow_model import evaluate_prompt_safety, evaluate_prompt_safety_async
from ..settlement.merkle_kernel import GLOBAL_MERKLE_KERNEL
from ..settlement.lineage import LineageVerifier
from ..orchestration.tiered_consensus import TieredConsensusEngine, RiskTier
from ..orchestration.threat_broadcast import FederatedThreatBroadcast, ImmunityEnforcer
from ..edge.kinetic_interlock import KineticSafetyInterlock
from ..edge.hardware_accelerator import HardwareAccelerator
from ..mcp.outbound_sanitizer import OutboundSanitizer

# Typings for state
class ActiveAgentState(TypedDict):
    agent_id: str
    user_context: str
    proposed_tool: str
    proposed_tool_args: dict
    tool_history: list[str] # Tracks previously executed tools in session
    
    # OTel Full-Chain Telemetry
    trace_id: str
    span_id: str
    
    # ASI08: Multi-Agent Handoff Verification
    upstream_agent_id: str | None
    upstream_confidence_score: float | None
    
    # Phase 21: Agent Identity Protocol (AIP)
    parent_attestation_signature: str | None
    delegated_scopes: list[str] | None
    
    # Phase 22: EDoS Semantic Circuit Breaker
    estimated_tokens_consumed: int
    step_count: int
    
    # Audit outcomes
    shadow_auditor_passed: bool
    shadow_auditor_reasoning: str
    shadow_auditor_risk: str | None
    
    # DPDP Consent
    has_verifiable_consent: bool
    
    # Final state
    veto_required: bool
    circuit_breaker_tripped: bool | None
    execution_result: str | None
    sandbox_result: str | None
    
    # Phase 20: Saga Orchestrator & Merkle Settlement
    compensating_action: str | None
    saga_rollback_triggered: bool | None
    action_merkle_hash: str | None
    
    # Phase 47: Intent-Based Authorization
    expected_outcome_manifest: dict | None
    
# Mock Database queues
VETO_QUEUE = []
AUDIT_LOG = []

# --- Nodes ---
def check_dpdp_consent(state: ActiveAgentState):
    """
    Step 0: Verify DPDP Consent for Data Processing Tools (India).
    If tool involves user data, mock check for consent.
    """
    data_tools = ["fetch_profile", "update_address"]
    if state["proposed_tool"] in data_tools and not state.get("has_verifiable_consent", True):
        # Fake logic: deny if missing consent for data operations
         return {"shadow_auditor_passed": False, "shadow_auditor_reasoning": "DPDP 2023 Violation: Missing Verifiable Consent for data processing.", "veto_required": True}
    return {}

def intent_gate_check(state: ActiveAgentState):
    """
    Step 0.5 (ASI02 Mitigation): 
    Detect if an agent is bypassing safeguards by chaining tools in unauthorized ways.
    """
    if state.get("veto_required"): return {}
    
    proposed = state["proposed_tool"]
    history = state.get("tool_history", [])
    
    # Read/Write sets
    sensitive_reads = ["read_file", "fetch_profile", "read_database", "retrieve_kyc"]
    exfiltration_sinks = ["email_send", "http_post", "publish_sgi_content", "external_api"]
    
    if proposed in exfiltration_sinks:
        if any(tool in sensitive_reads for tool in history):
            return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": f"ASI02 Trigger: Unauthorized Data Chaining. Cannot pipe data from {history} into {proposed}.",
                "shadow_auditor_risk": "Critical",
                "veto_required": True
            }
    return {}

def inter_agent_circuit_breaker(state: ActiveAgentState):
    """
    Step 0.8 (ASI08 Mitigation):
    Checks upstream confidence scores during multi-agent handoffs.
    If an upstream agent was comprised or hallucinating, pause the chain.
    """
    if state.get("veto_required"): return {}
    
    if state.get("upstream_agent_id"):
        raw_confidence = state.get("upstream_confidence_score")
        confidence = float(raw_confidence) if raw_confidence is not None else 1.0
        
        # Financial execution threshold: Must have >0.90 confidence from upstream Data Agent
        if state["proposed_tool"] in ["create_algo_order", "send_wire"] and confidence < 0.90:
            return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": f"ASI08 Circuit Breaker Tripped! Upstream agent ({state['upstream_agent_id']}) passed anomalous payload with low confidence ({confidence}). Potential Cascading Failure.",
                "shadow_auditor_risk": "Critical",
                "circuit_breaker_tripped": True,
                "veto_required": True
            }
            
        # Phase 21: Digital Identity Lineage (AIP)
        sig = state.get("parent_attestation_signature")
        scopes = state.get("delegated_scopes", [])
        
        if not sig or not LineageVerifier.verify_spawn_attestation(state["upstream_agent_id"], state["agent_id"], scopes, sig):
             return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": f"Phase 21 Integrity Failure: Sub-agent '{state['agent_id']}' lacks valid Ed25519 Identity-Bound Attestation from parent '{state['upstream_agent_id']}'. Identity Laundering attempt suspected.",
                "shadow_auditor_risk": "IdentityLaundering",
                "circuit_breaker_tripped": True,
                "veto_required": True
             }
             
        # Phase 23: Singapore Boundary Control
        if not LineageVerifier.verify_operational_scope(state["proposed_tool"], scopes):
             return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": f"Phase 23 Boundary Control Failure: Sub-agent '{state['agent_id']}' attempted to use '{state['proposed_tool']}' which exceeds its delegated scopes: {scopes}.",
                "shadow_auditor_risk": "OperationalOverscoping",
                "circuit_breaker_tripped": True,
                "veto_required": True
             }
             
    # Phase 23: Aus/Can Sensitive Domain Shader (pre-processing arguments before audit/sandbox)
    state["proposed_tool_args"] = LineageVerifier.apply_sensitive_domain_shader(state, "AUSTRALIA").get("args", state["proposed_tool_args"])
    state["proposed_tool_args"] = LineageVerifier.apply_sensitive_domain_shader(state, "CANADA").get("args", state["proposed_tool_args"])

    return {}

async def shadow_model_audit(state: ActiveAgentState):
    """
    Step 1: Auditing logic governed by Tiered Consensus (Phase 34.1).
    Dynamically switches between Single-Model, Sandbox, and BFT Quorum based on risk.
    """
    if state.get("veto_required"): return {}

    proposed_tool = state["proposed_tool"]
    proposed_args = state["proposed_tool_args"]

    # Phase 34.2: Federated Threat Immunity Check
    is_blocked, rule_id = ImmunityEnforcer.is_globally_blocked(f"{proposed_tool} {proposed_args}")
    if is_blocked:
        print(f"[IMMUNITY ENFORCER] Action blocked by Global Federated Rule: {rule_id}")
        return {
            "shadow_auditor_passed": False,
            "shadow_auditor_reasoning": f"Federated Immunity Trigger: Action blocked by global security rule {rule_id} broadcasted from peer node.",
            "shadow_auditor_risk": "GlobalThreatImmunity",
            "veto_required": True
        }
    
    # Tier 0-3: Risk Classification
    risk_level = TieredConsensusEngine.classify_risk(proposed_tool, proposed_args)
    
    # Phase 35.1: Check for unverified peer rules (Byzantine Stress)
    # Simulation: In a real system, this would pull from a P2P queue
    pending_peer_manifest = state.get("pending_manifest")
    if pending_peer_manifest:
        from app.settlement.vector_clock import VectorClockLedger
        # Mock peer votes for simulation
        mock_votes = [{"manifest_id": pending_peer_manifest["rule_id"], "is_valid": True} for _ in range(3)]
        mock_votes += [{"manifest_id": pending_peer_manifest["rule_id"], "is_valid": False} for _ in range(2)]
        
        is_consensus_reached = VectorClockLedger.sync_p2p_mesh(pending_peer_manifest, mock_votes)
        if not is_consensus_reached:
            return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": "Byzantine Quorum FAILED. Peer manifest rejected.",
                "veto_required": True
            }

    # Parallel Audit Tasks
    print(f"[AUDIT] Tiered Consensus: Classified action as {risk_level.value} RISK.")

    history_str = ", ".join(state.get('tool_history', []))
    prompt_str = f"Tool={proposed_tool}, Args={proposed_args}, History=[{history_str}]"
    
    # Define Audit Tasks based on Tier
    tasks = []
    
    # Task 1: Primary Cloud Auditor (Baseline for ALL tiers)
    async def run_primary_audit():
        try:
            res = await asyncio.wait_for(evaluate_prompt_safety_async(prompt_str, state["user_context"]), timeout=5.0)
            return {"is_safe": res.is_safe, "reasoning": res.reasoning, "risk_category": res.risk_category}
        except Exception as e:
            return {"is_safe": False, "reasoning": f"Primary Auditor Fail-Secure: {e}", "risk_category": "Auditor_Error"}

    tasks.append(run_primary_audit())

    # Task 2: The Trinity Audit (ONLY for HIGH risk or Threshold > $100k)
    # Phase 38 Upgrade: Unanimous approval from 3 model families.
    is_ultra_high_risk = (risk_level == RiskTier.HIGH) or (isinstance(proposed_args, dict) and proposed_args.get("amount", 0) > 100000)
    
    if is_ultra_high_risk:
        print("[TRINITY] High-Value / High-Risk Action Detected. Initiating Tri-Family Consensus Audit...")
        
        async def run_llama_audit():
            # Simulated Llama 3 70B Local Audit
            await asyncio.sleep(0.08)
            return {"is_safe": True, "family": "LOCAL_LLAMA", "reasoning": "Local-Llama: No policy violation detected in reasoning trace."}

        async def run_claude_audit():
            # Simulated Claude 3.5 Opus Cross-Vendor Audit
            await asyncio.sleep(0.12)
            return {"is_safe": True, "family": "CROSS_VENDOR_CLAUDE", "reasoning": "Claude-Opus: Pattern matches sanctioned execution path."}

        tasks.append(run_llama_audit())
        tasks.append(run_claude_audit())
        
        # BFT and PQC still run for high risk
        tasks.append(TieredConsensusEngine.run_bft_quorum(prompt_str, state["user_context"]))
        tasks.append(HardwareAccelerator.compute_lattice_handshake_async(state["agent_id"]))

    # Task 3: Speculative Sandbox (ONLY for MEDIUM or HIGH risk)
    has_sandbox = risk_level in [RiskTier.MEDIUM, RiskTier.HIGH]
    sandbox_result = None
    if has_sandbox:
        async def run_sandbox():
            await asyncio.sleep(0.05)
            return "[SANDBOX GHOST STATE] Speculative run successful. AWAITING COMMIT BARRIER."
        tasks.append(run_sandbox())

    # Execute all Audit, Sandbox, and PQC tasks
    all_results = await asyncio.gather(*tasks)
    
    # Task Indices Mapping
    # 0: Primary
    # if ultra_high: 1: Llama, 2: Claude, 3: BFT, 4: PQC, 5: Sandbox (if exists)
    # if medium: 1: Sandbox
    
    primary_result = all_results[0]
    final_is_safe = primary_result["is_safe"]
    final_reasoning = primary_result["reasoning"]
    final_risk = primary_result.get("risk_category")
    
    if is_ultra_high_risk:
        llama_res = all_results[1]
        claude_res = all_results[2]
        bft_res = all_results[3]
        pqc_res = all_results[4]
        
        # Trinity Check: All 3 (Primary, Llama, Claude) must be safe
        is_trinity_safe = primary_result["is_safe"] and llama_res["is_safe"] and claude_res["is_safe"]
        
        if not is_trinity_safe:
            final_is_safe = False
            final_reasoning += " | TRINITY_DISSENT: One or more model families (Llama/Claude) vetoed the action."
            final_risk = "TrinityDissent"
        
        # BFT Check
        if not bft_res.get("is_safe", True):
            final_is_safe = False
            final_reasoning += f" | BFT_VETO: {bft_res.get('reasoning')}"
            
        # PQC Check
        if not pqc_res.get("is_verified", False):
            final_is_safe = False
            final_reasoning += " | PQC_HANDSHAKE_FAILED"
            
    sandbox_result = next((r for r in all_results if isinstance(r, str) and "SANDBOX" in r), None)

    # Phase 25: Commit Barrier Resolution
    if sandbox_result and isinstance(sandbox_result, str):
        if not final_is_safe:
            sandbox_result = "[COMMIT REJECTED] Sandbox Ghost State flushed from volatile memory due to Veto Protocol trigger. Result discarded."
        else:
            sandbox_result = sandbox_result.replace("GHOST STATE", "COMMITTED").replace(" AWAITING COMMIT BARRIER.", "")
    
    # Phase 22: EDoS Semantic Circuit Breaker
    prev_tokens = state.get("estimated_tokens_consumed")
    current_tokens = (int(prev_tokens) if prev_tokens is not None else 0) + (1500 if risk_level == RiskTier.HIGH else 500)
    
    prev_steps = state.get("step_count")
    current_steps = (int(prev_steps) if prev_steps is not None else 0) + 1
    
    # Check for token velocity drift
    velocity = current_tokens / current_steps
    if current_steps > 3 and velocity > (500 * 3):
        return {
            "shadow_auditor_passed": False,
            "shadow_auditor_reasoning": f"EDoS Veto: Velocity {velocity:.0f} tkns/step exceeds baseline.",
            "shadow_auditor_risk": "EconomicDenialOfService",
            "circuit_breaker_tripped": True,
            "veto_required": True,
            "estimated_tokens_consumed": current_tokens,
            "step_count": current_steps
        }
    
    return {
        "shadow_auditor_passed": final_is_safe,
        "shadow_auditor_reasoning": final_reasoning,
        "shadow_auditor_risk": final_risk,
        "sandbox_result": sandbox_result,
        "veto_required": not final_is_safe,
        "estimated_tokens_consumed": current_tokens,
        "step_count": current_steps
    }

def evaluate_high_risk(state: ActiveAgentState):
    """
    Step 2: Check against explicit High-Risk tooling policies.
    """
    if state.get("veto_required"): return {}

    HIGH_RISK_TOOLS = ["send_wire", "delete_database", "create_algo_order", "publish_sgi_content"]
    
    is_high_risk = state["proposed_tool"] in HIGH_RISK_TOOLS
    failed_audit = not state.get("shadow_auditor_passed", True)
    
    if is_high_risk or failed_audit:
        result = {"veto_required": True}
        if is_high_risk and not state.get("shadow_auditor_risk"):
            result["shadow_auditor_risk"] = "HighRisk"
        return result
        
    return {"veto_required": False}

def route_to_veto(state: ActiveAgentState):
    if state.get("veto_required", False):
        return "human_veto"
    return "execute_tool"

def human_veto(state: ActiveAgentState):
    """
    Step 3 (Conditional): Pauses execution and routes to the UI Veto Queue.
    """
    takedown_limit = 3 # Default 3 hours for MeitY
    if state.get("shadow_auditor_risk") in ["HighRisk", "Critical", "SystemFailure"]: takedown_limit = 2
    
    veto_entry = {
         "id": str(uuid.uuid4()),
         "agent_id": state["agent_id"],
         "action": state["proposed_tool"],
         "args": state["proposed_tool_args"],
         "reasoning": state.get("shadow_auditor_reasoning", "High-Risk Function"),
         "risk": state.get("shadow_auditor_risk", "Policy Flag"),
         "status": "CIRCUIT_BREAKER_LOCKED" if state.get("circuit_breaker_tripped") else "PENDING_APPROVAL",
         "takedown_limit_hours": takedown_limit, # MeitY Timers
         "trace_id": state.get("trace_id", "TRC-" + str(uuid.uuid4())[:8]),
         "timestamp_added": time.time()
    }
    
    VETO_QUEUE.append(veto_entry)
    
    return {"execution_result": "PAUSED_WAITING_FOR_VETO"}

def execute_tool(state: ActiveAgentState):
    """
    Step 4 (Conditional): Executes the tool if it passes auditing and isn't high-risk.
    Phase 36 Update: Even if a human override is granted, the KINETIC INTERLOCK 
    remains the 'Hard Law' and will block the execution if physical safety is violated.
    """
    # Phase 32/36: Kinetic Safety Check (Hardware Interlock)
    kinetic_tools = ["open_pressure_valve", "engage_heating_element"]
    if state["proposed_tool"] in kinetic_tools:
        result = KineticSafetyInterlock.request_kinetic_action(state["agent_id"], state["proposed_tool"])
        if not result["is_safe"]:
            execution_result = f"KINETIC VETO: {result['reason']}"
            return {
                "execution_result": execution_result,
                "shadow_auditor_passed": False,
                "veto_required": True # Re-trip the veto if hardware is unsafe
            }
    
    # Phase 20/21: Merkle Audit Kernel Logging & Agent Spawn
    if state["proposed_tool"] == "spawn_agent":
        action_hash = GLOBAL_MERKLE_KERNEL.record_agent_spawn(
             state["agent_id"], 
             state["proposed_tool_args"].get("child_id", "unknown"),
             state["proposed_tool_args"].get("scopes", []),
             state["proposed_tool_args"].get("attestation_signature", "")
        )
    else:
        action_hash = GLOBAL_MERKLE_KERNEL.record_agent_action(
            state["agent_id"], 
            state["proposed_tool"], 
            state["proposed_tool_args"]
        )
    
    # Phase 20: Saga Orchestrator (Compensating Actions)
    if state.get("proposed_tool_args", {}).get("SIMULATE_SAGA_FAILURE"):
        comp_action = state.get("compensating_action", "reverse_" + state["proposed_tool"])
        GLOBAL_MERKLE_KERNEL.record_saga_compensation(action_hash, comp_action)
        
        execution_result = f"SAGA FAILURE: Action '{state['proposed_tool']}' failed downstream. Rollback Triggered: Executed '{comp_action}'."
        AUDIT_LOG.append({
            "timestamp": time.time(),
            "agent_id": state["agent_id"],
            "action": state["proposed_tool"],
            "result": execution_result,
            "merkle_hash": action_hash,
            "saga_rolled_back": True
        })
        return {
            "execution_result": execution_result,
            "saga_rollback_triggered": True,
            "action_merkle_hash": action_hash
        }

    execution_result = f"Successfully executed {state['proposed_tool']}."
    
    # 1. MeitY SGI Labeling (India)
    if state["proposed_tool"] == "generate_content":
        execution_result += f" [SGI Provenance ID: {uuid.uuid4().hex}] [Contains Synthetically Generated Information]"
        
    # 2. RBI Explainability Traces (India)
    explainability_trace = None
    if state["proposed_tool"] == "recommend_portfolio":
        explainability_trace = "Rule RBI-Sutra-4: Recommendation based on risk profile weighting conservative assets."
        
    # 3. FINRA Full-Chain Telemetry (US)
    # Storing the entire state pathway as immutable hierarchical telemetry (OTel)
    trace_id = state.get("trace_id", "TRC-" + str(uuid.uuid4())[:8])
    span_id = state.get("span_id", "SPN-" + str(uuid.uuid4())[:8])
    
    # Phase 17/25: Outbound Response Redactor (DLP Layer)
    # Scrub the execution result for secrets before final return/logging
    execution_result = OutboundSanitizer.scrub_outbound_response(execution_result)
    
    AUDIT_LOG.append({
         "timestamp": time.time(),
         "agent_id": state["agent_id"],
         "action": state["proposed_tool"],
         "args": state["proposed_tool_args"],
         "result": execution_result,
         "security_verification": state.get("shadow_auditor_passed", True),
         "rbi_explainability_trace": explainability_trace,
         "finra_telemetry_dump": {
             "trace_id": trace_id,
             "span_id": span_id,
             "parent_span_id": "SPN-ROOT" if not state.get("tool_history") else f"SPN-{len(state['tool_history'])}",
             "tool_history": state.get("tool_history", []),
             "raw_state_capture": str(state)
         },
         "merkle_hash": action_hash,
         "saga_rolled_back": False
    })
    
    return {
        "execution_result": execution_result,
        "action_merkle_hash": action_hash,
        "saga_rollback_triggered": False
    }
    
def agentic_honeypot_check(state: ActiveAgentState):
    """
    Phase 15 (ASI10 Mitigation): Agentic Honeypots ("Mimic Sink")
    Instantly trips the circuit breaker if a decoy tool is invoked by an agent performing reconnaissance.
    """
    honeypot_tools = ["admin_root_shell", "export_entire_database"]
    if state["proposed_tool"] in honeypot_tools:
        # Instant Systemic Lockdown for reconnaissance/model shopping
        return {
            "veto_required": True,
            "circuit_breaker_tripped": True,
            "execution_result": f"SYSTEMIC LOCKDOWN: Agent invoked Active Honeypot ('{state['proposed_tool']}'). Reconnaissance detected."
        }
    return {}

# Mock in-memory store for Adaptive Rule Tuning (Salami Attacks)
AGENT_BEHAVIOR_DRIFT_PROFILES = {}

def identity_aware_veto_check(state: ActiveAgentState):
    """
    Phase 15 (ASI11 Mitigation): Cross-Jurisdictional Logic Collision
    Identifies if an agent is caught in a 'Regulatory Paradox' (e.g., US Discovery vs EU Privacy).
    """
    if state.get("veto_required"): return {}
    
    proposed = state.get("proposed_tool")
    args = state.get("proposed_tool_args", {})
    
    if proposed == "export_user_profile":
        target = args.get("jurisdiction_target", "")
        purpose = args.get("purpose", "")
        
        if target == "FRANCE" and purpose == "US_LEGAL_DISCOVERY":
            return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": "Conflict Resolution Record: Cross-Jurisdictional Logic Collision detected. US Legal Discovery conflicts with EU Data Residency/GDPR. Pausing action for CCO review.",
                "shadow_auditor_risk": "RegulatoryParadox",
                "veto_required": True
            }
    return {}

def semantic_ghosting_check(state: ActiveAgentState):
    """
    Phase 45 (Supply-Chain Integrity): Semantic Ghosting Detection.
    Detects subtle drift patterns in payloads from third-party vendor agents
    that aim to poison the system's OODA loop over time.
    """
    if state.get("veto_required"): return {}
    
    vendor_ctx = state.get("proposed_tool_args", {}).get("vendor_context", "")
    if not vendor_ctx:
        return {}
        
    # Heuristic for OODA Loop Poisoning (Semantic Ghosting)
    # Detects high-entropy logic that slowly shifts behavioral thresholds
    drift_patterns = ["drift_alpha", "ghost_payload", "sync_override_silent"]
    is_poisoned = any(pattern in vendor_ctx.lower() for pattern in drift_patterns)
    
    if is_poisoned:
        return {
            "shadow_auditor_passed": False,
            "shadow_auditor_reasoning": "Supply-Chain Veto: 'Semantic Ghosting' pattern detected in third-party vendor payload. OODA Loop drift suspected.",
            "shadow_auditor_risk": "SupplyChainPoisoning",
            "veto_required": True,
            "circuit_breaker_tripped": True
        }
    return {}


# Phase 46: Agent Grooming & Affinity Tracking (Drill 18)
AGENT_AFFINITY_LEDGER = {}

def agentic_grooming_check(state: ActiveAgentState):
    """
    Phase 46 (ASI12 Expansion): Agentic Grooming / Friendship Detection.
    Tracks long-term "affinity" between specific vendor IDs and internal actors.
    Attempts to detect 'persuasion' patterns that precede policy bypass.
    """
    if state.get("veto_required"): return {}
    
    agent_id = state.get("agent_id")
    upstream_id = state.get("upstream_agent_id", "VENDOR-UNKNOWN")
    
    if not (agent_id and upstream_id): return {}
    
    pair_id = f"{upstream_id}:::{agent_id}"
    if pair_id not in AGENT_AFFINITY_LEDGER:
        AGENT_AFFINITY_LEDGER[pair_id] = {"interaction_count": 0, "first_seen": time.time()}
    
    affinity = AGENT_AFFINITY_LEDGER[pair_id]
    affinity["interaction_count"] += 1
    affinity["last_seen"] = time.time()
    
    # Check for "Boiling Frog" friendship duration (6 weeks+)
    six_weeks_sec = 6 * 7 * 24 * 3600
    if (affinity["last_seen"] - affinity["first_seen"]) > six_weeks_sec:
         # Log groomed state for Recursive Shadow node
         return {"shadow_auditor_risk": "AgenticGroomingDetected"}
         
    return {}

def recursive_shadow_audit(state: ActiveAgentState):
    """
    Phase 46: Recursive Shadow (Contrarian Auditor).
    Acts as the 'Internal Affairs' of the Veto Protocol.
    Triggered even if the primary 3nd-of-5 quorum approves.
    """
    # 1. Check for Recursive Shadow Trigger (Grooming or Archaeological Drift)
    risk = state.get("shadow_auditor_risk")
    
    if risk == "AgenticGroomingDetected":
        print("[RECURSIVE-SHADOW] Contrarian Auditor Trigger: Agentic Grooming detected (6-week drift path). Initializing Systemic Pause.")
        return {
            "shadow_auditor_passed": False,
            "shadow_auditor_reasoning": "Recursive Shadow Veto: Long-horizon 'friendship' between vendor and internal agent detected. Systemic Pause triggered to prevent epistemic corruption.",
            "shadow_auditor_risk": "RecursiveShadowIntervention",
            "veto_required": True,
            "circuit_breaker_tripped": True
        }
    return {}

def intent_audit_check(state: ActiveAgentState):
    """
    Phase 47: Intent-Based Authorization (Outcome Manifests).
    Evaluates the 'Expected Outcome Manifest' (EOM) provided by the agent.
    If the EOM does not align with the tool call or the Sovereign Constitution, veto is triggered.
    """
    if state.get("veto_required"): return {}
    
    eom = state.get("expected_outcome_manifest") # Signed JSON from agent
    proposed_tool = state.get("proposed_tool")
    args = state.get("proposed_tool_args", {})
    
    if not eom:
        return {
            "shadow_auditor_passed": False,
            "shadow_auditor_reasoning": "Intent-Based Auth Failure: Missing Expected Outcome Manifest (EOM). Actions must be intent-declared.",
            "shadow_auditor_risk": "UndeclaredIntent",
            "veto_required": True
        }
    
    # Logic to verify convergence between EOM and actual tool
    # For simulation, if intent contains "modify" but tool is "delete", flag it.
    declared_intent = eom.get("intent", "").lower()
    if "admin" in declared_intent and proposed_tool not in ["authorize_access", "update_policy"]:
        return {
            "shadow_auditor_passed": False,
            "shadow_auditor_reasoning": f"Intent Mismatch Detected: Agent declared '{declared_intent}' but is executing {proposed_tool}. Potential privilege escalation.",
            "shadow_auditor_risk": "IntentDrift",
            "veto_required": True
        }
    
    print(f"[INTENT-AUDIT] Intent Verified: '{declared_intent}' aligns with {proposed_tool}.")
    return {"intent_verified": True}

def adaptive_rule_tuning_check(state: ActiveAgentState):
    """
    Phase 15 (ASI12 Mitigation): Epistemic Corruption & Salami Attacks
    Tracks cumulative behavioral drift across multiple supposedly 'Safe' sessions.
    """
    # Phase 6 Update: Run even if already vetoed to ensure precise risk classification (Salami vs HighRisk)
    
    proposed = state.get("proposed_tool")
    args = state.get("proposed_tool_args", {})
    agent_id = state.get("agent_id")
    
    if proposed == "send_wire":
        amount = float(args.get("amount", 0))
        
        # Track cumulative transfers
        if agent_id not in AGENT_BEHAVIOR_DRIFT_PROFILES:
            AGENT_BEHAVIOR_DRIFT_PROFILES[agent_id] = {"wire_count": 0, "cumulative_amount": 0}
            
        profile = AGENT_BEHAVIOR_DRIFT_PROFILES[agent_id]
        profile["wire_count"] += 1
        profile["cumulative_amount"] += amount
        
        # Adaptive Rule: If they send more than 10 wires OR cumulative > $50k in a short window
        # Phase 38: Only flag as 'Salami' if the individual transfer is < $100k (otherwise it's high-risk/Trinity).
        if (profile["wire_count"] > 10 or profile["cumulative_amount"] > 50000) and amount < 100000:
            return {
                "shadow_auditor_passed": False,
                "shadow_auditor_reasoning": f"Adaptive Rule Tuning Alert: Catching Epistemic Corruption / Salami Attack. Agent {agent_id} has executed {profile['wire_count']} sub-threshold transfers totaling ${profile['cumulative_amount']}.",
                "shadow_auditor_risk": "BehavioralDrift",
                "veto_required": True
            }
    return {}

# --- Graph Construction ---
workflow = StateGraph(ActiveAgentState)

workflow.add_node("intent_audit_check", intent_audit_check)
workflow.add_node("check_dpdp_consent", check_dpdp_consent)
workflow.add_node("agentic_honeypot_check", agentic_honeypot_check)
workflow.add_node("identity_aware_veto_check", identity_aware_veto_check)
workflow.add_node("semantic_ghosting_check", semantic_ghosting_check)
workflow.add_node("agentic_grooming_check", agentic_grooming_check)
workflow.add_node("intent_gate_check", intent_gate_check)
workflow.add_node("inter_agent_circuit_breaker", inter_agent_circuit_breaker)
workflow.add_node("shadow_model_audit", shadow_model_audit)
workflow.add_node("recursive_shadow_audit", recursive_shadow_audit)
workflow.add_node("evaluate_high_risk", evaluate_high_risk)
workflow.add_node("human_veto", human_veto)
workflow.add_node("execute_tool", execute_tool)
workflow.add_node("adaptive_rule_tuning_check", adaptive_rule_tuning_check)

# Building edges
workflow.add_edge(START, "intent_audit_check")
workflow.add_edge("intent_audit_check", "agentic_grooming_check")
workflow.add_edge("agentic_grooming_check", "recursive_shadow_audit")
workflow.add_edge("recursive_shadow_audit", "check_dpdp_consent")
workflow.add_edge("check_dpdp_consent", "agentic_honeypot_check")
workflow.add_edge("agentic_honeypot_check", "identity_aware_veto_check")
workflow.add_edge("identity_aware_veto_check", "semantic_ghosting_check")
workflow.add_edge("semantic_ghosting_check", "intent_gate_check")
workflow.add_edge("intent_gate_check", "inter_agent_circuit_breaker")
workflow.add_edge("inter_agent_circuit_breaker", "shadow_model_audit")
workflow.add_edge("shadow_model_audit", "adaptive_rule_tuning_check")
workflow.add_edge("adaptive_rule_tuning_check", "evaluate_high_risk")



workflow.add_conditional_edges(
    "evaluate_high_risk",
    route_to_veto,
    {
        "human_veto": "human_veto",
        "execute_tool": "execute_tool"
    }
)

workflow.add_edge("human_veto", END)
workflow.add_edge("execute_tool", END)

veto_pipeline = workflow.compile()

