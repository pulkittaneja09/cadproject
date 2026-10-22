from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class FeedbackBase(BaseModel):
    review_text: str = Field(..., min_length=1, max_length=10000)
    date: Optional[datetime] = None
    product: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackAnalysis(BaseModel):
    sentiment: Literal["positive", "neutral", "negative"]
    confidence: float = Field(..., ge=0, le=1)
    category: str
    priority: Literal["low", "medium", "high"]
    priority_explanation: str


class Feedback(FeedbackBase):
    id: int
    dataset_id: int
    sentiment: Optional[str] = None
    confidence: Optional[float] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    priority_explanation: Optional[str] = None
    created_at: datetime
    analyzed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class FeedbackFilter(BaseModel):
    dataset_id: Optional[int] = None
    sentiment: Optional[str] = None
    product: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    search: Optional[str] = None


class FeedbackListResponse(BaseModel):
    items: list[Feedback]
    total: int
    page: int
    page_size: int
