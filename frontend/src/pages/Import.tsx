import React, { useState, useRef } from 'react';
import { apiClient } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { Upload, FileText, Download, CheckCircle, AlertCircle } from 'lucide-react';

interface ImportProps {
  selectedDataset: number | null;
  refreshDatasets: () => void;
}

export default function Import({ selectedDataset, refreshDatasets }: ImportProps) {
  const [file, setFile] = useState<File | null>(null);
  const [datasetName, setDatasetName] = useState('');
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.name.endsWith('.csv')) {
        setFile(droppedFile);
        if (!datasetName) {
          setDatasetName(droppedFile.name.replace('.csv', ''));
        }
        setError(null);
      } else {
        setError('Only CSV files are supported');
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile);
        if (!datasetName) {
          setDatasetName(selectedFile.name.replace('.csv', ''));
        }
        setError(null);
      } else {
        setError('Only CSV files are supported');
      }
    }
  };

  const handleUpload = async () => {
    if (!file || !datasetName) {
      setError('Please select a file and provide a dataset name');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      
      const response = await apiClient.uploadFeedback(file, datasetName, description);
      setUploadResult(response.data);
      refreshDatasets();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadResult) return;

    try {
      setAnalyzing(true);
      setError(null);
      
      await apiClient.analyzeFeedback(uploadResult.dataset_id);
      setUploadResult({ ...uploadResult, analyzed: true });
      refreshDatasets();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze feedback');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleDownloadSample = () => {
    const sampleCSV = `review_text,date,product,rating
"Great product, very satisfied!",2024-01-15,Product A,5
"Good quality but delivery was slow",2024-01-16,Product B,3
"Excellent customer service",2024-01-17,Product A,5
"Product arrived damaged",2024-01-18,Product C,1
"Too expensive for what you get",2024-01-19,Product B,2
"Easy to use and setup",2024-01-20,Product A,4
"Terrible experience, will not buy again",2024-01-21,Product C,1
"Average product, nothing special",2024-01-22,Product B,3`;
    
    const blob = new Blob([sampleCSV], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'sample_feedback.csv');
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const resetForm = () => {
    setFile(null);
    setDatasetName('');
    setDescription('');
    setUploadResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Upload Customer Feedback</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                dragActive
                  ? 'border-primary bg-primary/10'
                  : 'border-gray-600 hover:border-gray-500'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-gray-300 mb-2">
                Drag and drop your CSV file here, or click to browse
              </p>
              <p className="text-sm text-gray-500 mb-4">
                Required column: review_text. Optional: date, product, rating
              </p>
              <input
                ref={fileInputRef}
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
              />
              <Button
                variant="secondary"
                onClick={() => fileInputRef.current?.click()}
              >
                Browse Files
              </Button>
            </div>

            {file && (
              <div className="flex items-center gap-3 p-3 bg-surfaceLight rounded-lg">
                <FileText className="text-primary" size={20} />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-100">{file.name}</p>
                  <p className="text-xs text-gray-400">{(file.size / 1024).toFixed(2)} KB</p>
                </div>
                <Button variant="ghost" size="sm" onClick={() => setFile(null)}>
                  Remove
                </Button>
              </div>
            )}

            <Input
              label="Dataset Name"
              placeholder="Enter a name for this dataset"
              value={datasetName}
              onChange={(e) => setDatasetName(e.target.value)}
            />

            <Input
              label="Description (Optional)"
              placeholder="Describe this dataset"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />

            <Button
              onClick={handleUpload}
              disabled={!file || !datasetName || uploading}
              className="w-full"
            >
              {uploading ? (
                <>
                  <LoadingSpinner size="sm" />
                  <span className="ml-2">Uploading...</span>
                </>
              ) : (
                'Upload Dataset'
              )}
            </Button>

            {error && (
              <div className="flex items-center gap-2 text-danger text-sm">
                <AlertCircle size={16} />
                <span>{error}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {uploadResult && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3 mb-4">
              <CheckCircle className="text-success" size={24} />
              <div>
                <h3 className="font-medium text-gray-100">Upload Successful</h3>
                <p className="text-sm text-gray-400">
                  {uploadResult.row_count} reviews imported
                </p>
              </div>
            </div>

            {!uploadResult.analyzed ? (
              <Button
                onClick={handleAnalyze}
                disabled={analyzing}
                className="w-full"
              >
                {analyzing ? (
                  <>
                    <LoadingSpinner size="sm" />
                    <span className="ml-2">Analyzing...</span>
                  </>
                ) : (
                  'Start AI Analysis'
                )}
              </Button>
            ) : (
              <div className="flex items-center gap-2 text-success">
                <CheckCircle size={16} />
                <span>Analysis complete</span>
              </div>
            )}

            <Button
              variant="secondary"
              onClick={resetForm}
              className="w-full mt-3"
            >
              Upload Another Dataset
            </Button>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Need Help?</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-400 mb-4">
            Download a sample CSV file to see the expected format.
          </p>
          <Button variant="secondary" onClick={handleDownloadSample}>
            <Download size={16} className="mr-2" />
            Download Sample CSV
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
