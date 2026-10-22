export interface Feedback {
  id: number;
  dataset_id: number;
  review_text: string;
  date: string | null;
  product: string | null;
  rating: number | null;
  sentiment: 'positive' | 'neutral' | 'negative' | null;
  confidence: number | null;
  category: string | null;
  priority: 'low' | 'medium' | 'high' | null;
  priority_explanation: string | null;
  created_at: string;
  analyzed_at: string | null;
}

export interface Dataset {
  id: number;
  name: string;
  description: string | null;
  row_count: number;
  analyzed_count: number;
  status: string;
  created_at: string;
  analyzed_at: string | null;
}

export interface KPIMetrics {
  total_reviews: number;
  positive_percentage: number;
  neutral_percentage: number;
  negative_percentage: number;
  high_priority_complaints: number;
}

export interface SentimentDistribution {
  positive: number;
  neutral: number;
  negative: number;
}

export interface TrendData {
  date: string;
  count: number;
  positive: number;
  neutral: number;
  negative: number;
}

export interface CategoryBreakdown {
  category: string;
  count: number;
  percentage: number;
}

export interface ProductSentiment {
  product: string;
  total: number;
  positive: number;
  neutral: number;
  negative: number;
  positive_percentage: number;
}

export interface RatingDistribution {
  rating: number;
  count: number;
  percentage: number;
}

export interface OverviewAnalytics {
  kpi: KPIMetrics;
  sentiment_distribution: SentimentDistribution;
  volume_over_time: TrendData[];
  sentiment_trends: TrendData[];
  category_breakdown: CategoryBreakdown[];
  product_sentiment: ProductSentiment[];
  rating_distribution: RatingDistribution[];
}

export interface Theme {
  theme: string;
  count: number;
  examples: string[];
}

export interface InsightSummary {
  executive_summary: string;
  positive_themes: Theme[];
  negative_themes: Theme[];
  common_complaints: Theme[];
  category_wise_sentiment: Record<string, { positive: number; neutral: number; negative: number }>;
  representative_reviews: {
    positive: string[];
    negative: string[];
  };
  suggested_improvements: string[];
  emerging_issues: string[] | null;
  analysis_method: string;
}

export interface FeedbackListResponse {
  items: Feedback[];
  total: number;
  page: number;
  page_size: number;
}
