const stats = [
  {
    title: "Active Projects",
    value: "12",
    color: "#6366F1",
    change: "+18%",
  },
  {
    title: "Experiments Running",
    value: "48",
    color: "#06B6D4",
    change: "+11%",
  },
  {
    title: "Generated Molecules",
    value: "14,287",
    color: "#8B5CF6",
    change: "+27%",
  },
  {
    title: "Reliability Score",
    value: "94.8%",
    color: "#10B981",
    change: "+2.1%",
  },
];

const experiments = [
  {
    id: "EXP-1042",
    protein: "EGFR",
    status: "Running",
    progress: "73%",
  },
  {
    id: "EXP-1043",
    protein: "HER2",
    status: "Running",
    progress: "51%",
  },
  {
    id: "EXP-1044",
    protein: "KRAS",
    status: "Queued",
    progress: "0%",
  },
];

const molecules = [
  {
    id: "MOL-991",
    score: 98.1,
    confidence: 95.2,
  },
  {
    id: "MOL-992",
    score: 97.4,
    confidence: 94.1,
  },
  {
    id: "MOL-993",
    score: 96.8,
    confidence: 93.8,
  },
];

export default function DashboardPage() {
  return (
    <div>
      <h1
        style={{
          fontSize: 42,
          marginBottom: 10,
        }}
      >
        NovaQure Research Dashboard
      </h1>

      <p
        style={{
          color: "#94A3B8",
          marginBottom: 40,
        }}
      >
        AI + Quantum Molecular Discovery Platform
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {stats.map((card) => (
          <div
            key={card.title}
            style={{
              background: "rgba(255,255,255,0.05)",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: 24,
              padding: 30,
              backdropFilter: "blur(20px)",
            }}
          >
            <p
              style={{
                color: "#94A3B8",
              }}
            >
              {card.title}
            </p>

            <h1
              style={{
                fontSize: 42,
                marginTop: 18,
                color: card.color,
              }}
            >
              {card.value}
            </h1>

            <p
              style={{
                marginTop: 15,
                color: "#10B981",
              }}
            >
              {card.change} this month
            </p>
          </div>
        ))}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: 24,
        }}
      >
        <div
          style={{
            background: "rgba(255,255,255,0.05)",
            borderRadius: 24,
            padding: 30,
            border: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h2>Active Experiments</h2>

          <table
            style={{
              width: "100%",
              marginTop: 25,
            }}
          >
            <thead>
              <tr>
                <th align="left">Experiment</th>
                <th align="left">Protein</th>
                <th align="left">Status</th>
                <th align="left">Progress</th>
              </tr>
            </thead>

            <tbody>
              {experiments.map((exp) => (
                <tr key={exp.id}>
                  <td>{exp.id}</td>
                  <td>{exp.protein}</td>
                  <td>{exp.status}</td>
                  <td>{exp.progress}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div
          style={{
            background: "rgba(255,255,255,0.05)",
            borderRadius: 24,
            padding: 30,
            border: "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h2>Top Molecules</h2>

          {molecules.map((molecule) => (
            <div
              key={molecule.id}
              style={{
                marginTop: 25,
                paddingBottom: 20,
                borderBottom:
                  "1px solid rgba(255,255,255,0.05)",
              }}
            >
              <h3>{molecule.id}</h3>

              <p>Score: {molecule.score}</p>

              <p>
                Confidence:
                {" "}
                {molecule.confidence}%
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
