from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import auth_service
from app.utils.validators import validate_registration_payload

auth_bp = Blueprint('auth_api', __name__, url_prefix='/api/v1')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    is_valid, errors = validate_registration_payload(data)
    if not is_valid:
        return jsonify({"status": "error", "error": errors[0], "status_code": 400}), 400

    user, error = auth_service.register_user(
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        department=data.get('department', 'Computer Science'),
        skills=data.get('skills', ''),
        interest=data.get('interest', '')
    )

    if error:
        return jsonify({"status": "error", "error": error, "status_code": 400}), 400

    login_user(user)
    return jsonify({
        "status": "success",
        "message": "User created successfully",
        "user_id": user.id,
        "user": user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "error": "Email and password are required.", "status_code": 400}), 400

    user = auth_service.authenticate_user(email, password)
    if not user:
        return jsonify({"status": "error", "error": "Invalid email address or password.", "status_code": 401}), 401

    login_user(user, remember=data.get('remember', False))
    return jsonify({
        "status": "success",
        "message": "Logged in successfully",
        "user_id": user.id,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"status": "success", "message": "Logged out successfully"}), 200

@auth_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        return jsonify({"status": "success", "user": current_user.to_dict()}), 200

    data = request.get_json() or {}
    current_user.name = data.get('name', current_user.name)
    current_user.department = data.get('department', current_user.department)
    current_user.skills = data.get('skills', current_user.skills)
    current_user.interest = data.get('interest', current_user.interest)
    current_user.save()

    return jsonify({"status": "success", "message": "Profile updated successfully", "user": current_user.to_dict()}), 200
