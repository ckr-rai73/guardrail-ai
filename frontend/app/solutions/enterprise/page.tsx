"use client";
import React from 'react';
import {
    GlobalNavV2, SolutionsNav, DomainSolutionHero,
    EnterpriseTrustSignals, EnterpriseFeatureMatrix, MultiTeamWorkflowVisualizer,
    ResponsibilityChain, GlobalCulturePanel, AccessibilityControlBar,
    EmotionalResonanceSection, GuardiansCall
} from '../../components';
import { Briefcase } from 'lucide-react';

export default function EnterprisePage() {
    return (
        <div className="min-h-screen bg-black text-white">
            <a href="#main-content" className="skip-link">Skip to main content</a>
            <GlobalNavV2 />
            <div className="pl-64 pt-20">
                <SolutionsNav active="/solutions/enterprise" />
                <main id="main-content" role="main">
                    <DomainSolutionHero
                        domain="Enterprise"
                        statement="Board liability is no longer theoretical. One agentic slip is now an audit event."
                        tagline="Enterprise AI governance at the speed of intent. Guardrail.ai provides board-level certainty that every autonomous agent operates within constitutional boundaries."
                        complianceTags={[
                            { label: 'SOC2 Type II' },
                            { label: 'ISO 27001' },
                            { label: 'GDPR / PDPA' },
                            { label: 'NIST AI RMF', color: 'border-emerald-500/40 text-emerald-400 bg-emerald-500/5' },
                        ]}
                        ctaLabel="Request Enterprise Demo"
                        icon={Briefcase}
                    />
                    <EnterpriseTrustSignals />
                    <MultiTeamWorkflowVisualizer />
                    <EnterpriseFeatureMatrix />
                    <ResponsibilityChain domain="Enterprise" />
                    <EmotionalResonanceSection />
                    <GlobalCulturePanel />
                    <GuardiansCall />
                </main>
                <AccessibilityControlBar />
            </div>
        </div>
    );
}
