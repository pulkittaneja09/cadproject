import React, { useState, useEffect } from 'react';
import { Feedback } from '../types';
import { apiClient } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { formatDateTime, formatConfidence } from '../lib/utils';
import { ChevronDown, ChevronUp, Download, Search } from 'lucide-react';

interface FeedbackExplorerProps {
  selectedDataset: number | null;
  refreshDatasets: () => void;
}

export default function FeedbackExplorer({ selectedDataset, refreshDatasets }: FeedbackExplorerProps) {
  const [feedback, setFeedback] = useState<Feedback[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  
  const [filters, setFilters] = useState({
    sentiment: '',
    product: '',
    category: '',
    priority: '',
    search: ''
  });

  useEffect(() => {
    loadFeedback();
  }, [selectedDataset, page, filters]);

  const loadFeedback = async () => {
    try {
      setLoading(true);
      const response = await apiClient.listFeedback({
        dataset_id: selectedDataset || undefined,
        sentiment: filters.sentiment || undefined,
        product: filters.product || undefined,
        category: filters.category || undefined,
        priority: filters.priority || undefined,
        search: filters.search || undefined,
        page,
        page_size: 20
      });
      setFeedback(response.data.items);
      setTotal(response.data.total);
    } catch (error) {
      console.error('Failed to load feedback:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await apiClient.exportFeedback({
        dataset_id: selectedDataset || undefined,
        sentiment: filters.sentiment || undefined,
        product: filters.product || undefined,
        category: filters.category || undefined,
        priority: filters.priority || undefined,
        search: filters.search || undefined
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'feedback_export.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Failed to export:', error);
    }
  };

  const getSentimentVariant = (sentiment: string | null) => {
    switch (sentiment) {
      case 'positive': return 'success';
      case 'negative': return 'danger';
      case 'neutral': return 'warning';
      default: return 'neutral';
    }
  };

  const getPriorityVariant = (priority: string | null) => {
    switch (priority) {
      case 'high': return 'danger';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'neutral';
    }
  };

  const totalPages = Math.ceil(total / 20);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Filters</CardTitle>
            <Button variant="secondary" onClick={handleExport}>
              <Download size={16} className="mr-2" />
              Export CSV
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
              <Input
                placeholder="Search reviews..."
                value={filters.search}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
                className="pl-10"
              />
            </div>
            <Select
              value={filters.sentiment}
              onChange={(e) => setFilters({ ...filters, sentiment: e.target.value })}
            >
              <option value="">All Sentiments</option>
              <option value="positive">Positive</option>
              <option value="neutral">Neutral</option>
              <option value="negative">Negative</option>
            </Select>
            <Input
              placeholder="Product"
              value={filters.product}
              onChange={(e) => setFilters({ ...filters, product: e.target.value })}
            />
            <Select
              value={filters.category}
              onChange={(e) => setFilters({ ...filters, category: e.target.value })}
            >
              <option value="">All Categories</option>
              <option value="Delivery">Delivery</option>
              <option value="Customer Support">Customer Support</option>
              <option value="Payment">Payment</option>
              <option value="Product Quality">Product Quality</option>
              <option value="Pricing">Pricing</option>
              <option value="App / Usability">App / Usability</option>
              <option value="Other">Other</option>
            </Select>
            <Select
              value={filters.priority}
              onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
            >
              <option value="">All Priorities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="pt-6">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <LoadingSpinner size="lg" />
            </div>
          ) : feedback.length === 0 ? (
            <div className="text-center text-gray-400 py-12">
              <p>No feedback found</p>
            </div>
          ) : (
            <>
              <div className="space-y-4">
                {feedback.map((item) => (
                  <div
                    key={item.id}
                    className="border border-gray-700 rounded-lg p-4 hover:border-gray-600 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1">
                        <p className="text-gray-100 mb-2">{item.review_text}</p>
                        <div className="flex flex-wrap items-center gap-2 text-sm">
                          <span className="text-gray-400">{formatDateTime(item.created_at)}</span>
                          {item.product && (
                            <span className="text-gray-400">• {item.product}</span>
                          )}
                          {item.rating && (
                            <span className="text-gray-400">• Rating: {item.rating}/5</span>
                          )}
                        </div>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        {item.sentiment && (
                          <Badge variant={getSentimentVariant(item.sentiment)}>
                            {item.sentiment}
                          </Badge>
                        )}
                        {item.priority && (
                          <Badge variant={getPriorityVariant(item.priority)}>
                            {item.priority}
                          </Badge>
                        )}
                        <button
                          onClick={() => setExpandedId(expandedId === item.id ? null : item.id)}
                          className="text-gray-400 hover:text-gray-100"
                        >
                          {expandedId === item.id ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                        </button>
                      </div>
                    </div>
                    
                    {expandedId === item.id && (
                      <div className="mt-4 pt-4 border-t border-gray-700 space-y-2">
                        {item.category && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Category:</span>
                            <span className="text-gray-100">{item.category}</span>
                          </div>
                        )}
                        {item.confidence !== null && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Confidence:</span>
                            <span className="text-gray-100">{formatConfidence(item.confidence)}</span>
                          </div>
                        )}
                        {item.priority_explanation && (
                          <div className="text-sm">
                            <span className="text-gray-400">Priority explanation:</span>
                            <p className="text-gray-100 mt-1">{item.priority_explanation}</p>
                          </div>
                        )}
                        {item.analyzed_at && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-400">Analyzed at:</span>
                            <span className="text-gray-100">{formatDateTime(item.analyzed_at)}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {totalPages > 1 && (
                <div className="flex items-center justify-between mt-6 pt-6 border-t border-gray-700">
                  <div className="text-sm text-gray-400">
                    Showing {((page - 1) * 20) + 1} to {Math.min(page * 20, total)} of {total} results
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="secondary"
                      onClick={() => setPage(p => Math.max(1, p - 1))}
                      disabled={page === 1}
                    >
                      Previous
                    </Button>
                    <span className="flex items-center px-3 text-gray-100">
                      Page {page} of {totalPages}
                    </span>
                    <Button
                      variant="secondary"
                      onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                      disabled={page === totalPages}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
