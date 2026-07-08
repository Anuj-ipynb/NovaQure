import Plot from "react-plotly.js";

type Props = {
  shortlisted: number;
  promoted: number;
};

export default function PromotionFunnelChart({
  shortlisted,
  promoted,
}: Props) {
  return (
    <Plot
      data={[
        {
          type: "funnel",
          y: [
            "Ranked Molecules",
            "Shortlisted",
            "Promoted",
          ],
          x: [
            shortlisted * 2,
            shortlisted,
            promoted,
          ],
        },
      ]}
      layout={{
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: {
          color: "white",
        },
        margin: {
          l: 40,
          r: 20,
          t: 20,
          b: 40,
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
