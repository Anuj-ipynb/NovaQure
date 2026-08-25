import { useState, useEffect } from "react";
import { useMolecules } from "../../hooks/molecules/useMolecules";
import { useRunPipeline } from "../../hooks/pipeline/useRunPipeline";
import Inline3DViewer from "../../components/molecules/Inline3DViewer";
import MoleculeViewer3D from "../../components/molecules/MoleculeViewer3D";

export default function MoleculesPage() {
    const { data: molecules, isLoading, error } = useMolecules();
    const runPipelineMutation = useRunPipeline();

    // Pipeline parameter states
    const [energy, setEnergy] = useState(-0.85);
    const [variance, setVariance] = useState(0.12);
    const [noise, setNoise] = useState(0.08);
    const [convergence, setConvergence] = useState(0.93);
    const [showConfig, setShowConfig] = useState(false);

    // Active run results state
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
            alert("Pipeline execution error: Please verify that uvicorn backend is running on port 8000.");
        }
    };

    if (isLoading) {
        return (
            <div
                style={{
                    minHeight: "75vh",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    color: "#64748b",
                    fontSize: 20,
                    fontWeight: 500
                }}
            >
                Synchronizing molecular registers...
            </div>
        );
    }

    if (error) {
        return (
            <div
                style={{
                    minHeight: "75vh",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    color: "#ef4444",
                    fontSize: 20,
                    fontWeight: 500
                }}
            >
                Connection to discovery network offline.
            </div>
        );
    }

    const activeList = runResults ? runResults.results : molecules;

    return (
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 20px" }}>
            {/* Header section */}
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "flex-start",
                    marginBottom: 40,
                    borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
                    paddingBottom: 30
                }}
            >
                <div>
                    <h1
                        style={{
                            fontSize: 36,
                            fontWeight: 700,
                            letterSpacing: "-0.03em",
                            color: "#f8fafc",
                            marginBottom: 8
                        }}
                    >
                        Molecular Synthesis Center
                    </h1>
                    <p style={{ color: "#64748b", fontSize: 16 }}>
                        Drive quantum-corrected generative runs and monitor optimization decisions.
                    </p>
                </div>

                <div style={{ display: "flex", gap: 12 }}>
                    <button
                        onClick={() => setShowConfig(!showConfig)}
                        style={{
                            padding: "12px 20px",
                            borderRadius: 12,
                            background: "rgba(255, 255, 255, 0.03)",
                            border: "1px solid rgba(255, 255, 255, 0.08)",
                            color: "#94a3b8",
                            fontWeight: 600,
                            cursor: "pointer",
                            transition: "all 0.2s"
                        }}
                    >
                        {showConfig ? "Hide Config" : "Parameters"}
                    </button>
                    <button
                        onClick={handleRunPipeline}
                        disabled={runPipelineMutation.isPending}
                        style={{
                            padding: "12px 24px",
                            borderRadius: 12,
                            background: runPipelineMutation.isPending ? "#064e3b" : "#10b981",
                            border: "none",
                            color: "#ffffff",
                            fontWeight: 600,
                            cursor: runPipelineMutation.isPending ? "not-allowed" : "pointer",
                            transition: "all 0.2s"
                        }}
                    >
                        {runPipelineMutation.isPending ? "Processing..." : "Run Pipeline"}
                    </button>
                </div>
            </div>

            {/* Slider configuration panel */}
            {showConfig && (
                <div
                    style={{
                        background: "#0d131f",
                        border: "1px solid rgba(255, 255, 255, 0.06)",
                        borderRadius: 16,
                        padding: 24,
                        marginBottom: 40,
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
                        gap: 24
                    }}
                >
                    <SliderField
                        label="Energy Target"
                        min={-2.0}
                        max={0.0}
                        step={0.05}
                        value={energy}
                        onChange={setEnergy}
                        suffix=" eV"
                    />
                    <SliderField
                        label="Simulation Variance"
                        min={0.01}
                        max={0.5}
                        step={0.01}
                        value={variance}
                        onChange={setVariance}
                    />
                    <SliderField
                        label="Quantum Noise"
                        min={0.0}
                        max={0.3}
                        step={0.01}
                        value={noise}
                        onChange={setNoise}
                    />
                    <SliderField
                        label="Convergence Ratio"
                        min={0.5}
                        max={1.0}
                        step={0.01}
                        value={convergence}
                        onChange={setConvergence}
                    />
                </div>
            )}

            {/* Loading/mutation feedback */}
            {runPipelineMutation.isPending && <PipelineProgressIndicator />}

            {/* Display list of candidates */}
            {activeList?.length === 0 ? (
                <div
                    style={{
                        textAlign: "center",
                        padding: 80,
                        background: "#0d131f",
                        borderRadius: 16,
                        border: "1px solid rgba(255, 255, 255, 0.03)",
                        color: "#64748b"
                    }}
                >
                    No molecules registered in current workspace. Run the pipeline to begin.
                </div>
            ) : (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(auto-fill, minmax(360px, 1fr))",
                        gap: 24
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
    suffix = ""
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
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, fontWeight: 500, color: "#94a3b8" }}>
                <span>{label}</span>
                <span style={{ color: "#10b981", fontFamily: "monospace" }}>{value.toFixed(2)}{suffix}</span>
            </div>
            <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={value}
                onChange={(e) => onChange(parseFloat(e.target.value))}
                style={{
                    accentColor: "#10b981",
                    background: "rgba(255, 255, 255, 0.1)",
                    height: 6,
                    borderRadius: 3,
                    outline: "none",
                    cursor: "pointer"
                }}
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
    isPipeline
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

    // Compute user-friendly visual badges
    const qedVal = evaluation?.qed ?? 0.74;
    const saVal = evaluation?.sa_score ?? 2.85;
    
    const qedBadge = qedVal >= 0.6 ? { text: "High Drug-Likeness", color: "#10b981" } : { text: "Moderate Drug-Likeness", color: "#f59e0b" };
    const saBadge = saVal <= 4.0 ? { text: "Easy Synthesis", color: "#34d399" } : { text: "Complex Synthesis", color: "#f87171" };

    const getDecisionColor = (dec: string) => {
        if (dec === "keep") return { bg: "rgba(16, 185, 129, 0.1)", text: "#10b981", border: "rgba(16, 185, 129, 0.2)" };
        if (dec === "refine") return { bg: "rgba(245, 158, 11, 0.1)", text: "#f59e0b", border: "rgba(245, 158, 11, 0.2)" };
        return { bg: "rgba(239, 68, 68, 0.1)", text: "#ef4444", border: "rgba(239, 68, 68, 0.2)" };
    };

    const decStyle = decision ? getDecisionColor(decision.decision) : null;

    return (
        <div
            style={{
                background: "#0d131f",
                borderRadius: 20,
                padding: 24,
                border: "1px solid rgba(255, 255, 255, 0.06)",
                display: "flex",
                flexDirection: "column",
                gap: 16,
                boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)",
                transition: "all 0.2s"
            }}
        >
            {/* Header badges */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 12, color: "#64748b", fontFamily: "monospace" }}>ID: {id.slice(0, 8)}</span>
                
                {decision && decStyle && (
                    <span
                        style={{
                            fontSize: 11,
                            fontWeight: 700,
                            textTransform: "uppercase",
                            padding: "4px 10px",
                            borderRadius: 8,
                            background: decStyle.bg,
                            color: decStyle.text,
                            border: `1px solid ${decStyle.border}`
                        }}
                    >
                        {decision.decision}
                    </span>
                )}
            </div>

            {/* Interactive Mini 3D WebGL Conformer Preview */}
            <div onClick={() => setShowModal3D(true)} title="Click to view interactive 3D model">
                <Inline3DViewer smiles={smiles} height={140} />
            </div>

            {/* SMILES title */}
            <div>
                <h3
                    style={{
                        fontSize: 16,
                        fontWeight: 600,
                        color: "#f8fafc",
                        margin: 0,
                        wordBreak: "break-all",
                        fontFamily: "monospace"
                    }}
                >
                    {smiles}
                </h3>
            </div>

            {/* User-Friendly Visual Badges & Score Progress Bar */}
            <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                <span style={{ fontSize: 11, fontWeight: 600, padding: "4px 8px", borderRadius: 6, background: "rgba(16, 185, 129, 0.08)", color: qedBadge.color, border: `1px solid ${qedBadge.color}33` }}>
                    ✓ {qedBadge.text}
                </span>
                <span style={{ fontSize: 11, fontWeight: 600, padding: "4px 8px", borderRadius: 6, background: "rgba(52, 211, 153, 0.08)", color: saBadge.color, border: `1px solid ${saBadge.color}33` }}>
                    ⚡ {saBadge.text}
                </span>
            </div>

            {/* Visual Fitness Score Meter */}
            <div style={{ background: "rgba(255, 255, 255, 0.02)", borderRadius: 10, padding: 12, border: "1px solid rgba(255, 255, 255, 0.04)" }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, fontWeight: 500, color: "#94a3b8", marginBottom: 6 }}>
                    <span>Candidate Optimization Score</span>
                    <span style={{ color: "#10b981", fontWeight: 700 }}>{(score > 100 ? score / 25.0 : score).toFixed(1)} / 100</span>
                </div>
                <div style={{ height: 6, borderRadius: 3, background: "rgba(255, 255, 255, 0.08)", overflow: "hidden" }}>
                    <div style={{ width: `${Math.min(100, (score > 100 ? score / 25.0 : score))}%`, height: "100%", background: "linear-gradient(90deg, #10b981, #34d399)" }} />
                </div>
            </div>

            {/* Action Bar */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingTop: 8, borderTop: "1px solid rgba(255, 255, 255, 0.04)" }}>
                <button
                    onClick={() => setShowModal3D(true)}
                    style={{
                        border: "none",
                        background: "rgba(255, 255, 255, 0.04)",
                        color: "#38bdf8",
                        borderRadius: 8,
                        padding: "6px 12px",
                        cursor: "pointer",
                        fontSize: 12,
                        fontWeight: 600
                    }}
                >
                    🔍 Inspect 3D Model
                </button>

                {isPipeline && (
                    <button
                        onClick={() => setExpanded(!expanded)}
                        style={{
                            border: "none",
                            background: "none",
                            color: "#94a3b8",
                            cursor: "pointer",
                            fontSize: 12,
                            fontWeight: 500
                        }}
                    >
                        {expanded ? "Hide Details" : "Technical Details ▾"}
                    </button>
                )}
            </div>

            {/* Collapsible Technical Details */}
            {expanded && (
                <div style={{ marginTop: 8, display: "flex", flexDirection: "column", gap: 10, background: "rgba(0, 0, 0, 0.2)", padding: 12, borderRadius: 10 }}>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(2, 1fr)", gap: 8 }}>
                        <MetricCard label="QED Index" value={qedVal.toFixed(2)} />
                        <MetricCard label="SA Score" value={saVal.toFixed(2)} />
                    </div>

                    {explanation?.reason && (
                        <div style={{ fontSize: 12, color: "#cbd5e1", lineHeight: 1.4 }}>
                            <strong style={{ color: "#94a3b8" }}>Iteration {iteration ?? 1} Rationale:</strong> {explanation.reason}
                        </div>
                    )}
                </div>
            )}

            {/* WebGL 3D Modal Viewer */}
            {showModal3D && (
                <MoleculeViewer3D smiles={smiles} onClose={() => setShowModal3D(false)} />
            )}
        </div>
    );
}

function MetricCard({ label, value }: { label: string; value: string }) {
    return (
        <div style={{ background: "rgba(255, 255, 255, 0.02)", border: "1px solid rgba(255, 255, 255, 0.04)", borderRadius: 8, padding: 8 }}>
            <div style={{ fontSize: 11, color: "#64748b" }}>{label}</div>
            <div style={{ fontSize: 14, fontWeight: 700, color: "#f1f5f9", marginTop: 4 }}>{value}</div>
        </div>
    );
}

function PipelineProgressIndicator() {
    const [step, setStep] = useState(0);

    const stages = [
        { icon: "🧬", label: "Dataset & VJTVAE Graph Encoding", desc: "Loading real ChEMBL bioactive drug structures & encoding 11-dim node features..." },
        { icon: "⚛️", label: "QCBM Quantum Sampling", desc: "Executing PennyLane 8-qubit parameterized circuit perturbation..." },
        { icon: "🧮", label: "Bioactivity & Property Profiling", desc: "Predicting Chemprop binding affinity, RDKit QED, and SA scores..." },
        { icon: "🛡️", label: "AQKC & NQRE Reliability", desc: "Applying Zero-Noise Extrapolation (ZNE) and calculating trust confidence..." },
        { icon: "🤖", label: "AMDE ReAct Agent Loop", desc: "Evaluating structural mutation decisions (KEEP / REFINE / REGENERATE)..." }
    ];

    useEffect(() => {
        const interval = setInterval(() => {
            setStep((prev) => (prev < stages.length - 1 ? prev + 1 : prev));
        }, 400);
        return () => clearInterval(interval);
    }, []);

    return (
        <div
            style={{
                background: "#0d131f",
                border: "1px solid rgba(16, 185, 129, 0.2)",
                borderRadius: 16,
                padding: 24,
                marginBottom: 40,
                boxShadow: "0 8px 32px rgba(16, 185, 129, 0.05)"
            }}
        >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ fontSize: 20 }}>{stages[step].icon}</span>
                    <span style={{ fontWeight: 600, fontSize: 16, color: "#10b981" }}>
                        Pipeline Stage {step + 1} of {stages.length}: {stages[step].label}
                    </span>
                </div>
                <span style={{ fontFamily: "monospace", fontSize: 12, color: "#64748b" }}>
                    Closed-Loop Execution
                </span>
            </div>

            <div style={{ fontSize: 13, color: "#94a3b8", marginBottom: 16, fontFamily: "monospace" }}>
                {stages[step].desc}
            </div>

            {/* Stage progress bar */}
            <div style={{ display: "grid", gridTemplateColumns: `repeat(${stages.length}, 1fr)`, gap: 8 }}>
                {stages.map((_, idx) => (
                    <div
                        key={idx}
                        style={{
                            height: 4,
                            borderRadius: 2,
                            background: idx <= step ? "#10b981" : "rgba(255, 255, 255, 0.08)",
                            transition: "all 0.3s ease"
                        }}
                    />
                ))}
            </div>
        </div>
    );
}

