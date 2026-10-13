"""Prediction request/response schemas.

These are used for documentation and manual validation.
In production, consider using marshmallow or pydantic for
automatic request validation.
"""

PREDICT_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["message"],
    "properties": {
        "message": {
            "type": "string",
            "minLength": 1,
            "maxLength": 5000,
            "description": "The text message to classify",
        },
    },
}

PREDICT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "prediction_id": {"type": "integer"},
        "predicted_class": {
            "type": "string",
            "enum": ["spam", "ham"],
        },
        "risk_level": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"],
        },
        "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "model_version": {"type": "string"},
        "timestamp": {"type": "string", "format": "date-time"},
        "indicators": {
            "type": "array",
            "items": {"type": "string"},
        },
        "recommendation": {"type": "string"},
    },
}

BATCH_PREDICT_REQUEST_SCHEMA = {
    "type": "object",
    "required": ["messages"],
    "properties": {
        "messages": {
            "type": "array",
            "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 5000,
            },
            "minItems": 1,
            "maxItems": 100,
        },
    },
}
