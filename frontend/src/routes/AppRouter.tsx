import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Layout from "../components/layout/Layout";

import ProtectedRoute from "../components/auth/ProtectedRoute";

import DashboardPage from "../pages/Dashboard/DashboardPage";
import ProjectsPage from "../pages/Projects/ProjectsPage";
import ExperimentsPage from "../pages/Experiments/ExperimentsPage";
import MoleculesPage from "../pages/Molecules/MoleculesPage";
import RankingsPage from "../pages/Rankings/RankingsPage";
import ReliabilityPage from "../pages/Reliability/ReliabilityPage";

import LoginPage from "../pages/Auth/LoginPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Authentication Routes */}

        <Route
          path="/login"
          element={<LoginPage />}
        />

        {/* Protected Dashboard */}

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout>
                <DashboardPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Protected Projects */}

        <Route
          path="/projects"
          element={
            <ProtectedRoute>
              <Layout>
                <ProjectsPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Protected Experiments */}

        <Route
          path="/experiments"
          element={
            <ProtectedRoute>
              <Layout>
                <ExperimentsPage />
              </Layout>
            </ProtectedRoute>
          }
        />

        {/* Protected Molecules */}

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

        {/* Protected Rankings */}

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

        {/* Protected Reliability */}

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
      </Routes>
    </BrowserRouter>
  );
}
