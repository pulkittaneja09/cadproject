from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
import pandas as pd
import io
import csv
import logging

from app.schemas.feedback import FeedbackCreate, Feedback, FeedbackListResponse
from app.schemas.dataset import DatasetCreate
from app.storage.storage_adapter import get_storage_adapter, StorageAdapter
from app.ai.sentiment import sentiment_analyzer
from app.ai.categorizer import complaint_categorizer
from app.ai.priority import priority_detector

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def upload_feedback(
    file: UploadFile = File(...),
    name: str = Query(...),
    description: Optional[str] = Query(None),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        # Validate required column
        if 'review_text' not in df.columns:
            # Try to find similar column names
            possible_columns = [col for col in df.columns if 'review' in col.lower() or 'text' in col.lower() or 'comment' in col.lower()]
            if possible_columns:
                df = df.rename(columns={possible_columns[0]: 'review_text'})
            else:
                raise HTTPException(status_code=400, detail="CSV must contain 'review_text' column")
        
        # Normalize column names
        column_mapping = {
            'date': 'date',
            'product': 'product',
            'rating': 'rating',
            'review': 'review_text',
            'comment': 'review_text',
            'feedback': 'review_text'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns and new_name not in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Create dataset
        dataset = storage.create_dataset(DatasetCreate(
            name=name,
            description=description
        ))
        
        # Parse and create feedback records
        feedback_list = []
        for _, row in df.iterrows():
            feedback_data = {
                'review_text': str(row['review_text']),
                'date': None,
                'product': None,
                'rating': None
            }
            
            if 'date' in df.columns and pd.notna(row['date']):
                try:
                    feedback_data['date'] = pd.to_datetime(row['date']).to_pydatetime()
                except:
                    pass
            
            if 'product' in df.columns and pd.notna(row['product']):
                feedback_data['product'] = str(row['product'])
            
            if 'rating' in df.columns and pd.notna(row['rating']):
                try:
                    feedback_data['rating'] = int(row['rating'])
                except:
                    pass
            
            feedback_list.append(FeedbackCreate(**feedback_data))
        
        # Batch insert feedback
        storage.create_feedback_batch(feedback_list, dataset.id)
        
        # Update dataset row count
        storage.update_dataset(dataset.id, row_count=len(feedback_list))
        
        return {
            "dataset_id": dataset.id,
            "name": dataset.name,
            "row_count": len(feedback_list),
            "message": "File uploaded successfully"
        }
    
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/{dataset_id}/analyze")
async def analyze_feedback(
    dataset_id: int,
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    dataset = storage.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Get all unanalyzed feedback
    feedback_list, total = storage.list_feedback(dataset_id=dataset_id, page=1, page_size=10000)
    
    unanalyzed = [f for f in feedback_list if not f.sentiment]
    
    if not unanalyzed:
        return {"message": "All feedback already analyzed", "analyzed_count": 0}
    
    logger.info(f"Analyzing {len(unanalyzed)} feedback items")
    
    # Extract texts for batch processing
    texts = [f.review_text for f in unanalyzed]
    
    # Batch sentiment analysis
    sentiment_results = sentiment_analyzer.analyze_batch(texts)
    sentiments = [s[0] for s in sentiment_results]
    confidences = [s[1] for s in sentiment_results]
    
    # Batch categorization
    categories = complaint_categorizer.categorize_batch(texts)
    
    # Batch priority detection
    priority_results = priority_detector.detect_batch(sentiments, confidences, texts, categories)
    priorities = [p[0] for p in priority_results]
    priority_explanations = [p[1] for p in priority_results]
    
    # Update feedback with analysis results
    analyzed_count = 0
    for i, feedback in enumerate(unanalyzed):
        storage.update_feedback(
            feedback.id,
            sentiment=sentiments[i],
            confidence=confidences[i],
            category=categories[i],
            priority=priorities[i],
            priority_explanation=priority_explanations[i],
            analyzed_at=datetime.utcnow()
        )
        analyzed_count += 1
    
    # Update dataset
    storage.update_dataset(
        dataset_id,
        analyzed_count=dataset.analyzed_count + analyzed_count,
        status="analyzed",
        analyzed_at=datetime.utcnow()
    )
    
    return {
        "message": f"Analyzed {analyzed_count} feedback items",
        "analyzed_count": analyzed_count
    }


@router.get("", response_model=FeedbackListResponse)
async def list_feedback(
    dataset_id: Optional[int] = Query(None),
    sentiment: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    date_from_dt = None
    date_to_dt = None
    
    if date_from:
        try:
            date_from_dt = datetime.fromisoformat(date_from)
        except:
            pass
    
    if date_to:
        try:
            date_to_dt = datetime.fromisoformat(date_to)
        except:
            pass
    
    items, total = storage.list_feedback(
        dataset_id=dataset_id,
        sentiment=sentiment,
        product=product,
        category=category,
        priority=priority,
        date_from=date_from_dt,
        date_to=date_to_dt,
        search=search,
        page=page,
        page_size=page_size
    )
    
    return FeedbackListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/export")
async def export_feedback(
    dataset_id: Optional[int] = Query(None),
    sentiment: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    storage: StorageAdapter = Depends(get_storage_adapter)
):
    items, total = storage.list_feedback(
        dataset_id=dataset_id,
        sentiment=sentiment,
        product=product,
        category=category,
        priority=priority,
        search=search,
        page=1,
        page_size=10000
    )
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        'id', 'review_text', 'date', 'product', 'rating',
        'sentiment', 'confidence', 'category', 'priority', 'priority_explanation'
    ])
    
    for item in items:
        writer.writerow([
            item.id,
            item.review_text,
            item.date.isoformat() if item.date else '',
            item.product or '',
            item.rating or '',
            item.sentiment or '',
            item.confidence or '',
            item.category or '',
            item.priority or '',
            item.priority_explanation or ''
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=feedback_export.csv'}
    )
