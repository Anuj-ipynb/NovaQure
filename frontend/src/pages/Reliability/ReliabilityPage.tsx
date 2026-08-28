import { useReliability } from "../../hooks/reliability/useReliability";
import ReliabilityTrendChart from "../../components/charts/ReliabilityTrendChart";

function getStatusColor(status: string) {
  if (status === "Operational") return "#10B981";
  if (status === "Monitoring") return "#F59E0B";
  return "#EF4444";
}

export default function ReliabilityPage() {
  const { data, isLoading, error } = useReliability();
  const reliability = data?.[0];

  if (isLoading) {
    return (
      <div style={{ padding: "100px 0", textAlign: "center", color: "var(--color-graphite)" }}>
        Loading reliability telemetry...
      </div>
    );
  }

  if (error || !reliability) {
    return (
      <div style={{ padding: "100px 0", textAlign: "center", color: "#ef4444" }}>
        Failed to load reliability data.
      </div>
    );
  }

  const metrics = [
    {
      title: "NQRE Reliability",
      value: `${reliability.overall_reliability}%`,
      description: "Overall platform trust score",
    },
    {
      title: "AI Confidence",
      value: `${reliability.ai_confidence}%`,
      description: "Prediction confidence level",
    },
    {
      title: "Quantum Noise",
      value: `${reliability.quantum_noise}%`,
      description: "Measured quantum disturbance",
    },
    {
      title: "AQKC Corrections",
      value: `${reliability.aqkc_corrections}`,
      description: "Adaptive ZNE corrections applied",
    },
  ];

  const systems = [
    { name: "Reliability Engine", status: reliability.reliability_engine_status },
    { name: "Noise Estimator", status: reliability.noise_estimator_status },
    { name: "AQKC Module", status: reliability.aqkc_module_status },
    { name: "Calibration Layer", status: reliability.calibration_layer_status },
  ];

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
          QUANTUM TELEMETRY // AQKC & NQRE TRUST ENGINE
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
          Zero-Noise Extrapolation{" "}
          <span
            style={{
              background: "var(--color-signal-orange)",
              color: "var(--color-paper-white)",
              padding: "2px 8px",
              borderRadius: 2,
              display: "inline-block",
            }}
          >
            Quantum Telemetry
          </span>
        </h1>
        <p style={{ color: "var(--color-graphite)", marginTop: 10, fontSize: 16 }}>
          Zero-Noise Extrapolation (ZNE) error mitigation, noise profiling, and NQRE trust calibration telemetry.
        </p>
      </div>

      {/* Metric Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: 20,
          marginBottom: 40,
        }}
      >
        {metrics.map((metric) => (
          <div
            key={metric.title}
            style={{
              background: "var(--color-paper-white)",
              borderRadius: "var(--radius-cards)",
              padding: 24,
              border: "1px solid var(--color-lavender-mist)",
            }}
          >
            <p style={{ color: "var(--color-graphite)", fontSize: 12, fontFamily: "var(--font-gtstandardmono)" }}>
              {metric.title}
            </p>
            <h1
              style={{
                marginTop: 10,
                fontSize: 32,
                fontWeight: 700,
                color: "var(--color-ink-black)",
                fontFamily: "var(--font-gtstandardmono)",
                letterSpacing: "-0.04em",
              }}
            >
              {metric.value}
            </h1>
            <p style={{ marginTop: 8, fontSize: 12, color: "var(--color-graphite)" }}>
              {metric.description}
            </p>
          </div>
        ))}
      </div>

      {/* Subsystems & Historical Charts */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 2fr",
          gap: 24,
        }}
      >
        <div
          style={{
            background: "var(--color-paper-white)",
            borderRadius: "var(--radius-cards)",
            padding: 24,
            border: "1px solid var(--color-lavender-mist)",
          }}
        >
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16, color: "var(--color-ink-black)" }}>
            Subsystem Status
          </h2>

          {systems.map((system) => (
            <div
              key={system.name}
              style={{
                paddingTop: 12,
                paddingBottom: 12,
                borderBottom: "1px solid var(--color-lavender-mist)",
              }}
            >
              <h3 style={{ fontSize: 14, fontWeight: 500, color: "var(--color-ink-black)" }}>
                {system.name}
              </h3>
              <p style={{ marginTop: 4, fontSize: 12, fontWeight: 600, color: getStatusColor(system.status) }}>
                ● {system.status}
              </p>
            </div>
          ))}
        </div>

        <div
          style={{
            background: "var(--color-paper-white)",
            borderRadius: "var(--radius-cards)",
            padding: 24,
            border: "1px solid var(--color-lavender-mist)",
          }}
        >
          <h2 style={{ fontSize: 18, fontWeight: 600, marginBottom: 16, color: "var(--color-ink-black)" }}>
            Reliability & Energy Trends
          </h2>
          <ReliabilityTrendChart history={data ?? []} />
        </div>
      </div>
    </div>
  );
}
