"""Prediction history endpoints."""
import csv
import io
from flask import Blueprint, request, jsonify, current_app, Response
from app.extensions import db
from app.models import Prediction

history_bp = Blueprint('history', __name__)


@history_bp.route('/predictions', methods=['GET'])
def get_predictions():
    """Get paginated prediction history with search and filters.

    Query parameters:
        page: Page number (default 1)
        per_page: Items per page (default 20, max 100)
        search: Search in message text
        category: Filter by predicted_class
        risk_level: Filter by risk_level
        date_from: Filter by date (ISO format)
        date_to: Filter by date (ISO format)
        sort_by: Sort field (default: created_at)
        sort_order: asc or desc (default: desc)

    Returns:
        JSON with predictions and pagination metadata.
    """
    # Parse query parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 20, type=int), 100)
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    risk_level = request.args.get('risk_level', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')

    # Validate pagination
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 1

    # Build query
    query = Prediction.query

    # Apply search filter
    if search:
        query = query.filter(Prediction.message.ilike(f'%{search}%'))

    # Apply category filter
    if category:
        query = query.filter(Prediction.predicted_class == category)

    # Apply risk level filter
    if risk_level:
        query = query.filter(Prediction.risk_level == risk_level)

    # Apply date filters
    if date_from:
        try:
            from datetime import datetime
            date_from_dt = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
            query = query.filter(Prediction.created_at >= date_from_dt)
        except ValueError:
            pass

    if date_to:
        try:
            from datetime import datetime
            date_to_dt = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
            query = query.filter(Prediction.created_at <= date_to_dt)
        except ValueError:
            pass

    # Apply sorting
    sort_column = getattr(Prediction, sort_by, Prediction.created_at)
    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Execute paginated query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'predictions': [p.to_dict() for p in pagination.items],
        'pagination': {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev,
        },
    }), 200


@history_bp.route('/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    """Get a single prediction by ID.

    Args:
        prediction_id: The prediction ID.

    Returns:
        JSON with prediction details.
    """
    prediction = Prediction.query.get(prediction_id)

    if prediction is None:
        return jsonify({
            'error': 'Not Found',
            'message': f'Prediction with ID {prediction_id} not found.',
        }), 404

    return jsonify(prediction.to_dict()), 200


@history_bp.route('/predictions/<int:prediction_id>', methods=['DELETE'])
def delete_prediction(prediction_id):
    """Delete a prediction by ID.

    Args:
        prediction_id: The prediction ID.

    Returns:
        JSON confirmation message.
    """
    prediction = Prediction.query.get(prediction_id)

    if prediction is None:
        return jsonify({
            'error': 'Not Found',
            'message': f'Prediction with ID {prediction_id} not found.',
        }), 404

    db.session.delete(prediction)
    db.session.commit()

    current_app.logger.info(f"Deleted prediction {prediction_id}")

    return jsonify({
        'message': f'Prediction {prediction_id} deleted successfully.',
    }), 200


@history_bp.route('/predictions', methods=['DELETE'])
def clear_history():
    """Clear all prediction history.

    Returns:
        JSON confirmation message with count of deleted records.
    """
    count = Prediction.query.delete()
    db.session.commit()

    current_app.logger.info(f"Cleared {count} predictions from history")

    return jsonify({
        'message': f'Successfully deleted {count} predictions.',
        'deleted_count': count,
    }), 200


@history_bp.route('/predictions/export', methods=['GET'])
def export_predictions():
    """Export prediction history to CSV.

    Query parameters: same filters as /predictions endpoint.

    Returns:
        CSV file download.
    """
    # Get filtered predictions (same logic as get_predictions)
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    risk_level = request.args.get('risk_level', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    query = Prediction.query

    if search:
        query = query.filter(Prediction.message.ilike(f'%{search}%'))
    if category:
        query = query.filter(Prediction.predicted_class == category)
    if risk_level:
        query = query.filter(Prediction.risk_level == risk_level)

    predictions = query.order_by(Prediction.created_at.desc()).all()

    # Build CSV
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'ID', 'Message', 'Predicted Class', 'Risk Level',
        'Confidence', 'Model Version', 'Indicators',
        'Recommendation', 'Timestamp'
    ])

    # Data rows
    for p in predictions:
        writer.writerow([
            p.id,
            p.message,
            p.predicted_class,
            p.risk_level,
            p.confidence,
            p.model_version,
            p.indicators or '',
            p.recommendation or '',
            p.created_at.isoformat() if p.created_at else '',
        ])

    # Create response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=predictions_export.csv',
        },
    )
