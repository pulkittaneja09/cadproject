"""
Unit tests for sentiment analysis
"""

import pytest
from app.ai.sentiment import sentiment_analyzer


def test_fallback_sentiment_positive():
    """Test fallback sentiment analysis for positive text"""
    sentiment, confidence = sentiment_analyzer._fallback_sentiment(
        "This product is great and I love it"
    )
    assert sentiment == "positive"
    assert confidence > 0


def test_fallback_sentiment_negative():
    """Test fallback sentiment analysis for negative text"""
    sentiment, confidence = sentiment_analyzer._fallback_sentiment(
        "This is terrible and I hate it"
    )
    assert sentiment == "negative"
    assert confidence > 0


def test_fallback_sentiment_neutral():
    """Test fallback sentiment analysis for neutral text"""
    sentiment, confidence = sentiment_analyzer._fallback_sentiment(
        "This is a product"
    )
    assert sentiment == "neutral"
    assert confidence > 0


def test_batch_fallback():
    """Test batch fallback sentiment analysis"""
    texts = [
        "Great product",
        "Terrible service",
        "It's okay"
    ]
    results = sentiment_analyzer.analyze_batch(texts)
    assert len(results) == 3
    assert all(len(result) == 2 for result in results)
