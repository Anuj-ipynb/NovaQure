const projects = [
  {
    id: "PRJ-001",
    name: "EGFR Lung Cancer Discovery",
    molecules: 3214,
    experiments: 47,
    status: "Active",
    reliability: "95.2%",
    color: "#6366F1",
  },
  {
    id: "PRJ-002",
    name: "HER2 Breast Cancer Program",
    molecules: 2741,
    experiments: 38,
    status: "Running",
    reliability: "94.1%",
    color: "#8B5CF6",
  },
  {
    id: "PRJ-003",
    name: "KRAS Inhibitor Discovery",
    molecules: 1821,
    experiments: 19,
    status: "Paused",
    reliability: "92.4%",
    color: "#06B6D4",
  },
];

export default function ProjectsPage() {
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
        {[
          ["Projects", "12"],
          ["Running Experiments", "48"],
          ["Generated Molecules", "14,287"],
          ["Reliability", "94.8%"],
        ].map(([title, value]) => (
          <div
            key={title}
            style={{
              background: "rgba(255,255,255,0.05)",
              borderRadius: 24,
              padding: 28,
              border:
                "1px solid rgba(255,255,255,0.08)",
            }}
          >
            <p style={{ color: "#94A3B8" }}>
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
        ))}
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
        {projects.map((project) => (
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
                background: project.color,
                marginBottom: 25,
              }}
            />

            <h2>{project.name}</h2>

            <p
              style={{
                color: "#94A3B8",
                marginTop: 10,
              }}
            >
              {project.id}
            </p>

            <div
              style={{
                marginTop: 25,
              }}
            >
              <p>
                Molecules: {project.molecules}
              </p>

              <p>
                Experiments: {project.experiments}
              </p>

              <p>
                Reliability:
                {" "}
                {project.reliability}
              </p>
            </div>

            <div
              style={{
                marginTop: 25,
                display: "inline-block",
                padding: "8px 16px",
                borderRadius: 999,
                background:
                  "rgba(16,185,129,0.2)",
                color: "#10B981",
              }}
            >
              {project.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
