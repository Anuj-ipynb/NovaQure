import { FaAtom, FaDatabase, FaShieldAlt, FaSignOutAlt } from "react-icons/fa";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/auth/useAuth";

const navigationItems = [
  {
    title: "Discovery Studio",
    path: "/molecules",
    icon: <FaAtom />,
  },
  {
    title: "Leaderboard",
    path: "/rankings",
    icon: <FaDatabase />,
  },
  {
    title: "Quantum Reliability",
    path: "/reliability",
    icon: <FaShieldAlt />,
  },
];

export default function Sidebar() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header
      style={{
        background: "var(--color-paper-white)",
        borderBottom: "1px solid var(--color-lavender-mist)",
        padding: "0 24px",
        height: 64,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}
    >
      {/* Brand Logo */}
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span
          style={{
            background: "var(--color-signal-orange)",
            color: "var(--color-paper-white)",
            fontWeight: 800,
            fontSize: 12,
            padding: "3px 7px",
            borderRadius: 4,
            fontFamily: "var(--font-gtstandardmono)",
            letterSpacing: "0.06em",
          }}
        >
          NQ
        </span>
        <span
          style={{
            fontSize: 20,
            fontWeight: 700,
            color: "var(--color-ink-black)",
            letterSpacing: "-0.02em",
          }}
        >
          NovaQure
        </span>
      </div>

      {/* Streamlined 3-Tab Navigation Links */}
      <nav style={{ display: "flex", gap: 8 }}>
        {navigationItems.map((item) => (
          <NavLink
            key={item.title}
            to={item.path}
            style={({ isActive }) => ({
              display: "flex",
              alignItems: "center",
              gap: 8,
              padding: "8px 16px",
              borderRadius: "var(--radius-full)",
              textDecoration: "none",
              fontSize: 14,
              fontWeight: isActive ? 600 : 500,
              color: isActive ? "var(--color-ink-black)" : "var(--color-graphite)",
              background: isActive ? "var(--color-lavender-mist)" : "transparent",
              transition: "all 0.15s ease",
            })}
          >
            <span style={{ fontSize: 14 }}>{item.icon}</span>
            {item.title}
          </NavLink>
        ))}
      </nav>

      {/* User Actions & Pill Button */}
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <span
          style={{
            fontSize: 13,
            color: "var(--color-graphite)",
            fontFamily: "var(--font-gtstandardmono)",
          }}
        >
          {user?.full_name || "Researcher"}
        </span>

        <button
          onClick={handleLogout}
          style={{
            background: "var(--color-ink-black)",
            color: "var(--color-paper-white)",
            border: "none",
            borderRadius: "var(--radius-full)",
            padding: "8px 18px",
            fontSize: 13,
            fontWeight: 600,
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: 6,
            transition: "all 0.15s ease",
          }}
        >
          <FaSignOutAlt style={{ fontSize: 12 }} />
          Logout
        </button>
      </div>
    </header>
  );
}
