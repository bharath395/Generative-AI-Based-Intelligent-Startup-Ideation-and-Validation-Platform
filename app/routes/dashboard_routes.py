from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.services.analytics_service import analytics_service

dashboard_bp = Blueprint('dashboard_api', __name__, url_prefix='/api/v1')

@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    stats = analytics_service.get_dashboard_stats(user_id=current_user.id)
    return jsonify({
        "status": "success",
        "stats": stats
    }), 200
