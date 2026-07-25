from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.ai_service import ai_service
from app.models import StartupProject
from app.utils.validators import validate_idea_generation_payload

idea_bp = Blueprint('idea_api', __name__, url_prefix='/api/v1')

@idea_bp.route('/generate-idea', methods=['POST'])
@login_required
def generate_idea():
    data = request.get_json() or {}
    is_valid, errors = validate_idea_generation_payload(data)
    if not is_valid:
        return jsonify({"status": "error", "error": errors[0], "status_code": 400}), 400

    domain = data.get('domain')
    budget = data.get('budget', '50000')
    target_customers = data.get('target_customers')
    business_type = data.get('business_type')
    goal = data.get('goal')
    skills = data.get('skills', '')
    preferred_tech = data.get('preferred_tech', '')
    location = data.get('location', '')

    startup, pipeline_res = ai_service.generate_and_save_startup(
        user_id=current_user.id,
        domain=domain,
        budget=budget,
        target_customers=target_customers,
        business_type=business_type,
        goal=goal,
        skills=skills,
        preferred_tech=preferred_tech,
        location=location
    )

    return jsonify({
        "status": "success",
        "message": "Startup ideas generated and validated successfully",
        "startup_id": startup.id,
        "startup_name": startup.startup_name,
        "ideas": pipeline_res.get('ideas', []),
        "primary_idea": pipeline_res.get('primary_idea', {}),
        "validation": pipeline_res.get('validation', {}),
        "swot": pipeline_res.get('swot', ''),
        "market": pipeline_res.get('market', {}),
        "competitors": pipeline_res.get('competitors', [])
    }), 201

@idea_bp.route('/select-idea', methods=['POST'])
@login_required
def select_idea():
    data = request.get_json() or {}
    idea = data.get('idea', {})
    if not idea or not isinstance(idea, dict):
        return jsonify({"status": "error", "error": "No valid idea selected", "status_code": 400}), 400

    domain = data.get('domain', 'Technology')
    budget = data.get('budget', '50000')
    target_customers = data.get('target_customers', '')
    business_type = data.get('business_type', '')
    goal = data.get('goal', '')
    skills = data.get('skills', '')
    preferred_tech = data.get('preferred_tech', '')
    location = data.get('location', '')

    startup, pipeline_res = ai_service.save_chosen_idea(
        user_id=current_user.id,
        idea_dict=idea,
        domain=domain,
        budget=budget,
        target_customers=target_customers,
        business_type=business_type,
        goal=goal,
        skills=skills,
        preferred_tech=preferred_tech,
        location=location
    )

    return jsonify({
        "status": "success",
        "message": f"Selected idea '{startup.startup_name}' saved as active project!",
        "startup_id": startup.id,
        "startup_name": startup.startup_name,
        "idea": idea
    }), 201


@idea_bp.route('/ideas', methods=['GET'])
@login_required
def list_ideas():
    startups = StartupProject.query.filter_by(user_id=current_user.id).order_by(StartupProject.created_at.desc()).all()
    return jsonify({
        "status": "success",
        "ideas": [s.to_dict() for s in startups]
    }), 200

@idea_bp.route('/startup/<int:startup_id>', methods=['GET'])
@login_required
def get_startup_detail(startup_id):
    from app.routes.resource_utils import get_owned_startup_or_404
    startup = get_owned_startup_or_404(startup_id)
    
    # Parse skill_gap
    skill_gap_data = {}
    if startup.skill_gap:
        try:
            import json
            skill_gap_data = json.loads(startup.skill_gap)
        except Exception:
            skill_gap_data = {"analysis_markdown": startup.skill_gap}

    return jsonify({
        "status": "success",
        "startup": {
            **startup.to_dict(),
            "skill_gap_parsed": skill_gap_data,
            "market_analysis": startup.market_analysis.to_dict() if startup.market_analysis else None,
            "validation_result": startup.validation_result.to_dict() if startup.validation_result else None,
            "business_model": startup.business_model.to_dict() if startup.business_model else None,
            "financial_analysis": startup.financial_analysis.to_dict() if startup.financial_analysis else None,
            "competitors": [c.to_dict() for c in startup.competitors] if startup.competitors else []
        }
    }), 200

@idea_bp.route('/startup/<int:startup_id>/domain', methods=['PUT'])
@login_required
def update_startup_domain(startup_id):
    from app.routes.resource_utils import get_owned_startup_or_404
    from app.extensions import db
    startup = get_owned_startup_or_404(startup_id)
    data = request.get_json() or {}
    new_domain = data.get('domain', '').strip()
    if not new_domain:
        return jsonify({"status": "error", "error": "New domain name is required"}), 400

    startup.domain = new_domain
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": f"Domain updated to '{new_domain}' for '{startup.startup_name}'!",
        "startup_id": startup.id,
        "new_domain": new_domain
    }), 200

@idea_bp.route('/startup/<int:startup_id>', methods=['DELETE'])
@idea_bp.route('/ideas/<int:startup_id>', methods=['DELETE'])
@login_required
def delete_startup(startup_id):
    from app.routes.resource_utils import get_owned_startup_or_404
    from app.extensions import db
    startup = get_owned_startup_or_404(startup_id)
    try:
        db.session.delete(startup)
        db.session.commit()
        return jsonify({
            "status": "success",
            "message": f"Startup '{startup.startup_name}' deleted successfully."
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "error": str(e)}), 500



