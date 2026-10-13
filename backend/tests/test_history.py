"""Tests for prediction history endpoints."""
import json


def test_get_predictions_empty(client):
    """Test getting predictions when history is empty."""
    response = client.get('/api/predictions')
    assert response.status_code == 200

    data = response.get_json()
    assert data['predictions'] == []
    assert data['pagination']['total'] == 0


def test_get_predictions_with_data(client, sample_message):
    """Test getting predictions after making a prediction."""
    # First make a prediction
    client.post('/api/predict',
                data=json.dumps({'message': sample_message}),
                content_type='application/json')

    # Then get history
    response = client.get('/api/predictions')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data['predictions']) == 1
    assert data['pagination']['total'] == 1


def test_get_prediction_by_id(client, sample_message):
    """Test getting a single prediction by ID."""
    # Make a prediction
    response = client.post('/api/predict',
                           data=json.dumps({'message': sample_message}),
                           content_type='application/json')
    pred_id = response.get_json()['prediction_id']

    # Get by ID
    response = client.get(f'/api/predictions/{pred_id}')
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == pred_id
    assert data['message'] == sample_message


def test_get_prediction_not_found(client):
    """Test getting a non-existent prediction."""
    response = client.get('/api/predictions/99999')
    assert response.status_code == 404


def test_delete_prediction(client, sample_message):
    """Test deleting a prediction."""
    # Make a prediction
    response = client.post('/api/predict',
                           data=json.dumps({'message': sample_message}),
                           content_type='application/json')
    pred_id = response.get_json()['prediction_id']

    # Delete it
    response = client.delete(f'/api/predictions/{pred_id}')
    assert response.status_code == 200

    # Verify it's gone
    response = client.get(f'/api/predictions/{pred_id}')
    assert response.status_code == 404


def test_delete_prediction_not_found(client):
    """Test deleting a non-existent prediction."""
    response = client.delete('/api/predictions/99999')
    assert response.status_code == 404


def test_clear_history(client, sample_message):
    """Test clearing all history."""
    # Make predictions
    client.post('/api/predict',
                data=json.dumps({'message': sample_message}),
                content_type='application/json')
    client.post('/api/predict',
                data=json.dumps({'message': 'Another message'}),
                content_type='application/json')

    # Clear history
    response = client.delete('/api/predictions')
    assert response.status_code == 200

    data = response.get_json()
    assert data['deleted_count'] == 2

    # Verify empty
    response = client.get('/api/predictions')
    assert response.get_json()['pagination']['total'] == 0


def test_search_predictions(client, sample_message):
    """Test searching predictions."""
    # Make predictions
    client.post('/api/predict',
                data=json.dumps({'message': 'Congratulations you won'}),
                content_type='application/json')
    client.post('/api/predict',
                data=json.dumps({'message': 'Hey, lunch tomorrow?'}),
                content_type='application/json')

    # Search
    response = client.get('/api/predictions?search=Congratulations')
    assert response.status_code == 200

    data = response.get_json()
    assert data['pagination']['total'] == 1
    assert 'Congratulations' in data['predictions'][0]['message']


def test_filter_by_category(client, sample_message):
    """Test filtering predictions by category."""
    # Make a prediction (will be classified as spam or ham)
    client.post('/api/predict',
                data=json.dumps({'message': sample_message}),
                content_type='application/json')

    # Get the prediction to see its class
    response = client.get('/api/predictions')
    pred = response.get_json()['predictions'][0]
    category = pred['predicted_class']

    # Filter by that category
    response = client.get(f'/api/predictions?category={category}')
    assert response.status_code == 200
    assert response.get_json()['pagination']['total'] >= 1


def test_pagination(client):
    """Test pagination parameters."""
    # Make multiple predictions
    for i in range(5):
        client.post('/api/predict',
                    data=json.dumps({'message': f'Test message {i}'}),
                    content_type='application/json')

    # Get page 1 with 2 per page
    response = client.get('/api/predictions?page=1&per_page=2')
    assert response.status_code == 200

    data = response.get_json()
    assert len(data['predictions']) == 2
    assert data['pagination']['total'] == 5
    assert data['pagination']['pages'] == 3
