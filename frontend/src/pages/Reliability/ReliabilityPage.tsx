import { useReliability } from "../../hooks/reliability/useReliability";
import ReliabilityTrendChart from "../../components/charts/ReliabilityTrendChart";

function getStatusColor(status: string) {
  if (status === "Operational") return "#10B981";
  if (status === "Monitoring") return "#F59E0B";
  return "#EF4444";
}

export default function ReliabilityPage() {
  const {
    data,
    isLoading,
    error,
  } = useReliability();

  const reliability = data?.[0];

  if (isLoading) {
    return (
      <div
        style={{
          padding: 50,
          color: "white",
        }}
      >
        Loading reliability metrics...
      </div>
    );
  }

  if (
    error ||
    !reliability
  ) {
    return (
      <div
        style={{
          padding: 50,
          color: "#EF4444",
        }}
      >
        Failed to load reliability data.
      </div>
    );
  }

  const metrics = [
    {
      title: "NQRE Reliability",
      value: `${reliability.overall_reliability}%`,
      color: "#10B981",
      description:
        "Overall platform trust score",
    },
    {
      title: "AI Confidence",
      value: `${reliability.ai_confidence}%`,
      color: "#06B6D4",
      description:
        "Prediction confidence level",
    },
    {
      title: "Quantum Noise",
      value: `${reliability.quantum_noise}%`,
      color: "#F59E0B",
      description:
        "Measured quantum disturbance",
    },
    {
      title: "AQKC Corrections",
      value: `${reliability.aqkc_corrections}`,
      color: "#8B5CF6",
      description:
        "Adaptive corrections applied",
    },
  ];

  const systems = [
    {
      name: "Reliability Engine",
      status:
        reliability.reliability_engine_status,
    },
    {
      name: "Noise Estimator",
      status:
        reliability.noise_estimator_status,
    },
    {
      name: "AQKC Module",
      status:
        reliability.aqkc_module_status,
    },
    {
      name: "Calibration Layer",
      status:
        reliability.calibration_layer_status,
    },
  ];

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
            Reliability Intelligence Center
          </h1>

          <p
            style={{
              color: "#94A3B8",
              marginTop: 10,
            }}
          >
            Trust calibration and uncertainty
            quantification.
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
          Export Reliability Report
        </button>
      </div>

      {/* Metric Cards */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {metrics.map(
          (metric) => (
            <div
              key={metric.title}
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
                  color: "#94A3B8",
                }}
              >
                {metric.title}
              </p>

              <h1
                style={{
                  marginTop: 15,
                  fontSize: 42,
                  color: metric.color,
                }}
              >
                {metric.value}
              </h1>

              <p
                style={{
                  marginTop: 15,
                  color: "#94A3B8",
                }}
              >
                {metric.description}
              </p>
            </div>
          )
        )}
      </div>

      {/* System Status + Chart */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "1fr 2fr",
          gap: 24,
        }}
      >
        {/* System Status */}

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
            Subsystem Status
          </h2>

          {systems.map(
            (system) => (
              <div
                key={system.name}
                style={{
                  marginTop: 25,
                  paddingBottom: 20,
                  borderBottom:
                    "1px solid rgba(255,255,255,0.05)",
                }}
              >
                <h3>
                  {system.name}
                </h3>

                <p
                  style={{
                    marginTop: 8,
                    color:
                      getStatusColor(
                        system.status
                      ),
                  }}
                >
                  ● {system.status}
                </p>
              </div>
            )
          )}
        </div>

        {/* Real Historical Chart */}

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
            Reliability Trends
          </h2>

          <ReliabilityTrendChart
            history={data ?? []}
          />
        </div>
      </div>

      {/* Explainability */}

      <div
        style={{
          marginTop: 30,
          background:
            "rgba(255,255,255,0.05)",
          borderRadius: 28,
          padding: 30,
          border:
            "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <h2>
          Explainability Summary
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(3,1fr)",
            gap: 24,
            marginTop: 25,
          }}
        >
          <InfoCard
            title="Confidence Calibration"
            value={`${reliability.confidence_calibration}%`}
          />

          <InfoCard
            title="Noise Compensation"
            value={`${reliability.noise_compensation}%`}
          />

          <InfoCard
            title="Prediction Stability"
            value={`${reliability.prediction_stability}%`}
          />
        </div>
      </div>
    </div>
  );
}

function InfoCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div
      style={{
        padding: 22,
        borderRadius: 20,
        background:
          "rgba(255,255,255,0.03)",
      }}
    >
      <p
        style={{
          color: "#94A3B8",
        }}
      >
        {title}
      </p>

      <h2
        style={{
          marginTop: 10,
          color: "#7C3AED",
        }}
      >
        {value}
      </h2>
    </div>
  );
}
