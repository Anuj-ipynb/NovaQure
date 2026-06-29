import Plot from "react-plotly.js";

export default function PromotionFunnelChart() {
  return (
    <Plot
      data={[
        {
          type: "funnel",
          y: [
            "Generated",
            "Ranked",
            "Promoted",
            "Preclinical",
          ],
          x: [
            14287,
            8231,
            1420,
            327,
          ],
          textinfo:
            "value+percent initial",
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
          l: 80,
          r: 20,
          t: 20,
          b: 40,
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
