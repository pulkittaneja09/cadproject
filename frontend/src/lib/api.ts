import axios from "axios";
import {
  Dataset,
  FeedbackListResponse,
  OverviewAnalytics,
  InsightSummary,
} from "../types";
const api = axios.create({ baseURL: "/api" });
type Filters = {
  dataset_id?: number;
  sentiment?: string;
  product?: string;
  category?: string;
  priority?: string;
  search?: string;
  page?: number;
  page_size?: number;
};
export const apiClient = {
  listDatasets: () => api.get<Dataset[]>("/datasets"),
  deleteDataset: (id: number) => api.delete(`/datasets/${id}`),
  health: () =>
    api.get<{
      status: string;
      storage_mode: string;
      ai_model: string;
      ai_fallback_enabled: boolean;
    }>("/health"),
  getOverviewAnalytics: (dataset_id?: number) =>
    api.get<OverviewAnalytics>("/analytics/overview", {
      params: { dataset_id },
    }),
  getInsights: (dataset_id?: number, signal?: AbortSignal) =>
    api.get<InsightSummary>("/insights", { params: { dataset_id }, signal }),
  listFeedback: (params: Filters) =>
    api.get<FeedbackListResponse>("/feedback", { params }),
  exportFeedback: (params: Filters) =>
    api.get("/feedback/export", { params, responseType: "blob" }),
  uploadFeedback: (file: File, name: string, description: string) => {
    const data = new FormData();
    data.append("file", file);
    return api.post<{
      dataset_id: number;
      row_count: number;
      name: string;
      analyzed?: boolean;
    }>("/feedback/upload", data, { params: { name, description } });
  },
  analyzeFeedback: (id: number) => api.post(`/feedback/${id}/analyze`),
};
export function errorMessage(error: unknown, fallback: string) {
  return axios.isAxiosError(error) &&
    typeof error.response?.data?.detail === "string"
    ? error.response.data.detail
    : fallback;
}
