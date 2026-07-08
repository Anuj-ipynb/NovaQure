import {
  FaChartLine,
  FaProjectDiagram,
  FaFlask,
  FaAtom,
  FaDatabase,
  FaShieldAlt,
  FaSignOutAlt,
  FaUserCircle,
} from "react-icons/fa";

import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../../hooks/auth/useAuth";

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
  const navigate = useNavigate();

  const {
    user,
    logout,
  } = useAuth();

  const handleLogout = () => {
    logout();

    navigate("/login");
  };

  const initials =
    user?.full_name
      ?.split(" ")
      .map((word) => word[0])
      .join("")
      .slice(0, 2)
      .toUpperCase() || "NQ";

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
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Logo */}

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

      {/* Navigation */}

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

      {/* Spacer */}

      <div style={{ flex: 1 }} />

      {/* System Status */}

      <div
        style={{
          padding: 20,
          borderRadius: 20,
          background:
            "rgba(255,255,255,0.04)",
          border:
            "1px solid rgba(255,255,255,0.05)",
          marginBottom: 20,
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

      {/* User Profile */}

      <div
        style={{
          padding: 20,
          borderRadius: 20,
          background:
            "rgba(255,255,255,0.04)",
          border:
            "1px solid rgba(255,255,255,0.05)",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            marginBottom: 18,
          }}
        >
          <div
            style={{
              width: 50,
              height: 50,
              borderRadius: "50%",
              background:
                "linear-gradient(135deg,#7C3AED,#06B6D4)",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontWeight: 700,
              fontSize: 18,
            }}
          >
            {initials}
          </div>

          <div>
            <div
              style={{
                fontWeight: 600,
              }}
            >
              {user?.full_name || "Research User"}
            </div>

            <div
              style={{
                color: "#94A3B8",
                fontSize: 14,
              }}
            >
              {user?.role || "Researcher"}
            </div>
          </div>
        </div>

        <button
          onClick={handleLogout}
          style={{
            width: "100%",
            padding: "14px",
            borderRadius: 14,
            border: "none",
            background:
              "rgba(239,68,68,0.15)",
            color: "#EF4444",
            fontWeight: 600,
            cursor: "pointer",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: 10,
          }}
        >
          <FaSignOutAlt />
          Logout
        </button>
      </div>
    </aside>
  );
}
