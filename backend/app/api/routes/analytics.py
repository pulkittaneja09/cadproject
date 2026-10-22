from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import calendar

from app.schemas.analytics import (
    KPIMetrics, SentimentDistribution, TrendData, 
    CategoryBreakdown, ProductSentiment, RatingDistribution, OverviewAnalytics
)
from app.storage.storage_adapter import get_storage_adapter, StorageAdapter

router = APIRouter()


@router.get("/overview", response_model=OverviewAnalytics)
async def get_overview_analytics(
    dataset_id: Optional[int] = Query(None),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    feedback_list, total = storage.list_feedback(
        dataset_id=dataset_id,
        page=1,
        page_size=10000
    )
    
    analyzed_feedback = [f for f in feedback_list if f.sentiment]
    
    # KPI Metrics
    positive_count = sum(1 for f in analyzed_feedback if f.sentiment == "positive")
    neutral_count = sum(1 for f in analyzed_feedback if f.sentiment == "neutral")
    negative_count = sum(1 for f in analyzed_feedback if f.sentiment == "negative")
    high_priority_count = sum(1 for f in analyzed_feedback if f.priority == "high")
    
    total_analyzed = len(analyzed_feedback) if analyzed_feedback else 1
    
    kpi = KPIMetrics(
        total_reviews=total,
        positive_percentage=round((positive_count / total_analyzed) * 100, 1) if total_analyzed > 0 else 0,
        neutral_percentage=round((neutral_count / total_analyzed) * 100, 1) if total_analyzed > 0 else 0,
        negative_percentage=round((negative_count / total_analyzed) * 100, 1) if total_analyzed > 0 else 0,
        high_priority_complaints=high_priority_count
    )
    
    # Sentiment Distribution
    sentiment_distribution = SentimentDistribution(
        positive=positive_count,
        neutral=neutral_count,
        negative=negative_count
    )
    
    # Volume over time (by date)
    date_counts = Counter()
    sentiment_by_date = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    
    for f in feedback_list:
        if f.date:
            date_key = f.date.strftime("%Y-%m-%d")
            date_counts[date_key] += 1
            if f.sentiment:
                sentiment_by_date[date_key][f.sentiment] += 1
    
    volume_over_time = [
        TrendData(
            date=date,
            count=count,
            positive=sentiment_by_date[date]["positive"],
            neutral=sentiment_by_date[date]["neutral"],
            negative=sentiment_by_date[date]["negative"]
        )
        for date, count in sorted(date_counts.items())
    ]
    
    # Sentiment trends (same as volume over time for now)
    sentiment_trends = volume_over_time
    
    # Category breakdown
    category_counts = Counter(f.category for f in analyzed_feedback if f.category)
    category_breakdown = [
        CategoryBreakdown(
            category=cat,
            count=count,
            percentage=round((count / len(analyzed_feedback)) * 100, 1) if analyzed_feedback else 0
        )
        for cat, count in category_counts.most_common()
    ]
    
    # Product sentiment
    product_data = defaultdict(lambda: {"total": 0, "positive": 0, "neutral": 0, "negative": 0})
    for f in analyzed_feedback:
        if f.product:
            product_data[f.product]["total"] += 1
            product_data[f.product][f.sentiment] += 1
    
    product_sentiment = [
        ProductSentiment(
            product=product,
            total=data["total"],
            positive=data["positive"],
            neutral=data["neutral"],
            negative=data["negative"],
            positive_percentage=round((data["positive"] / data["total"]) * 100, 1) if data["total"] > 0 else 0
        )
        for product, data in sorted(product_data.items(), key=lambda x: x[1]["total"], reverse=True)
    ]
    
    # Rating distribution
    rating_counts = Counter(f.rating for f in feedback_list if f.rating)
    rating_distribution = [
        RatingDistribution(
            rating=rating,
            count=count,
            percentage=round((count / total) * 100, 1) if total > 0 else 0
        )
        for rating, count in sorted(rating_counts.items())
    ]
    
    return OverviewAnalytics(
        kpi=kpi,
        sentiment_distribution=sentiment_distribution,
        volume_over_time=volume_over_time,
        sentiment_trends=sentiment_trends,
        category_breakdown=category_breakdown,
        product_sentiment=product_sentiment,
        rating_distribution=rating_distribution
    )


@router.get("/trends")
async def get_trends(
    dataset_id: Optional[int] = Query(None),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    feedback_list, total = storage.list_feedback(
        dataset_id=dataset_id,
        page=1,
        page_size=10000
    )
    
    date_counts = Counter()
    sentiment_by_date = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    
    for f in feedback_list:
        if f.date:
            date_key = f.date.strftime("%Y-%m-%d")
            date_counts[date_key] += 1
            if f.sentiment:
                sentiment_by_date[date_key][f.sentiment] += 1
    
    return [
        TrendData(
            date=date,
            count=count,
            positive=sentiment_by_date[date]["positive"],
            neutral=sentiment_by_date[date]["neutral"],
            negative=sentiment_by_date[date]["negative"]
        )
        for date, count in sorted(date_counts.items())
    ]


@router.get("/categories")
async def get_categories(
    dataset_id: Optional[int] = Query(None),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    feedback_list, total = storage.list_feedback(
        dataset_id=dataset_id,
        page=1,
        page_size=10000
    )
    
    analyzed_feedback = [f for f in feedback_list if f.sentiment]
    category_counts = Counter(f.category for f in analyzed_feedback if f.category)
    
    return [
        CategoryBreakdown(
            category=cat,
            count=count,
            percentage=round((count / len(analyzed_feedback)) * 100, 1) if analyzed_feedback else 0
        )
        for cat, count in category_counts.most_common()
    ]
