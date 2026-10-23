"""
Unit tests for Gemini AI service
"""

import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from app.ai.gemini_service import gemini_service, AnalysisError


class TestGeminiService:
    """Test Gemini service with mocked API calls"""
    
    def test_fallback_sentiment_positive(self):
        """Test fallback sentiment analysis for positive text"""
        gemini_service._use_fallback = True
        sentiment, confidence = gemini_service.analyze_sentiment(
            "This product is great and I love it"
        )
        assert sentiment == "positive"
        assert confidence > 0
    
    def test_fallback_sentiment_negative(self):
        """Test fallback sentiment analysis for negative text"""
        gemini_service._use_fallback = True
        sentiment, confidence = gemini_service.analyze_sentiment(
            "This is terrible and I hate it"
        )
        assert sentiment == "negative"
        assert confidence > 0
    
    def test_fallback_sentiment_neutral(self):
        """Test fallback sentiment analysis for neutral text"""
        gemini_service._use_fallback = True
        sentiment, confidence = gemini_service.analyze_sentiment(
            "This is a product"
        )
        assert sentiment == "neutral"
        assert confidence > 0
    
    def test_fallback_categorize_delivery(self):
        """Test fallback categorization of delivery-related feedback"""
        gemini_service._use_fallback = True
        category = gemini_service.categorize_feedback(
            "The delivery was late and the package was damaged"
        )
        assert category == "Delivery"
    
    def test_fallback_categorize_customer_support(self):
        """Test fallback categorization of customer support feedback"""
        gemini_service._use_fallback = True
        category = gemini_service.categorize_feedback(
            "Customer support was rude and unhelpful"
        )
        assert category == "Customer Support"
    
    def test_fallback_priority_high(self):
        """Test fallback priority detection for high priority"""
        gemini_service._use_fallback = True
        priority, explanation = gemini_service.detect_priority(
            "negative", 0.8, "This is urgent and critical", "Other"
        )
        assert priority == "high"
        assert "urgent" in explanation.lower()
    
    def test_fallback_priority_low(self):
        """Test fallback priority detection for low priority"""
        gemini_service._use_fallback = True
        priority, explanation = gemini_service.detect_priority(
            "neutral", 0.5, "This is okay", "Other"
        )
        assert priority == "low"
    
    @patch('app.ai.gemini_service.settings')
    def test_missing_api_key_uses_fallback(self, mock_settings):
        """Test that missing API key triggers fallback mode"""
        mock_settings.gemini_api_key = ""
        gemini_service._initialized = False
        gemini_service._use_fallback = False
        
        # Re-initialize
        gemini_service._initialize()
        
        assert gemini_service._use_fallback is True
    
    @patch('app.ai.gemini_service.settings')
    def test_import_error_uses_fallback(self, mock_settings):
        """Test that import error triggers fallback mode"""
        mock_settings.gemini_api_key = "test_key"
        gemini_service._initialized = False
        gemini_service._use_fallback = False
        
        with patch.dict('sys.modules', {'google.generativeai': None}):
            gemini_service._initialize()
        
        assert gemini_service._use_fallback is True
    
    def test_batch_fallback_sentiment(self):
        """Test batch fallback sentiment analysis"""
        gemini_service._use_fallback = True
        texts = [
            "Great product",
            "Terrible service",
            "It's okay"
        ]
        results = gemini_service.analyze_sentiment_batch(texts)
        assert len(results) == 3
        assert all(len(result) == 2 for result in results)
    
    def test_batch_fallback_categorize(self):
        """Test batch fallback categorization"""
        gemini_service._use_fallback = True
        texts = [
            "Delivery was slow",
            "Support was bad",
            "Payment failed"
        ]
        categories = gemini_service.categorize_feedback_batch(texts)
        assert len(categories) == 3
        assert categories[0] == "Delivery"
        assert categories[1] == "Customer Support"
        assert categories[2] == "Payment"
