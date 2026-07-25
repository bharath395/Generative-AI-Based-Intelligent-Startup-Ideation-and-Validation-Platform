from flask import Blueprint, jsonify
from flask_login import login_required
from app.routes.resource_utils import get_owned_startup_or_404
from ai_engine.agents.pitch_agent import pitch_agent

pitch_bp = Blueprint('pitch_api', __name__, url_prefix='/api/v1')

@pitch_bp.route('/pitch/<int:startup_id>', methods=['GET'])
@pitch_bp.route('/pitch-deck/<int:startup_id>', methods=['GET'])
@login_required
def get_pitch_deck(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    pitch_data = pitch_agent.execute(
        startup.startup_name, startup.domain, startup.problem, startup.solution
    )
    return jsonify({"status": "success", "pitch": pitch_data, "pitch_deck": pitch_data}), 200

