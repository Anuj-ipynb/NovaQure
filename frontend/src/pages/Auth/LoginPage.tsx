import { useState } from "react";
import { useAuth } from "../../hooks/auth/useAuth";

export default function LoginPage() {
  const { login, register } = useAuth();

  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState("Researcher");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError("");
      await login(email, password);
      window.location.href = "/";
    } catch {
      setError("Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError("");
      await register({
        email,
        password,
        full_name: fullName || "New Researcher",
        role,
      });
      window.location.href = "/";
    } catch {
      setError("Registration failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleFillDemo = () => {
    setMode("signin");
    setEmail("researcher@novaqure.org");
    setPassword("password123");
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "var(--color-paper-white)",
        padding: 24,
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 460,
          background: "var(--color-paper-white)",
          borderRadius: "var(--radius-cards)",
          padding: 40,
          border: "1px solid var(--color-lavender-mist)",
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.04)",
        }}
      >
        {/* Opener Editorial Header */}
        <div style={{ marginBottom: 32, textAlign: "center" }}>
          <span
            style={{
              fontFamily: "var(--font-gtstandardmono)",
              fontSize: 11,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              color: "var(--color-graphite)",
              display: "block",
              marginBottom: 8,
            }}
          >
            AUTHENTICATION // BIOTECH ACCESS PORTAL
          </span>

          <h1
            style={{
              fontSize: 34,
              fontWeight: 500,
              letterSpacing: "-0.04em",
              color: "var(--color-ink-black)",
              lineHeight: 1.1,
            }}
          >
            NovaQure{" "}
            <span
              style={{
                background: "var(--color-signal-orange)",
                color: "var(--color-paper-white)",
                padding: "2px 8px",
                borderRadius: 2,
                display: "inline-block",
              }}
            >
              Platform
            </span>
          </h1>
          <p style={{ color: "var(--color-graphite)", marginTop: 8, fontSize: 14 }}>
            Quantum-Accelerated Drug Discovery Workspace
          </p>
        </div>

        {/* Dual Tab Switcher */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            background: "var(--color-faint-slate)",
            padding: 4,
            borderRadius: "var(--radius-full)",
            border: "1px solid var(--color-lavender-mist)",
            marginBottom: 28,
          }}
        >
          <button
            type="button"
            onClick={() => {
              setMode("signin");
              setError("");
            }}
            style={{
              padding: "8px 16px",
              borderRadius: "var(--radius-full)",
              border: "none",
              background: mode === "signin" ? "var(--color-ink-black)" : "transparent",
              color: mode === "signin" ? "var(--color-paper-white)" : "var(--color-graphite)",
              fontWeight: 600,
              fontSize: 13,
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
          >
            Sign In
          </button>

          <button
            type="button"
            onClick={() => {
              setMode("signup");
              setError("");
            }}
            style={{
              padding: "8px 16px",
              borderRadius: "var(--radius-full)",
              border: "none",
              background: mode === "signup" ? "var(--color-ink-black)" : "transparent",
              color: mode === "signup" ? "var(--color-paper-white)" : "var(--color-graphite)",
              fontWeight: 600,
              fontSize: 13,
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
          >
            Create Account
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div
            style={{
              marginBottom: 20,
              padding: "12px 16px",
              borderRadius: 4,
              background: "#fef2f2",
              border: "1px solid #fca5a5",
              color: "#dc2626",
              fontSize: 13,
              fontFamily: "var(--font-gtstandardmono)",
            }}
          >
            {error}
          </div>
        )}

        {/* Form Container */}
        <form onSubmit={mode === "signin" ? handleSignIn : handleSignUp}>
          {mode === "signup" && (
            <div style={{ marginBottom: 16 }}>
              <label style={labelStyle}>Full Name</label>
              <input
                type="text"
                placeholder="Dr. Anuj Srinivas"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                required
                style={inputStyle}
              />
            </div>
          )}

          <div style={{ marginBottom: 16 }}>
            <label style={labelStyle}>Work Email</label>
            <input
              type="email"
              placeholder="researcher@novaqure.org"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              style={inputStyle}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={labelStyle}>Password</label>
            <input
              type="password"
              placeholder="••••••••••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={inputStyle}
            />
          </div>

          {mode === "signup" && (
            <div style={{ marginBottom: 20 }}>
              <label style={labelStyle}>Research Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                style={{
                  ...inputStyle,
                  cursor: "pointer",
                  background: "var(--color-paper-white)",
                }}
              >
                <option value="Researcher">Lead Systems Architect / Researcher</option>
                <option value="AI Specialist">AI & Quantum Circuits Engineer</option>
                <option value="Medicinal Chemist">Medicinal Chemist</option>
              </select>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px 24px",
              border: "none",
              borderRadius: "var(--radius-full)",
              background: "var(--color-ink-black)",
              color: "var(--color-paper-white)",
              fontSize: 14,
              fontWeight: 600,
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
              marginTop: 8,
              transition: "all 0.15s ease",
            }}
          >
            {loading
              ? mode === "signin"
                ? "Signing In..."
                : "Registering Account..."
              : mode === "signin"
              ? "🚀 Sign In to Workspace"
              : "✨ Create Research Account"}
          </button>
        </form>

        {/* 1-Click Demo Credentials Shortcut */}
        <div style={{ marginTop: 24, textAlign: "center", borderTop: "1px solid var(--color-lavender-mist)", paddingTop: 20 }}>
          <button
            type="button"
            onClick={handleFillDemo}
            style={{
              background: "transparent",
              border: "1px solid var(--color-lavender-mist)",
              borderRadius: "var(--radius-full)",
              padding: "6px 16px",
              fontSize: 12,
              fontWeight: 600,
              color: "var(--color-graphite)",
              cursor: "pointer",
              transition: "all 0.15s ease",
            }}
          >
            ⚡ Fill Demo Credentials
          </button>
        </div>
      </div>
    </div>
  );
}

const labelStyle = {
  display: "block",
  fontSize: 12,
  fontWeight: 600,
  color: "var(--color-graphite)",
  marginBottom: 6,
} as const;

const inputStyle = {
  width: "100%",
  padding: "12px 14px",
  borderRadius: 4,
  border: "1px solid var(--color-lavender-mist)",
  background: "var(--color-faint-slate)",
  color: "var(--color-ink-black)",
  fontSize: 14,
  outline: "none",
  boxSizing: "border-box",
} as const;
