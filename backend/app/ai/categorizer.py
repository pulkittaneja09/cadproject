from typing import Dict, List
import logging
from app.config import settings
from app.ai.gemini_service import gemini_service, AnalysisError

logger = logging.getLogger(__name__)


class ComplaintCategorizer:
    def __init__(self):
        self.use_gemini = True
        self.fallback_mode = False
        
        # Fallback keyword-based categories
        self.categories = {
            "Delivery": [
                "delivery", "shipping", "shipped", "arrived", "late", "delayed",
                "package", "tracking", "courier", "logistics", "dispatch"
            ],
            "Customer Support": [
                "support", "service", "help", "agent", "representative", "response",
                "ticket", "contact", "call", "email", "chat", "assistance", "rude"
            ],
            "Payment": [
                "payment", "charge", "billing", "invoice", "refund", "credit card",
                "transaction", "price", "cost", "expensive", "overcharge", "fee"
            ],
            "Product Quality": [
                "quality", "defective", "broken", "damaged", "faulty", "poor quality",
                "cheap", "durability", "material", "manufacturing", "defect"
            ],
            "Pricing": [
                "price", "expensive", "cost", "cheap", "value", "affordable",
                "overpriced", "discount", "deal", "offer", "promotion"
            ],
            "App / Usability": [
                "app", "application", "website", "interface", "ui", "user experience",
                "navigation", "bug", "glitch", "crash", "slow", "loading", "login"
            ],
            "Other": []
        }
    
    def categorize(self, text: str) -> str:
        """Categorize feedback using Gemini API with fallback"""
        if self.fallback_mode:
            return self._fallback_categorize(text)
        
        try:
            return gemini_service.categorize_feedback(text)
        except AnalysisError as e:
            logger.warning(f"Gemini categorization failed: {e}, using fallback")
            if settings.enable_ai_fallback:
                self.fallback_mode = True
                return self._fallback_categorize(text)
            raise
    
    def categorize_batch(self, texts: List[str]) -> List[str]:
        """Categorize multiple feedback texts"""
        if self.fallback_mode:
            return [self._fallback_categorize(text) for text in texts]
        
        try:
            return gemini_service.categorize_feedback_batch(texts)
        except AnalysisError as e:
            logger.warning(f"Gemini batch categorization failed: {e}, using fallback")
            if settings.enable_ai_fallback:
                self.fallback_mode = True
                return [self._fallback_categorize(text) for text in texts]
            raise
    
    def _fallback_categorize(self, text: str) -> str:
        """Fallback keyword-based categorization"""
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in self.categories.items():
            if category == "Other":
                continue
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return "Other"


complaint_categorizer = ComplaintCategorizer()
