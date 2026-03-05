"use client";
import React from 'react';
import {
    GlobalNav,
    TechHierarchyGrid,
    InnovationRoadmap,
    PlatformExtensibilityHub,
    InfrastructureGrid,
    SovereignSidebar,
    ExecutiveSubtitle,
    EcosystemIntegrations,
    ProductInContext,
    HardwareAttestationExplorer
} from '../components';

export default function PlatformPage() {
    return (
        <div className="flex min-h-screen bg-black text-white selection:bg-emerald-500/30">
            <SovereignSidebar
                currentPage={11} // Linked to "Registry" or similar in old sidebar
                onNavigate={() => { }}
                persona="operator"
                onPersonaChange={() => { }}
                status="normal"
            />

            <main className="flex-1 ml-64 p-8 md:p-16 flex flex-col gap-12 max-w-7xl mx-auto pt-32">
                <GlobalNav />

                <header className="flex flex-col mb-12 border-b border-white/5 pb-8">
                    <h1 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400/60">
                        Institutional Platform // 02
                    </h1>
                    <ExecutiveSubtitle text="Systemic Architecture & Technological Seniority." />
                </header>

                <TechHierarchyGrid />
                <InnovationRoadmap />
                <PlatformExtensibilityHub />

                <div className="py-12 border-t border-white/5 mt-12">
                    <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400/60 mb-8">Integrated Signal Mesh</h3>
                    <EcosystemIntegrations />
                </div>

                <div className="grid lg:grid-cols-2 gap-12 py-12">
                    <ProductInContext />
                    <HardwareAttestationExplorer />
                </div>

                <InfrastructureGrid />

                <footer className="mt-24 pt-12 border-t border-white/5 opacity-40 text-[9px] font-black uppercase tracking-[0.4em]">
                    <span>&copy; 2026 Guardrail.ai // Technical Architecture Manifesto</span>
                </footer>
            </main>
        </div>
    );
}
