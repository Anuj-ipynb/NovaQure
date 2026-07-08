import Plot from "react-plotly.js";

type Ranking = {
  molecule_id: string;
  score: number;
  confidence: number;
};

type Props = {
  rankings: Ranking[];
};

export default function RankingConfidenceChart({
  rankings,
}: Props) {
  return (
    <Plot
      data={[
        {
          x: rankings.map(
            (r) => r.confidence * 100
          ),
          y: rankings.map(
            (r) => r.score
          ),
          text: rankings.map(
            (r) => r.molecule_id
          ),
          mode: "markers+text",
          type: "scatter",
          textposition: "top center",
          name: "Molecules",
        },
      ]}
      layout={{
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
          color: "white",
        },
        height: 400,
        margin: {
          l: 50,
          r: 20,
          t: 20,
          b: 50,
        },
        xaxis: {
          title: "Confidence (%)",
        },
        yaxis: {
          title: "Composite Score",
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
  );
}
