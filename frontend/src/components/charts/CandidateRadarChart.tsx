import Plot from "react-plotly.js";

type Props = {
  candidates: any[];
};

export default function CandidateRadarChart({ candidates }: Props) {
  const topCandidates = candidates.slice(0, 3);

  const categories = [
    "pIC₅₀ Affinity",
    "QED Drug-Likeness",
    "SA Synthesizability",
    "Quantum Reliability",
    "Lipinski Compliance",
  ];

  const colors = ["#ff4500", "#000000", "#4f46e5"];

  const plotData = topCandidates.map((cand, idx) => {
    const pIC50Norm = Math.min(100, Math.max(0, ((cand.evaluation?.affinity ?? cand.affinity ?? 7.5) / 10.0) * 100));
    const qedNorm = (cand.evaluation?.qed ?? cand.qed ?? 0.75) * 100;
    const saNorm = Math.min(100, Math.max(0, (1.0 - ((cand.evaluation?.sa_score ?? cand.sa ?? 2.5) - 1.0) / 9.0) * 100));
    const relNorm = cand.evaluation?.reliability_score ?? cand.reliability ?? 90.0;
    const lipNorm = cand.evaluation?.lipinski_pass ?? true ? 100 : 50;

    const rValues = [pIC50Norm, qedNorm, saNorm, relNorm, lipNorm];

    return {
      type: "scatterpolar" as const,
      r: [...rValues, rValues[0]],
      theta: [...categories, categories[0]],
      fill: "toself" as const,
      name: cand.iupac_name ? cand.iupac_name.slice(0, 20) + "..." : `Candidate #${idx + 1}`,
      line: { color: colors[idx % colors.length], width: 2 },
      fillcolor: idx === 0 ? "rgba(255, 69, 0, 0.15)" : "rgba(0, 0, 0, 0.05)",
    };
  });

  return (
    <div style={{ background: "var(--color-paper-white)", borderRadius: "var(--radius-cards)", padding: 24, border: "1px solid var(--color-lavender-mist)", marginBottom: 32 }}>
      {/* Header & Explanatory Caption */}
      <div style={{ marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ fontSize: 18, fontWeight: 600, color: "var(--color-ink-black)" }}>
            Multi-Dimensional Lead Candidate Quality Profile
          </h2>
          <span style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 11, background: "var(--color-faint-slate)", border: "1px solid var(--color-lavender-mist)", padding: "2px 8px", borderRadius: 4, color: "var(--color-graphite)" }}>
            5-Axis Radar Analysis
          </span>
        </div>

        {/* Caption explaining What it Shows and Why it is Important */}
        <div style={{ marginTop: 10, padding: 12, borderRadius: 4, background: "var(--color-faint-slate)", border: "1px solid var(--color-lavender-mist)", fontSize: 13, color: "var(--color-ink-black)", lineHeight: 1.4 }}>
          <p style={{ margin: "0 0 4px 0" }}>
            <strong>📌 What this plot shows:</strong> A 5-sided shape showing the overall quality profile of our top candidate molecules across Potency, Safety, Synthesizability, Reliability, and Lipinski Compliance.
          </p>
          <p style={{ margin: 0, color: "var(--color-graphite)" }}>
            <strong>💡 Why it matters:</strong> The larger and more balanced the shape, the better the candidate molecule is across all clinical drug requirements.
          </p>
        </div>
      </div>

      {/* Plotly Radar Chart */}
      <Plot
        data={plotData}
        layout={{
          paper_bgcolor: "rgba(0,0,0,0)",
          font: { family: "GT Standard Mono, monospace", color: "#000000", size: 11 },
          height: 380,
          margin: { l: 60, r: 60, t: 20, b: 30 },
          polar: {
            radialaxis: { visible: true, range: [0, 100], gridcolor: "#e2e9f3" },
            angularaxis: { gridcolor: "#e2e9f3" },
            bgcolor: "rgba(248,250,252,1)",
          },
          legend: { orientation: "h", y: -0.1 },
        }}
        style={{ width: "100%" }}
        config={{ responsive: true, displaylogo: false }}
      />
    </div>
  );
}
