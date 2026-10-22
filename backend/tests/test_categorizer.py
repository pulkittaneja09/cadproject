"""
Unit tests for complaint categorization
"""

import pytest
from app.ai.categorizer import complaint_categorizer


def test_categorize_delivery():
    """Test categorization of delivery-related feedback"""
    category = complaint_categorizer.categorize(
        "The delivery was late and the package was damaged"
    )
    assert category == "Delivery"


def test_categorize_customer_support():
    """Test categorization of customer support feedback"""
    category = complaint_categorizer.categorize(
        "Customer support was rude and unhelpful"
    )
    assert category == "Customer Support"


def test_categorize_payment():
    """Test categorization of payment-related feedback"""
    category = complaint_categorizer.categorize(
        "Payment failed and I was charged twice"
    )
    assert category == "Payment"


def test_categorize_product_quality():
    """Test categorization of product quality feedback"""
    category = complaint_categorizer.categorize(
        "The product is defective and poor quality"
    )
    assert category == "Product Quality"


def test_categorize_other():
    """Test categorization of uncategorized feedback"""
    category = complaint_categorizer.categorize(
        "This is just a random comment"
    )
    assert category == "Other"


def test_batch_categorize():
    """Test batch categorization"""
    texts = [
        "Delivery was slow",
        "Support was bad",
        "Payment failed"
    ]
    categories = complaint_categorizer.categorize_batch(texts)
    assert len(categories) == 3
    assert categories[0] == "Delivery"
    assert categories[1] == "Customer Support"
    assert categories[2] == "Payment"
