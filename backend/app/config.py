"""Application configuration loaded from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///fraud_detection.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MODEL_PATH = os.environ.get('MODEL_PATH', 'model_artifacts/fraud_detection_model.joblib')
    MODEL_VERSION = os.environ.get('MODEL_VERSION', '1.0.0')

    MAX_MESSAGE_LENGTH = int(os.environ.get('MAX_MESSAGE_LENGTH', 5000))
    MAX_BATCH_SIZE = int(os.environ.get('MAX_BATCH_SIZE', 100))

    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '100 per minute')


class TestConfig(Config):
    """Configuration for testing."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_fraud_detection.db'
    MODEL_PATH = 'model_artifacts/test_model.joblib'
    RATE_LIMIT = '1000 per minute'
