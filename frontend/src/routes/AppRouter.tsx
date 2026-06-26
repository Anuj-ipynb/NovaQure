import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "../components/layout/Layout";

import DashboardPage from "../pages/Dashboard/DashboardPage";
import ProjectsPage from "../pages/Projects/ProjectsPage";
import ExperimentsPage from "../pages/Experiments/ExperimentsPage";
import MoleculesPage from "../pages/Molecules/MoleculesPage";
import RankingsPage from "../pages/Rankings/RankingsPage";
import ReliabilityPage from "../pages/Reliability/ReliabilityPage";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/experiments" element={<ExperimentsPage />} />
          <Route path="/molecules" element={<MoleculesPage />} />
          <Route path="/rankings" element={<RankingsPage />} />
          <Route path="/reliability" element={<ReliabilityPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
