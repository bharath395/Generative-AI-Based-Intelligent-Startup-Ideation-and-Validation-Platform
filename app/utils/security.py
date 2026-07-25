import html
import re

def sanitize_input(text):
    if not isinstance(text, str):
        return text
    # Escape HTML special characters to prevent XSS
    cleaned = html.escape(text.strip())
    return cleaned

def validate_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email.strip() if email else ''))

def check_password_strength(password):
    """
    Returns (is_valid, message)
    Requires at least 6 characters.
    """
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, "Password strength is acceptable."
