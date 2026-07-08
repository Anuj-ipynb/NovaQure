import Plot from "react-plotly.js";

type Props = {
  rankings: {
    confidence: number;
  }[];
};

export default function RankingPieChart({
  rankings,
}: Props) {
  const high =
    rankings.filter(
      (r) =>
        r.confidence >= 0.95,
    ).length;

  const medium =
    rankings.filter(
      (r) =>
        r.confidence >= 0.9 &&
        r.confidence < 0.95,
    ).length;

  const low =
    rankings.length -
    high -
    medium;

  return (
    <Plot
      data={[
        {
          type: "pie",
          labels: [
            "High",
            "Medium",
            "Low",
          ],
          values: [
            high,
            medium,
            low,
          ],
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
