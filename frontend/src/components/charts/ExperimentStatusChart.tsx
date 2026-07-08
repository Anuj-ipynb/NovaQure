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
  );
}
