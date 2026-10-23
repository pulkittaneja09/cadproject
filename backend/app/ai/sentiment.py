from typing import List, Tuple, Optional
import logging
from app.config import settings
from app.ai.gemini_service import gemini_service, AnalysisError

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        self.use_gemini = True
        self.fallback_mode = False
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Analyze sentiment using Gemini API with fallback"""
        if self.fallback_mode:
            return self._fallback_sentiment(text)
        
        try:
            return gemini_service.analyze_sentiment(text)
        except AnalysisError as e:
            logger.warning(f"Gemini sentiment analysis failed: {e}, using fallback")
            if settings.enable_ai_fallback:
                return self._fallback_sentiment(text)
            raise
    
    def analyze_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        """Analyze sentiment for multiple texts"""
        if self.fallback_mode:
            return [self._fallback_sentiment(text) for text in texts]
        
        try:
            return gemini_service.analyze_sentiment_batch(texts)
        except AnalysisError as e:
            logger.warning(f"Gemini batch sentiment analysis failed: {e}, using fallback")
            if settings.enable_ai_fallback:
                return [self._fallback_sentiment(text) for text in texts]
            raise
    
    def _fallback_sentiment(self, text: str) -> Tuple[str, float]:
        text_lower = text.lower()
        
        positive_words = [
            "good", "great", "excellent", "amazing", "wonderful", "fantastic",
            "love", "loved", "awesome", "perfect", "best", "happy", "pleased",
            "satisfied", "recommend", "helpful", "easy", "fast", "quick"
        ]
        
        negative_words = [
            "bad", "terrible", "awful", "horrible", "worst", "hate", "hated",
            "disappointed", "disappointing", "poor", "slow", "difficult", "hard",
            "frustrating", "annoying", "useless", "waste", "broken", "error",
            "fail", "failed", "problem", "issue", "complaint", "never"
        ]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive", 0.6
        elif negative_count > positive_count:
            return "negative", 0.6
        else:
            return "neutral", 0.5


sentiment_analyzer = SentimentAnalyzer()
