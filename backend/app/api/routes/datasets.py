from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.dataset import DatasetCreate, Dataset, DatasetStats
from app.storage.storage_adapter import get_storage_adapter, StorageAdapter
from app.ai.sentiment import sentiment_analyzer
from app.ai.categorizer import complaint_categorizer
from app.ai.priority import priority_detector
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=Dataset)
async def create_dataset(
    dataset: DatasetCreate,
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    return storage.create_dataset(dataset)


@router.get("", response_model=List[Dataset])
async def list_datasets(storage: StorageAdapter = Depends(get_storage_adapter)):
    return storage.list_datasets()


@router.get("/{dataset_id}", response_model=Dataset)
async def get_dataset(
    dataset_id: int,
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    dataset = storage.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset


@router.get("/{dataset_id}/stats", response_model=DatasetStats)
async def get_dataset_stats(
    dataset_id: int,
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    from app.schemas.feedback import FeedbackFilter
    
    feedback_list, total = storage.list_feedback(dataset_id=dataset_id, page=1, page_size=10000)
    
    positive_count = sum(1 for f in feedback_list if f.sentiment == "positive")
    neutral_count = sum(1 for f in feedback_list if f.sentiment == "neutral")
    negative_count = sum(1 for f in feedback_list if f.sentiment == "negative")
    high_priority_count = sum(1 for f in feedback_list if f.priority == "high")
    
    dataset = storage.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return DatasetStats(
        id=dataset.id,
        name=dataset.name,
        total_reviews=total,
        analyzed_reviews=len([f for f in feedback_list if f.sentiment]),
        positive_count=positive_count,
        neutral_count=neutral_count,
        negative_count=negative_count,
        high_priority_count=high_priority_count
    )


@router.delete("/{dataset_id}")
async def delete_dataset(
    dataset_id: int,
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    success = storage.delete_dataset(dataset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {"message": "Dataset deleted successfully"}
