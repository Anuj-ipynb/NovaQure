import { useEffect, useRef } from "react";
import * as $3Dmol from "3dmol";
import { smilesToXYZ } from "../../utils/smilesTo3D";

interface Inline3DViewerProps {
    smiles: string;
    height?: number;
}

export default function Inline3DViewer({ smiles, height = 140 }: Inline3DViewerProps) {
    const containerRef = useRef<HTMLDivElement | null>(null);
    const viewerRef = useRef<any>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        try {
            // Clear container
            containerRef.current.innerHTML = "";

            // Initialize 3Dmol WebGL Viewer
            const config = { backgroundColor: "rgba(13, 19, 31, 0.6)" };
            const viewer = $3Dmol.createViewer(containerRef.current, config);
            viewerRef.current = viewer;

            // Load 3D XYZ chemical structure
            const xyzData = smilesToXYZ(smiles);
            viewer.addModel(xyzData, "xyz");

            // Set ball-and-stick style with CPK element coloring
            viewer.setStyle({}, { stick: { radius: 0.14 }, sphere: { scale: 0.28 } });
            viewer.zoomTo();
            viewer.render();

            // Auto-rotate 3D structure
            viewer.spin("y", 0.8);
        } catch (err) {
            console.warn("WebGL 3Dmol inline render fallback:", err);
        }

        return () => {
            if (viewerRef.current) {
                try {
                    viewerRef.current.clear();
                } catch {
                    // Ignore cleanup edge cases
                }
            }
        };
    }, [smiles]);

    return (
        <div
            ref={containerRef}
            style={{
                width: "100%",
                height,
                borderRadius: 12,
                overflow: "hidden",
                border: "1px solid rgba(255, 255, 255, 0.05)",
                position: "relative",
                background: "#0d131f",
                cursor: "pointer"
            }}
        />
    );
}
