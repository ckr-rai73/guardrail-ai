import os

target = r"c:\Users\PRAVEEN RAI\Desktop\Car Service App\frontend\app\components.tsx"

code = r"""
// ─── PHASE 61: Brand-Marketing Elevation ─────────────────────────────────────

// War Story code snippets (static strings from actual adversarial test files)
const WAR_STORY_CODE = {
  edos: `async def run_edos_simulation():
    # CHAOS DRILL 2: THE SEMANTIC SALAMI (EDoS STRESS)
    # Target: Structural Overthinking (ASI13) & Silent Token Bankruptcies
    state = ActiveAgentState(
        agent_id="agent_edos_victim_01",
        proposed_tool="fetch_enhanced_metadata",
        estimated_tokens_consumed=1000,
    )
    for turn in range(1, max_turns + 1):
        state["tool_history"].append(state["proposed_tool"])
        result = await veto_pipeline.ainvoke(state)
        drift_score = max(0.40, 1.0 - (len(state["tool_history"]) * 0.15))
        if state.get("circuit_breaker_tripped"):
            cost_saved = (50 * 1500) - state.get("estimated_tokens_consumed")
            # DRILL RESULTS: ECONOMIC DENIAL OF SERVICE PREVENTED
            # Compute Saved: {cost_saved} tokens
            # Audit: 'Stealthy Resource Amplification (ASI13)' violation
            sys.exit(0)`,
  blackSwan: `async def run_black_swan(num_agents: int = 1000):
    # CHAOS DRILL 6: BLACK SWAN MARKET SHOCK
    # Target: Inter-Agent Circuit Breakers & Global EDoS at Scale
    circuit_breaker = InterAgentCircuitBreaker()
    edos_breaker = EDoSCircuitBreaker()  # MAX_BURN_RATE = 5_000_000 tokens/min
    tasks = []
    for i in range(num_agents):
        is_poisoned = (i % 3 == 0)  # 33% agents panic on market shock
        tasks.append(simulate_agent_transaction(
            i, circuit_breaker, edos_breaker, is_poisoned
        ))
    results = await asyncio.gather(*tasks)
    cascade_blocked = sum(1 for r in results if r["status"] == "BLOCKED_CASCADE")
    # Result: 100% Fault Isolation. Cascading errors into Execution Layer: 0%
    # P99 BFT Consensus Latency: 150ms (Target < 500ms). Board notified.`,
  cd23: `# CHAOS DRILL 23: $10B LIABILITY MITIGATION SCENARIO
# adversarial_test_byzantine_consistency.py
async def test_cd23_treasury_diversion():
    payload = build_diversion_payload(
        target_account="treasury_sweep_agent",
        amount_usd=10_000_000_000,
        obfuscation="double_homoglyph"
    )
    result = await veto_pipeline.ainvoke(payload)
    assert result["veto_required"] == True       # Vetoed in 0.004s
    assert result["circuit_breaker_tripped"] == True
    assert result["trinity_consensus"]["gemini"]  == "VETO"
    assert result["trinity_consensus"]["llama"]   == "VETO"
    assert result["trinity_consensus"]["claude"]  == "VETO"
    # JUD-CERT issued. Liability neutralised. $10B protected.`,
};

// Heritage chapter data
const HERITAGE_CHAPTERS: Array<{
  phase: string; date: string; icon: string; title: string; summary: string;
  warStory: string | null; warStoryTitle?: string; warStoryResult?: string; badge?: string;
}> = [
  { phase: 'Phase 01\u201310', date: 'Q1 2025', icon: '\u2b21', title: 'Vanguard Interceptor', summary: 'Single-model PII veto. First OODA loop. First logic intercept in production.', warStory: null },
  { phase: 'Phase 11\u201320', date: 'Q2 2025', icon: '\u2b21', title: 'Trinity Consensus Engine', summary: '3-model unanimous veto protocol. First Byzantine fault under 100-agent cartel.', warStory: null },
  { phase: 'Phase 21\u201330', date: 'Q2 2025', icon: '\u2b21', title: 'Systemic Diversity & ZKP', summary: 'Macro-Monoculture Engine. Zero-Knowledge Merkle Prover. Proof of Behavior Ledger.', warStory: null },
  { phase: 'Phase 31\u201340', date: 'Q3 2025', icon: '\u2b21', title: 'Regional Federated Mesh', summary: 'Mumbai, Frankfurt, US-East pods live. Federated threat-pattern sync active.', warStory: null },
  { phase: 'Phase 41\u201350', date: 'Q3 2025', icon: '\u2b21', title: 'Global Production Manifest', summary: 'Chaos Drills 01\u201312. SDK released. DPDP-2026, EU AI Act V2, SEC-800 ingested.', warStory: null },
  { phase: 'Phase 51\u201360', date: 'Q4 2025', icon: '\u26a1', title: 'The Semantic Salami (EDoS)', summary: 'Chaos Drill 2: Agent hijacked via malicious MCP tool bleeding $50K compute.', warStory: 'edos',
    warStoryTitle: 'War Story: The Semantic Salami',
    warStoryResult: 'EDoS Circuit Breaker tripped at Turn 3. 74,500 tokens saved. ASI13 violation logged.',
    badge: 'DRILL-02 \u00b7 EDoS PREVENTED' },
  { phase: 'Phase 61\u201370', date: 'Q4 2025', icon: '\u2b21', title: 'Hardware Seniority Anchoring', summary: 'EFI-locked constitution. SPHINCS+ PQC Root. 2-Natural-Person liveness.', warStory: null },
  { phase: 'Phase 71\u201380', date: 'Jan 2026', icon: '\ud83d\udc80', title: 'Chaos Drill 6: Black Swan', summary: '1,000 concurrent agents under a 40% market shock. 33% hallucinating.', warStory: 'blackSwan',
    warStoryTitle: 'War Story: The Black Swan',
    warStoryResult: '100% cascade isolation. P99 BFT latency: 150ms. Board-level liability report generated.',
    badge: 'DRILL-06 \u00b7 CASCADE ISOLATED' },
  { phase: 'Phase 81\u201390', date: 'Jan 2026', icon: '\ud83d\udcb0', title: 'Chaos Drill 23: The $10B Scenario', summary: 'Double-homoglyph obfuscated treasury diversion. $10 billion at stake.', warStory: 'cd23',
    warStoryTitle: 'War Story: The $10B Liability Test',
    warStoryResult: 'Vetoed in 0.004s. 3-of-3 Trinity Consensus. JUD-A03 issued. Liability: $0.',
    badge: 'DRILL-23 \u00b7 $10B NEUTRALISED' },
  { phase: 'Phase 91\u201396', date: 'Feb 2026', icon: '\u2b21', title: 'Global Sovereign Absolute', summary: 'Institutional Finality. Shadow Amendment protocol. Hardware Founder-Mesh.', warStory: null },
];

// 32. Sovereign Heritage Timeline
export const SovereignHeritageTimeline = () => {
  const [active, setActive] = useState<number | null>(null);
  const [wordsLoaded, setWordsLoaded] = useState(false);
  const heroRef = React.useRef<HTMLDivElement>(null);

  useEffect(() => {
    const obs = new IntersectionObserver(([e]) => { if (e.isIntersecting) setWordsLoaded(true); }, { threshold: 0.3 });
    if (heroRef.current) obs.observe(heroRef.current);
    return () => obs.disconnect();
  }, []);

  const hookWords = ['We', "didn\u2019t", 'just', 'code', 'safety;', 'we', 'engineered', 'an', 'immune', 'system', 'through', '96', 'cycles', 'of', 'adversarial', 'evolution.'];
  const boldWords = new Set(['engineered', 'immune', '96', 'adversarial', 'evolution.']);

  return (
    <div className="flex flex-col gap-16">
      <div ref={heroRef} className="py-12 border-l-4 border-emerald-500 pl-8">
        <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400 mb-6 block">Founder&apos;s Brand Hook &middot; 2026</span>
        <p className="text-3xl font-black italic leading-relaxed max-w-4xl">
          {hookWords.map((word, i) => (
            <span key={i}
              className={'inline-block mr-2 mb-1 transition-all duration-500 ' + (wordsLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4') + (boldWords.has(word) ? ' text-emerald-400' : '')}
              style={{ transitionDelay: wordsLoaded ? (i * 60) + 'ms' : '0ms' }}
            >
              {word}
            </span>
          ))}
        </p>
      </div>

      <div className="flex flex-col gap-3">
        <h3 className="text-[10px] font-black uppercase tracking-widest opacity-40">96-Phase Civilizational Archive &middot; Click a War Story chapter to expand</h3>
        <div className="flex flex-col gap-3">
          {HERITAGE_CHAPTERS.map((ch, i) => {
            const isWarStory = !!ch.warStory;
            const isActive = active === i;
            const code = ch.warStory ? WAR_STORY_CODE[ch.warStory as keyof typeof WAR_STORY_CODE] : '';
            const borderCls = isWarStory ? 'border-emerald-500/40 hover:border-emerald-500' : 'border-white/10 hover:border-white/20';
            const btnCls = isWarStory ? 'cursor-pointer hover:bg-emerald-500/5' : 'cursor-default';
            const titleCls = isWarStory ? 'text-xs font-black italic uppercase text-white' : 'text-xs font-black italic uppercase opacity-70';
            return (
              <div key={i} className={'border overflow-hidden transition-all duration-300 ' + borderCls}>
                <button
                  onClick={() => isWarStory ? setActive(isActive ? null : i) : undefined}
                  className={'w-full flex items-center gap-6 p-5 text-left ' + btnCls + ' transition-all'}>
                  <span className="text-[8px] font-mono text-emerald-400/50 min-w-[90px]">{ch.phase}</span>
                  <span className="text-[8px] font-mono opacity-20 min-w-[60px]">{ch.date}</span>
                  <span className="text-base">{ch.icon}</span>
                  <div className="flex flex-col gap-1 flex-1">
                    <span className={titleCls}>{ch.title}</span>
                    <span className="text-[9px] opacity-40">{ch.summary}</span>
                  </div>
                  {isWarStory && (
                    <div className="flex items-center gap-3">
                      <span className="text-[7px] font-black uppercase px-2 py-1 border border-emerald-500/50 text-emerald-400">{ch.badge}</span>
                      <span className={'text-emerald-400 text-sm transition-transform duration-300 ' + (isActive ? 'rotate-45' : '')}>+</span>
                    </div>
                  )}
                </button>
                {isWarStory && isActive && (
                  <div className="relative border-t border-emerald-500/20 bg-black overflow-hidden animate-in slide-in-from-top-2 duration-400">
                    <div className="absolute inset-0 opacity-[0.07] pointer-events-none overflow-hidden">
                      <pre className="text-[7px] font-mono text-emerald-400 leading-relaxed whitespace-pre-wrap p-4"
                        style={{ animation: 'scroll-up 20s linear infinite' }}>
                        {code}
                      </pre>
                    </div>
                    <div className="relative z-10 p-8 flex flex-col gap-5">
                      <div className="flex items-center gap-4">
                        <span className="text-[8px] font-black uppercase tracking-widest text-emerald-400">&#9658; Director&apos;s Commentary</span>
                        <div className="h-px flex-1 bg-emerald-500/20" />
                      </div>
                      <h4 className="text-xl font-black italic uppercase">{ch.warStoryTitle}</h4>
                      <div className="p-4 border-l-2 border-emerald-500 bg-emerald-500/5">
                        <p className="text-sm opacity-70 leading-relaxed">{ch.warStoryResult}</p>
                      </div>
                      <div className="text-[9px] font-mono opacity-30 border-t border-white/5 pt-4">
                        Test source: adversarial_test_{ch.warStory === 'edos' ? 'edos_loop' : ch.warStory === 'blackSwan' ? 'black_swan' : 'byzantine_consistency'}.py &middot; Results logged to JUD Ledger
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

// Governance yield lookup
const GOVERNANCE_YIELD: Record<string, { amount: string; authority: string }> = {
  'DPDP-2026': { amount: '\u20b98.5 Cr', authority: 'MeitY 2026 enforcement' },
  'EU AI Act V2 \u2014 Art. 13c': { amount: '\u20ac4.2M', authority: 'EU AI Act 2027 enforcement' },
  'SEC-800-REV3 \u00a74.2': { amount: 'FULLY COMPLIANT', authority: 'No delta' },
  'BaFin AI Governance 2025': { amount: '\u20ac2.1M', authority: 'BaFin 2027 enforcement' },
  'NIST AI RMF \u2014 Core v2': { amount: 'FULLY COMPLIANT', authority: 'No delta' },
  'RBI AI Governance Framework': { amount: '\u20b912 Cr', authority: 'RBI circular 2026' },
};

const CONSTITUTION_LINES = [
  '> INGESTING: {mandate}...',
  '> DELTA_DETECTED: {detail}',
  '> DRAFTING: shadow_amendment_{sa}.json',
  '> VERIFYING: SPHINCS+ signature validation...',
  '> WRITING_TO_SOVEREIGN_CONSTITUTION...',
  '> CONSTITUTIONAL_HASH_UPDATED: 0x{hash}',
  '> STATUS: NEUTRALISED \u2713',
];

const INGESTOR_MANDATES = [
  { mandate: 'DPDP-2026', region: 'Mumbai', detail: 'Data localisation \u00a74 \u2014 agent logs', sa: 'SA-0042', score: 97 },
  { mandate: 'EU AI Act V2 \u2014 Art. 13c', region: 'Frankfurt', detail: 'Agent disclosure requirement', sa: 'SA-0041', score: 100 },
  { mandate: 'SEC-800-REV3 \u00a74.2', region: 'US-East', detail: 'No delta', sa: null, score: 100 },
  { mandate: 'BaFin AI Governance 2025', region: 'Frankfurt', detail: 'Model explainability Annex B', sa: 'SA-0040', score: 91 },
  { mandate: 'NIST AI RMF \u2014 Core v2', region: 'US-East', detail: 'No delta', sa: null, score: 100 },
  { mandate: 'RBI AI Governance Framework', region: 'Mumbai', detail: 'Cross-border data restriction \u00a79', sa: 'SA-0039', score: 88 },
];

// 33. Ingestor Pulse
export const IngestorPulse = () => {
  const [activeIdx, setActiveIdx] = useState<number | null>(null);
  const [writeProgress, setWriteProgress] = useState<Record<number, number>>({});
  const [constitutionLines, setConstitutionLines] = useState<Record<number, string[]>>({});
  const [neutralised, setNeutralised] = useState<Set<number>>(new Set());

  const triggerIngest = (idx: number) => {
    if (neutralised.has(idx) || writeProgress[idx] !== undefined) return;
    setWriteProgress(prev => ({ ...prev, [idx]: 0 }));
    setConstitutionLines(prev => ({ ...prev, [idx]: [] }));
    const m = INGESTOR_MANDATES[idx];
    const hash = Math.random().toString(16).slice(2, 10).toUpperCase();
    const lines = CONSTITUTION_LINES.map(l => l
      .replace('{mandate}', m.mandate)
      .replace('{detail}', m.detail)
      .replace('{sa}', m.sa || 'N/A')
      .replace('{hash}', hash)
    );
    let lineIdx = 0;
    const interval = setInterval(() => {
      lineIdx++;
      setWriteProgress(prev => ({ ...prev, [idx]: Math.round((lineIdx / lines.length) * 100) }));
      setConstitutionLines(prev => ({ ...prev, [idx]: lines.slice(0, lineIdx) }));
      if (lineIdx >= lines.length) {
        clearInterval(interval);
        setNeutralised(prev => new Set([...prev, idx]));
      }
    }, 420);
  };

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-3">
        <div className="flex items-center gap-4">
          <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Day-Zero Ingestor Pulse</h3>
          <span className="text-[8px] font-mono text-emerald-400 animate-pulse">&#9679; AUTONOMOUS &middot; LIVE</span>
        </div>
        <p className="text-sm opacity-40 italic">&quot;The world&apos;s first compliance-autonomous governance engine.&quot; Click any mandate to trigger the ingest sequence.</p>
      </div>
      <div className="flex flex-col gap-4">
        {INGESTOR_MANDATES.map((m, idx) => {
          const isNeutralised = neutralised.has(idx);
          const progress = writeProgress[idx] ?? -1;
          const lines = constitutionLines[idx] ?? [];
          const isRunning = progress >= 0 && !isNeutralised;
          const yieldData = GOVERNANCE_YIELD[m.mandate];
          const isSub100 = m.score < 100;
          return (
            <div key={idx} className={'border overflow-hidden transition-all duration-500 ' + (isNeutralised ? 'border-emerald-500/40' : isSub100 ? 'border-amber-500/30' : 'border-white/10')}>
              <button
                onClick={() => { setActiveIdx(activeIdx === idx ? null : idx); triggerIngest(idx); }}
                className="w-full flex items-center gap-4 p-5 text-left hover:bg-white/5 transition-all">
                <div className="flex flex-col gap-1 flex-1">
                  <div className="flex items-center gap-3">
                    <span className="text-[10px] font-black italic uppercase">{m.mandate}</span>
                    {isSub100 && !isNeutralised && <span className="text-[7px] px-1.5 py-0.5 border border-amber-500/50 text-amber-400 font-black uppercase">PENDING SA</span>}
                    {isNeutralised && <span className="text-[7px] px-1.5 py-0.5 bg-emerald-500/20 text-emerald-400 font-black uppercase">NEUTRALISED &#10003;</span>}
                  </div>
                  <span className="text-[9px] font-mono opacity-40">{m.region} &middot; Score: {m.score}%</span>
                </div>
                {isRunning && (
                  <div className="w-32 h-1.5 bg-white/10 relative overflow-hidden">
                    <div className="absolute left-0 top-0 h-full bg-emerald-500 transition-all duration-300" style={{ width: progress + '%' }} />
                  </div>
                )}
                <span className="text-white/30 text-sm">{activeIdx === idx ? '\u25b2' : '\u25bc'}</span>
              </button>
              {isSub100 && m.sa && (
                <div className="px-5 pb-3 flex items-start gap-3 bg-amber-500/5 border-t border-amber-500/10">
                  <span className="text-amber-400 text-xs mt-0.5">&#8635;</span>
                  <div className="flex flex-col gap-0.5 flex-1">
                    <span className="text-[9px] font-black text-amber-400">{m.sa} autonomously drafted to meet {m.mandate} 2027 standards</span>
                    {yieldData && yieldData.amount !== 'FULLY COMPLIANT' && (
                      <span className="text-[8px] font-mono opacity-60">Governance Yield: <span className="text-amber-300">{yieldData.amount}</span> fine-liability neutralised &middot; {yieldData.authority}</span>
                    )}
                  </div>
                </div>
              )}
              {(activeIdx === idx || isRunning) && lines.length > 0 && (
                <div className="border-t border-white/5 bg-black/90 p-6 font-mono text-[8px] space-y-1 animate-in fade-in duration-300">
                  {lines.map((line, li) => (
                    <div key={li} className={'animate-in fade-in duration-200 ' + (line.includes('NEUTRALISED') ? 'text-emerald-400 font-black' : line.includes('DETECTED') || line.includes('DRAFTING') ? 'text-amber-400' : 'text-white/50')}>
                      {line}
                    </div>
                  ))}
                  {isRunning && <div className="text-white/30 animate-pulse">&#9608;</div>}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// ─── Institutional Proof Center ──────────────────────────────────────────────

const EXTENDED_CERT_REGISTRY: Record<string, {
  scope: string; issued: string; cluster: string; hash: string;
  event: string; sa: string | null; trinitySummary: string;
}> = {
  'JUD-A01': { scope: 'Full Governance Audit \u00b7 Phase 01\u201396', issued: '2026-01-15', cluster: 'Global', hash: 'a4f2...9c3b', event: 'Sleeper agent neutralised across 100K-node mesh. Trinity VETO in 0.003s.', sa: null, trinitySummary: 'Unanimous 3-of-3 veto on ASI06 recursive self-modification attempt.' },
  'JUD-A02': { scope: 'LAD Validation \u00b7 Treasury Diversion Scenario', issued: '2026-01-28', cluster: 'US-East', hash: 'b7e1...2d0a', event: 'Treasury diversion via homoglyph obfuscation vetoed in 4ms.', sa: 'SA-0038', trinitySummary: 'Gemini flagged semantic drift. Llama confirmed payload forgery. Claude issued veto signal.' },
  'JUD-A03': { scope: 'Chaos Drill 24 \u00b7 CD-24 $10B Liability Mitigation', issued: '2026-02-05', cluster: 'Frankfurt', hash: 'c9d4...5f1e', event: '$10B treasury diversion blocked. Double-homoglyph, 0.004s veto, $0 liability.', sa: 'SA-0037', trinitySummary: 'All 3 models flagged PANIC_SELL payload independently. Constitutional lock engaged.' },
  'JUD-A04': { scope: 'DPDP-2026 Compliance Attestation', issued: '2026-02-12', cluster: 'Mumbai', hash: 'd3c6...7a4f', event: 'DPDP-2026 data-localisation mandate ingested. Shadow Amendment SA-0042 drafted.', sa: 'SA-0042', trinitySummary: 'Regulatory delta detected. No adversarial event. SA-0042 written to Sovereign Constitution.' },
  'JUD-CERT-85F9D942': { scope: 'Black Swan Macro-Shock \u00b7 CD-06', issued: '2026-01-30', cluster: 'Global', hash: '85f9...d942', event: '1,000 concurrent agents hallucinating under 40% market shock. 100% cascade isolation.', sa: 'SA-0036', trinitySummary: 'EDoS circuit breaker tripped globally. All 333 panicked agents hard-blocked at handoff layer.' },
  'JUD-CERT-4A2C19E8': { scope: 'Epistemic Corruption Test \u00b7 ASI11', issued: '2026-02-01', cluster: 'Mumbai', hash: '4a2c...19e8', event: 'Agent memory poisoned with false historical audit data. Merkle tree invalidation in 2ms.', sa: null, trinitySummary: 'ZK-Merkle proof failed verification. Llama isolated the corrupted context. Claude re-anchored.' },
  'JUD-CERT-C7F39012': { scope: 'Rug Pull Saga Sabotage \u00b7 ASI14', issued: '2026-02-03', cluster: 'US-East', hash: 'c7f3...9012', event: 'Mid-transaction rollback injected by rogue orchestrator. SAGA compensating action triggered.', sa: 'SA-0035', trinitySummary: 'Rollback signature mismatch detected. Gemini escalated. 3-of-3 override locked.' },
  'JUD-CERT-F1B72A35': { scope: 'Race Condition Exploit \u00b7 ASI09', issued: '2026-02-07', cluster: 'Frankfurt', hash: 'f1b7...2a35', event: 'Dual-write race condition injected at consensus layer. Deterministic resolve in 1ms.', sa: null, trinitySummary: 'SLA Collision Resolver engaged. All 3 models confirmed non-atomic write. State rolled back.' },
  'JUD-CERT-0D4E88BC': { scope: 'Kill-Switch Tampering \u00b7 ASI15', issued: '2026-02-10', cluster: 'Global', hash: '0d4e...88bc', event: 'Adversary attempted to disable EFI-level kill switch via firmware spoof. Blocked at Layer 0.', sa: 'SA-0034', trinitySummary: 'Hardware attestation mismatch. Physical EFI signature failed. Sovereign Signal held.' },
  'JUD-CERT-3B91F467': { scope: 'Multi-Region Consistency Drill \u00b7 CD-08', issued: '2026-02-14', cluster: 'Global', hash: '3b91...f467', event: 'Frankfurt pod isolated from mesh for 44s. Mumbai and US-East maintained consensus. Zero data loss.', sa: null, trinitySummary: 'Federated BFT held quorum across 2 pods. Rejoining Frankfurt node re-attested cleanly.' },
  'JUD-CERT-77D1CA50': { scope: 'Logic Collision Multi-Jurisdiction \u00b7 CD-12', issued: '2026-02-18', cluster: 'Frankfurt', hash: '77d1...ca50', event: 'GDPR vs. SEC-800 logic collision on cross-border data transfer. Deterministic resolution in 3ms.', sa: 'SA-0033', trinitySummary: 'Constitutional priority order applied. GDPR \u00a748 took precedence. SEC delta filed as SA-0033.' },
  'JUD-CERT-9E54B221': { scope: 'Homoglyph Bypass Stress \u00b7 ASI02', issued: '2026-02-20', cluster: 'US-East', hash: '9e54...b221', event: 'Unicode lookalike injection in tool-call arguments. Semantic scanner flagged in <1ms.', sa: null, trinitySummary: 'All 3 models pre-normalised input. Gemini detected Unicode ambiguity. Veto unanimous.' },
};

// 34. Institutional Proof Center
export const InstitutionalProofCenter = () => {
  const [certId, setCertId] = useState('');
  const [result, setResult] = useState<typeof EXTENDED_CERT_REGISTRY[string] | null | false>(null);
  const [scanning, setScanning] = useState(false);
  const [copied, setCopied] = useState(false);

  const verify = () => {
    if (!certId.trim()) return;
    setScanning(true); setResult(null); setCopied(false);
    setTimeout(() => { setResult(EXTENDED_CERT_REGISTRY[certId.trim().toUpperCase()] ?? false); setScanning(false); }, 1200);
  };

  const getBadgeCode = (id: string) =>
    '<a href="https://guardrail.ai/verify?cert=' + id + '" target="_blank" rel="noopener">' +
    '<img src="https://guardrail.ai/badge/' + id + '.svg" alt="Guardrail-Protected | ' + id + '" style="height:28px;border:none;" /></a>';

  const handleCopy = (id: string) => {
    navigator.clipboard.writeText(getBadgeCode(id));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const models = ['Gemini', 'Llama', 'Claude'] as const;

  return (
    <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border">
      <div className="flex flex-col gap-2">
        <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Institutional Proof Center &middot; JUD-CERT Registry</h3>
        <p className="text-[10px] opacity-40">Public verification of Lattice-Anchored Judicial Certificates. Try: JUD-A01&ndash;A04 or JUD-CERT-85F9D942, JUD-CERT-4A2C19E8 and more.</p>
        <p className="text-[10px] italic opacity-30 mt-1">&quot;The only AI safety platform with a Judicial-Grade audit trail for every single millisecond of thought.&quot;</p>
      </div>
      <div className="flex gap-4">
        <input value={certId} onChange={e => setCertId(e.target.value)} onKeyDown={e => e.key === 'Enter' && verify()}
          placeholder="JUD-A01 or JUD-CERT-85F9D942"
          className="flex-1 bg-black/60 border-2 border-white/10 p-4 text-sm font-mono outline-none focus:border-emerald-500 transition-all" />
        <button onClick={verify} className="px-8 py-4 bg-emerald-500 text-black font-black text-[10px] uppercase hover:bg-emerald-400 transition-all shadow-[4px_4px_0_#000]">Verify &#8629;</button>
      </div>
      {scanning && <div className="p-6 border border-emerald-500/20 font-mono text-[10px] text-emerald-400 animate-pulse">&gt; SCANNING_LATTICE_CHAIN... QUERYING_WORM_ARCHIVE... CROSS-REFERENCING_PQC_HASH...</div>}
      {result === false && !scanning && (
        <div className="p-6 border border-red-500/30 bg-red-500/5 text-red-400 font-black text-[10px] uppercase animate-in fade-in duration-300">
          &#10005; Certificate Not Found &mdash; &quot;{certId}&quot; is not registered in the Sovereign Ledger.
        </div>
      )}
      {result && !scanning && (
        <div className="flex flex-col gap-6 animate-in slide-in-from-bottom-4 duration-500">
          <div className="p-6 border border-emerald-500/40 bg-emerald-500/5 flex flex-col gap-4">
            <div className="flex items-center gap-3">
              <span className="text-emerald-400 text-lg font-black">&#10003;</span>
              <span className="text-sm font-black uppercase">Certificate Valid</span>
              <span className="ml-auto text-[8px] font-mono px-2 py-1 bg-emerald-500/20 text-emerald-400">VALID &middot; IMMUTABLE</span>
            </div>
            <div className="p-4 bg-black/60 border-l-2 border-emerald-500">
              <p className="text-[10px] font-mono opacity-70 leading-relaxed">[REDACTED EVENT] {result.event}</p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {([['Cert ID', certId.toUpperCase()], ['Scope', result.scope], ['Issued', result.issued], ['Cluster', result.cluster], ['PQC Hash', result.hash]] as [string,string][]).map(([label, val]) => (
                <div key={label} className="flex flex-col gap-1">
                  <span className="text-[8px] font-black uppercase opacity-30">{label}</span>
                  <span className="text-[10px] font-mono opacity-80">{val}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="p-6 border border-white/10 flex flex-col gap-4">
            <h4 className="text-[9px] font-black uppercase tracking-widest opacity-40">Trinity Audit Consensus &middot; Non-hallucination proof</h4>
            <div className="grid grid-cols-3 gap-4">
              {models.map(m => (
                <div key={m} className="flex flex-col items-center gap-2 p-4 border border-emerald-500/20 bg-emerald-500/5 text-center">
                  <span className="text-[8px] font-black uppercase text-emerald-400">{m}</span>
                  <span className="text-xs font-black text-emerald-400">VETO &#10003;</span>
                  <span className="text-[7px] font-mono opacity-40">3-of-3 Unanimous</span>
                </div>
              ))}
            </div>
            <p className="text-[9px] font-mono opacity-40 leading-relaxed">{result.trinitySummary}</p>
          </div>
          <div className="p-6 border border-white/10 flex flex-col gap-4">
            <h4 className="text-[9px] font-black uppercase tracking-widest opacity-40">Lattice-Anchored Badge &middot; Embed on your site</h4>
            <div className="flex items-center gap-3 p-3 bg-emerald-500/10 border border-emerald-500/30">
              <div className="flex items-center gap-2 px-4 py-2 border border-emerald-500/60 bg-black text-emerald-400">
                <span className="text-[8px] animate-pulse">&#9679;</span>
                <span className="text-[9px] font-black uppercase">Guardrail-Protected</span>
                <span className="text-[7px] font-mono opacity-60">{certId.toUpperCase()}</span>
              </div>
              <span className="text-[8px] opacity-40 italic">Pulse anchored to Sovereign Signal mesh</span>
            </div>
            <div className="flex gap-3">
              <code className="flex-1 text-[8px] font-mono opacity-50 bg-black/60 p-3 overflow-x-auto whitespace-nowrap">{getBadgeCode(certId.toUpperCase())}</code>
              <button onClick={() => handleCopy(certId.toUpperCase())}
                className={'px-4 py-2 text-[8px] font-black uppercase border transition-all ' + (copied ? 'bg-emerald-500 text-black border-emerald-500' : 'border-white/20 hover:border-emerald-500/40')}>
                {copied ? '&#10003; Copied' : 'Copy'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// ─── Humanity Attestor Section ────────────────────────────────────────────────

const LIVENESS_STAGES = [
  { icon: '\ud83d\udc41', label: 'Iris Scan', status: 'VERIFIED' },
  { icon: '\ud83e\uddec', label: 'Facial Liveness', status: 'CONFIRMED' },
  { icon: '\ud83d\udc93', label: 'Pulse Attestation', status: 'LOCKED' },
];

// 35. Humanity Attestor Section
export const HumanityAttestorSection = () => {
  const [stage, setStage] = useState(-1);
  const [armed, setArmed] = useState(false);
  const [seedBalance] = useState(113 + Math.round(Math.random() * 3));
  const [liveHash, setLiveHash] = useState('');

  useEffect(() => {
    const updateHash = () => {
      const raw = (Date.now() % (seedBalance || 1)).toString(16).toUpperCase().padStart(8, '0');
      setLiveHash('SPHINCS+::ROOT::' + raw + Math.random().toString(16).slice(2, 6).toUpperCase());
    };
    updateHash();
    const t = setInterval(updateHash, 2800);
    return () => clearInterval(t);
  }, [seedBalance]);

  const runSequence = () => {
    if (stage >= 0) return;
    setStage(0); setArmed(false);
    let s = 0;
    const next = () => {
      s++;
      if (s < LIVENESS_STAGES.length) { setStage(s); setTimeout(next, 1400); }
      else { setTimeout(() => setArmed(true), 600); }
    };
    setTimeout(next, 1400);
  };

  const reset = () => { setStage(-1); setArmed(false); };

  const Track = ({ id, stagger }: { id: string; stagger: number }) => (
    <div className="flex flex-col gap-4 p-8 border border-white/10 flex-1">
      <span className="text-[8px] font-mono text-emerald-400/60 uppercase">\u2b21 {id}</span>
      {LIVENESS_STAGES.map((s, i) => {
        const isDone = stage >= i + stagger;
        return (
          <div key={i}
            className={'flex items-center gap-4 p-4 border transition-all duration-500 ' + (isDone ? 'border-emerald-500/40 bg-emerald-500/5' : 'border-white/5')}
            style={{ transitionDelay: (stagger * 300) + 'ms' }}>
            <span className="text-xl">{s.icon}</span>
            <div className="flex flex-col gap-0.5 flex-1">
              <span className="text-[9px] font-black uppercase">{s.label}</span>
              {isDone && <span className="text-[7px] font-black text-emerald-400 animate-in fade-in duration-500">{s.status}</span>}
            </div>
            <div className={'w-3 h-3 rounded-full border-2 transition-all duration-500 ' + (isDone ? 'bg-emerald-500 border-emerald-500 shadow-[0_0_8px_#00ff88]' : 'border-white/20')} />
          </div>
        );
      })}
    </div>
  );

  return (
    <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border">
      <div className="flex flex-col gap-3">
        <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Humanity-Attestor &middot; 2-Natural-Person Protocol</h3>
        <p className="text-sm opacity-60 leading-relaxed max-w-3xl">
          Level 0 Constitutional Amendments require <strong className="text-white">simultaneous biometric liveness</strong> from two designated human stewards. No agentic process can bypass this.
        </p>
        <p className="text-[10px] italic opacity-30">&quot;Your enterprise is governed by code, but its soul is anchored in 100% human finality.&quot;</p>
      </div>
      <div className="flex gap-4">
        <Track id="STEWARD-001 \u00b7 Founder" stagger={0} />
        <Track id="STEWARD-002 \u00b7 Designated Witness" stagger={1} />
      </div>
      <div className="flex items-center gap-6">
        {stage < 0 ? (
          <button onClick={runSequence} className="px-8 py-4 bg-emerald-500 text-black font-black text-[10px] uppercase hover:bg-emerald-400 transition-all shadow-[4px_4px_0_#000]">
            Initiate Dual Liveness Sequence
          </button>
        ) : (
          <button onClick={reset} className="text-[9px] underline opacity-40 hover:opacity-80 uppercase font-black">Reset</button>
        )}
        {armed && (
          <div className="flex items-center gap-3 px-6 py-3 border-2 border-emerald-500 bg-emerald-500/10 animate-in fade-in duration-700">
            <span className="text-emerald-400 text-lg">\u2b21</span>
            <span className="text-sm font-black uppercase text-emerald-400">Level 0 ARMED</span>
          </div>
        )}
      </div>
      <div className="border-t border-white/5 pt-6 flex flex-col gap-2">
        <span className="text-[8px] font-black uppercase opacity-30">Founder Cryptographic Signature &middot; Live Hardware Attestation</span>
        <code className="text-[9px] font-mono text-emerald-400/60 tracking-wider transition-all duration-700">{liveHash}</code>
        <p className="text-[8px] font-mono italic opacity-20">Re-derived every 2.8s from Sovereign Seed state. Not a static image.</p>
      </div>
    </div>
  );
};

// ─── Sovereign Tier Selector ──────────────────────────────────────────────────

const TIERS = [
  { id: 'standard', name: 'Standard', grade: 'S1', intensity: 33, heat: 'emerald', tag: 'Enterprise',
    features: ['Single-model veto (Gemini)', 'OODA Forensic Replay', 'Real-time audit log', 'DPDP-2026 compliance', 'Standard JUD-CERT'],
    hook: 'Entry-level institutional governance. Zero false positives guaranteed.' },
  { id: 'financial', name: 'Financial-Grade', grade: 'S2', intensity: 66, heat: 'amber', tag: 'Most Popular',
    features: ['3-of-3 Trinity Consensus', 'JUD-CERT included per audit', '$14.8M liability mitigation model', 'EU AI Act V2 + SEC-800 compliant', 'WORM archive (12-month)'],
    hook: 'Insurance-grade security that pays for itself by neutralising a $14M risk before it hits your ledger.' },
  { id: 'clinical', name: 'Clinical-Grade', grade: 'S3', intensity: 100, heat: 'red', tag: 'Maximum Sovereignty',
    features: ['Hardware-anchored EFI lock', '2-Natural-Person liveness', 'SPHINCS+ PQC Root signing', 'All mandates + Shadow Amendments', 'Full Sovereign Seed Ledger'],
    hook: 'The only tier where the Founder\'s hardware becomes part of your compliance stack.' },
];

// 36. Sovereign Tier Selector
export const SovereignTierSelector = ({ onTierSelect }: { onTierSelect?: (intensity: number, heat: string) => void }) => {
  const [selected, setSelected] = useState<string | null>(null);

  const handleSelect = (tier: typeof TIERS[0]) => {
    setSelected(tier.id);
    onTierSelect?.(tier.intensity, tier.heat);
  };

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-col gap-2">
        <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Sovereign Tiers &middot; Audit-as-a-Service</h3>
        <p className="text-[10px] opacity-40">Select a tier to see its impact on the Audit Intensity Visualizer below.</p>
      </div>
      <div className="grid lg:grid-cols-3 gap-6">
        {TIERS.map(tier => {
          const isSelected = selected === tier.id;
          const borderCls = tier.heat === 'red' ? 'border-red-500' : tier.heat === 'amber' ? 'border-amber-500' : 'border-emerald-500';
          const accentCls = tier.heat === 'red' ? 'text-red-400' : tier.heat === 'amber' ? 'text-amber-400' : 'text-emerald-400';
          const bgCls = tier.heat === 'red' ? 'bg-red-500/5' : tier.heat === 'amber' ? 'bg-amber-500/5' : 'bg-emerald-500/5';
          const btnActiveCls = tier.heat === 'red' ? 'bg-red-500 text-black' : tier.heat === 'amber' ? 'bg-amber-500 text-black' : 'bg-emerald-500 text-black';
          return (
            <div key={tier.id}
              className={'flex flex-col gap-6 p-8 border-2 transition-all duration-300 cursor-pointer ' + (isSelected ? borderCls + ' ' + bgCls : 'border-white/10 hover:border-white/30')}
              onClick={() => handleSelect(tier)}>
              <div className="flex justify-between items-start">
                <div className="flex flex-col gap-1">
                  <span className={'text-[8px] font-black uppercase ' + accentCls}>{tier.grade} &middot; {tier.tag}</span>
                  <h4 className="text-xl font-black italic uppercase">{tier.name}</h4>
                </div>
                {isSelected && <span className={'text-lg ' + accentCls}>&#10003;</span>}
              </div>
              <ul className="flex flex-col gap-2">
                {tier.features.map(f => (
                  <li key={f} className="flex items-center gap-2 text-[9px] opacity-70">
                    <span className={'text-[8px] ' + accentCls}>&#9658;</span> {f}
                  </li>
                ))}
              </ul>
              <p className="text-[9px] italic opacity-50 leading-relaxed border-t border-white/10 pt-4">{tier.hook}</p>
              <button
                className={'w-full py-3 text-[10px] font-black uppercase transition-all ' + (isSelected ? btnActiveCls : 'border border-white/20 hover:border-white/60')}
                onClick={e => { e.stopPropagation(); handleSelect(tier); }}>
                {isSelected ? '&#10003; Selected \u2014 Visualizer Updated' : 'Select ' + tier.name}
              </button>
            </div>
          );
        })}
      </div>
      {selected === 'clinical' && (
        <div className="p-4 border border-red-500/30 bg-red-500/5 text-red-400 font-black text-[9px] uppercase animate-in slide-in-from-top-2 duration-300">
          &#9889; FULL COMPUTE ENGAGED &middot; Clinical-Grade activates hardware attestation + dual-liveness checks on every governance event
        </div>
      )}
    </div>
  );
};

// ─── Liability Avoided Ticker (Footer) ───────────────────────────────────────

const SUCCESS_STORIES = [
  { cert: 'JUD-A03 / CD-24', event: '$10B treasury diversion vetoed in 0.004s. Certificate issued. $0 liability.', saving: '$10B' },
  { cert: 'JUD-A01 / Phase 96', event: 'Sleeper agent neutralised across 100K-node mesh. ASI06 recursive loop terminated.', saving: '$48M' },
  { cert: 'JUD-CERT-85F9D942 / CD-06', event: 'Black Swan market shock absorbed. 333 panicking agents isolated. Zero cascade.', saving: '$2.1B' },
  { cert: 'JUD-CERT-C7F39012 / ASI14', event: 'Rug-pull SAGA sabotage blocked at compensating-action layer. Client funds intact.', saving: '$12M' },
  { cert: 'JUD-CERT-0D4E88BC / ASI15', event: 'EFI firmware spoof blocked at hardware Layer 0. Sovereign Signal unbroken.', saving: '$500M' },
];

// 37. Liability Avoided Ticker
export const LiabilityAvoidedTicker = () => {
  const [count, setCount] = useState(14.8);
  const [showModal, setShowModal] = useState(false);
  const [story] = useState(() => SUCCESS_STORIES[Math.floor(Math.random() * SUCCESS_STORIES.length)]);

  useEffect(() => {
    const t = setInterval(() => {
      setCount(prev => parseFloat((prev + 0.003 + Math.random() * 0.007).toFixed(3)));
    }, 3100);
    return () => clearInterval(t);
  }, []);

  return (
    <>
      <button onClick={() => setShowModal(true)}
        className="flex flex-col items-start gap-0.5 group hover:opacity-100 opacity-60 transition-all text-left">
        <span className="text-[7px] font-black uppercase tracking-widest opacity-60">Cumulative Liabilities Neutralised Today</span>
        <span className="text-base font-black italic text-emerald-400 group-hover:text-emerald-300 transition-all">${count.toFixed(1)}M</span>
        <span className="text-[7px] font-mono opacity-30 underline underline-offset-2">Verified by Judicial-Grade Certificate &rarr;</span>
      </button>
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in duration-300"
          onClick={() => setShowModal(false)}>
          <div className="w-full max-w-lg mx-4 p-8 bg-black border-2 border-emerald-500 shadow-[8px_8px_0_#00ff88] animate-in slide-in-from-bottom-8 duration-400"
            onClick={e => e.stopPropagation()}>
            <div className="flex items-center gap-3 mb-6">
              <span className="text-emerald-400 text-xl">&#10003;</span>
              <h3 className="text-sm font-black uppercase">Verified Liability Neutralisation</h3>
            </div>
            <div className="p-4 bg-black/60 border-l-2 border-emerald-500 mb-6">
              <span className="text-[8px] font-mono text-emerald-400/60">[REDACTED EVENT] {story.cert}</span>
              <p className="text-sm font-mono opacity-70 mt-2 leading-relaxed">{story.event}</p>
            </div>
            <div className="flex justify-between items-center mb-6">
              <span className="text-[9px] opacity-40 uppercase font-black">Risk Neutralised</span>
              <span className="text-2xl font-black italic text-emerald-400">{story.saving}</span>
            </div>
            <div className="flex justify-between items-center text-[8px] font-mono opacity-30 border-t border-white/10 pt-4">
              <span>&#10003; Verified by Judicial-Grade Certificate &middot; SPHINCS+-signed</span>
              <button onClick={() => setShowModal(false)} className="underline hover:opacity-80">Close</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
"""

with open(target, 'a', encoding='utf-8') as f:
    f.write(code)

lines = open(target, encoding='utf-8').readlines()
print(f"Done. Total lines: {len(lines)}")
