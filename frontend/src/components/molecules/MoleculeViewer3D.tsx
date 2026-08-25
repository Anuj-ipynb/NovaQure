import { useEffect, useRef, useState } from "react";
import * as $3Dmol from "3dmol";
import { smilesToXYZ } from "../../utils/smilesTo3D";

interface MoleculeViewer3DProps {
  smiles: string;
  onClose: () => void;
}

export default function MoleculeViewer3D({ smiles, onClose }: MoleculeViewer3DProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewerRef = useRef<any>(null);
  const [styleMode, setStyleMode] = useState<"stick" | "ball" | "sphere">("ball");

  useEffect(() => {
    if (!containerRef.current) return;

    try {
      containerRef.current.innerHTML = "";

      const viewer = $3Dmol.createViewer(containerRef.current, {
        backgroundColor: "rgb(13, 19, 31)"
      });
      viewerRef.current = viewer;

      const xyzData = smilesToXYZ(smiles);
      viewer.addModel(xyzData, "xyz");

      applyStyle(viewer, styleMode);
      viewer.zoomTo();
      viewer.render();
      viewer.spin("y", 0.6);
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
      // Ball and stick default
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
          background: "#0d131f",
          borderRadius: 24,
          padding: 32,
          maxWidth: 640,
          width: "90%",
          border: "1px solid rgba(255, 255, 255, 0.08)",
          textAlign: "center",
          boxShadow: "0 20px 50px rgba(0,0,0,0.5)"
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
          <div>
            <span style={{ fontFamily: "monospace", fontSize: 11, textTransform: "uppercase", color: "#10b981", letterSpacing: 0.5 }}>
              3D WebGL Conformer
            </span>
            <h2 style={{ fontSize: 20, color: "#f8fafc", margin: "4px 0 0 0", fontWeight: 600 }}>
              Molecular Spatial Conformation
            </h2>
          </div>

          <button
            onClick={onClose}
            style={{
              background: "rgba(255, 255, 255, 0.05)",
              border: "1px solid rgba(255, 255, 255, 0.1)",
              borderRadius: 10,
              padding: "6px 16px",
              cursor: "pointer",
              color: "#f1f5f9",
              fontSize: 13,
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
            height: 360,
            borderRadius: 16,
            overflow: "hidden",
            border: "1px solid rgba(255, 255, 255, 0.05)",
            position: "relative"
          }}
        />

        {/* Display Controls & Style Selector */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 20 }}>
          <div style={{ display: "flex", gap: 8 }}>
            {(["ball", "stick", "sphere"] as const).map((m) => (
              <button
                key={m}
                onClick={() => handleStyleChange(m)}
                style={{
                  padding: "6px 14px",
                  borderRadius: 8,
                  border: "1px solid rgba(255, 255, 255, 0.08)",
                  background: styleMode === m ? "#10b981" : "rgba(255, 255, 255, 0.03)",
                  color: styleMode === m ? "#ffffff" : "#94a3b8",
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

          <span style={{ fontSize: 12, color: "#64748b", fontFamily: "monospace" }}>
            Drag to Rotate • Scroll to Zoom
          </span>
        </div>

        {/* SMILES text */}
        <div style={{ marginTop: 20, textAlign: "left", background: "rgba(255, 255, 255, 0.02)", padding: 16, borderRadius: 12, border: "1px solid rgba(255, 255, 255, 0.04)" }}>
          <div style={{ fontFamily: "monospace", fontSize: 11, color: "#64748b", textTransform: "uppercase" }}>
            SMILES Structural Representation:
          </div>
          <div style={{ fontFamily: "monospace", fontSize: 14, marginTop: 4, color: "#f1f5f9", wordBreak: "break-all" }}>
            {smiles}
          </div>
        </div>
      </div>
    </div>
  );
}
