"""Prediction database model."""
from datetime import datetime
from app.extensions import db


class Prediction(db.Model):
    """Stores prediction history.

    Privacy note: Messages are stored as-is. Users are warned that
    messages may contain personal or financial information. The
    application does not encrypt messages at rest — for production
    use, consider enabling encryption or disabling history.
    """

    __tablename__ = 'predictions'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    predicted_class = db.Column(db.String(50), nullable=False, index=True)
    risk_level = db.Column(db.String(20), nullable=False, index=True)
    confidence = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(50), nullable=False)
    indicators = db.Column(db.Text)  # JSON string
    recommendation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        db.Index('idx_predicted_class', 'predicted_class'),
        db.Index('idx_risk_level', 'risk_level'),
        db.Index('idx_created_at', 'created_at'),
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'message': self.message,
            'predicted_class': self.predicted_class,
            'risk_level': self.risk_level,
            'confidence': self.confidence,
            'model_version': self.model_version,
            'indicators': self.indicators,
            'recommendation': self.recommendation,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
