"""
Gemini AI Service for InsightPulse AI

This module provides AI-powered analysis using Google Gemini API:
- Sentiment analysis
- Feedback categorization
- Priority detection
- Insights generation
"""

import json
import logging
from typing import List, Tuple, Dict, Any, Optional
from enum import Enum

from app.config import settings

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    """Custom exception for AI analysis errors"""
    pass


class SentimentLabel(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class PriorityLabel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class GeminiService:
    """Centralized service for Gemini API calls"""
    
    # Predefined categories from existing categorizer
    CATEGORIES = [
        "Delivery",
        "Customer Support",
        "Payment",
        "Product Quality",
        "Pricing",
        "App / Usability",
        "Other"
    ]
    
    def __init__(self):
        self._client = None
        self._model = None
        self._initialized = False
        self._use_fallback = False
        
    def _initialize(self):
        """Lazy initialization of Gemini client"""
        if self._initialized:
            return
            
        try:
            if not settings.gemini_api_key:
                logger.warning("GEMINI_API_KEY not configured, using fallback mode")
                self._use_fallback = True
                self._initialized = True
                return
            
            import google.generativeai as genai
            
            genai.configure(api_key=settings.gemini_api_key)
            self._client = genai
            self._model = genai.GenerativeModel(settings.gemini_model)
            self._initialized = True
            logger.info(f"Gemini service initialized with model: {settings.gemini_model}")
            
        except ImportError:
            logger.error("google-generativeai not installed, using fallback mode")
            self._use_fallback = True
            self._initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Gemini service: {e}")
            self._use_fallback = True
            self._initialized = True
    
    def _call_gemini(self, prompt: str, response_format: Optional[Dict] = None) -> str:
        """Make a synchronous call to Gemini API"""
        if self._use_fallback:
            raise AnalysisError("Gemini API not available, using fallback")
        
        try:
            self._initialize()
            
            # Configure generation parameters
            generation_config = {
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,
            }
            
            if response_format:
                # For structured output, include JSON format instruction
                prompt += f"\n\nRespond in valid JSON format with this schema: {json.dumps(response_format)}"
            
            response = self._model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise AnalysisError(f"Gemini API error: {str(e)}")
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text using Gemini
        
        Returns:
            Tuple of (sentiment_label, confidence_score)
        """
        if self._use_fallback:
            return self._fallback_sentiment(text)
        
        try:
            prompt = f"""
            Analyze the sentiment of the following customer feedback.
            Classify as "positive", "neutral", or "negative".
            Also provide a confidence score between 0.0 and 1.0.
            
            Feedback: "{text}"
            
            Respond in JSON format: {{"sentiment": "positive|neutral|negative", "confidence": 0.0-1.0}}
            """
            
            response = self._call_gemini(prompt)
            
            # Parse JSON response
            try:
                result = json.loads(response)
                sentiment = result.get("sentiment", "neutral").lower()
                confidence = float(result.get("confidence", 0.5))
                
                # Validate sentiment
                if sentiment not in ["positive", "neutral", "negative"]:
                    sentiment = "neutral"
                
                # Clamp confidence
                confidence = max(0.0, min(1.0, confidence))
                
                return sentiment, confidence
                
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse Gemini response as JSON: {response}")
                return self._fallback_sentiment(text)
                
        except AnalysisError:
            return self._fallback_sentiment(text)
    
    def analyze_sentiment_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        """
        Analyze sentiment for multiple texts
        """
        results = []
        for text in texts:
            results.append(self.analyze_sentiment(text))
        return results
    
    def categorize_feedback(self, text: str) -> str:
        """
        Categorize feedback into predefined categories using Gemini
        """
        if self._use_fallback:
            return self._fallback_categorize(text)
        
        try:
            categories_str = ", ".join(self.CATEGORIES)
            
            prompt = f"""
            Categorize the following customer feedback into one of these categories: {categories_str}.
            
            Feedback: "{text}"
            
            Respond with only the category name.
            """
            
            response = self._call_gemini(prompt).strip()
            
            # Validate category
            if response in self.CATEGORIES:
                return response
            else:
                logger.warning(f"Gemini returned invalid category: {response}")
                return self._fallback_categorize(text)
                
        except AnalysisError:
            return self._fallback_categorize(text)
    
    def categorize_feedback_batch(self, texts: List[str]) -> List[str]:
        """
        Categorize multiple feedback texts
        """
        results = []
        for text in texts:
            results.append(self.categorize_feedback(text))
        return results
    
    def detect_priority(
        self,
        sentiment: str,
        confidence: float,
        text: str,
        category: str
    ) -> Tuple[str, str]:
        """
        Detect priority level of feedback using Gemini
        
        Returns:
            Tuple of (priority_level, explanation)
        """
        if self._use_fallback:
            return self._fallback_priority(sentiment, confidence, text, category)
        
        try:
            prompt = f"""
            Determine the priority level of this customer feedback.
            Consider: sentiment, category, and urgency indicators.
            
            Feedback: "{text}"
            Sentiment: {sentiment} (confidence: {confidence})
            Category: {category}
            
            Classify as "high", "medium", or "low" priority.
            Provide a brief explanation (under 100 words).
            
            Respond in JSON format: {{"priority": "high|medium|low", "explanation": "..."}}
            """
            
            response = self._call_gemini(prompt)
            
            try:
                result = json.loads(response)
                priority = result.get("priority", "low").lower()
                explanation = result.get("explanation", "")
                
                # Validate priority
                if priority not in ["high", "medium", "low"]:
                    priority = "low"
                
                return priority, explanation
                
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse Gemini response as JSON: {response}")
                return self._fallback_priority(sentiment, confidence, text, category)
                
        except AnalysisError:
            return self._fallback_priority(sentiment, confidence, text, category)
    
    def detect_priority_batch(
        self,
        sentiments: List[str],
        confidences: List[float],
        texts: List[str],
        categories: List[str]
    ) -> List[Tuple[str, str]]:
        """
        Detect priority for multiple feedback items
        """
        results = []
        for sentiment, confidence, text, category in zip(sentiments, confidences, texts, categories):
            results.append(self.detect_priority(sentiment, confidence, text, category))
        return results
    
    def generate_insights(
        self,
        feedback_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate AI-powered insights from feedback data
        """
        if self._use_fallback:
            return self._fallback_insights(feedback_list)
        
        try:
            # Sample feedback to avoid hitting token limits
            sample_size = min(50, len(feedback_list))
            sampled_feedback = feedback_list[:sample_size]
            
            feedback_text = "\n".join([
                f"- {f.get('review_text', '')} (sentiment: {f.get('sentiment', 'N/A')}, category: {f.get('category', 'N/A')})"
                for f in sampled_feedback
            ])
            
            prompt = f"""
            Analyze the following customer feedback and provide insights.
            
            Feedback samples:
            {feedback_text}
            
            Provide:
            1. A concise executive summary (2-3 sentences)
            2. Top 3 positive themes with examples
            3. Top 3 negative themes with examples
            4. 3 suggested improvements based on common issues
            
            Respond in JSON format with these fields:
            {{
                "executive_summary": "...",
                "positive_themes": [{"theme": "...", "count": N, "examples": ["...", "..."]}],
                "negative_themes": [{"theme": "...", "count": N, "examples": ["...", "..."]}],
                "suggested_improvements": ["...", "...", "..."]
            }}
            """
            
            response = self._call_gemini(prompt)
            
            try:
                result = json.loads(response)
                return {
                    "executive_summary": result.get("executive_summary", ""),
                    "positive_themes": result.get("positive_themes", []),
                    "negative_themes": result.get("negative_themes", []),
                    "suggested_improvements": result.get("suggested_improvements", []),
                    "analysis_method": "gemini"
                }
                
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse Gemini insights as JSON: {response}")
                return self._fallback_insights(feedback_list)
                
        except AnalysisError:
            return self._fallback_insights(feedback_list)
    
    # Fallback methods (preserving existing keyword-based logic)
    def _fallback_sentiment(self, text: str) -> Tuple[str, float]:
        """Fallback keyword-based sentiment analysis"""
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
    
    def _fallback_categorize(self, text: str) -> str:
        """Fallback keyword-based categorization"""
        text_lower = text.lower()
        
        categories = {
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
        
        category_scores = {}
        for category, keywords in categories.items():
            if category == "Other":
                continue
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return "Other"
    
    def _fallback_priority(
        self,
        sentiment: str,
        confidence: float,
        text: str,
        category: str
    ) -> Tuple[str, str]:
        """Fallback keyword-based priority detection"""
        text_lower = text.lower()
        
        high_priority_keywords = [
            "urgent", "emergency", "critical", "serious", "severe",
            "dangerous", "safety", "hazard", "illegal", "fraud",
            "scam", "lawsuit", "legal action", "report", "complaint"
        ]
        
        medium_priority_keywords = [
            "disappointed", "frustrated", "annoyed", "upset", "unhappy",
            "dissatisfied", "problem", "issue", "concern", "trouble",
            "difficult", "complicated", "confusing", "broken", "failed"
        ]
        
        # High priority conditions
        if sentiment == "negative" and confidence > 0.7:
            for keyword in high_priority_keywords:
                if keyword in text_lower:
                    return "high", f"Negative sentiment with high confidence and contains keyword: '{keyword}'"
        
        if category in ["Product Quality", "Payment"]:
            if sentiment == "negative" and confidence > 0.8:
                return "high", f"Negative sentiment in critical category: {category}"
        
        # Medium priority conditions
        if sentiment == "negative":
            for keyword in medium_priority_keywords:
                if keyword in text_lower:
                    return "medium", f"Negative sentiment with keyword: '{keyword}'"
        
        if sentiment == "negative" and confidence > 0.6:
            return "medium", f"Negative sentiment with confidence: {confidence:.2f}"
        
        # Low priority
        if sentiment == "neutral":
            return "low", "Neutral sentiment"
        
        return "low", "Positive or low-risk feedback"
    
    def _fallback_insights(self, feedback_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback extractive insights (use existing logic)"""
        # This will be handled by the existing insights route logic
        return {
            "executive_summary": "Using fallback extractive analysis",
            "positive_themes": [],
            "negative_themes": [],
            "suggested_improvements": [],
            "analysis_method": "extractive"
        }


# Global service instance
gemini_service = GeminiService()
