import { useState } from "react";
import { useRankings } from "../../hooks/rankings/useRankings";
import MoleculeViewer3D from "../../components/molecules/MoleculeViewer3D";
import ParetoScatterChart from "../../components/charts/ParetoScatterChart";

export default function RankingsPage() {
  const [selectedItem, setSelectedItem] = useState<{ smiles: string; iupacName?: string } | null>(null);
  const { data: rankings, isLoading, error } = useRankings();

  if (isLoading) {
    return (
      <div style={{ padding: "100px 0", textAlign: "center", color: "var(--color-graphite)" }}>
        Loading lead rankings...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "100px 0", textAlign: "center", color: "#ef4444" }}>
        Failed to connect to ranking service.
      </div>
    );
  }

  return (
    <div>
      {/* Editorial Header Opener */}
      <div style={{ marginBottom: 40, borderBottom: "1px solid var(--color-lavender-mist)", paddingBottom: 32 }}>
        <span
          style={{
            fontFamily: "var(--font-gtstandardmono)",
            fontSize: 12,
            textTransform: "uppercase",
            letterSpacing: "0.06em",
            color: "var(--color-graphite)",
            display: "block",
            marginBottom: 12,
          }}
        >
          PRIORITIZATION ENGINE // EXPLAINABLE AI LEADERBOARD
        </span>

        <h1
          style={{
            fontSize: 38,
            fontWeight: 500,
            letterSpacing: "-0.04em",
            color: "var(--color-ink-black)",
            lineHeight: 1.1,
          }}
        >
          Explainable AI{" "}
          <span
            style={{
              background: "var(--color-signal-orange)",
              color: "var(--color-paper-white)",
              padding: "2px 8px",
              borderRadius: 2,
              display: "inline-block",
            }}
          >
            Lead Leaderboard
          </span>
        </h1>
        <p style={{ color: "var(--color-graphite)", marginTop: 10, fontSize: 16 }}>
          Prioritized ranking of candidate drug scaffolds evaluated across bioactivity, QED, SA score, and ZNE reliability.
        </p>
      </div>

      {/* Leaderboard Cards or Empty State Hero Banner */}
      {rankings?.length === 0 ? (
        <div
          style={{
            textAlign: "center",
            padding: "60px 32px",
            background: "var(--color-faint-slate)",
            borderRadius: "var(--radius-cards)",
            border: "1px solid var(--color-lavender-mist)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            gap: 16,
          }}
        >
          <div style={{ fontSize: 36 }}>🏆</div>
          <h2 style={{ fontSize: 22, fontWeight: 600, color: "var(--color-ink-black)" }}>
            Leaderboard Ready
          </h2>
          <p style={{ color: "var(--color-graphite)", fontSize: 15, maxWidth: 520, lineHeight: 1.5 }}>
            No candidates registered in the leaderboard. Execute a discovery run in <strong>Discovery Studio</strong> to generate and rank lead candidates.
          </p>
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 32 }}>
          {/* Bioactivity vs QED Pareto Frontier Scatter Plot */}
          <ParetoScatterChart rankings={rankings || []} />

          {/* Leaderboard Candidate Cards */}
          <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
          {(rankings || []).map((ranking) => {
            const relVal =
              ranking.reliability != null
                ? ranking.reliability > 1.0
                  ? `${ranking.reliability.toFixed(1)}%`
                  : `${(ranking.reliability * 100).toFixed(1)}%`
                : "N/A";

            const affVal =
              ranking.affinity != null ? `${ranking.affinity.toFixed(2)} pIC50` : "N/A";

            const qedVal = ranking.qed != null ? ranking.qed.toFixed(2) : "N/A";
            const saVal = ranking.sa != null ? ranking.sa.toFixed(2) : "N/A";

            return (
              <div
                key={ranking.id}
                onClick={() => setSelectedItem({ smiles: ranking.smiles || "C", iupacName: ranking.iupac_name })}
                style={{
                  background: "var(--color-paper-white)",
                  borderRadius: "var(--radius-cards)",
                  padding: 24,
                  border: "1px solid var(--color-lavender-mist)",
                  cursor: "pointer",
                  transition: "all 0.15s ease",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 16 }}>
                  <div>
                    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                      <span
                        style={{
                          fontFamily: "var(--font-gtstandardmono)",
                          fontSize: 12,
                          fontWeight: 700,
                          color: "var(--color-paper-white)",
                          background: "var(--color-ink-black)",
                          padding: "3px 8px",
                          borderRadius: 4,
                        }}
                      >
                        #{ranking.rank} LEAD
                      </span>
                      <span style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 12, color: "var(--color-graphite)" }}>
                        ID: {ranking.molecule_id?.slice(0, 8)}
                      </span>
                    </div>

                    <h2
                      style={{
                        fontSize: 18,
                        fontWeight: 700,
                        marginTop: 10,
                        color: "var(--color-ink-black)",
                        lineHeight: 1.2,
                      }}
                    >
                      {ranking.iupac_name || "Novel EGFR Candidate"}
                    </h2>
                    <h3
                      style={{
                        fontFamily: "var(--font-gtstandardmono)",
                        fontSize: 13,
                        fontWeight: 500,
                        marginTop: 4,
                        color: "var(--color-graphite)",
                        wordBreak: "break-all",
                      }}
                    >
                      {ranking.smiles || "Generating Structure..."}
                    </h3>
                  </div>

                  <div style={{ textAlign: "right" }}>
                    <span style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 11, textTransform: "uppercase", color: "var(--color-graphite)" }}>
                      Fitness Score
                    </span>
                    <h1
                      style={{
                        fontSize: 36,
                        fontWeight: 700,
                        color: "var(--color-ink-black)",
                        letterSpacing: "-0.04em",
                        marginTop: 2,
                      }}
                    >
                      {ranking.score.toFixed(1)}
                    </h1>
                  </div>
                </div>

                {/* 5-Metric Box Grid */}
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                    gap: 12,
                    marginTop: 20,
                    borderTop: "1px solid var(--color-lavender-mist)",
                    paddingTop: 16,
                  }}
                >
                  <Metric title="Confidence" value={ranking.confidence > 1.0 ? `${ranking.confidence.toFixed(1)}%` : `${(ranking.confidence * 100).toFixed(1)}%`} />
                  <Metric title="Reliability" value={relVal} />
                  <Metric title="Binding Affinity" value={affVal} />
                  <Metric title="QED Index" value={qedVal} />
                  <Metric title="SA Score" value={saVal} />
                </div>
              </div>
            );
          })}
        </div>
        </div>
      )}

      {selectedItem && (
        <MoleculeViewer3D smiles={selectedItem.smiles} iupacName={selectedItem.iupacName} onClose={() => setSelectedItem(null)} />
      )}
    </div>
  );
}

function Metric({ title, value }: { title: string; value: string }) {
  return (
    <div style={{ padding: 12, borderRadius: 4, background: "var(--color-faint-slate)", border: "1px solid var(--color-lavender-mist)" }}>
      <p style={{ color: "var(--color-graphite)", fontSize: 11, fontFamily: "var(--font-gtstandardmono)", textTransform: "uppercase" }}>
        {title}
      </p>
      <h3 style={{ marginTop: 4, fontSize: 14, fontWeight: 700, color: "var(--color-ink-black)", fontFamily: "var(--font-gtstandardmono)" }}>
        {value}
      </h3>
    </div>
  );
}
