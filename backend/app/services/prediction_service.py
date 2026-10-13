"""Prediction service — orchestrates model inference, risk assessment,
indicator generation, and database persistence."""
import json
import logging
from typing import Any, Dict, List

from app.extensions import db
from app.models import Prediction
from app.ml.explainability import ExplainabilityEngine

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for making predictions and managing prediction history."""

    def __init__(self, predictor):
        """Initialize with a model predictor.

        Args:
            predictor: ModelPredictor instance.
        """
        self.predictor = predictor
        self.explainer = ExplainabilityEngine(predictor.pipeline)

    def predict_single(self, message: str) -> Dict[str, Any]:
        """Predict a single message and build the full response.

        Args:
            message: The text message to classify.

        Returns:
            Dictionary with prediction results, indicators, and recommendation.
        """
        # Get model prediction
        result = self.predictor.predict(message)

        # Calculate risk level
        risk_level = self._calculate_risk_level(
            result['predicted_class'],
            result['confidence']
        )

        # Generate explanation
        explanation = self.explainer.explain(message, result['predicted_class'])

        # Generate recommendation
        recommendation = self._generate_recommendation(
            result['predicted_class'],
            risk_level
        )

        return {
            'predicted_class': result['predicted_class'],
            'risk_level': risk_level,
            'confidence': result['confidence'],
            'probabilities': result['probabilities'],
            'model_version': result['model_version'],
            'indicators': explanation['indicators'],
            'recommendation': recommendation,
            'explanation_disclaimer': explanation['disclaimer'],
        }

    def predict_batch(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Predict multiple messages.

        Args:
            messages: List of text messages.

        Returns:
            List of prediction result dictionaries.
        """
        results = self.predictor.predict_batch(messages)
        output = []

        for message, result in zip(messages, results):
            risk_level = self._calculate_risk_level(
                result['predicted_class'],
                result['confidence']
            )

            explanation = self.explainer.explain(message, result['predicted_class'])
            recommendation = self._generate_recommendation(
                result['predicted_class'],
                risk_level
            )

            output.append({
                'message': message,
                'predicted_class': result['predicted_class'],
                'risk_level': risk_level,
                'confidence': result['confidence'],
                'probabilities': result['probabilities'],
                'model_version': result['model_version'],
                'indicators': explanation['indicators'],
                'recommendation': recommendation,
            })

        return output

    def store_prediction(self, message: str, result: Dict[str, Any]) -> Prediction:
        """Store a prediction in the database.

        Args:
            message: The original message text.
            result: The prediction result dictionary.

        Returns:
            The created Prediction model instance.
        """
        prediction = Prediction(
            message=message,
            predicted_class=result['predicted_class'],
            risk_level=result['risk_level'],
            confidence=result['confidence'],
            model_version=result['model_version'],
            indicators=json.dumps(result.get('indicators', [])),
            recommendation=result.get('recommendation', ''),
        )

        db.session.add(prediction)
        db.session.commit()

        return prediction

    def _calculate_risk_level(self, predicted_class: str, confidence: float) -> str:
        """Calculate risk level based on prediction and confidence.

        Args:
            predicted_class: The predicted class label.
            confidence: The model confidence score.

        Returns:
            Risk level string: 'low', 'medium', 'high', or 'critical'.
        """
        if predicted_class == 'spam':
            if confidence >= 0.9:
                return 'critical'
            elif confidence >= 0.7:
                return 'high'
            else:
                return 'medium'
        else:  # ham
            if confidence >= 0.8:
                return 'low'
            else:
                return 'medium'

    def _generate_recommendation(self, predicted_class: str, risk_level: str) -> str:
        """Generate a user recommendation based on the prediction.

        Args:
            predicted_class: The predicted class label.
            risk_level: The calculated risk level.

        Returns:
            Recommendation string.
        """
        if predicted_class == 'spam':
            if risk_level == 'critical':
                return (
                    "This message shows strong spam indicators. "
                    "Do not click any links, reply, or provide personal information. "
                    "Delete the message and report it as spam."
                )
            elif risk_level == 'high':
                return (
                    "This message shows suspicious patterns consistent with spam. "
                    "Avoid clicking links or responding. "
                    "Verify through official channels if the message claims to be from a known service."
                )
            else:
                return (
                    "This message has some spam-like characteristics but with lower confidence. "
                    "Exercise caution with links and requests for information."
                )
        else:  # ham
            if risk_level == 'low':
                return (
                    "This message appears to be legitimate based on its content patterns. "
                    "No specific action needed, but always use good judgment."
                )
            else:
                return (
                    "This message was classified as legitimate but with moderate confidence. "
                    "If the message seems unexpected, verify through official channels."
                )
