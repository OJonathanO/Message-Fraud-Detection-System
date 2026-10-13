"""Tests for health and model info endpoints."""


def test_health_check(client):
    """Test health check endpoint returns 200."""
    response = client.get('/api/health')
    assert response.status_code == 200

    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'model_loaded' in data
    assert 'model_version' in data


def test_model_info(client):
    """Test model info endpoint returns model metadata."""
    response = client.get('/api/model/info')
    assert response.status_code == 200

    data = response.get_json()
    assert 'model_version' in data
    assert 'classes' in data
    assert isinstance(data['classes'], list)
