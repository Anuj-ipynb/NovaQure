import {
  FaChartLine,
  FaProjectDiagram,
  FaFlask,
  FaAtom,
  FaDatabase,
  FaShieldAlt,
} from "react-icons/fa";

import { NavLink } from "react-router-dom";

const navigationItems = [
  {
    title: "Dashboard",
    path: "/",
    icon: <FaChartLine />,
  },
  {
    title: "Projects",
    path: "/projects",
    icon: <FaProjectDiagram />,
  },
  {
    title: "Experiments",
    path: "/experiments",
    icon: <FaFlask />,
  },
  {
    title: "Molecules",
    path: "/molecules",
    icon: <FaAtom />,
  },
  {
    title: "Rankings",
    path: "/rankings",
    icon: <FaDatabase />,
  },
  {
    title: "Reliability",
    path: "/reliability",
    icon: <FaShieldAlt />,
  },
];

export default function Sidebar() {
  return (
    <aside
      style={{
        width: 280,
        background:
          "linear-gradient(180deg,#08111f,#111827)",
        minHeight: "100vh",
        padding: 30,
        borderRight:
          "1px solid rgba(255,255,255,0.05)",
      }}
    >
      <div
        style={{
          marginBottom: 50,
        }}
      >
        <h1
          style={{
            fontSize: 32,
            color: "#7C3AED",
            fontWeight: 800,
          }}
        >
          NovaQure
        </h1>

        <p
          style={{
            color: "#94A3B8",
            marginTop: 8,
          }}
        >
          AI + Quantum Discovery
        </p>
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        {navigationItems.map((item) => (
          <NavLink
            key={item.title}
            to={item.path}
            style={({ isActive }) => ({
              display: "flex",
              alignItems: "center",
              gap: 16,
              padding: "16px 18px",
              borderRadius: 16,
              textDecoration: "none",
              color: "white",
              background: isActive
                ? "linear-gradient(90deg,#7C3AED,#4F46E5)"
                : "rgba(255,255,255,0.03)",
              transition: "0.3s",
              fontWeight: isActive ? 700 : 500,
            })}
          >
            <span
              style={{
                fontSize: 18,
              }}
            >
              {item.icon}
            </span>

            {item.title}
          </NavLink>
        ))}
      </div>

      <div
        style={{
          marginTop: 50,
          padding: 20,
          borderRadius: 20,
          background:
            "rgba(255,255,255,0.04)",
          border:
            "1px solid rgba(255,255,255,0.05)",
        }}
      >
        <h3
          style={{
            marginBottom: 12,
          }}
        >
          System Status
        </h3>

        <p
          style={{
            color: "#10B981",
          }}
        >
          ● All services operational
        </p>

        <p
          style={{
            color: "#94A3B8",
            marginTop: 10,
          }}
        >
          Backend API connected
        </p>

        <p
          style={{
            color: "#94A3B8",
            marginTop: 5,
          }}
        >
          Quantum Engine standby
        </p>
      </div>
    </aside>
  );
}
