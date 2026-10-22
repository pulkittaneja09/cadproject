from pydantic import BaseModel
from typing import List, Optional


class Theme(BaseModel):
    theme: str
    count: int
    examples: List[str]


class InsightSummary(BaseModel):
    executive_summary: str
    positive_themes: List[Theme]
    negative_themes: List[Theme]
    common_complaints: List[Theme]
    category_wise_sentiment: dict
    representative_reviews: dict
    suggested_improvements: List[str]
    emerging_issues: Optional[List[str]] = None
    analysis_method: str
