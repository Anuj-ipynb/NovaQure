import Plot from "react-plotly.js";

type Experiment = {
  status: string;
};

type Props = {
  experiments: Experiment[];
};

export default function ExperimentStatusChart({
  experiments,
}: Props) {
  const running = experiments.filter(
    (e) => e.status === "running"
  ).length;

  const queued = experiments.filter(
    (e) => e.status === "queued"
  ).length;

  const completed = experiments.filter(
    (e) => e.status === "completed"
  ).length;

  return (
    <div>
      {/* Explanatory Caption Block */}
      <div style={{ marginBottom: 16, padding: 12, borderRadius: 4, background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)", fontSize: 13, color: "#94A3B8", lineHeight: 1.4 }}>
        <p style={{ margin: "0 0 4px 0", color: "#FFFFFF" }}>
          <strong>📌 What this shows:</strong> Proportional breakdown of active, queued, and completed generative drug discovery experiments.
        </p>
        <p style={{ margin: 0 }}>
          <strong>💡 Why it's important:</strong> Monitors queue throughput and ensures zero execution bottlenecks across concurrent optimization runs.
        </p>
      </div>

      <Plot
      data={[
        {
          type: "pie",
          labels: [
            "Running",
            "Queued",
            "Completed",
          ],
          values: [
            running,
            queued,
            completed,
          ],
        },
      ]}
      layout={{
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
          color: "white",
        },
        height: 350,
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
