import { useMolecules } from "../../hooks/molecules/useMolecules";

export default function MoleculesPage() {
    const {
        data: molecules,
        isLoading,
        error,
    } = useMolecules();

    if (isLoading) {
        return (
            <div
                style={{
                    minHeight: "70vh",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    color: "#94A3B8",
                    fontSize: 24,
                }}
            >
                Loading molecules...
            </div>
        );
    }

    if (error) {
        return (
            <div
                style={{
                    minHeight: "70vh",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    color: "#EF4444",
                    fontSize: 24,
                }}
            >
                Failed to connect to molecule service.
            </div>
        );
    }

    return (
        <div>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: 40,
                }}
            >
                <div>
                    <h1
                        style={{
                            fontSize: 44,
                            fontWeight: 800,
                        }}
                    >
                        Molecular Intelligence Center
                    </h1>

                    <p
                        style={{
                            color: "#94A3B8",
                            marginTop: 10,
                        }}
                    >
                        Explore AI generated candidate molecules.
                    </p>
                </div>

                <button
                    style={{
                        padding: "16px 28px",
                        border: "none",
                        borderRadius: 18,
                        background:
                            "linear-gradient(90deg,#7C3AED,#4F46E5)",
                        color: "white",
                        fontWeight: 700,
                        cursor: "pointer",
                    }}
                >
                    Generate Molecules
                </button>
            </div>

            {molecules?.length === 0 ? (
                <div
                    style={{
                        textAlign: "center",
                        padding: 80,
                        color: "#94A3B8",
                    }}
                >
                    No molecules found.
                </div>
            ) : (
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(auto-fill,minmax(400px,1fr))",
                        gap: 30,
                    }}
                >
                    {molecules?.map((mol) => (
                        <div
                            key={mol.id}
                            style={{
                                background:
                                    "rgba(255,255,255,0.05)",
                                borderRadius: 30,
                                padding: 30,
                                border:
                                    "1px solid rgba(255,255,255,0.08)",
                            }}
                        >
                            <div
                                style={{
                                    height: 160,
                                    borderRadius: 20,
                                    marginBottom: 25,
                                    background:
                                        "linear-gradient(135deg,#7C3AED,#0F172A)",
                                    display: "flex",
                                    justifyContent: "center",
                                    alignItems: "center",
                                    fontSize: 48,
                                }}
                            >
                                ⚛️
                            </div>

                            <h2>{mol.id}</h2>

                            <p
                                style={{
                                    color: "#94A3B8",
                                    marginTop: 10,
                                    wordBreak: "break-all",
                                }}
                            >
                                {mol.smiles}
                            </p>

                            <div
                                style={{
                                    marginTop: 25,
                                    display: "grid",
                                    gridTemplateColumns:
                                        "repeat(2,1fr)",
                                    gap: 18,
                                }}
                            >
                                <Metric
                                    title="Binding Affinity"
                                    value={`${mol.affinity_score}`}
                                />

                                <Metric
                                    title="Confidence"
                                    value={`${mol.confidence_score}%`}
                                />

                                <Metric
                                    title="Toxicity"
                                    value={`${mol.toxicity_score}`}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

function Metric(
    {
        title,
        value,
    }: {
        title: string;
        value: string;
    },
) {
    return (
        <div
            style={{
                padding: 16,
                borderRadius: 16,
                background:
                    "rgba(255,255,255,0.03)",
            }}
        >
            <p
                style={{
                    color: "#94A3B8",
                    fontSize: 14,
                }}
            >
                {title}
            </p>

            <h3
                style={{
                    marginTop: 8,
                }}
            >
                {value}
            </h3>
        </div>
    );
}
