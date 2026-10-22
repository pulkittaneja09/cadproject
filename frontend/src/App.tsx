import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Overview from './pages/Overview';
import FeedbackExplorer from './pages/FeedbackExplorer';
import Insights from './pages/Insights';
import Import from './pages/Import';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout title="Overview" showDatasetSelector={true}><Overview selectedDataset={null} refreshDatasets={() => {}} /></MainLayout>} />
        <Route path="/feedback" element={<MainLayout title="Feedback Explorer" showDatasetSelector={true}><FeedbackExplorer selectedDataset={null} refreshDatasets={() => {}} /></MainLayout>} />
        <Route path="/insights" element={<MainLayout title="AI Insights" showDatasetSelector={true}><Insights selectedDataset={null} refreshDatasets={() => {}} /></MainLayout>} />
        <Route path="/import" element={<MainLayout title="Import Feedback" showDatasetSelector={false}><Import selectedDataset={null} refreshDatasets={() => {}} /></MainLayout>} />
        <Route path="/settings" element={<MainLayout title="Settings" showDatasetSelector={false}><Settings selectedDataset={null} refreshDatasets={() => {}} /></MainLayout>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
