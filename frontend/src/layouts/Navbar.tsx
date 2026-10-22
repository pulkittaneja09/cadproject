import { Database } from "lucide-react";
import { Dataset } from "../types";
import Select from "../components/ui/Select";
interface NavbarProps {
  title: string;
  datasets: Dataset[];
  selectedDataset: number | null;
  onDatasetChange: (id: number | null) => void;
  showDatasetSelector?: boolean;
}
export default function Navbar({
  title,
  datasets,
  selectedDataset,
  onDatasetChange,
  showDatasetSelector = true,
}: NavbarProps) {
  return (
    <header className="topbar">
      <div className="breadcrumbs">
        Workspace <span>/</span>
        <strong>{title}</strong>
      </div>
      {showDatasetSelector && (
        <div className="dataset-control">
          <Database size={15} />
          <Select
            aria-label="Active dataset"
            value={selectedDataset ?? ""}
            onChange={(e) =>
              onDatasetChange(e.target.value ? Number(e.target.value) : null)
            }
          >
            <option value="">All datasets</option>
            {datasets.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </Select>
        </div>
      )}
      <span className="local-label">Local workspace</span>
    </header>
  );
}
