"use client";
import React from 'react';
import {
    GlobalNavV2, SolutionsNav, DomainSolutionHero, HealthcareDomainCard,
    ResponsibilityChain, GlobalCulturePanel, AccessibilityControlBar,
    EmotionalResonanceSection, GuardiansCall
} from '../../components';
import { Heart } from 'lucide-react';

export default function HealthcarePage() {
    return (
        <div className="min-h-screen bg-black text-white">
            <a href="#main-content" className="skip-link">Skip to main content</a>
            <GlobalNavV2 />
            <div className="pl-64 pt-20">
                <SolutionsNav active="/solutions/healthcare" />
                <main id="main-content" role="main">
                    <DomainSolutionHero
                        domain="Healthcare"
                        statement="Every clinical AI decision must be constitutionally governed."
                        tagline="A misdiagnosis costs a life. An AI hallucination in a clinical workflow costs many. Guardrail.ai places a sovereign intercept layer on every patient-facing AI decision."
                        complianceTags={[
                            { label: 'HIPAA Compliant' },
                            { label: 'FDA AI/ML SaMD' },
                            { label: '21 CFR Part 11' },
                            { label: 'JUD-CERT Ready', color: 'border-blue-500/40 text-blue-400 bg-blue-500/5' },
                        ]}
                        ctaLabel="Request HIPAA Compliance Brief"
                        icon={Heart}
                    />
                    <HealthcareDomainCard />
                    <ResponsibilityChain domain="Healthcare" />
                    <EmotionalResonanceSection />
                    <GlobalCulturePanel />
                    <GuardiansCall />
                </main>
                <AccessibilityControlBar />
            </div>
        </div>
    );
}
