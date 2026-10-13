"""Prediction endpoints."""
import json
from flask import Blueprint, request, jsonify, current_app
from app.services.prediction_service import PredictionService
from app.utils.validators import validate_message, validate_batch_messages

predict_bp = Blueprint('predict', __name__)


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """Classify a single message.

    Request body: {"message": "text to classify"}

    Returns:
        JSON with prediction results.
    """
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Request body must contain a "message" field.',
        }), 400

    message = data['message']

    # Validate message
    is_valid, error_msg = validate_message(message)
    if not is_valid:
        return jsonify({
            'error': 'Validation Error',
            'message': error_msg,
        }), 400

    # Check model availability
    if current_app.predictor is None:
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'Model is not loaded. Run the training script first.',
        }), 503

    try:
        service = PredictionService(current_app.predictor)
        result = service.predict_single(message)

        # Store in history
        prediction_model = service.store_prediction(message, result)
        result['prediction_id'] = prediction_model.id
        result['timestamp'] = prediction_model.created_at.isoformat()

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({
            'error': 'Validation Error',
            'message': str(e),
        }), 400
    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An error occurred during prediction.',
        }), 500


@predict_bp.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Classify multiple messages.

    Request body: {"messages": ["msg1", "msg2", ...]}

    Returns:
        JSON with prediction results for each message.
    """
    data = request.get_json()

    if not data or 'messages' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Request body must contain a "messages" array.',
        }), 400

    messages = data['messages']

    if not isinstance(messages, list):
        return jsonify({
            'error': 'Bad Request',
            'message': '"messages" must be an array.',
        }), 400

    if len(messages) == 0:
        return jsonify({
            'error': 'Bad Request',
            'message': '"messages" array cannot be empty.',
        }), 400

    # Check batch size limit
    max_batch = current_app.config.get('MAX_BATCH_SIZE', 100)
    if len(messages) > max_batch:
        return jsonify({
            'error': 'Bad Request',
            'message': f'Batch size exceeds maximum of {max_batch}.',
        }), 400

    # Validate all messages
    for i, msg in enumerate(messages):
        is_valid, error_msg = validate_message(msg)
        if not is_valid:
            return jsonify({
                'error': 'Validation Error',
                'message': f'Message at index {i}: {error_msg}',
            }), 400

    # Check model availability
    if current_app.predictor is None:
        return jsonify({
            'error': 'Service Unavailable',
            'message': 'Model is not loaded. Run the training script first.',
        }), 503

    try:
        service = PredictionService(current_app.predictor)
        results = service.predict_batch(messages)

        return jsonify({
            'predictions': results,
            'batch_size': len(messages),
        }), 200

    except Exception as e:
        current_app.logger.error(f"Batch prediction error: {e}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An error occurred during batch prediction.',
        }), 500
