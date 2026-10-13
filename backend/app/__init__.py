"""Application factory for the Message Fraud Detection System."""
import logging
import os
from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, limiter
from .ml.predictor import ModelPredictor


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.setLevel(logging.INFO)

    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)

    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', '*'),
            "methods": ["GET", "POST", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize database tables
    with app.app_context():
        db.create_all()

    # Load ML model once at startup
    model_path = app.config.get('MODEL_PATH', 'model_artifacts/fraud_detection_model.joblib')
    try:
        app.predictor = ModelPredictor(model_path)
        app.logger.info(f"Model loaded successfully from {model_path}")
    except Exception as e:
        app.logger.error(f"Failed to load model from {model_path}: {e}")
        app.predictor = None

    # Register blueprints
    from .routes.health import health_bp
    from .routes.predict import predict_bp
    from .routes.history import history_bp
    from .routes.analytics import analytics_bp

    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(history_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')

    # Register error handlers
    from .utils.errors import register_error_handlers
    register_error_handlers(app)

    return app
