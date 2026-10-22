from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from collections import Counter, defaultdict
import logging

from app.schemas.insights import InsightSummary, Theme
from app.storage.storage_adapter import get_storage_adapter, StorageAdapter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=InsightSummary)
async def get_insights(
    dataset_id: Optional[int] = Query(None),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    feedback_list, total = storage.list_feedback(
        dataset_id=dataset_id,
        page=1,
        page_size=10000
    )
    
    analyzed_feedback = [f for f in feedback_list if f.sentiment]
    
    if not analyzed_feedback:
        return InsightSummary(
            executive_summary="No analyzed feedback available for insights generation.",
            positive_themes=[],
            negative_themes=[],
            common_complaints=[],
            category_wise_sentiment={},
            representative_reviews={},
            suggested_improvements=["Upload and analyze feedback data to generate insights."],
            analysis_method="extractive"
        )
    
    # Executive Summary
    positive_count = sum(1 for f in analyzed_feedback if f.sentiment == "positive")
    neutral_count = sum(1 for f in analyzed_feedback if f.sentiment == "neutral")
    negative_count = sum(1 for f in analyzed_feedback if f.sentiment == "negative")
    high_priority_count = sum(1 for f in analyzed_feedback if f.priority == "high")
    
    executive_summary = (
        f"This dataset contains {len(analyzed_feedback)} analyzed customer reviews. "
        f"Sentiment distribution shows {positive_count} positive ({round(positive_count/len(analyzed_feedback)*100, 1)}%), "
        f"{neutral_count} neutral ({round(neutral_count/len(analyzed_feedback)*100, 1)}%), and "
        f"{negative_count} negative ({round(negative_count/len(analyzed_feedback)*100, 1)}%) reviews. "
        f"There are {high_priority_count} high-priority issues requiring immediate attention."
    )
    
    # Extract themes by sentiment
    positive_reviews = [f for f in analyzed_feedback if f.sentiment == "positive"]
    negative_reviews = [f for f in analyzed_feedback if f.sentiment == "negative"]
    
    positive_themes = _extract_themes(positive_reviews, "positive")
    negative_themes = _extract_themes(negative_reviews, "negative")
    
    # Common complaints (by category)
    category_counts = Counter(f.category for f in negative_reviews if f.category)
    common_complaints = []
    for category, count in category_counts.most_common(5):
        examples = [f.review_text[:100] + "..." for f in negative_reviews if f.category == category][:2]
        common_complaints.append(
            Theme(
                theme=category,
                count=count,
                examples=examples
            )
        )
    
    # Category-wise sentiment
    category_sentiment = defaultdict(lambda: {"positive": 0, "neutral": 0, "negative": 0})
    for f in analyzed_feedback:
        if f.category:
            category_sentiment[f.category][f.sentiment] += 1
    
    category_wise_sentiment = dict(category_sentiment)
    
    # Representative reviews
    representative_reviews = {
        "positive": [f.review_text for f in positive_reviews[:3]],
        "negative": [f.review_text for f in negative_reviews[:3]]
    }
    
    # Suggested improvements (based on common complaints)
    suggested_improvements = []
    for complaint in common_complaints[:3]:
        if complaint.theme == "Delivery":
            suggested_improvements.append("Review and optimize delivery logistics to reduce delays and improve tracking accuracy.")
        elif complaint.theme == "Customer Support":
            suggested_improvements.append("Enhance customer support training and reduce response times.")
        elif complaint.theme == "Product Quality":
            suggested_improvements.append("Implement stricter quality control measures and improve product durability.")
        elif complaint.theme == "Payment":
            suggested_improvements.append("Simplify payment processes and ensure billing accuracy.")
        elif complaint.theme == "App / Usability":
            suggested_improvements.append("Improve application interface and fix reported usability issues.")
        else:
            suggested_improvements.append(f"Address issues related to {complaint.theme} to improve customer satisfaction.")
    
    return InsightSummary(
        executive_summary=executive_summary,
        positive_themes=positive_themes,
        negative_themes=negative_themes,
        common_complaints=common_complaints,
        category_wise_sentiment=category_wise_sentiment,
        representative_reviews=representative_reviews,
        suggested_improvements=suggested_improvements,
        analysis_method="extractive"
    )


def _extract_themes(reviews: List, sentiment_type: str) -> List[Theme]:
    """Extract themes from reviews using category-based grouping"""
    if not reviews:
        return []
    
    category_reviews = defaultdict(list)
    for f in reviews:
        if f.category:
            category_reviews[f.category].append(f.review_text)
    
    themes = []
    for category, texts in category_reviews.items():
        examples = [text[:100] + "..." for text in texts[:2]]
        themes.append(
            Theme(
                theme=category,
                count=len(texts),
                examples=examples
            )
        )
    
    return sorted(themes, key=lambda x: x.count, reverse=True)[:5]
