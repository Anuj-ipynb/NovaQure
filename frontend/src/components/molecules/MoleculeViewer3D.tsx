import { useEffect, useRef } from "react";

interface MoleculeViewer3DProps {
  smiles: string;
  onClose: () => void;
}

export default function MoleculeViewer3D({ smiles, onClose }: MoleculeViewer3DProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let angle = 0;

    // Generate pseudo-3D atom coordinates based on SMILES characters
    const atoms = Array.from(smiles).map((char, index) => {
      const theta = (index / Math.max(1, smiles.length)) * Math.PI * 2;
      const phi = (index / Math.max(1, smiles.length)) * Math.PI;
      const r = 80 + (index % 3) * 15;
      
      let color = "#a8927c"; // Warm Sandstone
      if (char === "C") color = "#212121"; // Carbon Charcoal
      else if (char === "O") color = "#EF4444"; // Oxygen Red
      else if (char === "N") color = "#3B82F6"; // Nitrogen Blue
      else if (char === "F" || char === "Cl" || char === "Br") color = "#10B981"; // Halogen Green

      return {
        x: r * Math.sin(phi) * Math.cos(theta),
        y: r * Math.sin(phi) * Math.sin(theta),
        z: r * Math.cos(phi),
        element: char,
        color,
      };
    });

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      angle += 0.015;

      const cosA = Math.cos(angle);
      const sinA = Math.sin(angle);

      // Project 3D points to 2D canvas
      const projected = atoms.map((atom) => {
        const x1 = atom.x * cosA - atom.z * sinA;
        const z1 = atom.x * sinA + atom.z * cosA;
        const scale = 250 / (250 + z1);
        const x2 = canvas.width / 2 + x1 * scale;
        const y2 = canvas.height / 2 + atom.y * scale;

        return { ...atom, px: x2, py: y2, scale, z1 };
      });

      // Sort by depth (z1) for proper rendering order
      projected.sort((a, b) => b.z1 - a.z1);

      // Draw chemical bonds (lines between consecutive atoms)
      ctx.lineWidth = 2;
      ctx.strokeStyle = "rgba(168, 146, 124, 0.4)";
      for (let i = 0; i < projected.length - 1; i++) {
        ctx.beginPath();
        ctx.moveTo(projected[i].px, projected[i].py);
        ctx.lineTo(projected[i + 1].px, projected[i + 1].py);
        ctx.stroke();
      }

      // Draw 3D atom spheres
      projected.forEach((atom) => {
        const radius = Math.max(6, 12 * atom.scale);
        ctx.beginPath();
        ctx.arc(atom.px, atom.py, radius, 0, Math.PI * 2);
        ctx.fillStyle = atom.color;
        ctx.fill();
        ctx.lineWidth = 1.5;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();

        // Atom label
        ctx.fillStyle = "#ffffff";
        ctx.font = `${Math.max(10, Math.floor(12 * atom.scale))}px monospace`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(atom.element, atom.px, atom.py);
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [smiles]);

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0, 0, 0, 0.85)",
        backdropFilter: "blur(12px)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: "var(--surface-canvas)",
          borderRadius: "var(--radius-cards)",
          padding: 32,
          maxWidth: 540,
          width: "90%",
          border: "1px solid var(--color-pale-stone)",
          textAlign: "center",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
          <span style={{ fontFamily: "var(--font-mono)", fontSize: 11, textTransform: "uppercase", color: "var(--color-warm-sandstone)" }}>
            3D Molecular Conformation
          </span>
          <button
            onClick={onClose}
            style={{
              background: "none",
              border: "1px solid var(--color-silhouette)",
              borderRadius: "var(--radius-buttons)",
              padding: "4px 12px",
              cursor: "pointer",
              fontFamily: "var(--font-aeonik)",
              fontSize: 14,
            }}
          >
            Close
          </button>
        </div>

        <canvas ref={canvasRef} width={450} height={320} style={{ borderRadius: 12, background: "var(--surface-soft-mist)" }} />

        <div style={{ marginTop: 20, textAlign: "left" }}>
          <p style={{ fontFamily: "var(--font-mono)", fontSize: 12, color: "var(--color-graphite)" }}>
            SMILES Specification:
          </p>
          <p style={{ fontFamily: "var(--font-mono)", fontSize: 16, marginTop: 4, color: "var(--color-obsidian)", wordBreak: "break-all" }}>
            {smiles}
          </p>
        </div>
      </div>
    </div>
  );
}
