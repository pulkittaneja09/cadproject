import { useState, useEffect } from "react";
import { apiClient } from "../lib/api";
import { Dataset } from "../types";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "../components/ui/Card";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import { Database, Cloud, Trash2, Check } from "lucide-react";

interface SettingsProps {
  selectedDataset: number | null;
  refreshDatasets: () => void;
}

export default function Settings({ refreshDatasets }: SettingsProps) {
  const [health, setHealth] = useState<{
    status: string;
    storage_mode: string;
    ai_model: string;
    ai_fallback_enabled: boolean;
  } | null>(null);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [healthRes, datasetsRes] = await Promise.all([
        apiClient.health(),
        apiClient.listDatasets(),
      ]);
      setError(null);
      setHealth(healthRes.data);
      setDatasets(datasetsRes.data);
    } catch (error) {
      setError(
        "Could not load workspace settings. Check the backend connection.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteDataset = async (id: number) => {
    if (
      !confirm(
        "Are you sure you want to delete this dataset? This action cannot be undone.",
      )
    ) {
      return;
    }

    try {
      setDeletingId(id);
      await apiClient.deleteDataset(id);
      setDatasets(datasets.filter((d) => d.id !== id));
      refreshDatasets();
    } catch (error) {
      console.error("Failed to delete dataset:", error);
      alert("Failed to delete dataset");
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6 settings-page">
      {error && (
        <div className="notice" role="alert">
          {error}
          <button onClick={() => void loadData()}>Retry</button>
        </div>
      )}
      <Card>
        <CardHeader>
          <CardTitle>System Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Database className="text-primary" size={20} />
                <span className="text-gray-300">Storage Mode</span>
              </div>
              <Badge variant={health ? "success" : "neutral"}>
                {health?.storage_mode || "Unknown"}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Cloud className="text-primary" size={20} />
                <span className="text-gray-300">AI Model</span>
              </div>
              <span className="text-sm text-gray-400">
                {health?.ai_model || "Not configured"}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Check className="text-primary" size={20} />
                <span className="text-gray-300">AI Fallback</span>
              </div>
              <Badge
                variant={health?.ai_fallback_enabled ? "success" : "neutral"}
              >
                {health ? (health.ai_fallback_enabled ? "Enabled" : "Disabled") : "Unknown"}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Analysis transparency</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-400 leading-relaxed">
            Sentiment analysis uses the configured transformer model, with
            rule-based fallback when enabled. Model configuration does not
            confirm readiness. Individual records do not report which inference
            method was used, and confidence is a classification score rather
            than a guarantee of accuracy.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Dataset Management</CardTitle>
        </CardHeader>
        <CardContent>
          {datasets.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No datasets found</p>
          ) : (
            <div className="space-y-3">
              {datasets.map((dataset) => (
                <div
                  key={dataset.id}
                  className="flex items-center justify-between p-4 bg-surfaceLight rounded-lg"
                >
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-100">
                      {dataset.name}
                    </h4>
                    <div className="flex items-center gap-4 text-sm text-gray-400 mt-1">
                      <span>{dataset.row_count} reviews</span>
                      <span>{dataset.analyzed_count} analyzed</span>
                      <Badge
                        variant={
                          dataset.status === "analyzed" ? "success" : "neutral"
                        }
                      >
                        {dataset.status}
                      </Badge>
                    </div>
                  </div>
                  <Button
                    variant="danger"
                    size="sm"
                    aria-label={`Delete dataset ${dataset.name}`}
                    onClick={() => handleDeleteDataset(dataset.id)}
                    disabled={deletingId === dataset.id}
                  >
                    {deletingId === dataset.id ? (
                      <LoadingSpinner size="sm" />
                    ) : (
                      <Trash2 size={16} />
                    )}
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Application Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2 text-sm text-gray-400">
            <p>
              <strong className="text-gray-300">Version:</strong> 1.0.0
            </p>
            <p>
              <strong className="text-gray-300">Backend:</strong> FastAPI
            </p>
            <p>
              <strong className="text-gray-300">Frontend:</strong> React +
              TypeScript + Vite
            </p>
            <p>
              <strong className="text-gray-300">AI Model:</strong> Hugging Face
              Transformers (with fallback)
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
