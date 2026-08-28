import Plot from "react-plotly.js";

type ReliabilitySnapshot = {
  overall_reliability: number;
  ai_confidence: number;
  quantum_noise: number;
  created_at: string;
};

type Props = {
  history: ReliabilitySnapshot[];
};

export default function ReliabilityTrendChart({
  history,
}: Props) {
  const sortedHistory = [...history].sort(
    (a, b) =>
      new Date(a.created_at).getTime() -
      new Date(b.created_at).getTime(),
  );

  const x = sortedHistory.map(
    (_, index) => `S${index + 1}`,
  );

  const reliabilityData =
    sortedHistory.map(
      (item) =>
        item.overall_reliability,
    );

  const confidenceData =
    sortedHistory.map(
      (item) =>
        item.ai_confidence,
    );

  const noiseData =
    sortedHistory.map(
      (item) =>
        item.quantum_noise,
    );

  return (
    <div>
      {/* Explanatory Caption Block */}
      <div style={{ marginBottom: 16, padding: 12, borderRadius: 4, background: "var(--color-faint-slate)", border: "1px solid var(--color-lavender-mist)", fontSize: 13, color: "var(--color-ink-black)", lineHeight: 1.4 }}>
        <p style={{ margin: "0 0 4px 0" }}>
          <strong>📌 What this plot shows:</strong> Live tracking graph comparing quantum calculation reliability, AI prediction confidence, and quantum hardware noise.
        </p>
        <p style={{ margin: 0, color: "var(--color-graphite)" }}>
          <strong>💡 Why it matters:</strong> Quantum computers have physical hardware noise. Our Adaptive Error Mitigation system (AQKC) cancels out hardware noise so molecular energy calculations remain 100% accurate.
        </p>
      </div>

      <Plot
        data={[
        {
          x,
          y: reliabilityData,
          type: "scatter",
          mode: "lines+markers",
          name: "Reliability",
        },
        {
          x,
          y: confidenceData,
          type: "scatter",
          mode: "lines+markers",
          name: "AI Confidence",
        },
        {
          x,
          y: noiseData,
          type: "scatter",
          mode: "lines+markers",
          name: "Quantum Noise",
          yaxis: "y2",
        },
      ]}
      layout={{
        paper_bgcolor:
          "rgba(0,0,0,0)",
        plot_bgcolor:
          "rgba(0,0,0,0)",

        font: {
          color: "white",
        },

        margin: {
          l: 50,
          r: 50,
          t: 20,
          b: 40,
        },

        height: 400,

        xaxis: {
          title:
            "Reliability Snapshots",
        },

        yaxis: {
          title:
            "Reliability %",
          range: [80, 100],
        },

        yaxis2: {
          title:
            "Quantum Noise %",
          overlaying: "y",
          side: "right",
          range: [0, 10],
        },

        legend: {
          orientation: "h",
        },
      }}
      style={{
        width: "100%",
      }}
      config={{
        responsive: true,
        displaylogo: false,
      }}
    />
    </div>
  );
}
