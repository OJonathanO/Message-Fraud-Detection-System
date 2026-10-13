"""Model predictor — loads the trained pipeline and makes predictions.

The model is loaded ONCE at application startup and reused for all
predictions. This avoids the overhead of reloading the model for
every request.
"""
import json
import logging
import os
from typing import Any, Dict, List, Optional

import joblib
import numpy as np

logger = logging.getLogger(__name__)


class ModelPredictor:
    """Singleton predictor that loads and caches the trained pipeline."""

    def __init__(self, model_path: str):
        """Initialize the predictor by loading the trained model.

        Args:
            model_path: Path to the saved model artifact (.joblib file).

        Raises:
            FileNotFoundError: If the model file does not exist.
            ValueError: If the model artifact is invalid.
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}. "
                "Run the training script first: python -m app.ml.train"
            )

        self.pipeline = joblib.load(model_path)
        self.model_path = model_path
        self.model_version = self._load_model_version(model_path)
        self.classes = list(self.pipeline.classes_)

        logger.info(f"Model loaded: version={self.model_version}, classes={self.classes}")

    def _load_model_version(self, model_path: str) -> str:
        """Load model version from training metadata.

        Args:
            model_path: Path to the model file.

        Returns:
            Model version string, or 'unknown' if metadata not found.
        """
        model_dir = os.path.dirname(model_path)
        metadata_path = os.path.join(model_dir, 'training_metadata.json')

        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                return metadata.get('model_version', 'unknown')
            except (json.JSONDecodeError, IOError):
                pass

        return 'unknown'

    def predict(self, message: str) -> Dict[str, Any]:
        """Predict the class of a single message.

        Args:
            message: The text message to classify.

        Returns:
            Dictionary with prediction results including:
                - predicted_class: The predicted label
                - confidence: The probability of the predicted class
                - probabilities: Dict mapping each class to its probability
                - model_version: The model version used

        Raises:
            ValueError: If the message is empty or invalid.
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        # Get prediction and probabilities
        predicted_class = self.pipeline.predict([message])[0]
        probabilities = self.pipeline.predict_proba([message])[0]

        # Build probability dict
        prob_dict = {
            cls: round(float(prob), 4)
            for cls, prob in zip(self.classes, probabilities)
        }

        # Confidence is the probability of the predicted class
        confidence = round(float(probabilities[self.classes.index(predicted_class)]), 4)

        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'probabilities': prob_dict,
            'model_version': self.model_version,
        }

    def predict_batch(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Predict classes for multiple messages.

        Args:
            messages: List of text messages to classify.

        Returns:
            List of prediction result dictionaries.
        """
        if not messages:
            return []

        predictions = self.pipeline.predict(messages)
        probabilities = self.pipeline.predict_proba(messages)

        results = []
        for i, (pred_class, probs) in enumerate(zip(predictions, probabilities)):
            prob_dict = {
                cls: round(float(prob), 4)
                for cls, prob in zip(self.classes, probs)
            }
            confidence = round(float(probs[self.classes.index(pred_class)]), 4)

            results.append({
                'predicted_class': pred_class,
                'confidence': confidence,
                'probabilities': prob_dict,
                'model_version': self.model_version,
            })

        return results

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model.

        Returns:
            Dictionary with model metadata.
        """
        model_dir = os.path.dirname(self.model_path)
        metadata_path = os.path.join(model_dir, 'training_metadata.json')
        eval_path = os.path.join(model_dir, 'evaluation_report.json')

        info = {
            'model_version': self.model_version,
            'classes': self.classes,
            'model_path': self.model_path,
        }

        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    info['training_metadata'] = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        if os.path.exists(eval_path):
            try:
                with open(eval_path, 'r') as f:
                    info['evaluation'] = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        return info
