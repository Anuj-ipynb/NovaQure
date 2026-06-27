const metrics = [
  {
    title: "NQRE Reliability",
    value: "94.8%",
    color: "#10B981",
    description: "Overall platform trust score",
  },
  {
    title: "AI Confidence",
    value: "93.2%",
    color: "#06B6D4",
    description: "Prediction confidence level",
  },
  {
    title: "Quantum Noise",
    value: "4.1%",
    color: "#F59E0B",
    description: "Measured quantum disturbance",
  },
  {
    title: "AQKC Corrections",
    value: "128",
    color: "#8B5CF6",
    description: "Adaptive corrections applied",
  },
]

const systems = [
  {
    name: "Reliability Engine",
    status: "Operational",
    color: "#10B981",
  },
  {
    name: "Noise Estimator",
    status: "Operational",
    color: "#10B981",
  },
  {
    name: "AQKC Module",
    status: "Operational",
    color: "#10B981",
  },
  {
    name: "Calibration Layer",
    status: "Monitoring",
    color: "#F59E0B",
  },
]

const distributions = [
  {
    range: "95-100%",
    count: 142,
  },
  {
    range: "90-95%",
    count: 487,
  },
  {
    range: "85-90%",
    count: 1024,
  },
  {
    range: "80-85%",
    count: 812,
  },
]

export default function ReliabilityPage() {
  return (
    <div>
      {/* Header */}

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
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
            Trust calibration and uncertainty quantification.
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
          gridTemplateColumns: "repeat(4,1fr)",
          gap: 24,
          marginBottom: 40,
        }}
      >
        {metrics.map((metric) => (
          <div
            key={metric.title}
            style={{
              background: "rgba(255,255,255,0.05)",
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
        ))}
      </div>

      {/* Main Grid */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "2fr 1fr",
          gap: 24,
        }}
      >
        {/* Distribution */}

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
          <h2>
            Reliability Distribution
          </h2>

          <div
            style={{
              marginTop: 30,
            }}
          >
            {distributions.map((item) => (
              <div
                key={item.range}
                style={{
                  marginBottom: 28,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                    marginBottom: 10,
                  }}
                >
                  <span>{item.range}</span>
                  <span>{item.count}</span>
                </div>

                <div
                  style={{
                    height: 14,
                    borderRadius: 999,
                    background:
                      "#1E293B",
                  }}
                >
                  <div
                    style={{
                      width:
                        `${Math.min(
                          item.count / 12,
                          100
                        )}%`,
                      height: "100%",
                      borderRadius:
                        999,
                      background:
                        "linear-gradient(90deg,#06B6D4,#7C3AED)",
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* System Health */}

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
          <h2>Subsystem Status</h2>

          {systems.map((system) => (
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
                  color: system.color,
                }}
              >
                ● {system.status}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom Panel */}

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
            value="92.4%"
          />

          <InfoCard
            title="Noise Compensation"
            value="96.8%"
          />

          <InfoCard
            title="Prediction Stability"
            value="95.1%"
          />
        </div>
      </div>
    </div>
  )
}

function InfoCard(
  {
    title,
    value,
  }: {
    title: string
    value: string
  }
) {
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
  )
}
