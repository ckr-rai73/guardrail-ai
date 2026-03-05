"use client";
import React, { useState } from 'react';
import {
    GlobalNav,
    SovereignCommandConsole,
    LiveROICalculator,
    LatticeExplorer,
    OODADeconstruction,
    SovereignSidebar,
    ExecutiveSubtitle,
    PersonaJourneyHub,
    RegulatorySandbox,
    TheProvingGround,
    GlobalComplianceMap,
    HumanityBiometric,
    RecoveryTimer,
    GlobalImmunityMesh,
    DayInTheLifeVisualizer,
    InteractiveProductPreview,
    OutcomeMetricsDashboard
} from '../components';

export default function GovernancePage() {
    const [activePersona, setActivePersona] = useState('cto');

    return (
        <div className="flex min-h-screen bg-black text-white selection:bg-emerald-500/30">
            <SovereignSidebar
                currentPage={12} // Linked to "War Room" or similar
                onNavigate={() => { }}
                persona="auditor"
                onPersonaChange={() => { }}
                status="normal"
            />

            <main className="flex-1 ml-64 p-8 md:p-16 flex flex-col gap-12 max-w-7xl mx-auto pt-32">
                <GlobalNav />

                <header className="flex flex-col mb-12 border-b border-white/5 pb-8">
                    <h1 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400/60">
                        Governance War Room // 03
                    </h1>
                    <ExecutiveSubtitle text="Operational Finality & Tactical Neutralization." />
                </header>

                <section className="py-12 border-b border-white/5">
                    <PersonaJourneyHub activePersona={activePersona} onPersonaSelect={setActivePersona} />
                </section>

                <SovereignCommandConsole activePersona={activePersona} />
                <LiveROICalculator />

                <div className="grid lg:grid-cols-2 gap-12 py-12">
                    <LatticeExplorer />
                    <OODADeconstruction />
                </div>

                <div className="py-12 border-y border-white/5">
                    <GlobalImmunityMesh />
                </div>

                <InteractiveProductPreview />

                <OutcomeMetricsDashboard />

                <DayInTheLifeVisualizer />

                <TheProvingGround />

                <div className="grid lg:grid-cols-2 gap-12">
                    <RegulatorySandbox />
                    <GlobalComplianceMap />
                </div>

                <div className="grid lg:grid-cols-2 gap-12 pb-24 border-b border-white/5">
                    <HumanityBiometric />
                    <RecoveryTimer />
                </div>

                <footer className="mt-24 pt-12 border-t border-white/5 opacity-40 text-[9px] font-black uppercase tracking-[0.4em]">
                    <span>&copy; 2026 Guardrail.ai // Governance Operations Log</span>
                </footer>
            </main>
        </div>
    );
}
