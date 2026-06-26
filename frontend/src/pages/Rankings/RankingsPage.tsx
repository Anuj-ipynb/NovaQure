const rankings = [
  {
    rank: 1,
    molecule: "NQ-MOL-001",
    score: 98.7,
    confidence: 96.2,
    reliability: 95.7,
    affinity: -12.1,
    recommendation: "Advance to preclinical screening",
    color: "#FFD700",
  },
  {
    rank: 2,
    molecule: "NQ-MOL-002",
    score: 96.8,
    confidence: 94.1,
    reliability: 94.0,
    affinity: -11.7,
    recommendation: "Further optimization suggested",
    color: "#C0C0C0",
  },
  {
    rank: 3,
    molecule: "NQ-MOL-003",
    score: 94.5,
    confidence: 92.8,
    reliability: 91.6,
    affinity: -11.2,
    recommendation: "Retain in candidate pool",
    color: "#CD7F32",
  },
  {
    rank: 4,
    molecule: "NQ-MOL-004",
    score: 92.4,
    confidence: 90.3,
    reliability: 89.8,
    affinity: -10.8,
    recommendation: "Monitor",
    color: "#6366F1",
  },
];
export default function RankingsPage() {
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
              fontSize: 44,
              fontWeight: 800,
            }}
          >
            Molecular Ranking Engine
          </h1>

          <p
            style={{
              color: "#94A3B8",
              marginTop: 10,
            }}
          >
            Explainable AI prioritization of candidate molecules.
          </p>
        </div>

        <button
          style={{
            padding: "16px 28px",
            borderRadius: 18,
            border: "none",
            background:
              "linear-gradient(90deg,#7C3AED,#4F46E5)",
            color: "white",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          Export Rankings
        </button>
      </div>

      {/* Top Stats */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {[
          ["Candidates Ranked", "14,287"],
          ["Top Score", "98.7"],
          ["Avg Confidence", "94.2%"],
          ["Promotion Rate", "2.3%"],
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
            <p style={{ color: "#94A3B8" }}>
              {title}
            </p>

            <h1
              style={{
                marginTop: 15,
                fontSize: 38,
              }}
            >
              {value}
            </h1>
          </div>
        ))}
      </div>

      {/* Leaderboard */}

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 24,
        }}
      >
        {rankings.map((mol) => (
          <div
            key={mol.molecule}
            style={{
              background:
                "rgba(255,255,255,0.05)",
              borderRadius: 28,
              padding: 30,
              border:
                `2px solid ${mol.color}`,
            }}
          >
            <div
              style={{
                display: "flex",
                justifyContent:
                  "space-between",
                alignItems: "center",
              }}
            >
              <div>
                <h1
                  style={{
                    color: mol.color,
                    fontSize: 40,
                  }}
                >
                  #{mol.rank}
                </h1>

                <h2>
                  {mol.molecule}
                </h2>

                <p
                  style={{
                    color: "#94A3B8",
                    marginTop: 10,
                  }}
                >
                  {mol.recommendation}
                </p>
              </div>

              <div
                style={{
                  textAlign: "right",
                }}
              >
                <h1
                  style={{
                    fontSize: 48,
                    color: mol.color,
                  }}
                >
                  {mol.score}
                </h1>

                <p>Composite Score</p>
              </div>
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(4,1fr)",
                gap: 18,
                marginTop: 30,
              }}
            >
              <Metric
                title="Confidence"
                value={`${mol.confidence}%`}
              />

              <Metric
                title="Reliability"
                value={`${mol.reliability}%`}
              />

              <Metric
                title="Binding Affinity"
                value={`${mol.affinity}`}
              />

              <Metric
                title="AI Score"
                value={`${mol.score}`}
              />
            </div>
          </div>
        ))}
      </div>
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
        padding: 18,
        borderRadius: 18,
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
          marginTop: 10,
          fontSize: 24,
        }}
      >
        {value}
      </h3>
    </div>
  );
}
