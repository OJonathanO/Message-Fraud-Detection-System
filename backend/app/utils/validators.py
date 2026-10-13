"""Input validation utilities."""


def validate_message(message) -> tuple:
    """Validate a single message.

    Args:
        message: The message to validate.

    Returns:
        Tuple of (is_valid: bool, error_message: str).
    """
    if message is None:
        return False, "Message is required"

    if not isinstance(message, str):
        return False, "Message must be a string"

    if len(message.strip()) == 0:
        return False, "Message cannot be empty"

    if len(message) > 5000:
        return False, "Message exceeds maximum length of 5000 characters"

    return True, ""


def validate_batch_messages(messages) -> tuple:
    """Validate a batch of messages.

    Args:
        messages: List of messages to validate.

    Returns:
        Tuple of (is_valid: bool, error_message: str).
    """
    if not isinstance(messages, list):
        return False, "Messages must be provided as a list"

    if len(messages) == 0:
        return False, "At least one message is required"

    if len(messages) > 100:
        return False, "Batch size cannot exceed 100 messages"

    for i, msg in enumerate(messages):
        is_valid, error = validate_message(msg)
        if not is_valid:
            return False, f"Message at index {i}: {error}"

    return True, ""
