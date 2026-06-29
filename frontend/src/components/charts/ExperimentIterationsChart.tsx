import Plot from "react-plotly.js";

type Experiment = {
  target_protein: string;
  iterations: number;
};

type Props = {
  experiments: Experiment[];
};

export default function ExperimentIterationsChart({
  experiments,
}: Props) {
  return (
    <Plot
      data={[
        {
          x: experiments.map(
            (e) => e.target_protein
          ),
          y: experiments.map(
            (e) => e.iterations
          ),
          type: "bar",
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
