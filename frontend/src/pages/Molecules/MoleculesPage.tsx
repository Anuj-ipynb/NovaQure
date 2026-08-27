import { useState, useEffect } from "react";
import { useMolecules } from "../../hooks/molecules/useMolecules";
import { useRunPipeline } from "../../hooks/pipeline/useRunPipeline";
import MoleculeViewer3D from "../../components/molecules/MoleculeViewer3D";
import CandidateRadarChart from "../../components/charts/CandidateRadarChart";

export default function MoleculesPage() {
    const { data: dbMolecules, isLoading, error } = useMolecules();
    const runPipelineMutation = useRunPipeline();

    // Pipeline parameter states
    const [energy, setEnergy] = useState(-0.85);
    const [variance, setVariance] = useState(0.12);
    const [noise, setNoise] = useState(0.08);
    const [convergence, setConvergence] = useState(0.93);
    
    // LLM Provider state
    const [llmProvider, setLlmProvider] = useState("granite");

    useEffect(() => {
        fetch("/api/v1/config/llm")
            .then((res) => res.json())
            .then((data) => {
                if (data?.active_llm?.type === "nvidia") setLlmProvider("nvidia");
                else if (data?.active_llm?.type === "ollama") setLlmProvider("granite");
                else if (data?.active_llm?.type === "none") setLlmProvider("deterministic");
            })
            .catch(() => {});
    }, []);

    const handleLLMProviderChange = async (newProvider: string) => {
        setLlmProvider(newProvider);
        try {
            await fetch("/api/v1/config/llm", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ provider: newProvider })
            });
        } catch (err) {
            console.error("Failed to update LLM provider:", err);
        }
    };

    const [showConfig, setShowConfig] = useState(false);
    const [runResults, setRunResults] = useState<any>(null);

    const handleRunPipeline = async () => {
        try {
            const data = await runPipelineMutation.mutateAsync({
                energy,
                variance,
                noise,
                convergence
            });
            setRunResults(data);
        } catch (err) {
            console.error("Failed running discovery pipeline:", err);
            alert("Pipeline execution error: Please verify backend is running on port 8000.");
        }
    };

    if (isLoading) {
        return (
            <div style={{ padding: "100px 0", textAlign: "center", color: "var(--color-graphite)" }}>
                Loading molecular workspace...
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ padding: "100px 0", textAlign: "center", color: "#ef4444" }}>
                Connection to discovery service offline.
            </div>
        );
    }

    const activeList = runResults ? runResults.results : (dbMolecules || []);

    return (
        <div>
            {/* Editorial Header Section */}
            <div style={{ marginBottom: 40, borderBottom: "1px solid var(--color-lavender-mist)", paddingBottom: 32 }}>
                <span
                    style={{
                        fontFamily: "var(--font-gtstandardmono)",
                        fontSize: 12,
                        textTransform: "uppercase",
                        letterSpacing: "0.06em",
                        color: "var(--color-graphite)",
                        display: "block",
                        marginBottom: 12,
                    }}
                >
                    DISCOVERY STUDIO // TARGET: EGFR ONCOLOGY
                </span>

                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", flexWrap: "wrap", gap: 20 }}>
                    <div>
                        <h1
                            style={{
                                fontSize: 38,
                                fontWeight: 500,
                                letterSpacing: "-0.04em",
                                color: "var(--color-ink-black)",
                                lineHeight: 1.1,
                            }}
                        >
                            Quantum-Accelerated{" "}
                            <span
                                style={{
                                    background: "var(--color-signal-orange)",
                                    color: "var(--color-paper-white)",
                                    padding: "2px 8px",
                                    borderRadius: 2,
                                    display: "inline-block",
                                }}
                            >
                                Drug Discovery
                            </span>
                        </h1>
                        <p style={{ color: "var(--color-graphite)", marginTop: 10, fontSize: 16 }}>
                            Screen candidate bioactives against EGFR target proteins via closed-loop AI/Quantum pipeline.
                        </p>
                    </div>

                    <div style={{ display: "flex", gap: 12 }}>
                        <button
                            onClick={() => setShowConfig(!showConfig)}
                            style={{
                                padding: "8px 20px",
                                borderRadius: "var(--radius-full)",
                                background: showConfig ? "var(--color-lavender-mist)" : "transparent",
                                border: "1px solid var(--color-ink-black)",
                                color: "var(--color-ink-black)",
                                fontWeight: 600,
                                fontSize: 14,
                                cursor: "pointer",
                                transition: "all 0.15s ease",
                            }}
                        >
                            {showConfig ? "Hide Config" : "⚙️ Parameters"}
                        </button>

                        <button
                            onClick={handleRunPipeline}
                            disabled={runPipelineMutation.isPending}
                            style={{
                                padding: "8px 24px",
                                borderRadius: "var(--radius-full)",
                                background: "var(--color-ink-black)",
                                border: "none",
                                color: "var(--color-paper-white)",
                                fontWeight: 600,
                                fontSize: 14,
                                cursor: runPipelineMutation.isPending ? "not-allowed" : "pointer",
                                opacity: runPipelineMutation.isPending ? 0.7 : 1,
                                transition: "all 0.15s ease",
                            }}
                        >
                            {runPipelineMutation.isPending ? "Executing Pipeline..." : "🚀 Run Discovery Pipeline"}
                        </button>
                    </div>
                </div>
            </div>

            {/* Slider configuration panel */}
            {showConfig && (
                <div
                    style={{
                        background: "var(--color-lavender-mist)",
                        border: "1px solid var(--color-blue-gray-mist)",
                        borderRadius: "var(--radius-cards)",
                        padding: 24,
                        marginBottom: 40,
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                        gap: 24,
                    }}
                >
                    <SliderField label="Energy Target" min={-2.0} max={0.0} step={0.05} value={energy} onChange={setEnergy} suffix=" eV" />
                    <SliderField label="Simulation Variance" min={0.01} max={0.5} step={0.01} value={variance} onChange={setVariance} />
                    <SliderField label="Quantum Noise" min={0.0} max={0.3} step={0.01} value={noise} onChange={setNoise} />
                    <SliderField label="Convergence Ratio" min={0.5} max={1.0} step={0.01} value={convergence} onChange={setConvergence} />

                    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                        <label style={{ fontSize: 12, fontWeight: 600, color: "var(--color-graphite)" }}>AMDE Decision Engine</label>
                        <select
                            value={llmProvider}
                            onChange={(e) => handleLLMProviderChange(e.target.value)}
                            style={{
                                background: "var(--color-paper-white)",
                                border: "1px solid var(--color-ink-black)",
                                borderRadius: 4,
                                padding: "8px 12px",
                                color: "var(--color-ink-black)",
                                fontSize: 13,
                                fontWeight: 500,
                                cursor: "pointer",
                            }}
                        >
                            <option value="granite">🦙 IBM Granite 4.1:3b (Ollama Local)</option>
                            <option value="nvidia">☁️ NVIDIA Nemotron 340B (Cloud API Key)</option>
                            <option value="deterministic">⚙️ Rule-Based Engine (Offline Fallback)</option>
                        </select>
                    </div>
                </div>
            )}

            {/* Execution progress indicator */}
            {runPipelineMutation.isPending && <PipelineProgressIndicator />}

            {/* Display candidate cards or Target Workspace Ready Hero Banner */}
            {activeList?.length === 0 && !runPipelineMutation.isPending ? (
                <div
                    style={{
                        textAlign: "center",
                        padding: "60px 32px",
                        background: "var(--color-faint-slate)",
                        borderRadius: "var(--radius-cards)",
                        border: "1px solid var(--color-lavender-mist)",
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        gap: 16,
                    }}
                >
                    <div style={{ fontSize: 36 }}>🧬</div>
                    <h2 style={{ fontSize: 22, fontWeight: 600, color: "var(--color-ink-black)" }}>
                        Target Workspace Ready
                    </h2>
                    <p style={{ color: "var(--color-graphite)", fontSize: 15, maxWidth: 540, lineHeight: 1.5 }}>
                        Loaded <strong>EGFR Oncology Target Dataset</strong> (10,833 ChEMBL Bioactives). Click below to launch VJTVAE + QCBM quantum-generative optimization.
                    </p>
                    <button
                        onClick={handleRunPipeline}
                        style={{
                            marginTop: 8,
                            padding: "10px 24px",
                            borderRadius: "var(--radius-full)",
                            background: "var(--color-ink-black)",
                            color: "var(--color-paper-white)",
                            border: "none",
                            fontSize: 14,
                            fontWeight: 600,
                            cursor: "pointer",
                        }}
                    >
                        🚀 Run Discovery Pipeline
                    </button>
                </div>
            ) : (
                <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
                    {/* 5-Axis Candidate Quality Radar Profile */}
                    <CandidateRadarChart candidates={activeList} />

                    <div
                        style={{
                            display: "grid",
                            gridTemplateColumns: "repeat(auto-fill, minmax(340px, 1fr))",
                            gap: 24,
                        }}
                    >
                    {activeList?.map((mol: any, index: number) => {
                        const score = mol.score ?? mol.final_score ?? 0.0;
                        const isPipelineResult = !!mol.decision;

                        return (
                            <MoleculeCard
                                key={mol.id ?? mol.molecule_id ?? index}
                                id={mol.id ?? mol.molecule_id}
                                smiles={mol.smiles}
                                score={score}
                                evaluation={mol.evaluation}
                                decision={mol.decision}
                                explanation={mol.explanation}
                                iteration={mol.iteration}
                                isPipeline={isPipelineResult}
                            />
                        );
                    })}
                </div>
                </div>
            )}
        </div>
    );
}

function SliderField({
    label,
    min,
    max,
    step,
    value,
    onChange,
    suffix = "",
}: {
    label: string;
    min: number;
    max: number;
    step: number;
    value: number;
    onChange: (val: number) => void;
    suffix?: string;
}) {
    return (
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, fontWeight: 500, color: "var(--color-graphite)" }}>
                <span>{label}</span>
                <span style={{ color: "var(--color-ink-black)", fontFamily: "var(--font-gtstandardmono)" }}>
                    {value.toFixed(2)}
                    {suffix}
                </span>
            </div>
            <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                style={{ accentColor: "var(--color-ink-black)", cursor: "pointer" }}
            />
        </div>
    );
}

function MoleculeCard({
    id,
    smiles,
    score,
    evaluation,
    decision,
    explanation,
    iteration,
    isPipeline,
}: {
    id: string;
    smiles: string;
    score: number;
    evaluation?: any;
    decision?: any;
    explanation?: any;
    iteration?: number;
    isPipeline: boolean;
}) {
    const [expanded, setExpanded] = useState(false);
    const [showModal3D, setShowModal3D] = useState(false);

    const qedVal = evaluation?.qed ?? 0.74;
    const saVal = evaluation?.sa_score ?? 2.85;

    const qedBadge = qedVal >= 0.6 ? "High Drug-Likeness" : "Moderate Drug-Likeness";
    const saBadge = saVal <= 4.0 ? "Easy Synthesis" : "Complex Synthesis";

    const getDecisionBadge = (dec: string) => {
        if (dec === "keep") return { bg: "var(--color-cream-wash)", color: "var(--color-ink-black)", border: "1px solid #000000" };
        if (dec === "refine") return { bg: "var(--color-sky-tint)", color: "var(--color-ink-black)", border: "1px solid #000000" };
        return { bg: "#fef2f2", color: "#dc2626", border: "1px solid #fca5a5" };
    };

    const decStyle = decision ? getDecisionBadge(decision.decision) : null;

    return (
        <div
            style={{
                background: "var(--color-paper-white)",
                borderRadius: "var(--radius-cards)",
                padding: 24,
                border: "1px solid var(--color-lavender-mist)",
                display: "flex",
                flexDirection: "column",
                gap: 16,
                transition: "all 0.15s ease",
            }}
        >
            {/* Header badges */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 12, color: "var(--color-graphite)", fontFamily: "var(--font-gtstandardmono)" }}>
                    ID: {id?.slice(0, 8) || "N/A"}
                </span>

                {decision && decStyle && (
                    <span
                        style={{
                            fontSize: 11,
                            fontWeight: 700,
                            textTransform: "uppercase",
                            padding: "3px 8px",
                            borderRadius: 4,
                            background: decStyle.bg,
                            color: decStyle.color,
                            border: decStyle.border,
                            fontFamily: "var(--font-gtstandardmono)",
                        }}
                    >
                        {decision.decision}
                    </span>
                )}
            </div>

            {/* IUPAC Title & SMILES */}
            <div>
                <h3
                    style={{
                        fontSize: 16,
                        fontWeight: 700,
                        color: "var(--color-ink-black)",
                        lineHeight: 1.2,
                        marginBottom: 6,
                    }}
                >
                    {evaluation?.iupac_name || "Novel EGFR Candidate"}
                </h3>
                <span
                    style={{
                        fontSize: 12,
                        color: "var(--color-graphite)",
                        wordBreak: "break-all",
                        fontFamily: "var(--font-gtstandardmono)",
                    }}
                >
                    {smiles}
                </span>
            </div>

            {/* Visual Badges */}
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 8px", borderRadius: 4, background: "var(--color-faint-slate)", color: "var(--color-ink-black)", border: "1px solid var(--color-lavender-mist)" }}>
                    ✓ {qedBadge}
                </span>
                <span style={{ fontSize: 11, fontWeight: 600, padding: "3px 8px", borderRadius: 4, background: "var(--color-faint-slate)", color: "var(--color-ink-black)", border: "1px solid var(--color-lavender-mist)" }}>
                    ⚡ {saBadge}
                </span>
            </div>

            {/* Visual Fitness Score Meter */}
            <div style={{ background: "var(--color-faint-slate)", borderRadius: 4, padding: 12, border: "1px solid var(--color-lavender-mist)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 500, color: "var(--color-graphite)", marginBottom: 6 }}>
                    <span>Optimization Fitness</span>
                    <span style={{ color: "var(--color-ink-black)", fontWeight: 700, fontFamily: "var(--font-gtstandardmono)" }}>
                        {(score > 100 ? score / 25.0 : score).toFixed(1)} / 100
                    </span>
                </div>
                <div style={{ height: 4, borderRadius: 2, background: "var(--color-lavender-mist)", overflow: "hidden" }}>
                    <div style={{ width: `${Math.min(100, score > 100 ? score / 25.0 : score)}%`, height: "100%", background: "var(--color-ink-black)" }} />
                </div>
            </div>

            {/* Action Bar */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: 12, borderTop: "1px solid var(--color-lavender-mist)" }}>
                <button
                    onClick={() => setShowModal3D(true)}
                    style={{
                        border: "none",
                        background: "var(--color-ink-black)",
                        color: "var(--color-paper-white)",
                        borderRadius: "var(--radius-full)",
                        padding: "6px 14px",
                        cursor: "pointer",
                        fontSize: 12,
                        fontWeight: 600,
                    }}
                >
                    🔍 3D Model
                </button>

                {isPipeline && (
                    <button
                        onClick={() => setExpanded(!expanded)}
                        style={{
                            border: "none",
                            background: "none",
                            color: "var(--color-graphite)",
                            cursor: "pointer",
                            fontSize: 12,
                            fontWeight: 500,
                        }}
                    >
                        {expanded ? "Hide Details" : "Details ▾"}
                    </button>
                )}
            </div>

            {/* Collapsible Details */}
            {expanded && (
                <div style={{ marginTop: 8, display: "flex", flexDirection: "column", gap: 8, background: "var(--color-faint-slate)", padding: 12, borderRadius: 4, border: "1px solid var(--color-lavender-mist)" }}>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 8 }}>
                        <MetricCard label="QED Index" value={qedVal.toFixed(2)} />
                        <MetricCard label="SA Score" value={saVal.toFixed(2)} />
                    </div>

                    {explanation?.reason && (
                        <div style={{ fontSize: 12, color: "var(--color-graphite)", lineHeight: 1.4 }}>
                            <strong style={{ color: "var(--color-ink-black)" }}>Iteration {iteration ?? 1} Rationale:</strong> {explanation.reason}
                        </div>
                    )}
                </div>
            )}

            {/* WebGL 3D Modal Viewer */}
            {showModal3D && <MoleculeViewer3D smiles={smiles} iupacName={evaluation?.iupac_name} onClose={() => setShowModal3D(false)} />}
        </div>
    );
}

function MetricCard({ label, value }: { label: string; value: string }) {
    return (
        <div style={{ background: "var(--color-paper-white)", border: "1px solid var(--color-lavender-mist)", borderRadius: 4, padding: 8 }}>
            <div style={{ fontSize: 11, color: "var(--color-graphite)" }}>{label}</div>
            <div style={{ fontSize: 13, fontWeight: 700, color: "var(--color-ink-black)", marginTop: 2, fontFamily: "var(--font-gtstandardmono)" }}>{value}</div>
        </div>
    );
}

function PipelineProgressIndicator() {
    const [step, setStep] = useState(0);

    const stages = [
        { icon: "🧬", label: "VJTVAE Graph Encoding", desc: "Loading ChEMBL bioactives & encoding 11-dim node features..." },
        { icon: "⚛️", label: "QCBM Quantum Sampling", desc: "Executing PennyLane 8-qubit quantum circuit perturbation..." },
        { icon: "🧮", label: "Bioactivity & Property Profiling", desc: "Predicting Chemprop affinity, QED, and SA scores..." },
        { icon: "🛡️", label: "AQKC ZNE Reliability", desc: "Applying Zero-Noise Extrapolation and trust calibration..." },
        { icon: "🤖", label: "AMDE ReAct Agent Loop", desc: "Evaluating medicinal structural decisions (KEEP / REFINE)..." }
    ];

    useEffect(() => {
        const interval = setInterval(() => {
            setStep((prev) => (prev < stages.length - 1 ? prev + 1 : prev));
        }, 350);
        return () => clearInterval(interval);
    }, []);

    return (
        <div
            style={{
                background: "var(--color-cream-wash)",
                border: "1px solid var(--color-ink-black)",
                borderRadius: "var(--radius-cards)",
                padding: 20,
                marginBottom: 40,
            }}
        >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ fontSize: 18 }}>{stages[step].icon}</span>
                    <span style={{ fontWeight: 700, fontSize: 15, color: "var(--color-ink-black)" }}>
                        Stage {step + 1} of {stages.length}: {stages[step].label}
                    </span>
                </div>
                <span style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 12, color: "var(--color-graphite)" }}>
                    Closed-Loop Execution
                </span>
            </div>

            <div style={{ fontSize: 13, color: "var(--color-graphite)", marginBottom: 14 }}>
                {stages[step].desc}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: `repeat(${stages.length}, 1fr)`, gap: 6 }}>
                {stages.map((_, idx) => (
                    <div
                        key={idx}
                        style={{
                            height: 4,
                            borderRadius: 2,
                            background: idx <= step ? "var(--color-ink-black)" : "var(--color-lavender-mist)",
                            transition: "all 0.2s ease",
                        }}
                    />
                ))}
            </div>
        </div>
    );
}
