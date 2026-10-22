from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.storage.database import DatasetModel, FeedbackModel, get_db, init_db
from app.schemas.dataset import DatasetCreate, Dataset
from app.schemas.feedback import FeedbackCreate, Feedback, FeedbackFilter
import logging

logger = logging.getLogger(__name__)


class StorageAdapter(ABC):
    @abstractmethod
    def create_dataset(self, dataset: DatasetCreate) -> Dataset:
        pass
    
    @abstractmethod
    def get_dataset(self, dataset_id: int) -> Optional[Dataset]:
        pass
    
    @abstractmethod
    def list_datasets(self) -> List[Dataset]:
        pass
    
    @abstractmethod
    def update_dataset(self, dataset_id: int, **kwargs) -> Optional[Dataset]:
        pass
    
    @abstractmethod
    def create_feedback(self, feedback: FeedbackCreate, dataset_id: int) -> Feedback:
        pass
    
    @abstractmethod
    def create_feedback_batch(self, feedback_list: List[FeedbackCreate], dataset_id: int) -> List[Feedback]:
        pass
    
    @abstractmethod
    def get_feedback(self, feedback_id: int) -> Optional[Feedback]:
        pass
    
    @abstractmethod
    def list_feedback(
        self, 
        dataset_id: Optional[int] = None,
        sentiment: Optional[str] = None,
        product: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> tuple[List[Feedback], int]:
        pass
    
    @abstractmethod
    def update_feedback(self, feedback_id: int, **kwargs) -> Optional[Feedback]:
        pass
    
    @abstractmethod
    def delete_dataset(self, dataset_id: int) -> bool:
        pass


class LocalStorageAdapter(StorageAdapter):
    def __init__(self):
        init_db()
        self.db_generator = get_db
    
    def _get_db(self):
        return next(self.db_generator())
    
    def create_dataset(self, dataset: DatasetCreate) -> Dataset:
        db = self._get_db()
        try:
            db_dataset = DatasetModel(**dataset.model_dump())
            db.add(db_dataset)
            db.commit()
            db.refresh(db_dataset)
            return Dataset.model_validate(db_dataset)
        finally:
            db.close()
    
    def get_dataset(self, dataset_id: int) -> Optional[Dataset]:
        db = self._get_db()
        try:
            db_dataset = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
            return Dataset.model_validate(db_dataset) if db_dataset else None
        finally:
            db.close()
    
    def list_datasets(self) -> List[Dataset]:
        db = self._get_db()
        try:
            db_datasets = db.query(DatasetModel).order_by(DatasetModel.created_at.desc()).all()
            return [Dataset.model_validate(d) for d in db_datasets]
        finally:
            db.close()
    
    def update_dataset(self, dataset_id: int, **kwargs) -> Optional[Dataset]:
        db = self._get_db()
        try:
            db_dataset = db.query(DatasetModel).filter(DatasetModel.id == dataset_id).first()
            if not db_dataset:
                return None
            for key, value in kwargs.items():
                setattr(db_dataset, key, value)
            db.commit()
            db.refresh(db_dataset)
            return Dataset.model_validate(db_dataset)
        finally:
            db.close()
    
    def create_feedback(self, feedback: FeedbackCreate, dataset_id: int) -> Feedback:
        db = self._get_db()
        try:
            db_feedback = FeedbackModel(**feedback.model_dump(), dataset_id=dataset_id)
            db.add(db_feedback)
            db.commit()
            db.refresh(db_feedback)
            return Feedback.model_validate(db_feedback)
        finally:
            db.close()
    
    def create_feedback_batch(self, feedback_list: List[FeedbackCreate], dataset_id: int) -> List[Feedback]:
        db = self._get_db()
        try:
            db_feedbacks = [
                FeedbackModel(**f.model_dump(), dataset_id=dataset_id) 
                for f in feedback_list
            ]
            db.add_all(db_feedbacks)
            db.commit()
            for fb in db_feedbacks:
                db.refresh(fb)
            return [Feedback.model_validate(fb) for fb in db_feedbacks]
        finally:
            db.close()
    
    def get_feedback(self, feedback_id: int) -> Optional[Feedback]:
        db = self._get_db()
        try:
            db_feedback = db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
            return Feedback.model_validate(db_feedback) if db_feedback else None
        finally:
            db.close()
    
    def list_feedback(
        self, 
        dataset_id: Optional[int] = None,
        sentiment: Optional[str] = None,
        product: Optional[str] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> tuple[List[Feedback], int]:
        db = self._get_db()
        try:
            query = db.query(FeedbackModel)
            
            if dataset_id is not None:
                query = query.filter(FeedbackModel.dataset_id == dataset_id)
            if sentiment:
                query = query.filter(FeedbackModel.sentiment == sentiment)
            if product:
                query = query.filter(FeedbackModel.product == product)
            if category:
                query = query.filter(FeedbackModel.category == category)
            if priority:
                query = query.filter(FeedbackModel.priority == priority)
            if date_from:
                query = query.filter(FeedbackModel.date >= date_from)
            if date_to:
                query = query.filter(FeedbackModel.date <= date_to)
            if search:
                query = query.filter(FeedbackModel.review_text.ilike(f"%{search}%"))
            
            total = query.count()
            
            offset = (page - 1) * page_size
            db_feedbacks = query.order_by(FeedbackModel.created_at.desc()).offset(offset).limit(page_size).all()
            
            return [Feedback.model_validate(fb) for fb in db_feedbacks], total
        finally:
            db.close()
    
    def update_feedback(self, feedback_id: int, **kwargs) -> Optional[Feedback]:
        db = self._get_db()
        try:
            db_feedback = db.query(FeedbackModel).filter(FeedbackModel.id == feedback_id).first()
            if not db_feedback:
                return None
            for key, value in kwargs.items():
                setattr(db_feedback, key, value)
            db.commit()
            db.refresh(db_feedback)
            return Feedback.model_validate(db_feedback)
        finally:
            db.close()
    
    def delete_dataset(self, dataset_id: int) -> bool:
        db = self._get_db()
        try:
            db.query(FeedbackModel).filter(FeedbackModel.dataset_id == dataset_id).delete()
            db.query(DatasetModel).filter(DatasetModel.id == dataset_id).delete()
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting dataset: {e}")
            db.rollback()
            return False
        finally:
            db.close()


def get_storage_adapter() -> StorageAdapter:
    from app.config import settings
    if settings.storage_mode == "local":
        return LocalStorageAdapter()
    else:
        raise ValueError(f"Unsupported storage mode: {settings.storage_mode}")
