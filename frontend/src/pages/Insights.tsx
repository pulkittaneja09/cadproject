import React, { useState, useEffect } from 'react';
import { InsightSummary } from '../types';
import { apiClient } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import LoadingSpinner from '../components/ui/LoadingSpinner';
import Badge from '../components/ui/Badge';

interface InsightsProps {
  selectedDataset: number | null;
  refreshDatasets: () => void;
}

export default function Insights({ selectedDataset, refreshDatasets }: InsightsProps) {
  const [insights, setInsights] = useState<InsightSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInsights();
  }, [selectedDataset]);

  const loadInsights = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getInsights(selectedDataset || undefined);
      setInsights(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load insights');
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

  if (error || !insights) {
    return (
      <div className="text-center text-gray-400 py-12">
        <p>{error || 'No insights available'}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Executive Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-300 leading-relaxed">{insights.executive_summary}</p>
          <div className="mt-4">
            <Badge variant="neutral">Analysis method: {insights.analysis_method}</Badge>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Positive Themes</CardTitle>
          </CardHeader>
          <CardContent>
            {insights.positive_themes.length === 0 ? (
              <p className="text-gray-400">No positive themes identified</p>
            ) : (
              <div className="space-y-4">
                {insights.positive_themes.map((theme, index) => (
                  <div key={index} className="border-l-2 border-success pl-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-100">{theme.theme}</h4>
                      <Badge variant="success">{theme.count} mentions</Badge>
                    </div>
                    <div className="space-y-1">
                      {theme.examples.map((example, i) => (
                        <p key={i} className="text-sm text-gray-400 italic">{example}</p>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Negative Themes</CardTitle>
          </CardHeader>
          <CardContent>
            {insights.negative_themes.length === 0 ? (
              <p className="text-gray-400">No negative themes identified</p>
            ) : (
              <div className="space-y-4">
                {insights.negative_themes.map((theme, index) => (
                  <div key={index} className="border-l-2 border-danger pl-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-100">{theme.theme}</h4>
                      <Badge variant="danger">{theme.count} mentions</Badge>
                    </div>
                    <div className="space-y-1">
                      {theme.examples.map((example, i) => (
                        <p key={i} className="text-sm text-gray-400 italic">{example}</p>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Common Complaints</CardTitle>
        </CardHeader>
        <CardContent>
          {insights.common_complaints.length === 0 ? (
            <p className="text-gray-400">No common complaints identified</p>
          ) : (
            <div className="space-y-4">
              {insights.common_complaints.map((complaint, index) => (
                <div key={index} className="border border-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-100">{complaint.theme}</h4>
                    <Badge variant="warning">{complaint.count} complaints</Badge>
                  </div>
                  <div className="space-y-1">
                    {complaint.examples.map((example, i) => (
                      <p key={i} className="text-sm text-gray-400 italic">{example}</p>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Suggested Improvements</CardTitle>
        </CardHeader>
        <CardContent>
          {insights.suggested_improvements.length === 0 ? (
            <p className="text-gray-400">No suggestions available</p>
          ) : (
            <ul className="space-y-3">
              {insights.suggested_improvements.map((improvement, index) => (
                <li key={index} className="flex items-start gap-3">
                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primaryLight flex items-center justify-center text-white text-sm">
                    {index + 1}
                  </span>
                  <p className="text-gray-300">{improvement}</p>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      {insights.emerging_issues && insights.emerging_issues.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Emerging Issues</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {insights.emerging_issues.map((issue, index) => (
                <li key={index} className="text-gray-300">• {issue}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Representative Reviews</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            <div>
              <h4 className="font-medium text-success mb-3">Positive Reviews</h4>
              {insights.representative_reviews.positive.length === 0 ? (
                <p className="text-gray-400">No positive reviews available</p>
              ) : (
                <div className="space-y-2">
                  {insights.representative_reviews.positive.map((review, index) => (
                    <p key={index} className="text-sm text-gray-300 bg-surfaceLight rounded p-3">
                      {review}
                    </p>
                  ))}
                </div>
              )}
            </div>
            <div>
              <h4 className="font-medium text-danger mb-3">Negative Reviews</h4>
              {insights.representative_reviews.negative.length === 0 ? (
                <p className="text-gray-400">No negative reviews available</p>
              ) : (
                <div className="space-y-2">
                  {insights.representative_reviews.negative.map((review, index) => (
                    <p key={index} className="text-sm text-gray-300 bg-surfaceLight rounded p-3">
                      {review}
                    </p>
                  ))}
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
