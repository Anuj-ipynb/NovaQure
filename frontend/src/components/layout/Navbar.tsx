export default function Navbar() {
  return (
    <div
      style={{
        height: 80,
        background:
          "rgba(255,255,255,0.03)",
        backdropFilter: "blur(20px)",
        display: "flex",
        justifyContent:
          "space-between",
        alignItems: "center",
        padding: "0 40px",
        borderBottom:
          "1px solid rgba(255,255,255,0.05)",
      }}
    >
      <div>
        <h2>
          AI–Quantum Drug Discovery Platform
        </h2>

        <p
          style={{
            color: "#94a3b8",
            marginTop: 5,
          }}
        >
          Noise Adaptive Molecular Optimization
        </p>
      </div>

      <div
        style={{
          width: 50,
          height: 50,
          borderRadius: "50%",
          background:
            "linear-gradient(45deg,#4f46e5,#7c3aed)",
        }}
      />
    </div>
  );
}
