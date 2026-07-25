from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from app.models import StartupProject
from app.routes.resource_utils import get_owned_startup_or_404
from app.services.advanced_service import advanced_service


advanced_bp = Blueprint('advanced_api', __name__, url_prefix='/api/v1')


@advanced_bp.route('/startup-history', methods=['GET'])
@login_required
def startup_history():
    return jsonify({
        "status": "success",
        "history": advanced_service.get_startup_history(current_user.id),
    }), 200


@advanced_bp.route('/idea-comparison', methods=['POST'])
@login_required
def idea_comparison():
    data = request.get_json() or {}
    startup_ids = data.get('startup_ids') or []
    if len(set(startup_ids)) < 2:
        return jsonify({
            "status": "error",
            "error": "Select at least two startup ideas to compare.",
            "status_code": 400,
        }), 400

    startups = StartupProject.query.filter(
        StartupProject.id.in_(startup_ids),
        StartupProject.user_id == current_user.id,
    ).all()
    if len(startups) != len(set(startup_ids)):
        return jsonify({
            "status": "error",
            "error": "One or more startup ideas were not found for this user.",
            "status_code": 404,
        }), 404

    return jsonify({
        "status": "success",
        **advanced_service.compare_startups(startups),
    }), 200


@advanced_bp.route('/recommendations', methods=['GET'])
@login_required
def recommendations():
    return jsonify({
        "status": "success",
        "recommendations": advanced_service.recommend_directions(current_user),
    }), 200


@advanced_bp.route('/progress/<int:startup_id>', methods=['GET'])
@login_required
def startup_progress(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    return jsonify({
        "status": "success",
        "progress": advanced_service.get_progress(startup),
    }), 200


@advanced_bp.route('/notifications', methods=['GET'])
@login_required
def notifications():
    return jsonify({
        "status": "success",
        "notifications": advanced_service.get_notifications(current_user.id),
    }), 200


@advanced_bp.route('/admin-dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return jsonify({
            "status": "error",
            "error": "Admin access is required.",
            "status_code": 403,
        }), 403

    return jsonify({
        "status": "success",
        "stats": advanced_service.get_admin_dashboard(),
    }), 200
