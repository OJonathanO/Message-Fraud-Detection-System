"""Tests for analytics endpoints."""
import json


def test_analytics_summary_empty(client):
    """Test analytics summary with no data."""
    response = client.get('/api/analytics/summary')
    assert response.status_code == 200

    data = response.get_json()
    assert data['total_messages'] == 0
    assert data['suspicious_count'] == 0
    assert data['legitimate_count'] == 0


def test_analytics_summary_with_data(client, sample_message):
    """Test analytics summary with prediction data."""
    # Make predictions
    client.post('/api/predict',
                data=json.dumps({'message': sample_message}),
                content_type='application/json')

    response = client.get('/api/analytics/summary')
    assert response.status_code == 200

    data = response.get_json()
    assert data['total_messages'] == 1
    assert data['suspicious_count'] + data['legitimate_count'] == 1


def test_analytics_categories(client, sample_message):
    """Test category distribution endpoint."""
    client.post('/api/predict',
                data=json.dumps({'message': sample_message}),
                content_type='application/json')

    response = client.get('/api/analytics/categories')
    assert response.status_code == 200

    data = response.get_json()
    assert 'categories' in data
    assert isinstance(data['categories'], dict)


def test_analytics_trends(client, sample_message):
    """Test trends endpoint."""
    client.post('/api/predict',
                data=json.dumps({'message': sample_message}),
                content_type='application/json')

    response = client.get('/api/analytics/trends')
    assert response.status_code == 200

    data = response.get_json()
    assert 'trends' in data
    assert isinstance(data['trends'], list)
