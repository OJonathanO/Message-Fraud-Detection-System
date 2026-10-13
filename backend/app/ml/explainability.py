"""Model explainability module.

Extracts the most influential terms for a prediction using
Logistic Regression coefficients and TF-IDF feature names.

Important: Influential words are indicators learned from the training
dataset, NOT proof that a message is fraudulent. A message containing
the word "bank" is not automatically a scam.
"""
import logging
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger(__name__)


class ExplainabilityEngine:
    """Extracts human-readable explanations from the trained pipeline."""

    def __init__(self, pipeline):
        """Initialize with a trained scikit-learn pipeline.

        Args:
            pipeline: Trained Pipeline with 'tfidf' and 'classifier' steps.
        """
        self.pipeline = pipeline
        self.tfidf = pipeline.named_steps.get('tfidf')
        self.classifier = pipeline.named_steps.get('classifier')

        if self.tfidf is None or self.classifier is None:
            raise ValueError(
                "Pipeline must have 'tfidf' and 'classifier' steps"
            )

        self.feature_names = self.tfidf.get_feature_names_out()
        self.coefficients = self.classifier.coef_[0]

    def get_top_features(self, message: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """Get the most influential features for a message.

        Args:
            message: The input message.
            top_n: Number of top features to return.

        Returns:
            List of dicts with 'term', 'weight', and 'direction' keys.
            Direction is 'spam' if the feature pushes toward spam,
            'ham' if it pushes toward legitimate.
        """
        # Transform message to TF-IDF vector
        tfidf_vector = self.tfidf.transform([message])

        # Get non-zero feature indices
        feature_indices = tfidf_vector.nonzero()[1]

        if len(feature_indices) == 0:
            return []

        # Calculate contribution of each feature
        contributions = []
        for idx in feature_indices:
            term = self.feature_names[idx]
            tfidf_value = tfidf_vector[0, idx]
            coef = self.coefficients[idx]
            contribution = tfidf_value * coef

            direction = 'spam' if contribution > 0 else 'ham'

            contributions.append({
                'term': term,
                'weight': round(float(contribution), 4),
                'direction': direction,
            })

        # Sort by absolute contribution (most influential first)
        contributions.sort(key=lambda x: abs(x['weight']), reverse=True)

        return contributions[:top_n]

    def get_indicators(self, message: str, predicted_class: str) -> List[str]:
        """Get human-readable indicators for the predicted class.

        Args:
            message: The input message.
            predicted_class: The predicted class label.

        Returns:
            List of indicator strings describing why the message
            was classified as the predicted class.
        """
        top_features = self.get_top_features(message, top_n=10)
        indicators = []

        # Filter features that push toward the predicted class
        class_features = [
            f for f in top_features
            if f['direction'] == predicted_class
        ]

        # Build indicator strings from top features
        for feat in class_features[:5]:
            term = feat['term']
            if term == 'url':
                indicators.append("Contains external links (URLs)")
            elif term == 'email':
                indicators.append("Contains email addresses")
            elif term == 'phone':
                indicators.append("Contains phone numbers")
            elif term == 'money':
                indicators.append("Contains monetary amounts")
            elif term == 'num':
                indicators.append("Contains numeric patterns")
            elif ' ' in term:
                indicators.append(f"Contains phrase: '{term}'")
            else:
                indicators.append(f"Contains term: '{term}'")

        # Add generic indicators based on predicted class
        if predicted_class == 'spam':
            if not indicators:
                indicators.append("Message patterns match known spam characteristics")
        elif predicted_class == 'ham':
            if not indicators:
                indicators.append("Message patterns match known legitimate characteristics")

        return indicators

    def explain(self, message: str, predicted_class: str) -> Dict[str, Any]:
        """Generate a full explanation for a prediction.

        Args:
            message: The input message.
            predicted_class: The predicted class label.

        Returns:
            Dictionary with explanation details.
        """
        top_features = self.get_top_features(message, top_n=10)
        indicators = self.get_indicators(message, predicted_class)

        return {
            'top_features': top_features,
            'indicators': indicators,
            'disclaimer': (
                "These indicators are derived from patterns learned in the "
                "training dataset. They do not prove that a message is "
                "fraudulent or legitimate. Always use judgment when "
                "evaluating suspicious messages."
            ),
        }
