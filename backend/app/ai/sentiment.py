from typing import List, Tuple, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.fallback_mode = False
    
    def load_model(self):
        if self.model_loaded:
            return
        
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch
            
            logger.info(f"Loading sentiment model: {settings.sentiment_model}")
            self.tokenizer = AutoTokenizer.from_pretrained(settings.sentiment_model)
            self.model = AutoModelForSequenceClassification.from_pretrained(settings.sentiment_model)
            self.model_loaded = True
            logger.info("Sentiment model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            if settings.enable_ai_fallback:
                logger.warning("Falling back to rule-based sentiment analysis")
                self.fallback_mode = True
            else:
                raise
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        if not self.model_loaded and not self.fallback_mode:
            self.load_model()
        
        if self.fallback_mode:
            return self._fallback_sentiment(text)
        
        try:
            import torch
            
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            predictions = outputs.logits.softmax(dim=-1)
            scores = predictions[0].tolist()
            
            # Model returns [negative, neutral, positive]
            labels = ["negative", "neutral", "positive"]
            max_idx = scores.index(max(scores))
            sentiment = labels[max_idx]
            confidence = scores[max_idx]
            
            return sentiment, confidence
        except Exception as e:
            logger.error(f"Error during sentiment analysis: {e}")
            if settings.enable_ai_fallback:
                return self._fallback_sentiment(text)
            raise
    
    def analyze_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        if not self.model_loaded and not self.fallback_mode:
            self.load_model()
        
        if self.fallback_mode:
            return [self._fallback_sentiment(text) for text in texts]
        
        try:
            import torch
            
            results = []
            batch_size = 16
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                inputs = self.tokenizer(batch, return_tensors="pt", truncation=True, max_length=512, padding=True)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                predictions = outputs.logits.softmax(dim=-1)
                
                for j in range(len(batch)):
                    scores = predictions[j].tolist()
                    labels = ["negative", "neutral", "positive"]
                    max_idx = scores.index(max(scores))
                    sentiment = labels[max_idx]
                    confidence = scores[max_idx]
                    results.append((sentiment, confidence))
            
            return results
        except Exception as e:
            logger.error(f"Error during batch sentiment analysis: {e}")
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
