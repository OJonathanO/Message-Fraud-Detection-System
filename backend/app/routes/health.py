"""Health check and model info endpoints."""
from flask import Blueprint, jsonify, current_app

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint.

    Returns:
        JSON with status, model info, and timestamp.
    """
    predictor = current_app.predictor

    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'model_version': predictor.model_version if predictor else None,
    }), 200


@health_bp.route('/model/info', methods=['GET'])
def model_info():
    """Get model information and evaluation metrics.

    Returns:
        JSON with model metadata, classes, and evaluation results.
    """
    predictor = current_app.predictor

    if predictor is None:
        return jsonify({
            'error': 'Model not loaded',
            'message': 'The machine learning model could not be loaded. '
                       'Run the training script first: python -m app.ml.train',
        }), 503

    info = predictor.get_model_info()

    return jsonify(info), 200
