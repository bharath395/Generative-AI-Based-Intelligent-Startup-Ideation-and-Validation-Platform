from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import ValidationResult
from app.routes.resource_utils import get_owned_startup_or_404
from ai_engine.agents.validation_agent import validation_agent

validation_bp = Blueprint('validation_api', __name__, url_prefix='/api/v1')

@validation_bp.route('/validate', methods=['POST'])
@login_required
def validate_startup():
    data = request.get_json() or {}
    innov = data.get('innovation', 90)
    mkt = data.get('market', 85)
    tech = data.get('technology', 80)
    biz = data.get('business', 88)

    res = validation_agent.execute(innov, mkt, tech, biz)
    return jsonify({
        "status": "success",
        "innovation": res['innovation_score'],
        "market": res['market_score'],
        "technology": res['technology_score'],
        "business": res['business_score'],
        "risk": res['risk_score'],
        "overall": res['overall_score'],
        "recommendation": res['recommendation']
    }), 200

@validation_bp.route('/validation/<int:startup_id>', methods=['GET'])
@validation_bp.route('/validation-result/<int:startup_id>', methods=['GET'])
@login_required
def get_validation_result(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    val = ValidationResult.objects(startup_id=startup.id).first()
    if not val:
        val_res = validation_agent.execute(startup.innovation_score or 90.0, 85.0, 80.0, 88.0)
        val = ValidationResult(
            startup_id=startup.id,
            innovation_score=val_res['innovation_score'],
            market_score=val_res['market_score'],
            technology_score=val_res['technology_score'],
            business_score=val_res['business_score'],
            risk_score=val_res['risk_score'],
            overall_score=val_res['overall_score'],
            recommendation=val_res['recommendation']
        )
        val.save()

    val_dict = val.to_dict()
    val_dict['explanation'] = (
        f"• Strong overall score of {val.overall_score}/100 driven by high market viability ({val.market_score}%) and technical execution ({val.technology_score}%).\n"
        f"• Recommended action: {val.recommendation}"
    )

    return jsonify({"status": "success", "validation": val_dict, "validation_result": val_dict}), 200
