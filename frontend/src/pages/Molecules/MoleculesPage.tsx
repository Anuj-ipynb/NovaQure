const molecules = [
  {
    id: "NQ-MOL-001",
    smiles: "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
    affinity: -11.2,
    toxicity: "Low",
    confidence: 96.8,
    reliability: 95.4,
    drugLikeness: 91,
    synth: 88,
    color: "#6366F1",
  },
  {
    id: "NQ-MOL-002",
    smiles: "CN1CCC(CC1)OC2=CC=CC=C2",
    affinity: -10.7,
    toxicity: "Low",
    confidence: 94.2,
    reliability: 93.1,
    drugLikeness: 89,
    synth: 92,
    color: "#06B6D4",
  },
  {
    id: "NQ-MOL-003",
    smiles: "CCN(CC)CCCC(C)NC1=NC=NC2",
    affinity: -12.1,
    toxicity: "Moderate",
    confidence: 92.6,
    reliability: 91.5,
    drugLikeness: 85,
    synth: 83,
    color: "#8B5CF6",
  },
];

export default function MoleculesPage() {
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

      {/* Search */}

      <input
        placeholder="Search by Molecule ID or SMILES..."
        style={{
          width: "100%",
          padding: 18,
          borderRadius: 18,
          border:
            "1px solid rgba(255,255,255,0.08)",
          background:
            "rgba(255,255,255,0.05)",
          color: "white",
          marginBottom: 35,
        }}
      />

      {/* Stats */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {[
          ["Total Molecules", "14,287"],
          ["Top Affinity", "-12.1"],
          ["Avg Confidence", "94.2%"],
          ["Drug Candidates", "327"],
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
                fontSize: 36,
                marginTop: 15,
              }}
            >
              {value}
            </h1>
          </div>
        ))}
      </div>

      {/* Molecules */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fill,minmax(400px,1fr))",
          gap: 30,
        }}
      >
        {molecules.map((mol) => (
          <div
            key={mol.id}
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
            {/* Molecule Graphic */}

            <div
              style={{
                height: 160,
                borderRadius: 20,
                marginBottom: 25,
                background:
                  `linear-gradient(135deg,${mol.color},#0F172A)`,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                fontSize: 48,
                fontWeight: 700,
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
                value={`${mol.affinity}`}
              />

              <Metric
                title="AI Confidence"
                value={`${mol.confidence}%`}
              />

              <Metric
                title="Reliability"
                value={`${mol.reliability}%`}
              />

              <Metric
                title="Drug Likeness"
                value={`${mol.drugLikeness}%`}
              />

              <Metric
                title="Synthetic Score"
                value={`${mol.synth}%`}
              />

              <Metric
                title="Toxicity"
                value={mol.toxicity}
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
