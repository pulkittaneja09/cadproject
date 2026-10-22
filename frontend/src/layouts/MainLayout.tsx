import React, { useState, useEffect, useCallback } from "react";
import { useLocation, Link } from "react-router-dom";
import { Upload, ArrowUpRight } from "lucide-react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import { Dataset } from "../types";
import { apiClient } from "../lib/api";
interface Props {
  children: React.ReactNode;
  title: string;
  showDatasetSelector?: boolean;
}
const subtitles: Record<string, string> = {
  Overview: "Listen closer. See the bigger picture.",
  "Feedback Explorer": "Find the feedback behind the numbers.",
  "AI Insights": "From customer voices to a clearer direction.",
  "Import Feedback": "Bring your customer conversations into focus.",
  Settings: "Your data, your workspace.",
};
export default function MainLayout({
  children,
  title,
  showDatasetSelector = true,
}: Props) {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<number | null>(() => {
    const saved = sessionStorage.getItem("dataset");
    return saved ? Number(saved) : null;
  });
  const [error, setError] = useState(false);
  const location = useLocation();
  const loadDatasets = useCallback(async () => {
    try {
      const { data } = await apiClient.listDatasets();
      setDatasets(data);
      setError(false);
      setSelectedDataset((current) =>
        current && !data.some((d) => d.id === current) ? null : current,
      );
    } catch {
      setError(true);
    }
  }, []);
  useEffect(() => {
    void loadDatasets();
  }, [loadDatasets, location.pathname]);
  const change = (id: number | null) => {
    setSelectedDataset(id);
    if (id) sessionStorage.setItem("dataset", String(id));
    else sessionStorage.removeItem("dataset");
  };
  return (
    <div className="app-shell">
      <a href="#main-content" className="skip-link">
        Skip to content
      </a>
      <Sidebar />
      <div className="main-shell">
        <Navbar
          title={title}
          datasets={datasets}
          selectedDataset={selectedDataset}
          onDatasetChange={change}
          showDatasetSelector={showDatasetSelector}
        />
        <main id="main-content">
          <div className="page-heading">
            <div>
              <h1>{title === "AI Insights" ? "Customer insights" : title}</h1>
              <p>{subtitles[title]}</p>
            </div>
            {title !== "Import Feedback" && (
              <Link className="import-link" to="/import">
                <Upload size={16} />
                Import feedback
                <ArrowUpRight size={15} />
              </Link>
            )}
          </div>
          {error && (
            <div className="notice error" role="alert">
              Cannot connect to the backend. Check that it is running on port
              8000.
              <button onClick={() => void loadDatasets()}>
                Retry connection
              </button>
            </div>
          )}
          {React.cloneElement(children as React.ReactElement, {
            selectedDataset,
            refreshDatasets: loadDatasets,
          })}
          <footer className="page-footer">
            <span>
              <span className="footer-mark">◈</span> InsightPulse AI
            </span>
            <span>Clarity from every conversation.</span>
          </footer>
        </main>
      </div>
    </div>
  );
}
