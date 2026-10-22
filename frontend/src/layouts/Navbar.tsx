import { Dataset } from '../types';
import Select from '../components/ui/Select';

interface NavbarProps {
  title: string;
  datasets: Dataset[];
  selectedDataset: number | null;
  onDatasetChange: (datasetId: number | null) => void;
}

export default function Navbar({ title, datasets, selectedDataset, onDatasetChange }: NavbarProps) {
  return (
    <header className="bg-surface border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-6">
          <h2 className="text-xl font-semibold text-gray-100">{title}</h2>
          
          {datasets.length > 0 && (
            <div className="w-64">
              <Select
                value={selectedDataset?.toString() || ''}
                onChange={(e) => onDatasetChange(e.target.value ? parseInt(e.target.value) : null)}
              >
                <option value="">All Datasets</option>
                {datasets.map((dataset) => (
                  <option key={dataset.id} value={dataset.id.toString()}>
                    {dataset.name} ({dataset.row_count} reviews)
                  </option>
                ))}
              </Select>
            </div>
          )}
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <div className="w-8 h-8 rounded-full bg-primaryLight flex items-center justify-center">
              <span className="text-white font-medium">U</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
