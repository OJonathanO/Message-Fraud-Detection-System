"""Analytics endpoints."""
from flask import Blueprint, jsonify, current_app
from app.extensions import db
from app.models import Prediction
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    """Get summary statistics.

    Returns:
        JSON with total, suspicious, and legitimate counts.
    """
    total = Prediction.query.count()

    suspicious = Prediction.query.filter(
        Prediction.predicted_class == 'spam'
    ).count()

    legitimate = Prediction.query.filter(
        Prediction.predicted_class == 'ham'
    ).count()

    # Risk level distribution
    risk_counts = db.session.query(
        Prediction.risk_level, func.count(Prediction.id)
    ).group_by(Prediction.risk_level).all()

    risk_distribution = {level: count for level, count in risk_counts}

    return jsonify({
        'total_messages': total,
        'suspicious_count': suspicious,
        'legitimate_count': legitimate,
        'risk_distribution': risk_distribution,
    }), 200


@analytics_bp.route('/analytics/categories', methods=['GET'])
def analytics_categories():
    """Get category distribution.

    Returns:
        JSON with counts per category.
    """
    category_counts = db.session.query(
        Prediction.predicted_class, func.count(Prediction.id)
    ).group_by(Prediction.predicted_class).all()

    categories = {cat: count for cat, count in category_counts}

    return jsonify({
        'categories': categories,
    }), 200


@analytics_bp.route('/analytics/trends', methods=['GET'])
def analytics_trends():
    """Get prediction trends over time.

    Returns:
        JSON with daily prediction counts.
    """
    # Get daily counts for the last 30 days
    trends = db.session.query(
        func.date(Prediction.created_at).label('date'),
        Prediction.predicted_class,
        func.count(Prediction.id).label('count')
    ).group_by(
        func.date(Prediction.created_at),
        Prediction.predicted_class
    ).order_by('date').all()

    # Build trend data
    trend_data = {}
    for date, pred_class, count in trends:
        date_str = str(date)
        if date_str not in trend_data:
            trend_data[date_str] = {'date': date_str, 'spam': 0, 'ham': 0}
        trend_data[date_str][pred_class] = count

    trends_list = sorted(trend_data.values(), key=lambda x: x['date'])

    return jsonify({
        'trends': trends_list,
    }), 200
