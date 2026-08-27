import { useEffect, useRef, useState } from "react";
import * as $3Dmol from "3dmol";
import { smilesToXYZ } from "../../utils/smilesTo3D";

interface MoleculeViewer3DProps {
  smiles: string;
  iupacName?: string;
  onClose: () => void;
}

export default function MoleculeViewer3D({ smiles, iupacName, onClose }: MoleculeViewer3DProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewerRef = useRef<any>(null);
  const [styleMode, setStyleMode] = useState<"stick" | "ball" | "sphere">("ball");

  useEffect(() => {
    if (!containerRef.current) return;

    try {
      containerRef.current.innerHTML = "";

      const viewer = $3Dmol.createViewer(containerRef.current, {
        backgroundColor: "rgb(248, 250, 252)"
      });
      viewerRef.current = viewer;

      const xyzData = smilesToXYZ(smiles);
      viewer.addModel(xyzData, "xyz");

      applyStyle(viewer, styleMode);
      viewer.zoomTo();
      viewer.render();
      viewer.spin("y", 0.5);
    } catch (err) {
      console.error("3Dmol modal render error:", err);
    }

    return () => {
      if (viewerRef.current) {
        try {
          viewerRef.current.clear();
        } catch {
          // Cleanup error handling
        }
      }
    };
  }, [smiles]);

  const applyStyle = (viewer: any, mode: string) => {
    if (!viewer) return;

    if (mode === "stick") {
      viewer.setStyle({}, { stick: { radius: 0.18 } });
    } else if (mode === "sphere") {
      viewer.setStyle({}, { sphere: { scale: 0.5 } });
    } else {
      viewer.setStyle({}, { stick: { radius: 0.15 }, sphere: { scale: 0.3 } });
    }
    viewer.render();
  };

  const handleStyleChange = (mode: "stick" | "ball" | "sphere") => {
    setStyleMode(mode);
    applyStyle(viewerRef.current, mode);
  };

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0, 0, 0, 0.4)",
        backdropFilter: "blur(6px)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: "var(--color-paper-white)",
          borderRadius: "var(--radius-cards)",
          padding: 28,
          maxWidth: 600,
          width: "90%",
          border: "1px solid var(--color-lavender-mist)",
          textAlign: "center",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <div style={{ textAlign: "left" }}>
            <span style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 11, textTransform: "uppercase", color: "var(--color-graphite)" }}>
              3D WebGL Conformer
            </span>
            <h2 style={{ fontSize: 18, color: "var(--color-ink-black)", margin: "2px 0 0 0", fontWeight: 600 }}>
              {iupacName || "3D Spatial Conformation Model"}
            </h2>
          </div>

          <button
            onClick={onClose}
            style={{
              background: "var(--color-ink-black)",
              border: "none",
              borderRadius: "var(--radius-full)",
              padding: "6px 14px",
              cursor: "pointer",
              color: "var(--color-paper-white)",
              fontSize: 12,
              fontWeight: 600,
            }}
          >
            ✕ Close
          </button>
        </div>

        {/* 3D WebGL Canvas */}
        <div
          ref={containerRef}
          style={{
            width: "100%",
            height: 340,
            borderRadius: 4,
            overflow: "hidden",
            border: "1px solid var(--color-lavender-mist)",
            position: "relative"
          }}
        />

        {/* Controls & Style Selector */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 16 }}>
          <div style={{ display: "flex", gap: 6 }}>
            {(["ball", "stick", "sphere"] as const).map((m) => (
              <button
                key={m}
                onClick={() => handleStyleChange(m)}
                style={{
                  padding: "6px 12px",
                  borderRadius: "var(--radius-full)",
                  border: "1px solid var(--color-ink-black)",
                  background: styleMode === m ? "var(--color-ink-black)" : "transparent",
                  color: styleMode === m ? "var(--color-paper-white)" : "var(--color-ink-black)",
                  fontSize: 12,
                  fontWeight: 600,
                  textTransform: "capitalize",
                  cursor: "pointer"
                }}
              >
                {m === "ball" ? "Ball & Stick" : m}
              </button>
            ))}
          </div>

          <span style={{ fontSize: 11, color: "var(--color-graphite)", fontFamily: "var(--font-gtstandardmono)" }}>
            Drag to Rotate • Scroll to Zoom
          </span>
        </div>

        {/* SMILES text */}
        <div style={{ marginTop: 16, textAlign: "left", background: "var(--color-faint-slate)", padding: 12, borderRadius: 4, border: "1px solid var(--color-lavender-mist)" }}>
          <div style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 11, color: "var(--color-graphite)", textTransform: "uppercase" }}>
            SMILES Chemical Notation:
          </div>
          <div style={{ fontFamily: "var(--font-gtstandardmono)", fontSize: 13, marginTop: 2, color: "var(--color-ink-black)", wordBreak: "break-all" }}>
            {smiles}
          </div>
        </div>
      </div>
    </div>
  );
}
