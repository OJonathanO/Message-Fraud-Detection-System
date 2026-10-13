"""Tests for prediction endpoints."""
import json


def test_predict_valid_message(client, sample_message):
    """Test prediction with a valid message."""
    response = client.post('/api/predict',
                           data=json.dumps({'message': sample_message}),
                           content_type='application/json')

    assert response.status_code == 200

    data = response.get_json()
    assert 'predicted_class' in data
    assert 'risk_level' in data
    assert 'confidence' in data
    assert 'model_version' in data
    assert 'indicators' in data
    assert 'recommendation' in data
    assert 'prediction_id' in data
    assert 'timestamp' in data


def test_predict_missing_message(client):
    """Test prediction with missing message field."""
    response = client.post('/api/predict',
                           data=json.dumps({}),
                           content_type='application/json')

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_predict_empty_message(client):
    """Test prediction with empty message."""
    response = client.post('/api/predict',
                           data=json.dumps({'message': ''}),
                           content_type='application/json')

    assert response.status_code == 400


def test_predict_whitespace_message(client):
    """Test prediction with whitespace-only message."""
    response = client.post('/api/predict',
                           data=json.dumps({'message': '   '}),
                           content_type='application/json')

    assert response.status_code == 400


def test_predict_long_message(client):
    """Test prediction with excessively long message."""
    long_message = "a" * 5001
    response = client.post('/api/predict',
                           data=json.dumps({'message': long_message}),
                           content_type='application/json')

    assert response.status_code == 400


def test_predict_no_json(client):
    """Test prediction without JSON body."""
    response = client.post('/api/predict')
    assert response.status_code == 400


def test_predict_batch(client):
    """Test batch prediction."""
    messages = [
        "Congratulations! You've won! Click here!",
        "Hey, are we still meeting tomorrow?",
        "URGENT: Your account has been compromised. Verify now.",
    ]

    response = client.post('/api/predict/batch',
                           data=json.dumps({'messages': messages}),
                           content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert 'predictions' in data
    assert len(data['predictions']) == 3


def test_predict_batch_empty(client):
    """Test batch prediction with empty list."""
    response = client.post('/api/predict/batch',
                           data=json.dumps({'messages': []}),
                           content_type='application/json')

    assert response.status_code == 400


def test_predict_batch_too_large(client):
    """Test batch prediction with too many messages."""
    messages = ["test"] * 101
    response = client.post('/api/predict/batch',
                           data=json.dumps({'messages': messages}),
                           content_type='application/json')

    assert response.status_code == 400
