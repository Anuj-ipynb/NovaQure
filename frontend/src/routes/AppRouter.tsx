import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "../components/layout/Layout";
import ProtectedRoute from "../components/auth/ProtectedRoute";

import MoleculesPage from "../pages/Molecules/MoleculesPage";
import RankingsPage from "../pages/Rankings/RankingsPage";
import ReliabilityPage from "../pages/Reliability/ReliabilityPage";
import LoginPage from "../pages/Auth/LoginPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Authentication */}
        <Route path="/login" element={<LoginPage />} />

        {/* Discovery Studio (Primary Home) */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout>
                <MoleculesPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        <Route
          path="/molecules"
          element={
            <ProtectedRoute>
              <Layout>
                <MoleculesPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Prioritization Leaderboard */}
        <Route
          path="/rankings"
          element={
            <ProtectedRoute>
              <Layout>
                <RankingsPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Quantum Telemetry */}
        <Route
          path="/reliability"
          element={
            <ProtectedRoute>
              <Layout>
                <ReliabilityPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Redirect Legacy Routes */}
        <Route path="/projects" element={<Navigate to="/molecules" replace />} />
        <Route path="/dashboard" element={<Navigate to="/molecules" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
