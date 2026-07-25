from app.utils.security import sanitize_input, validate_email_format, check_password_strength

def validate_registration_payload(data):
    errors = []
    name = sanitize_input(data.get('name', ''))
    email = sanitize_input(data.get('email', ''))
    password = data.get('password', '')

    if not name:
        errors.append("Full Name is required.")
    if not email or not validate_email_format(email):
        errors.append("A valid email address is required.")
    
    is_valid_pw, pw_msg = check_password_strength(password)
    if not is_valid_pw:
        errors.append(pw_msg)

    return len(errors) == 0, errors

def validate_idea_generation_payload(data):
    # All fields are optional! AI will auto-supply smart defaults if left empty.
    return True, []

