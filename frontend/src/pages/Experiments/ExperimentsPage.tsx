const experiments = [
  {
    id: "EXP-1042",
    protein: "EGFR",
    status: "Running",
    progress: 73,
    molecules: 421,
    node: "Quantum-01",
  },
  {
    id: "EXP-1043",
    protein: "HER2",
    status: "Running",
    progress: 51,
    molecules: 312,
    node: "Quantum-02",
  },
  {
    id: "EXP-1044",
    protein: "KRAS",
    status: "Queued",
    progress: 0,
    molecules: 0,
    node: "Waiting",
  },
  {
    id: "EXP-1045",
    protein: "BRAF",
    status: "Completed",
    progress: 100,
    molecules: 923,
    node: "Quantum-01",
  },
];

export default function ExperimentsPage() {
  return (
    <div>
      {/* Header */}

      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
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
            Experiment Control Center
          </h1>

          <p
            style={{
              color: "#94A3B8",
              marginTop: 10,
            }}
          >
            Monitor AI and Quantum optimization runs.
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
          + Launch Experiment
        </button>
      </div>

      {/* Top Cards */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {[
          ["Running", "18"],
          ["Queued", "7"],
          ["Completed", "124"],
          ["Success Rate", "94.2%"],
        ].map(([title, value]) => (
          <div
            key={title}
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
                fontSize: 36,
                marginTop: 15,
              }}
            >
              {value}
            </h1>
          </div>
        ))}
      </div>

      {/* Main Grid */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "2fr 1fr",
          gap: 24,
        }}
      >
        {/* Table */}

        <div
          style={{
            background:
              "rgba(255,255,255,0.05)",
            borderRadius: 28,
            padding: 30,
            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h2
            style={{
              marginBottom: 25,
            }}
          >
            Active Experiments
          </h2>

          <table
            style={{
              width: "100%",
            }}
          >
            <thead>
              <tr>
                <th align="left">
                  Experiment
                </th>
                <th align="left">
                  Protein
                </th>
                <th align="left">
                  Status
                </th>
                <th align="left">
                  Progress
                </th>
              </tr>
            </thead>

            <tbody>
              {experiments.map((exp) => (
                <tr
                  key={exp.id}
                  style={{
                    height: 90,
                  }}
                >
                  <td>{exp.id}</td>

                  <td>
                    {exp.protein}
                  </td>

                  <td>
                    <div
                      style={{
                        display:
                          "inline-block",
                        padding:
                          "8px 14px",
                        borderRadius:
                          999,
                        background:
                          exp.status ===
                          "Running"
                            ? "rgba(16,185,129,0.2)"
                            : exp.status ===
                              "Completed"
                            ? "rgba(99,102,241,0.2)"
                            : "rgba(251,191,36,0.2)",
                      }}
                    >
                      {exp.status}
                    </div>
                  </td>

                  <td>
                    <div
                      style={{
                        width: 180,
                        height: 12,
                        background:
                          "#1E293B",
                        borderRadius:
                          999,
                      }}
                    >
                      <div
                        style={{
                          width:
                            `${exp.progress}%`,
                          height:
                            "100%",
                          borderRadius:
                            999,
                          background:
                            "linear-gradient(90deg,#06B6D4,#7C3AED)",
                        }}
                      />
                    </div>

                    <p
                      style={{
                        marginTop: 8,
                      }}
                    >
                      {exp.progress}%
                    </p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* System Panel */}

        <div
          style={{
            display: "flex",
            flexDirection:
              "column",
            gap: 24,
          }}
        >
          {/* GPU */}

          <div
            style={{
              background:
                "rgba(255,255,255,0.05)",
              borderRadius: 28,
              padding: 28,
              border:
                "1px solid rgba(255,255,255,0.08)",
            }}
          >
            <h2>GPU Cluster</h2>

            <h1
              style={{
                fontSize: 48,
                marginTop: 20,
                color: "#06B6D4",
              }}
            >
              71%
            </h1>

            <p
              style={{
                color: "#94A3B8",
              }}
            >
              Utilization
            </p>
          </div>

          {/* Quantum */}

          <div
            style={{
              background:
                "rgba(255,255,255,0.05)",
              borderRadius: 28,
              padding: 28,
              border:
                "1px solid rgba(255,255,255,0.08)",
            }}
          >
            <h2>Quantum Nodes</h2>

            <h1
              style={{
                fontSize: 48,
                marginTop: 20,
                color: "#8B5CF6",
              }}
            >
              2 / 4
            </h1>

            <p
              style={{
                color: "#94A3B8",
              }}
            >
              Nodes Active
            </p>
          </div>

          {/* AI Agents */}

          <div
            style={{
              background:
                "rgba(255,255,255,0.05)",
              borderRadius: 28,
              padding: 28,
              border:
                "1px solid rgba(255,255,255,0.08)",
            }}
          >
            <h2>AI Agents</h2>

            <p
              style={{
                marginTop: 20,
                color: "#10B981",
              }}
            >
              ● Generator Agent Online
            </p>

            <p
              style={{
                marginTop: 10,
                color: "#10B981",
              }}
            >
              ● Ranking Agent Online
            </p>

            <p
              style={{
                marginTop: 10,
                color: "#10B981",
              }}
            >
              ● Reliability Agent Online
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
