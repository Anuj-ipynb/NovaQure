import { useExperiments } from "../../hooks/experiments/useExperiments";

import ExperimentStatusChart from "../../components/charts/ExperimentStatusChart";
import ExperimentIterationsChart from "../../components/charts/ExperimentIterationsChart";

export default function ExperimentsPage() {
  const {
    data: experiments,
    isLoading,
    error,
  } = useExperiments();

  if (isLoading) {
    return (
      <div
        style={{
          minHeight: "70vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: 24,
          color: "#94A3B8",
        }}
      >
        Loading experiments...
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
          fontSize: 24,
          color: "#EF4444",
        }}
      >
        Failed to connect to experiment service.
      </div>
    );
  }

  const running =
    experiments?.filter(
      (e) => e.status === "running"
    ).length || 0;

  const queued =
    experiments?.filter(
      (e) => e.status === "queued"
    ).length || 0;

  const completed =
    experiments?.filter(
      (e) => e.status === "completed"
    ).length || 0;

  const avgIterations =
    experiments?.length
      ? Math.round(
          experiments.reduce(
            (sum, e) =>
              sum + e.iterations,
            0,
          ) / experiments.length,
        )
      : 0;

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
              fontSize: 42,
              fontWeight: 800,
            }}
          >
            Experiment Control Center
          </h1>

          <p
            style={{
              color: "#94A3B8",
              marginTop: 10,
            }}
          >
            Monitor AI and Quantum optimization runs.
          </p>
        </div>

        <button
          style={{
            padding: "16px 28px",
            border: "none",
            borderRadius: 18,
            background:
              "linear-gradient(90deg,#7C3AED,#4F46E5)",
            color: "white",
            fontWeight: 700,
            cursor: "pointer",
          }}
        >
          + Launch Experiment
        </button>
      </div>

      {/* KPI Cards */}

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
            "Running",
            running.toString(),
          ],
          [
            "Queued",
            queued.toString(),
          ],
          [
            "Completed",
            completed.toString(),
          ],
          [
            "Avg Iterations",
            avgIterations.toString(),
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
                  fontSize: 36,
                  marginTop: 15,
                }}
              >
                {value}
              </h1>
            </div>
          ),
        )}
      </div>

      {/* Analytics */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "1fr 1fr",
          gap: 24,
          marginBottom: 40,
        }}
      >
        <div
          style={{
            background:
              "rgba(255,255,255,0.05)",
            borderRadius: 28,
            padding: 30,
            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h2
            style={{
              marginBottom: 20,
            }}
          >
            Experiment Status Distribution
          </h2>

          <ExperimentStatusChart
            experiments={
              experiments ?? []
            }
          />
        </div>

        <div
          style={{
            background:
              "rgba(255,255,255,0.05)",
            borderRadius: 28,
            padding: 30,
            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h2
            style={{
              marginBottom: 20,
            }}
          >
            Optimization Iterations
          </h2>

          <ExperimentIterationsChart
            experiments={
              experiments ?? []
            }
          />
        </div>
      </div>

      {/* Main Grid */}

      <div>
        {/* Experiment Table */}

        <div
          style={{
            background:
              "rgba(255,255,255,0.05)",
            borderRadius: 28,
            padding: 30,
            border:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <h2
            style={{
              marginBottom: 25,
            }}
          >
            Active Experiments
          </h2>

          {experiments?.length ===
          0 ? (
            <div
              style={{
                textAlign:
                  "center",
                padding: 50,
                color:
                  "#94A3B8",
              }}
            >
              No experiments found.
            </div>
          ) : (
            <table
              style={{
                width: "100%",
              }}
            >
              <thead>
                <tr>
                  <th align="left">
                    ID
                  </th>
                  <th align="left">
                    Protein Target
                  </th>
                  <th align="left">
                    Iterations
                  </th>
                  <th align="left">
                    Status
                  </th>
                </tr>
              </thead>

              <tbody>
                {experiments?.map(
                  (exp) => (
                    <tr
                      key={
                        exp.id
                      }
                      style={{
                        height: 70,
                        borderBottom: "1px solid rgba(255,255,255,0.05)",
                      }}
                    >
                      <td style={{ fontFamily: "monospace" }}>
                        {exp.id.slice(
                          0,
                          12,
                        )}...
                      </td>

                      <td style={{ fontWeight: 600 }}>
                        {
                          exp.target_protein
                        }
                      </td>

                      <td>
                        {
                          exp.iterations
                        }
                      </td>

                      <td>
                        <div
                          style={{
                            display:
                              "inline-block",
                            padding:
                              "6px 14px",
                            borderRadius:
                              999,
                            background:
                              exp.status ===
                              "running"
                                ? "rgba(16,185,129,0.2)"
                                : exp.status ===
                                  "completed"
                                ? "rgba(99,102,241,0.2)"
                                : "rgba(251,191,36,0.2)",
                            color:
                              exp.status ===
                              "running"
                                ? "#34D399"
                                : exp.status ===
                                  "completed"
                                ? "#818CF8"
                                : "#FBBF24",
                            fontSize: 13,
                            fontWeight: 600,
                          }}
                        >
                          {
                            exp.status
                          }
                        </div>
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
