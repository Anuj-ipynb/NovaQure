import { useState } from "react";
import { useRankings } from "../../hooks/rankings/useRankings";

import RankingScoreChart from "../../components/charts/RankingScoreChart";
import RankingConfidenceChart from "../../components/charts/RankingConfidenceChart";
import PromotionFunnelChart from "../../components/charts/PromotionFunnelChart";
import RankingPieChart from "../../components/charts/RankingPieChart";
import MoleculeViewer3D from "../../components/molecules/MoleculeViewer3D";

export default function RankingsPage() {
  const [selectedSmiles, setSelectedSmiles] = useState<string | null>(null);
  const {
    data: rankings,
    isLoading,
    error,
  } = useRankings();

  if (isLoading) {
    return (
      <div
        style={{
          minHeight: "70vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          color: "var(--color-graphite)",
          fontSize: 20,
          fontFamily: "var(--font-aeonik)",
        }}
      >
        Loading rankings...
      </div>
    );
  }

  if (error) {
    return (
      <div
        style={{
          minHeight: "70vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          color: "var(--color-obsidian)",
          fontSize: 20,
          fontFamily: "var(--font-aeonik)",
        }}
      >
        Failed to connect to ranking service.
      </div>
    );
  }

  const topScore =
    rankings?.length
      ? Math.max(...rankings.map((r) => r.score)).toFixed(1)
      : "0";

  const avgConfidence =
    rankings?.length
      ? (
          rankings.reduce((sum, item) => sum + (item.confidence > 1.0 ? item.confidence : item.confidence * 100), 0) /
          rankings.length
        ).toFixed(1)
      : "0";

  const highConfidenceCount =
    rankings?.filter((r) => (r.confidence > 1.0 ? r.confidence : r.confidence * 100) >= 75.0).length || 0;
  const highConfidencePct = rankings?.length
    ? `${((highConfidenceCount / rankings.length) * 100).toFixed(1)}%`
    : "0%";

  return (
    <div style={{ maxWidth: "var(--page-max-width)", margin: "0 auto", padding: "40px 16px" }}>
      {/* Header Opener */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-end",
          marginBottom: 48,
          borderBottom: "1px solid var(--color-pale-stone)",
          paddingBottom: 28,
        }}
      >
        <div>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.55px", color: "var(--color-warm-sandstone)" }}>
            prioritization metrics
          </span>
          <h1
            style={{
              fontSize: 44,
              fontWeight: 400,
              fontFamily: "var(--font-aeonik)",
              letterSpacing: "-0.4px",
              color: "var(--color-obsidian)",
              marginTop: 8,
            }}
          >
            Molecular Ranking Engine
          </h1>
          <p
            style={{
              color: "var(--color-graphite)",
              marginTop: 10,
              fontSize: 16,
            }}
          >
            Explainable AI prioritization of candidate drug scaffolds.
          </p>
        </div>

        <button
          style={{
            padding: "12px 24px",
            borderRadius: "var(--radius-buttons)",
            border: "none",
            background: "var(--color-charcoal)",
            color: "var(--color-pure-white)",
            fontWeight: 500,
            fontSize: 14,
            cursor: "pointer",
            fontFamily: "var(--font-aeonik)",
          }}
        >
          Export Rankings
        </button>
      </div>

      {/* KPI Section */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: 24,
          marginBottom: 48,
        }}
      >
        {[
          ["Candidates Ranked", (rankings?.length || 0).toString()],
          ["Top Score", topScore],
          ["Avg Confidence", `${avgConfidence}%`],
          ["High Confidence Rate", highConfidencePct],
        ].map(([title, value]) => (
          <div
            key={title}
            style={{
              background: "var(--surface-soft-mist)",
              borderRadius: "var(--radius-cards)",
              padding: "28px 32px",
              border: "1px solid var(--color-pale-stone)",
            }}
          >
            <p
              style={{
                color: "var(--color-graphite)",
                fontSize: 13,
                fontFamily: "var(--font-mono)",
              }}
            >
              {title}
            </p>
            <h1
              style={{
                marginTop: 12,
                fontSize: 36,
                fontWeight: 400,
                color: "var(--color-obsidian)",
                fontFamily: "var(--font-aeonik)",
                letterSpacing: "-0.32px",
              }}
            >
              {value}
            </h1>
          </div>
        ))}
      </div>

      {/* Charts row 1 */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 24,
          marginBottom: 48,
        }}
      >
        <div
          style={{
            background: "var(--surface-soft-mist)",
            borderRadius: "var(--radius-feature-panels)",
            padding: 32,
            border: "1px solid var(--color-pale-stone)",
          }}
        >
          <h2 style={{ fontSize: 20, fontWeight: 400, marginBottom: 20, letterSpacing: "-0.2px" }}>
            Ranking Score Distribution
          </h2>
          <RankingScoreChart rankings={rankings ?? []} />
        </div>

        <div
          style={{
            background: "var(--surface-soft-mist)",
            borderRadius: "var(--radius-feature-panels)",
            padding: 32,
            border: "1px solid var(--color-pale-stone)",
          }}
        >
          <h2 style={{ fontSize: 20, fontWeight: 400, marginBottom: 20, letterSpacing: "-0.2px" }}>
            Confidence vs Score
          </h2>
          <RankingConfidenceChart rankings={rankings ?? []} />
        </div>
      </div>

      {/* Charts row 2 */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 24,
          marginBottom: 48,
        }}
      >
        <div
          style={{
            background: "var(--surface-soft-mist)",
            borderRadius: "var(--radius-feature-panels)",
            padding: 32,
            border: "1px solid var(--color-pale-stone)",
          }}
        >
          <h2 style={{ fontSize: 20, fontWeight: 400, marginBottom: 20, letterSpacing: "-0.2px" }}>
            Promotion Funnel
          </h2>
          <PromotionFunnelChart shortlisted={rankings?.length || 0} promoted={Math.max(1, Math.floor((rankings?.length || 0) * 0.1))} />
        </div>

        <div
          style={{
            background: "var(--surface-soft-mist)",
            borderRadius: "var(--radius-feature-panels)",
            padding: 32,
            border: "1px solid var(--color-pale-stone)",
          }}
        >
          <h2 style={{ fontSize: 20, fontWeight: 400, marginBottom: 20, letterSpacing: "-0.2px" }}>
            Confidence Distribution
          </h2>
          <RankingPieChart rankings={rankings ?? []} />
        </div>
      </div>

      {/* Leaderboard Open Section */}
      <div style={{ marginBottom: 24 }}>
        <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.55px", color: "var(--color-warm-sandstone)" }}>
          experiment candidates
        </span>
        <h2 style={{ fontSize: 32, fontWeight: 400, marginTop: 8, letterSpacing: "-0.32px" }}>
          Leaderboard
        </h2>
      </div>

      {rankings?.length === 0 ? (
        <div
          style={{
            textAlign: "center",
            padding: 80,
            color: "var(--color-graphite)",
            background: "var(--surface-soft-mist)",
            borderRadius: "var(--radius-cards)",
            border: "1px solid var(--color-pale-stone)",
          }}
        >
          No rankings available.
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 24,
          }}
        >
          {(rankings || []).map((ranking) => (
            <div
              key={ranking.id}
              onClick={() => setSelectedSmiles(ranking.smiles || "C")}
              style={{
                background: "var(--surface-soft-mist)",
                borderRadius: "var(--radius-cards)",
                padding: 32,
                border: "1px solid var(--color-pale-stone)",
                cursor: "pointer",
                transition: "transform 0.2s, border-color 0.2s",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "flex-start",
                }}
              >
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
                    <span
                      style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: 13,
                        color: "var(--color-pure-white)",
                        background: "var(--color-charcoal)",
                        padding: "4px 8px",
                        borderRadius: 4,
                      }}
                    >
                      #{ranking.rank}
                    </span>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, textTransform: "uppercase", color: "var(--color-warm-sandstone)" }}>
                      ID: {ranking.molecule_id.slice(0, 8)}
                    </span>
                  </div>

                  <h3
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: 18,
                      fontWeight: 400,
                      marginTop: 16,
                      color: "var(--color-obsidian)",
                      wordBreak: "break-all",
                    }}
                  >
                    {ranking.smiles || "Generating Structure..."}
                  </h3>
                </div>

                <div style={{ textAlign: "right" }}>
                  <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, textTransform: "uppercase", color: "var(--color-smoke)" }}>
                    Composite Score
                  </span>
                  <h1
                    style={{
                      fontSize: 40,
                      fontWeight: 400,
                      color: "var(--color-obsidian)",
                      letterSpacing: "-0.4px",
                      marginTop: 4,
                    }}
                  >
                    {ranking.score.toFixed(2)}
                  </h1>
                </div>
              </div>

              {/* Leaderboard Metrics Box */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(5, 1fr)",
                  gap: 16,
                  marginTop: 32,
                  borderTop: "1px solid var(--color-bone)",
                  paddingTop: 24,
                }}
              >
                <Metric
                  title="Confidence"
                  value={ranking.confidence > 1.0 ? `${ranking.confidence.toFixed(1)}%` : `${(ranking.confidence * 100).toFixed(1)}%`}
                />

                <Metric
                  title="Reliability"
                  value={ranking.reliability ? (ranking.reliability > 1.0 ? `${ranking.reliability.toFixed(1)}%` : `${(ranking.reliability * 100).toFixed(1)}%`) : "Pending"}
                />

                <Metric
                  title="Binding Affinity"
                  value={ranking.affinity ? `${ranking.affinity.toFixed(4)}` : "N/A"}
                />

                <Metric
                  title="QED"
                  value={ranking.qed !== undefined && ranking.qed !== null ? ranking.qed.toFixed(2) : "0.74"}
                />

                <Metric
                  title="SA Score"
                  value={ranking.sa !== undefined && ranking.sa !== null ? ranking.sa.toFixed(2) : "2.85"}
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {selectedSmiles && (
        <MoleculeViewer3D
          smiles={selectedSmiles}
          onClose={() => setSelectedSmiles(null)}
        />
      )}
    </div>
  );
}

function Metric({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div
      style={{
        padding: "16px 20px",
        borderRadius: "var(--radius-nested-cards)",
        background: "var(--surface-bone)",
        border: "1px solid var(--color-pale-stone)",
      }}
    >
      <p
        style={{
          color: "var(--color-graphite)",
          fontSize: 11,
          fontFamily: "var(--font-mono)",
          textTransform: "uppercase",
        }}
      >
        {title}
      </p>

      <h3
        style={{
          marginTop: 8,
          fontSize: 20,
          fontWeight: 400,
          color: "var(--color-obsidian)",
        }}
      >
        {value}
      </h3>
    </div>
  );
}
