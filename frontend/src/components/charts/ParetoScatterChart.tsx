import Plot from "react-plotly.js";
import type { Ranking } from "../../types/models/ranking";

type Props = {
  rankings: Ranking[];
};

export default function ParetoScatterChart({ rankings }: Props) {
  const validRankings = rankings.filter(
    (r) => r.affinity !== undefined && r.qed !== undefined
  );

  const xData = validRankings.map((r) => r.affinity ?? 7.5);
  const yData = validRankings.map((r) => r.qed ?? 0.7);
  const textData = validRankings.map(
    (r) =>
      `Rank #${r.rank}<br>IUPAC: ${r.iupac_name || "Novel Candidate"}<br>pIC50: ${(r.affinity ?? 0).toFixed(2)}<br>QED: ${(r.qed ?? 0).toFixed(2)}`
  );

  return (
    <div style={{ background: "var(--color-paper-white)", borderRadius: "var(--radius-cards)", padding: 24, border: "1px solid var(--color-lavender-mist)" }}>
      {/* Header & Explanatory Caption */}
      <div style={{ marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ fontSize: 18, fontWeight: 600, color: "var(--color-ink-black)" }}>
            Bioactivity vs. Drug-Likeness (Pareto Frontier)
          </h2>
          <span style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 11, background: "var(--color-faint-slate)", border: "1px solid var(--color-lavender-mist)", padding: "2px 8px", borderRadius: 4, color: "var(--color-graphite)" }}>
            Pareto Quadrant Analysis
          </span>
        </div>

        {/* Caption explaining What it Shows and Why it is Important */}
        <div style={{ marginTop: 10, padding: 12, borderRadius: 4, background: "var(--color-faint-slate)", border: "1px solid var(--color-lavender-mist)", fontSize: 13, color: "var(--color-ink-black)", lineHeight: 1.4 }}>
          <p style={{ margin: "0 0 4px 0" }}>
            <strong>📌 What this plot shows:</strong> Compares how strongly each molecule binds to the target cancer protein (X-axis) versus how safe and drug-like it is (Y-axis).
          </p>
          <p style={{ margin: 0, color: "var(--color-graphite)" }}>
            <strong>💡 Why it matters:</strong> The highlighted top-right section is the best zone. Candidates in this area bind tightly to the target protein while staying safe and easy for the body to absorb.
          </p>
        </div>
      </div>

      {/* Plotly Chart */}
      <Plot
        data={[
          {
            x: xData,
            y: yData,
            mode: "markers+text",
            type: "scatter",
            hoverinfo: "text",
            hovertext: textData,
            marker: {
              size: 12,
              color: xData.map((xVal, idx) => {
                const yVal = yData[idx];
                return xVal >= 8.0 && yVal >= 0.6 ? "#ff4500" : "#000000";
              }),
              opacity: 0.85,
              line: { width: 1, color: "#000000" },
            },
          },
        ]}
        layout={{
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(248,250,252,1)",
          font: { family: "GT Standard Mono, monospace", color: "#000000", size: 12 },
          height: 360,
          margin: { l: 50, r: 30, t: 20, b: 50 },
          xaxis: {
            title: "Binding Affinity (pIC₅₀)",
            gridcolor: "#e2e9f3",
            zerolinecolor: "#e2e9f3",
          },
          yaxis: {
            title: "Drug-Likeness (QED Index)",
            range: [0.3, 1.0],
            gridcolor: "#e2e9f3",
            zerolinecolor: "#e2e9f3",
          },
          shapes: [
            // Sweet spot quadrant shading
            {
              type: "rect",
              xref: "x",
              yref: "y",
              x0: 8.0,
              y0: 0.6,
              x1: Math.max(...xData, 12),
              y1: 1.0,
              fillcolor: "rgba(255, 69, 0, 0.08)",
              line: { width: 1, color: "#ff4500", dash: "dot" },
            },
          ],
        }}
        style={{ width: "100%" }}
        config={{ responsive: true, displaylogo: false }}
      />
    </div>
  );
}
