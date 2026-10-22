from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class PriorityDetector:
    def __init__(self):
        self.high_priority_keywords = [
            "urgent", "emergency", "critical", "serious", "severe",
            "dangerous", "safety", "hazard", "illegal", "fraud",
            "scam", "lawsuit", "legal action", "report", "complaint"
        ]
        
        self.medium_priority_keywords = [
            "disappointed", "frustrated", "annoyed", "upset", "unhappy",
            "dissatisfied", "problem", "issue", "concern", "trouble",
            "difficult", "complicated", "confusing", "broken", "failed"
        ]
    
    def detect_priority(
        self, 
        sentiment: str, 
        confidence: float, 
        text: str,
        category: str
    ) -> tuple[str, str]:
        text_lower = text.lower()
        
        # High priority conditions
        if sentiment == "negative" and confidence > 0.7:
            for keyword in self.high_priority_keywords:
                if keyword in text_lower:
                    return "high", f"Negative sentiment with high confidence and contains keyword: '{keyword}'"
        
        if category in ["Product Quality", "Payment"]:
            if sentiment == "negative" and confidence > 0.8:
                return "high", f"Negative sentiment in critical category: {category}"
        
        # Medium priority conditions
        if sentiment == "negative":
            for keyword in self.medium_priority_keywords:
                if keyword in text_lower:
                    return "medium", f"Negative sentiment with keyword: '{keyword}'"
        
        if sentiment == "negative" and confidence > 0.6:
            return "medium", f"Negative sentiment with confidence: {confidence:.2f}"
        
        # Low priority
        if sentiment == "neutral":
            return "low", "Neutral sentiment"
        
        return "low", "Positive or low-risk feedback"
    
    def detect_batch(
        self, 
        sentiments: List[str], 
        confidences: List[float], 
        texts: List[str],
        categories: List[str]
    ) -> List[tuple[str, str]]:
        results = []
        for sentiment, confidence, text, category in zip(sentiments, confidences, texts, categories):
            results.append(self.detect_priority(sentiment, confidence, text, category))
        return results


priority_detector = PriorityDetector()
