# API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

No authentication required for local development. For production, implement API key or JWT-based authentication.

## Endpoints

### Health Check

#### `GET /api/health`

Check if the service is running and the model is loaded.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_version": "1.0.0"
}
```

---

### Model Information

#### `GET /api/model/info`

Get model metadata, classes, and evaluation metrics.

**Response:**
```json
{
  "model_version": "1.0.0",
  "classes": ["ham", "spam"],
  "model_path": "model_artifacts/fraud_detection_model.joblib",
  "training_metadata": { ... },
  "evaluation": { ... }
}
```

---

### Single Prediction

#### `POST /api/predict`

Classify a single message.

**Request:**
```json
{
  "message": "Congratulations! You've won a $1000 gift card. Click here to claim now!"
}
```

**Response:**
```json
{
  "prediction_id": 1,
  "predicted_class": "spam",
  "risk_level": "high",
  "confidence": 0.9234,
  "probabilities": {
    "ham": 0.0766,
    "spam": 0.9234
  },
  "model_version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00",
  "indicators": [
    "Contains external links (URLs)",
    "Contains monetary amounts",
    "Contains term: 'won'"
  ],
  "recommendation": "This message shows suspicious patterns consistent with spam...",
  "explanation_disclaimer": "These indicators are derived from patterns learned..."
}
```

**Error Responses:**
- `400` — Missing or invalid message
- `503` — Model not loaded

---

### Batch Prediction

#### `POST /api/predict/batch`

Classify multiple messages (max 100).

**Request:**
```json
{
  "messages": [
    "Congratulations! You've won!",
    "Hey, are we still meeting tomorrow?"
  ]
}
```

**Response:**
```json
{
  "predictions": [
    {
      "message": "Congratulations! You've won!",
      "predicted_class": "spam",
      "risk_level": "high",
      "confidence": 0.9123,
      ...
    },
    {
      "message": "Hey, are we still meeting tomorrow?",
      "predicted_class": "ham",
      "risk_level": "low",
      "confidence": 0.9567,
      ...
    }
  ],
  "batch_size": 2
}
```

---

### Prediction History

#### `GET /api/predictions`

Get paginated prediction history.

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | int | 1 | Page number |
| per_page | int | 20 | Items per page (max 100) |
| search | string | — | Search in message text |
| category | string | — | Filter by class (spam/ham) |
| risk_level | string | — | Filter by risk level |
| date_from | string | — | Filter from date (ISO format) |
| date_to | string | — | Filter to date (ISO format) |
| sort_by | string | created_at | Sort field |
| sort_order | string | desc | Sort order (asc/desc) |

**Response:**
```json
{
  "predictions": [
    {
      "id": 1,
      "message": "Congratulations!...",
      "predicted_class": "spam",
      "risk_level": "high",
      "confidence": 0.9234,
      "model_version": "1.0.0",
      "indicators": "[...]",
      "recommendation": "...",
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 50,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

---

#### `GET /api/predictions/<id>`

Get a single prediction by ID.

---

#### `DELETE /api/predictions/<id>`

Delete a prediction by ID.

---

#### `DELETE /api/predictions`

Clear all prediction history.

---

#### `GET /api/predictions/export`

Export filtered history to CSV. Accepts same query parameters as `/api/predictions`.

---

### Analytics

#### `GET /api/analytics/summary`

Get summary statistics.

**Response:**
```json
{
  "total_messages": 150,
  "suspicious_count": 45,
  "legitimate_count": 105,
  "risk_distribution": {
    "low": 80,
    "medium": 40,
    "high": 20,
    "critical": 10
  }
}
```

---

#### `GET /api/analytics/categories`

Get category distribution.

**Response:**
```json
{
  "categories": {
    "spam": 45,
    "ham": 105
  }
}
```

---

#### `GET /api/analytics/trends`

Get prediction trends over time.

**Response:**
```json
{
  "trends": [
    {
      "date": "2024-01-15",
      "spam": 5,
      "ham": 15
    }
  ]
}
```

---

## Error Format

All errors follow this format:

```json
{
  "error": "Error Type",
  "message": "Human-readable error description"
}
```

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request — Invalid input |
| 404 | Not Found — Resource doesn't exist |
| 429 | Too Many Requests — Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable — Model not loaded |
