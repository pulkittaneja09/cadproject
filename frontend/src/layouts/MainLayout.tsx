import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import { Dataset } from '../types';
import { apiClient } from '../lib/api';

interface MainLayoutProps {
  children: React.ReactNode;
  title: string;
  showDatasetSelector?: boolean;
}

export default function MainLayout({ children, title, showDatasetSelector = true }: MainLayoutProps) {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const response = await apiClient.listDatasets();
      setDatasets(response.data);
      if (response.data.length > 0) {
        setSelectedDataset(response.data[0].id);
      }
    } catch (error) {
      console.error('Failed to load datasets:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDatasetChange = (datasetId: number | null) => {
    setSelectedDataset(datasetId);
  };

  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        {showDatasetSelector && !loading && (
          <Navbar
            title={title}
            datasets={datasets}
            selectedDataset={selectedDataset}
            onDatasetChange={handleDatasetChange}
          />
        )}
        {!showDatasetSelector && (
          <header className="bg-surface border-b border-gray-700 px-6 py-4">
            <h2 className="text-xl font-semibold text-gray-100">{title}</h2>
          </header>
        )}
        <main className="flex-1 overflow-auto p-6 scrollbar-thin">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-gray-400">Loading...</div>
            </div>
          ) : (
            <div className="max-w-7xl mx-auto">
              {React.cloneElement(children as React.ReactElement, {
                selectedDataset,
                refreshDatasets: loadDatasets
              })}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
