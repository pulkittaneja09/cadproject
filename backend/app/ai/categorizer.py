from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ComplaintCategorizer:
    def __init__(self):
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
    
    def categorize_batch(self, texts: List[str]) -> List[str]:
        return [self.categorize(text) for text in texts]


complaint_categorizer = ComplaintCategorizer()
