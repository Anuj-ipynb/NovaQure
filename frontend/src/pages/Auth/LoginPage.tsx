import { useState } from "react";
import { useAuth } from "../../hooks/auth/useAuth";

export default function LoginPage() {
  const { login } = useAuth();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    try {
      setLoading(true);
      setError("");

      await login(
        email,
        password
      );

      window.location.href = "/";
    } catch {
      setError(
        "Invalid email or password."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background:
          "linear-gradient(135deg,#0F172A,#1E293B)",
      }}
    >
      <div
        style={{
          width: 450,
          padding: 50,
          borderRadius: 30,
          background:
            "rgba(255,255,255,0.05)",
          backdropFilter:
            "blur(20px)",
          border:
            "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <h1
          style={{
            fontSize: 42,
            marginBottom: 10,
          }}
        >
          NovaQure
        </h1>

        <p
          style={{
            color: "#94A3B8",
            marginBottom: 40,
          }}
        >
          Sign in to continue to the platform.
        </p>

        {error && (
          <div
            style={{
              marginBottom: 20,
              padding: 15,
              borderRadius: 12,
              background:
                "rgba(239,68,68,0.2)",
              color: "#EF4444",
            }}
          >
            {error}
          </div>
        )}

        <form
          onSubmit={
            handleSubmit
          }
        >
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
            style={inputStyle}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
            style={inputStyle}
          />

          <button
            type="submit"
            disabled={
              loading
            }
            style={{
              width: "100%",
              padding: 16,
              border: "none",
              borderRadius: 14,
              marginTop: 20,
              background:
                "linear-gradient(90deg,#7C3AED,#4F46E5)",
              color: "white",
              fontSize: 16,
              fontWeight: 700,
              cursor: "pointer",
            }}
          >
            {loading
              ? "Signing In..."
              : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: 18,
  marginBottom: 18,
  borderRadius: 14,
  border:
    "1px solid rgba(255,255,255,0.1)",
  background:
    "rgba(255,255,255,0.04)",
  color: "white",
  fontSize: 16,
  outline: "none",
} as const;
