from pydantic import BaseModel
from typing import Optional, Dict, List, Any


class KPIMetrics(BaseModel):
    total_reviews: int
    positive_percentage: float
    neutral_percentage: float
    negative_percentage: float
    high_priority_complaints: int


class SentimentDistribution(BaseModel):
    positive: int
    neutral: int
    negative: int


class TrendData(BaseModel):
    date: str
    count: int
    positive: int
    neutral: int
    negative: int


class CategoryBreakdown(BaseModel):
    category: str
    count: int
    percentage: float


class ProductSentiment(BaseModel):
    product: str
    total: int
    positive: int
    neutral: int
    negative: int
    positive_percentage: float


class RatingDistribution(BaseModel):
    rating: int
    count: int
    percentage: float


class OverviewAnalytics(BaseModel):
    kpi: KPIMetrics
    sentiment_distribution: SentimentDistribution
    volume_over_time: List[TrendData]
    sentiment_trends: List[TrendData]
    category_breakdown: List[CategoryBreakdown]
    product_sentiment: List[ProductSentiment]
    rating_distribution: List[RatingDistribution]
