from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.api.routes import feedback, analytics, insights, datasets
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting InsightPulse AI backend...")
    yield
    logger.info("Shutting down InsightPulse AI backend...")


app = FastAPI(
    title="InsightPulse AI API",
    description="Customer Feedback Analytics Platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback.router, prefix="/api/feedback", tags=["feedback"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "storage_mode": settings.storage_mode,
        "ai_model": settings.sentiment_model,
        "ai_fallback_enabled": settings.enable_ai_fallback
    }
