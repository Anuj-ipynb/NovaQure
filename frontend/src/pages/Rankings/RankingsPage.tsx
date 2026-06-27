import { useRankings } from "../../hooks/rankings/useRankings";

const medalColors = [
  "#FFD700",
  "#C0C0C0",
  "#CD7F32",
  "#6366F1",
];

export default function RankingsPage() {
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
          color: "#94A3B8",
          fontSize: 24,
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
          color: "#EF4444",
          fontSize: 24,
        }}
      >
        Failed to connect to ranking service.
      </div>
    );
  }

  const topScore =
    rankings?.length
      ? Math.max(
          ...rankings.map(
            (r) => r.score,
          ),
        ).toFixed(1)
      : "0";

  const avgConfidence =
    rankings?.length
      ? (
          rankings.reduce(
            (sum, item) =>
              sum +
              item.confidence *
                100,
            0,
          ) / rankings.length
        ).toFixed(1)
      : "0";

  return (
    <div>
      {/* Header */}

      <div
        style={{
          display: "flex",
          justifyContent:
            "space-between",
          alignItems: "center",
          marginBottom: 40,
        }}
      >
        <div>
          <h1
            style={{
              fontSize: 44,
              fontWeight: 800,
            }}
          >
            Molecular Ranking Engine
          </h1>

          <p
            style={{
              color: "#94A3B8",
              marginTop: 10,
            }}
          >
            Explainable AI prioritization of candidate molecules.
          </p>
        </div>

        <button
          style={{
            padding:
              "16px 28px",
            borderRadius: 18,
            border: "none",
            background:
              "linear-gradient(90deg,#7C3AED,#4F46E5)",
            color: "white",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          Export Rankings
        </button>
      </div>

      {/* Top Stats */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {[
          [
            "Candidates Ranked",
            (
              rankings?.length ||
              0
            ).toString(),
          ],
          [
            "Top Score",
            topScore,
          ],
          [
            "Avg Confidence",
            `${avgConfidence}%`,
          ],
          [
            "Promotion Rate",
            "2.3%",
          ],
        ].map(
          ([title, value]) => (
            <div
              key={title}
              style={{
                background:
                  "rgba(255,255,255,0.05)",
                borderRadius: 24,
                padding: 28,
                border:
                  "1px solid rgba(255,255,255,0.08)",
              }}
            >
              <p
                style={{
                  color:
                    "#94A3B8",
                }}
              >
                {title}
              </p>

              <h1
                style={{
                  marginTop: 15,
                  fontSize: 38,
                }}
              >
                {value}
              </h1>
            </div>
          ),
        )}
      </div>

      {/* Leaderboard */}

      {rankings?.length ===
      0 ? (
        <div
          style={{
            textAlign:
              "center",
            padding: 80,
            color:
              "#94A3B8",
          }}
        >
          No rankings available.
        </div>
      ) : (
        <div
          style={{
            display: "flex",
            flexDirection:
              "column",
            gap: 24,
          }}
        >
          {rankings?.map(
            (
              ranking,
              index,
            ) => (
              <div
                key={
                  ranking.id
                }
                style={{
                  background:
                    "rgba(255,255,255,0.05)",
                  borderRadius:
                    28,
                  padding: 30,
                  border: `2px solid ${
                    medalColors[
                      index %
                        medalColors.length
                    ]
                  }`,
                }}
              >
                <div
                  style={{
                    display:
                      "flex",
                    justifyContent:
                      "space-between",
                    alignItems:
                      "center",
                  }}
                >
                  <div>
                    <h1
                      style={{
                        color:
                          medalColors[
                            index %
                              medalColors.length
                          ],
                        fontSize: 40,
                      }}
                    >
                      #
                      {
                        ranking.rank
                      }
                    </h1>

                    <h2>
                      {
                        ranking.molecule_id
                      }
                    </h2>

                    <p
                      style={{
                        color:
                          "#94A3B8",
                        marginTop: 10,
                      }}
                    >
                      AI ranked
                      candidate
                      molecule
                    </p>
                  </div>

                  <div
                    style={{
                      textAlign:
                        "right",
                    }}
                  >
                    <h1
                      style={{
                        fontSize: 48,
                        color:
                          medalColors[
                            index %
                              medalColors.length
                          ],
                      }}
                    >
                      {
                        ranking.score
                      }
                    </h1>

                    <p>
                      Composite
                      Score
                    </p>
                  </div>
                </div>

                <div
                  style={{
                    display:
                      "grid",
                    gridTemplateColumns:
                      "repeat(4,1fr)",
                    gap: 18,
                    marginTop: 30,
                  }}
                >
                  <Metric
                    title="Confidence"
                    value={`${(
                      ranking.confidence *
                      100
                    ).toFixed(
                      1,
                    )}%`}
                  />

                  <Metric
                    title="Reliability"
                    value="Pending"
                  />

                  <Metric
                    title="Binding Affinity"
                    value="N/A"
                  />

                  <Metric
                    title="AI Score"
                    value={`${ranking.score}`}
                  />
                </div>
              </div>
            ),
          )}
        </div>
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
        padding: 18,
        borderRadius: 18,
        background:
          "rgba(255,255,255,0.03)",
      }}
    >
      <p
        style={{
          color: "#94A3B8",
          fontSize: 14,
        }}
      >
        {title}
      </p>

      <h3
        style={{
          marginTop: 10,
          fontSize: 24,
        }}
      >
        {value}
      </h3>
    </div>
  );
}
