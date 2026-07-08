import Plot from "react-plotly.js";

type Ranking = {
  rank: number;
  score: number;
  molecule_id: string;
};

type Props = {
  rankings: Ranking[];
};

export default function RankingScoreChart({
  rankings,
}: Props) {
  return (
    <Plot
      data={[
        {
          x: rankings.map(
            (r) => r.molecule_id,
          ),
          y: rankings.map(
            (r) => r.score,
          ),
          type: "bar",
          name: "Score",
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
        height: 400,
        margin: {
          l: 50,
          r: 20,
          t: 20,
          b: 80,
        },
        xaxis: {
          title: "Molecule",
        },
        yaxis: {
          title:
            "Composite Score",
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
