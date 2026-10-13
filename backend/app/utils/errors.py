"""Centralized error handlers for the Flask application."""
from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register error handlers with the Flask app.

    Args:
        app: Flask application instance.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error.description) if hasattr(error, 'description') else 'Invalid request',
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The requested method is not allowed for this endpoint.',
        }), 405

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.',
        }), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Log the error
        app.logger.error(f"Unhandled exception: {error}", exc_info=True)

        # If it's an HTTP exception, use its status code
        if isinstance(error, HTTPException):
            return jsonify({
                'error': error.name,
                'message': error.description,
            }), error.code

        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
        }), 500
