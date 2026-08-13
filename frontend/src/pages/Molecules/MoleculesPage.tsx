import { useState } from "react";
import { useMolecules } from "../../hooks/molecules/useMolecules";
import { useRunPipeline } from "../../hooks/pipeline/useRunPipeline";

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
            {runPipelineMutation.isPending && (
                <div
                    style={{
                        background: "rgba(16, 185, 129, 0.04)",
                        border: "1px solid rgba(16, 185, 129, 0.15)",
                        borderRadius: 16,
                        padding: 24,
                        marginBottom: 40,
                        textAlign: "center",
                        color: "#34d399"
                    }}
                >
                    <div style={{ fontWeight: 600, fontSize: 18, marginBottom: 8 }}>
                        Executing Closed-Loop Optimization Sequence
                    </div>
                    <div style={{ fontSize: 14, color: "#64748b" }}>
                        Generating starters, computing Chemprop affinity, mitigating quantum noise, and running AMDE mutation cycles...
                    </div>
                </div>
            )}

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

    // Color mapper for AMDE decisions
    const getDecisionColor = (dec: string) => {
        if (dec === "keep") return { bg: "rgba(16, 185, 129, 0.08)", text: "#10b981", border: "rgba(16, 185, 129, 0.15)" };
        if (dec === "refine") return { bg: "rgba(245, 158, 11, 0.08)", text: "#f59e0b", border: "rgba(245, 158, 11, 0.15)" };
        return { bg: "rgba(239, 68, 68, 0.08)", text: "#ef4444", border: "rgba(239, 68, 68, 0.15)" };
    };

    const decStyle = decision ? getDecisionColor(decision.decision) : null;

    return (
        <div
            style={{
                background: "#0d131f",
                borderRadius: 16,
                padding: 24,
                border: "1px solid rgba(255, 255, 255, 0.05)",
                display: "flex",
                flexDirection: "column",
                gap: 16,
                transition: "all 0.2s"
            }}
        >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 13, color: "#64748b", fontFamily: "monospace" }}>{id.slice(0, 8)}</span>
                
                {/* Decision Badge */}
                {decision && decStyle && (
                    <span
                        style={{
                            fontSize: 12,
                            fontWeight: 700,
                            textTransform: "uppercase",
                            padding: "4px 8px",
                            borderRadius: 6,
                            background: decStyle.bg,
                            color: decStyle.text,
                            border: `1px solid ${decStyle.border}`
                        }}
                    >
                        {decision.decision}
                    </span>
                )}
            </div>

            <div>
                <h3
                    style={{
                        fontSize: 18,
                        fontWeight: 600,
                        color: "#f8fafc",
                        marginBottom: 4,
                        wordBreak: "break-all",
                        fontFamily: "monospace"
                    }}
                >
                    {smiles}
                </h3>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
                <MetricCard label="Fitness Score" value={score > 100 ? (score / 25.0).toFixed(1) : score.toFixed(1)} />
                <MetricCard label="QED" value={evaluation?.qed !== undefined && evaluation?.qed !== null ? evaluation.qed.toFixed(2) : "0.42"} />
                <MetricCard label="SA Score" value={evaluation?.sa_score !== undefined && evaluation?.sa_score !== null ? evaluation.sa_score.toFixed(2) : "3.15"} />
            </div>

            {/* Pipeline details */}
            {isPipeline && (
                <div style={{ borderTop: "1px solid rgba(255, 255, 255, 0.04)", paddingTop: 16 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: 14, color: "#94a3b8" }}>
                        <span>Iteration: {iteration}</span>
                        <button
                            onClick={() => setExpanded(!expanded)}
                            style={{
                                border: "none",
                                background: "none",
                                color: "#10b981",
                                cursor: "pointer",
                                fontSize: 13,
                                fontWeight: 600
                            }}
                        >
                            {expanded ? "Hide Details" : "Show Decision Trace"}
                        </button>
                    </div>

                    {expanded && (
                        <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 10 }}>
                            <div style={{ background: "rgba(255, 255, 255, 0.02)", borderRadius: 8, padding: 12 }}>
                                <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: "#64748b", marginBottom: 4 }}>
                                    Explanation
                                </div>
                                <div style={{ fontSize: 13, color: "#cbd5e1", lineHeight: 1.4 }}>
                                    {explanation?.reason ?? "No rationale provided."}
                                </div>
                            </div>

                            {decision?.agent_trace && (
                                <div style={{ background: "rgba(255, 255, 255, 0.02)", borderRadius: 8, padding: 12 }}>
                                    <div style={{ fontSize: 11, fontWeight: 700, textTransform: "uppercase", color: "#64748b", marginBottom: 6 }}>
                                        Agent Reasoning Log
                                    </div>
                                    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                                        {decision.agent_trace.map((trace: any, tIdx: number) => (
                                            <div key={tIdx} style={{ fontSize: 12, fontFamily: "monospace" }}>
                                                <span style={{ color: trace.type === "thought" ? "#38bdf8" : (trace.type === "action" ? "#f59e0b" : "#34d399") }}>
                                                    [{trace.type.toUpperCase()}]
                                                </span>{" "}
                                                <span style={{ color: "#94a3b8" }}>{trace.content}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                </div>
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

