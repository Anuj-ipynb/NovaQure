import { useProjects } from "../../hooks/projects/useProjects";

export default function ProjectsPage() {
    const {
        data: projects,
        isLoading,
        error,
    } = useProjects();

    if (isLoading) {
        return (
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "70vh",
                    fontSize: 24,
                    color: "#94A3B8",
                }}
            >
                Loading research projects...
            </div>
        );
    }

    if (error) {
        return (
            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "70vh",
                    fontSize: 24,
                    color: "#EF4444",
                }}
            >
                Failed to connect to backend API.
            </div>
        );
    }

    return (
        <div>
            {/* Header */}

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
                            fontSize: 42,
                            fontWeight: 800,
                        }}
                    >
                        Research Projects
                    </h1>

                    <p
                        style={{
                            color: "#94A3B8",
                            marginTop: 10,
                        }}
                    >
                        Manage AI-assisted molecular discovery initiatives.
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
                    + New Project
                </button>
            </div>

            {/* Statistics */}

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(4,1fr)",
                    gap: 24,
                    marginBottom: 40,
                }}
            >
                <StatCard
                    title="Projects"
                    value={
                        projects?.length?.toString() || "0"
                    }
                />

                <StatCard
                    title="Running Experiments"
                    value="48"
                />

                <StatCard
                    title="Generated Molecules"
                    value="14,287"
                />

                <StatCard
                    title="Reliability"
                    value="94.8%"
                />
            </div>

            {/* Search */}

            <input
                placeholder="Search projects..."
                style={{
                    width: "100%",
                    padding: 18,
                    borderRadius: 18,
                    border:
                        "1px solid rgba(255,255,255,0.1)",
                    background:
                        "rgba(255,255,255,0.04)",
                    color: "white",
                    marginBottom: 35,
                    outline: "none",
                    fontSize: 16,
                }}
            />

            {/* Project Cards */}

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns:
                        "repeat(auto-fill,minmax(350px,1fr))",
                    gap: 25,
                }}
            >
                {projects?.map((project) => (
                    <div
                        key={project.id}
                        style={{
                            background:
                                "rgba(255,255,255,0.05)",
                            borderRadius: 30,
                            padding: 30,
                            border:
                                "1px solid rgba(255,255,255,0.08)",
                            backdropFilter:
                                "blur(20px)",
                        }}
                    >
                        <div
                            style={{
                                width: 70,
                                height: 70,
                                borderRadius: "50%",
                                background:
                                    "linear-gradient(135deg,#7C3AED,#06B6D4)",
                                marginBottom: 25,
                            }}
                        />

                        <h2>
                            {project.name}
                        </h2>

                        <p
                            style={{
                                color: "#94A3B8",
                                marginTop: 10,
                            }}
                        >
                            {project.id}
                        </p>

                        <p
                            style={{
                                marginTop: 20,
                                color: "#CBD5E1",
                                lineHeight: 1.6,
                            }}
                        >
                            {project.description}
                        </p>

                        <div
                            style={{
                                marginTop: 25,
                                display: "flex",
                                justifyContent:
                                    "space-between",
                            }}
                        >
                            <div>
                                <p
                                    style={{
                                        color:
                                            "#94A3B8",
                                    }}
                                >
                                    Created
                                </p>

                                <p>
                                    {new Date(
                                        project.created_at,
                                    ).toLocaleDateString()}
                                </p>
                            </div>

                            <div
                                style={{
                                    padding:
                                        "8px 16px",
                                    borderRadius:
                                        999,
                                    background:
                                        "rgba(16,185,129,0.2)",
                                    color:
                                        "#10B981",
                                    height:
                                        "fit-content",
                                }}
                            >
                                Active
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {projects?.length === 0 && (
                <div
                    style={{
                        marginTop: 60,
                        textAlign: "center",
                        color: "#94A3B8",
                        fontSize: 20,
                    }}
                >
                    No projects found in database.
                </div>
            )}
        </div>
    );
}

type StatCardProps = {
    title: string;
    value: string;
};

function StatCard({
    title,
    value,
}: StatCardProps) {
    return (
        <div
            style={{
                background:
                    "rgba(255,255,255,0.05)",
                borderRadius: 24,
                padding: 28,
                border:
                    "1px solid rgba(255,255,255,0.08)",
            }}
        >
            <p
                style={{
                    color: "#94A3B8",
                }}
            >
                {title}
            </p>

            <h1
                style={{
                    marginTop: 15,
                    fontSize: 36,
                }}
            >
                {value}
            </h1>
        </div>
    );
}
