import { lazy, Suspense } from "react";
import LoadingSpinner from "./components/ui/LoadingSpinner";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
const Overview = lazy(() => import("./pages/Overview"));
const FeedbackExplorer = lazy(() => import("./pages/FeedbackExplorer"));
const Insights = lazy(() => import("./pages/Insights"));
const Import = lazy(() => import("./pages/Import"));
const Settings = lazy(() => import("./pages/Settings"));

function App() {
  return (
    <Router>
      <Suspense
        fallback={
          <div className="loading-state">
            <LoadingSpinner />
          </div>
        }
      >
        <Routes>
          <Route
            path="/"
            element={
              <MainLayout title="Overview" showDatasetSelector={true}>
                <Overview selectedDataset={null} refreshDatasets={() => {}} />
              </MainLayout>
            }
          />
          <Route
            path="/feedback"
            element={
              <MainLayout title="Feedback Explorer" showDatasetSelector={true}>
                <FeedbackExplorer
                  selectedDataset={null}
                  refreshDatasets={() => {}}
                />
              </MainLayout>
            }
          />
          <Route
            path="/insights"
            element={
              <MainLayout title="AI Insights" showDatasetSelector={true}>
                <Insights selectedDataset={null} refreshDatasets={() => {}} />
              </MainLayout>
            }
          />
          <Route
            path="/import"
            element={
              <MainLayout title="Import Feedback" showDatasetSelector={false}>
                <Import selectedDataset={null} refreshDatasets={() => {}} />
              </MainLayout>
            }
          />
          <Route
            path="/settings"
            element={
              <MainLayout title="Settings" showDatasetSelector={false}>
                <Settings selectedDataset={null} refreshDatasets={() => {}} />
              </MainLayout>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
