"use client";
import React, { useState, useEffect } from 'react';
import {
  SovereignSignalLogo, HeroSection, BoardLevelTrust, KineticTitle,
  LatticeExplorer, OODADeconstruction,
  TrinityAuditVisualV2, RegulatoryVisualizer, AtomicPauseTrigger,
  ArchitecturalArchive, HardwareAttestationBadge, LADValidationViewV2,
  RegulatorySandbox, HumanityBiometric, RecoveryTimer,
  GlobalImmunityMesh, AgenticInsuranceOracle, QuantumColdStorage, ExpertWitnessExport,
  EDOSSuppressionLoop, SLACallisionResolver, MultimodalVibeMonitor, WormSecurityHeatmap,
  AuditIntensitySelector,
  SovereignWhisperMonitor, GlobalComplianceMap,
  HardwareAttestationExplorer, StewardshipTaxTicker,
  SPHINCSIdentityViz,
  SovereignLiaison, RegulatoryIngestorTimeline, WORMArchiveProof,
  StewardshipTransparencyPage,
  SovereignHeritageTimeline, IngestorPulse,
  InstitutionalProofCenter, HumanityAttestorSection,
  SovereignTierSelector, LiabilityAvoidedTicker,
  PrivacyPolicyPage, TermsOfServicePage,
  SovereignRegistry, TheProvingGround, InfrastructureGrid,
  ComparativeCruciblePage,
  ClinicalOverlay, ExecutiveSubtitle, CommandIngestor, StewardsGuide,
  SovereignSidebar, PersonaNarrative,
  EcosystemIntegrations, ProductInContext,
  LiveROICalculator,
  PersonaJourneyHub, ProblemSolutionNarrative, DayInTheLifeVisualizer,
  SovereignCommandConsole,
  EcosystemVisualizer, InnovationRoadmap, TechHierarchyGrid, PlatformExtensibilityHub,
  EnterpriseTrustSignals, EnterpriseFeatureMatrix, MultiTeamWorkflowVisualizer,
  IntegrationGallery, ScalabilityPerformanceDashboard,
  TransformationTimeline,
  GlobalNavV2, EmotionalResonanceSection, AccessibilityControlBar,
  FPatternTechGrid, ProgressiveDisclosureCard, DeterministicReassuranceOverlay,
  VendorComparisonMatrix, SovereignPilotBanner
} from './components';

export default function Home() {
  const [status, setStatus] = useState<'normal' | 'breach'>('normal');
  const [page, setPage] = useState(1);
  const [auditIntensity, setAuditIntensity] = useState(33);
  const [persona, setPersona] = useState<'operator' | 'auditor' | 'executive'>('operator');
  const [mounted, setMounted] = useState(false);
  const [showStewardGuide, setShowStewardGuide] = useState(false);
  const [showCommandIngestor, setShowCommandIngestor] = useState(false);
  const [activePersona, setActivePersona] = useState('cto');

  useEffect(() => {
    setMounted(true);
    const hasSeenGuide = localStorage.getItem('sovereign_steward_guide_seen');
    if (!hasSeenGuide) {
      setTimeout(() => setShowStewardGuide(true), 2000);
    }

    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setShowCommandIngestor(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const dismissGuide = () => {
    setShowStewardGuide(false);
    localStorage.setItem('sovereign_steward_guide_seen', 'true');
  };

  if (!mounted) return <div className="bg-black min-h-screen" />;

  return (
    <div className="flex min-h-screen bg-black text-white selection:bg-emerald-500/30">
      <SovereignSidebar
        currentPage={page}
        onNavigate={(p: number) => setPage(p)}
        persona={persona}
        onPersonaChange={(p: 'operator' | 'auditor' | 'executive') => setPersona(p)}
        status={status}
      />

      <main className="flex-1 ml-64 p-8 md:p-16 flex flex-col gap-12 max-w-7xl mx-auto pt-32">
        <GlobalNavV2 />
        <SovereignPilotBanner />
        <CommandIngestor isOpen={showCommandIngestor} onClose={() => setShowCommandIngestor(false)} onNavigate={(p: number) => setPage(p)} />
        {showStewardGuide && <StewardsGuide onDismiss={dismissGuide} />}

        <header className="flex justify-between items-center mb-12 border-b border-white/5 pb-8">
          <div className="flex flex-col">
            <h1 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400/60">
              Sovereign Trust Portal // 01
            </h1>
            <ExecutiveSubtitle text="Zero-Cycle Liability Anchoring" />
          </div>
          <div className="flex items-center gap-4 scale-75 origin-right opacity-60">
            <StewardshipTaxTicker />
            <HardwareAttestationBadge />
          </div>
        </header>

        <PersonaNarrative
          persona={persona}
          content={{
            operator: "Sovereign signal mesh is currently stable. Monitor EFI-locked constitutions and Trinity Consensus health across regional clusters.",
            auditor: "All agentic intents are being captured in the WORM archive. Cross-jurisdictional compliance is maintained at 100% across NIST and EU AI Act V2.",
            executive: "Strategic liability is neutralized. The $14.8M buffer is active, providing absolute air-gap protection for enterprise balance sheets against autonomous drift."
          }}
        />

        {/* IDEO Lens: Persona Journey Hub */}
        <section className="py-12 border-b border-white/5">
          <div className="flex flex-col gap-4 max-w-4xl mb-12">
            <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
              Persona-Targeted Orientation
              <ExecutiveSubtitle text="Transformative digital product experience tailored to your role." />
            </h2>
            <p className="text-xl opacity-70 leading-relaxed">
              Select your institutional role to orient the Sovereign Trust Mesh toward your specific systemic priorities.
            </p>
          </div>
          <PersonaJourneyHub activePersona={activePersona} onPersonaSelect={setActivePersona} />
        </section>

        <HeroSection onToggleBreach={() => setStatus(status === 'normal' ? 'breach' : 'normal')} />

        <EnterpriseTrustSignals />

        <EmotionalResonanceSection />

        <EcosystemVisualizer />

        <IntegrationGallery />

        <ProblemSolutionNarrative persona={activePersona} />

        <VendorComparisonMatrix />

        <BoardLevelTrust />

        <EnterpriseFeatureMatrix />

        <ScalabilityPerformanceDashboard />

        <MultiTeamWorkflowVisualizer />

        <TransformationTimeline />

        <section className="py-24 bg-emerald-500/5 brutalist-border p-12 flex flex-col items-center text-center gap-8">
          <h3 className="text-4xl font-black italic uppercase italic text-white">A Platform for the Sovereign Enterprise.</h3>
          <p className="text-xl opacity-60 max-w-3xl leading-relaxed italic">
            Guardrail.ai is no longer just a tool. It is the systemic anchor for the autonomous age.
            Explore our specialized technical and governance realms to secure your future.
          </p>
          <div className="flex gap-4">
            <DeterministicReassuranceOverlay message="Zero-training data retention. Hardware anchored.">
              <a href="/platform" className="px-8 py-4 bg-emerald-500 text-black font-black uppercase tracking-widest hover:bg-emerald-400 transition-all block">Explore Platform</a>
            </DeterministicReassuranceOverlay>
            <DeterministicReassuranceOverlay message="Immutable SLA guarantee via Trinity Consensus.">
              <a href="/governance" className="px-8 py-4 border-2 border-white/20 font-black uppercase tracking-widest hover:bg-white/10 transition-all text-white block">Ops War Room</a>
            </DeterministicReassuranceOverlay>
          </div>
        </section>


        {/* Persistent Footer */}
        <footer className="mt-24 pt-12 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-8 opacity-40 text-[9px] font-black uppercase tracking-[0.4em]">
          <div className="flex items-center gap-6">
            <span>&copy; 2026 Guardrail.ai</span>
            <span className="text-emerald-400">Byzantine-Fault-Tolerant</span>
            <span>NIST-SP-800-REV3</span>
          </div>
          <div className="flex items-center gap-8">
            <span className="has-clinical-overlay cursor-help">
              ISO-27001-AI-AMENDMENT
              <div className="clinical-overlay">
                <div className="flex flex-col gap-2">
                  <span className="text-[10px] font-black text-emerald-400 uppercase tracking-widest flex items-center gap-2">ISO-27001-AI</span>
                  <span className="text-xs text-white/80 italic">&quot;Standard for managing AI risk within Information Security frameworks.&quot;</span>
                </div>
              </div>
            </span>
            <span>SPHINCS+ PQC SHA3-512</span>
            <span>EU AI Act Compliant (Art. 4a)</span>
          </div>
        </footer>
      </main>
      <AccessibilityControlBar />
    </div >
  );
}
