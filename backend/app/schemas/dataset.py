from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DatasetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class DatasetCreate(DatasetBase):
    pass


class Dataset(DatasetBase):
    id: int
    row_count: int
    analyzed_count: int
    status: str
    created_at: datetime
    analyzed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DatasetStats(BaseModel):
    id: int
    name: str
    total_reviews: int
    analyzed_reviews: int
    positive_count: int
    neutral_count: int
    negative_count: int
    high_priority_count: int
