"""
Unit tests for sentiment analysis
"""

import pytest
from app.ai.sentiment import sentiment_analyzer
from app.ai.gemini_service import gemini_service


def test_sentiment_positive():
    """Test sentiment analysis for positive text (uses fallback by default)"""
    gemini_service._use_fallback = True
    sentiment, confidence = sentiment_analyzer.analyze_sentiment(
        "This product is great and I love it"
    )
    assert sentiment == "positive"
    assert confidence > 0


def test_sentiment_negative():
    """Test sentiment analysis for negative text (uses fallback by default)"""
    gemini_service._use_fallback = True
    sentiment, confidence = sentiment_analyzer.analyze_sentiment(
        "This is terrible and I hate it"
    )
    assert sentiment == "negative"
    assert confidence > 0


def test_sentiment_neutral():
    """Test sentiment analysis for neutral text (uses fallback by default)"""
    gemini_service._use_fallback = True
    sentiment, confidence = sentiment_analyzer.analyze_sentiment(
        "This is a product"
    )
    assert sentiment == "neutral"
    assert confidence > 0


def test_batch_sentiment():
    """Test batch sentiment analysis (uses fallback by default)"""
    gemini_service._use_fallback = True
    texts = [
        "Great product",
        "Terrible service",
        "It's okay"
    ]
    results = sentiment_analyzer.analyze_batch(texts)
    assert len(results) == 3
    assert all(len(result) == 2 for result in results)
