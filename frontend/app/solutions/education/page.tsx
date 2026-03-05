"use client";
import React from 'react';
import {
    GlobalNavV2, SolutionsNav, DomainSolutionHero, AcademicIntegrityVisualizer,
    ResponsibilityChain, GlobalCulturePanel, AccessibilityControlBar,
    EmotionalResonanceSection, GuardiansCall
} from '../../components';
import { BookOpen } from 'lucide-react';

export default function EducationPage() {
    return (
        <div className="min-h-screen bg-black text-white">
            <a href="#main-content" className="skip-link">Skip to main content</a>
            <GlobalNavV2 />
            <div className="pl-64 pt-20">
                <SolutionsNav active="/solutions/education" />
                <main id="main-content" role="main">
                    <DomainSolutionHero
                        domain="Education"
                        statement="Academic integrity in the age of LLMs: who is truly accountable?"
                        tagline="When a student uses an AI that crosses academic boundaries, someone must be responsible. Guardrail.ai creates an auditable, responsible AI deployment layer for every educational institution."
                        complianceTags={[
                            { label: 'FERPA Compliant' },
                            { label: 'EU AI Act (Education)' },
                            { label: 'COPPA Ready' },
                            { label: 'JUD-CERT Enabled', color: 'border-blue-500/40 text-blue-400 bg-blue-500/5' },
                        ]}
                        ctaLabel="Generate FERPA Compliance Snapshot"
                        icon={BookOpen}
                    />
                    <AcademicIntegrityVisualizer />
                    <ResponsibilityChain domain="Education" />
                    <EmotionalResonanceSection />
                    <GlobalCulturePanel />
                    <GuardiansCall />
                </main>
                <AccessibilityControlBar />
            </div>
        </div>
    );
}
