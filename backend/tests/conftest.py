"""Test fixtures and configuration."""
import os
import sys
import pytest

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_message():
    """Return a sample spam message."""
    return "Congratulations! You've won a $1000 gift card. Click here to claim now!"


@pytest.fixture
def sample_legitimate_message():
    """Return a sample legitimate message."""
    return "Hey, are we still meeting for lunch tomorrow at 12?"
