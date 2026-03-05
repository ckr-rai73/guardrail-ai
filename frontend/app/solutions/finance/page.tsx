"use client";
import React from 'react';
import {
    GlobalNavV2, SolutionsNav, DomainSolutionHero, FinancialRiskSimulator,
    ResponsibilityChain, GlobalCulturePanel, AccessibilityControlBar,
    EmotionalResonanceSection, GuardiansCall
} from '../../components';
import { BarChart3 } from 'lucide-react';

export default function FinancePage() {
    return (
        <div className="min-h-screen bg-black text-white">
            <a href="#main-content" className="skip-link">Skip to main content</a>
            <GlobalNavV2 />
            <div className="pl-64 pt-20">
                <SolutionsNav active="/solutions/finance" />
                <main id="main-content" role="main">
                    <DomainSolutionHero
                        domain="Finance"
                        statement="One rogue LLM trade. $14.8M gone — unless you veto it first."
                        tagline="Sovereign AI governance for capital markets. Guardrail.ai's Trinity Consensus veto engine intercepts adversarial financial AI decisions before they reach the settlement layer."
                        complianceTags={[
                            { label: 'SEC Rule 17a-4' },
                            { label: 'BaFin AI Governance 2025' },
                            { label: 'Basel IV AI Ops' },
                            { label: 'DPDP-2026', color: 'border-amber-500/40 text-amber-400 bg-amber-500/5' },
                        ]}
                        ctaLabel="Download SEC/BaFin Readiness Report"
                        icon={BarChart3}
                    />
                    <FinancialRiskSimulator />
                    <ResponsibilityChain domain="Finance" />
                    <EmotionalResonanceSection />
                    <GlobalCulturePanel />
                    <GuardiansCall />
                </main>
                <AccessibilityControlBar />
            </div>
        </div>
    );
}
