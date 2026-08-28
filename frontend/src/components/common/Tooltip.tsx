import { useState } from "react";

interface TooltipProps {
  text: string;
  children: React.ReactNode;
}

export default function Tooltip({ text, children }: TooltipProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div
      style={{ position: "relative", display: "inline-flex", alignItems: "center" }}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}

      <span
        style={{
          marginLeft: 4,
          cursor: "help",
          color: "var(--color-graphite)",
          fontSize: 11,
          fontWeight: 700,
          fontFamily: "var(--font-gtstandardmono)",
          background: "var(--color-faint-slate)",
          border: "1px solid var(--color-lavender-mist)",
          width: 15,
          height: 15,
          borderRadius: "50%",
          display: "inline-flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        ?
      </span>

      {visible && (
        <div
          style={{
            position: "absolute",
            bottom: "125%",
            left: "50%",
            transform: "translateX(-50%)",
            background: "var(--color-ink-black)",
            color: "var(--color-paper-white)",
            padding: "8px 12px",
            borderRadius: 4,
            fontSize: 12,
            lineHeight: 1.3,
            whiteSpace: "normal",
            width: 220,
            zIndex: 100,
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            textAlign: "left",
            fontFamily: "sans-serif",
          }}
        >
          {text}
        </div>
      )}
    </div>
  );
}
