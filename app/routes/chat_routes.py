from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ai_engine.agents.mentor_agent import mentor_agent

chat_bp = Blueprint('chat_api', __name__, url_prefix='/api/v1')

@chat_bp.route('/mentor-chat', methods=['POST'])
@login_required
def mentor_chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')
    if not user_message.strip():
        return jsonify({"status": "error", "error": "Message cannot be empty."}), 400

    ai_reply = mentor_agent.execute(current_user.id, user_message)
    return jsonify({
        "status": "success",
        "reply": ai_reply
    }), 200
