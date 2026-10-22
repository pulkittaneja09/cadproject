import React, { useState, useEffect } from 'react';
import { OverviewAnalytics, Feedback } from '../types';
import { apiClient } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';

interface OverviewProps {
  selectedDataset: number | null;
  refreshDatasets: () => void;
}

const COLORS = {
  positive: '#10b981',
  neutral: '#f59e0b',
  negative: '#ef4444'
};

export default function Overview({ selectedDataset, refreshDatasets }: OverviewProps) {
  const [analytics, setAnalytics] = useState<OverviewAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
  }, [selectedDataset]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getOverviewAnalytics(selectedDataset || undefined);
      setAnalytics(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load analytics data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !analytics) {
    return (
      <div className="text-center text-gray-400 py-12">
        <p>{error || 'No data available'}</p>
      </div>
    );
  }

  const sentimentData = [
    { name: 'Positive', value: analytics.sentiment_distribution.positive, color: COLORS.positive },
    { name: 'Neutral', value: analytics.sentiment_distribution.neutral, color: COLORS.neutral },
    { name: 'Negative', value: analytics.sentiment_distribution.negative, color: COLORS.negative },
  ];

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-gray-100">{analytics.kpi.total_reviews}</div>
            <div className="text-sm text-gray-400 mt-1">Total Reviews</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-success">{analytics.kpi.positive_percentage}%</div>
            <div className="text-sm text-gray-400 mt-1">Positive</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-warning">{analytics.kpi.neutral_percentage}%</div>
            <div className="text-sm text-gray-400 mt-1">Neutral</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-danger">{analytics.kpi.negative_percentage}%</div>
            <div className="text-sm text-gray-400 mt-1">Negative</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="text-2xl font-bold text-danger">{analytics.kpi.high_priority_complaints}</div>
            <div className="text-sm text-gray-400 mt-1">High Priority</div>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Sentiment Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Feedback Volume Over Time</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analytics.volume_over_time}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Legend />
                <Line type="monotone" dataKey="count" stroke="#6366f1" name="Total" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Sentiment Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analytics.sentiment_trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Legend />
                <Line type="monotone" dataKey="positive" stroke="#10b981" name="Positive" />
                <Line type="monotone" dataKey="neutral" stroke="#f59e0b" name="Neutral" />
                <Line type="monotone" dataKey="negative" stroke="#ef4444" name="Negative" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Category Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={analytics.category_breakdown}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="category" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Bar dataKey="count" fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Product Sentiment */}
      {analytics.product_sentiment.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Product-wise Sentiment</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {analytics.product_sentiment.map((product) => (
                <div key={product.product} className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-100">{product.product}</div>
                    <div className="text-xs text-gray-400">{product.total} reviews</div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-sm font-medium text-success">{product.positive}</div>
                      <div className="text-xs text-gray-400">Positive</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-warning">{product.neutral}</div>
                      <div className="text-xs text-gray-400">Neutral</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-danger">{product.negative}</div>
                      <div className="text-xs text-gray-400">Negative</div>
                    </div>
                    <div className="w-24">
                      <div className="h-2 bg-surfaceLight rounded-full overflow-hidden">
                        <div
                          className="h-full bg-success"
                          style={{ width: `${product.positive_percentage}%` }}
                        />
                      </div>
                      <div className="text-xs text-gray-400 text-center mt-1">
                        {product.positive_percentage}% positive
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Rating Distribution */}
      {analytics.rating_distribution.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Rating Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={analytics.rating_distribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="rating" stroke="#9ca3af" label={{ value: 'Rating', position: 'insideBottom', fill: '#9ca3af' }} />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151' }}
                />
                <Bar dataKey="count" fill="#8b5cf6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
