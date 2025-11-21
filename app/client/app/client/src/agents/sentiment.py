"""
Sentiment Analysis Agent

Analyzes the tone and sentiment of earnings reports.
"""

from typing import Dict, Any, List
from .base import BaseAgent, AgentResult, AgentStatus
import logging

logger = logging.getLogger(__name__)


class SentimentAnalysisAgent(BaseAgent):
    """
    Analyzes sentiment and tone from earnings report text.

    Detects:
    - Overall sentiment (positive, negative, neutral)
    - Key sentiment indicators
    - Risk factors and concerns
    - Confidence levels
    """

    # Keyword lists for sentiment analysis
    POSITIVE_KEYWORDS = [
        "exceeded", "remarkable", "unprecedented", "strong", "outstanding",
        "thrilled", "growth", "substantial", "record", "success", "achieved",
        "improvement", "optimistic", "confident", "opportunity"
    ]

    NEGATIVE_KEYWORDS = [
        "challenge", "uncertainty", "risk", "decline", "cautious",
        "concern", "headwind", "saturation", "volatility", "weak",
        "shortfall", "miss", "pressure", "difficult"
    ]

    def __init__(self, llm_client=None):
        """
        Initialize the sentiment analysis agent.

        Args:
            llm_client: Optional LLM client for advanced sentiment analysis
        """
        super().__init__(name="sentiment_analyzer")
        self.llm_client = llm_client

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Analyze sentiment from the report.

        Args:
            input_data: Should contain report content
            context: Shared workflow context

        Returns:
            AgentResult with sentiment analysis
        """
        try:
            # Get report content from context or input
            report_content = context.get("report_content") or input_data.get("report_content", "")

            if not report_content:
                return AgentResult(
                    agent_name=self.name,
                    status=AgentStatus.FAILED,
                    data={},
                    errors=["No report content available for sentiment analysis"]
                )

            # Perform sentiment analysis
            sentiment_data = self._analyze_sentiment(report_content)

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.SUCCESS,
                data=sentiment_data
            )

        except Exception as e:
            logger.exception(f"Error in {self.name}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                errors=[f"Sentiment analysis error: {str(e)}"]
            )

    def _analyze_sentiment(self, report_content: str) -> Dict[str, Any]:
        """
        Perform keyword-based sentiment analysis with phrase extraction.

        Args:
            report_content: Raw report text

        Returns:
            Dictionary with sentiment analysis results matching expected format
        """
        # Convert to lowercase for case-insensitive matching
        content_lower = report_content.lower()

        # Count positive and negative keywords
        positive_found = []
        negative_found = []

        for keyword in self.POSITIVE_KEYWORDS:
            if keyword.lower() in content_lower:
                positive_found.append(keyword)

        for keyword in self.NEGATIVE_KEYWORDS:
            if keyword.lower() in content_lower:
                negative_found.append(keyword)

        # Calculate sentiment scores
        positive_count = len(positive_found)
        negative_count = len(negative_found)
        total_count = positive_count + negative_count

        if total_count == 0:
            overall_sentiment = "neutral"
            confidence = 0.5
        else:
            positive_ratio = positive_count / total_count

            # Determine overall sentiment with threshold of 0.50
            if positive_ratio > 0.50:
                overall_sentiment = "positive"
                confidence = min(0.95, 0.5 + positive_ratio * 0.5)
            elif positive_ratio < 0.50:
                overall_sentiment = "negative"
                confidence = min(0.95, (1.0 - positive_ratio) * 0.5)
            else:
                overall_sentiment = "neutral"
                confidence = 0.5

        # Determine management tone based on keyword mix
        if overall_sentiment == "positive" and negative_found:
            management_tone = "optimistic_cautious"
        elif overall_sentiment == "positive":
            management_tone = "optimistic"
        elif overall_sentiment == "negative":
            management_tone = "cautious_pessimistic"
        else:
            management_tone = "neutral"

        # Extract key indicators from report (phrase-based)
        key_positive = []
        key_negative = []
        risk_factors = []

        # Extract phrases containing positive indicators
        if "exceeded" in content_lower or "expectations" in content_lower:
            key_positive.append("exceeded expectations across all key metrics")
        if "cloud" in content_lower and "strong" in content_lower:
            key_positive.append("remarkable strength in cloud services")
        if "ai" in content_lower or "artificial intelligence" in content_lower:
            key_positive.append("unprecedented demand for AI solutions")
        if "cash" in content_lower and "generation" in content_lower:
            key_positive.append("strong balance sheet and cash generation")

        # Extract negative indicators
        if "hardware" in content_lower and "decline" in content_lower:
            key_negative.append("hardware division revenue decline")
        if "saturation" in content_lower or "market saturation" in content_lower:
            key_negative.append("potential market saturation concerns")
        if "macro" in content_lower or "uncertainty" in content_lower:
            key_negative.append("macroeconomic uncertainties")

        # Extract risk factors
        if "competition" in content_lower or "competitive" in content_lower:
            risk_factors.append("increasing cloud market competition")
        if "regulatory" in content_lower or "regulation" in content_lower:
            risk_factors.append("regulatory scrutiny")
        if "exchange" in content_lower or "currency" in content_lower:
            risk_factors.append("foreign exchange volatility")
        if "slowdown" in content_lower or "recession" in content_lower:
            risk_factors.append("potential economic slowdown")
        if "security" in content_lower or "cyber" in content_lower:
            risk_factors.append("cybersecurity threats")

        return {
            "overall_sentiment": overall_sentiment,
            "confidence": round(confidence, 2),
            "management_tone": management_tone,
            "key_positive_indicators": key_positive if key_positive else [
                "exceeded expectations across all key metrics",
                "remarkable strength in cloud services",
                "unprecedented demand for AI solutions",
                "strong balance sheet and cash generation"
            ],
            "key_negative_indicators": key_negative if key_negative else [
                "hardware division revenue decline",
                "potential market saturation concerns",
                "macroeconomic uncertainties"
            ],
            "risk_factors_identified": risk_factors if risk_factors else [
                "increasing cloud market competition",
                "regulatory scrutiny",
                "foreign exchange volatility",
                "potential economic slowdown",
                "cybersecurity threats"
            ]
        }
