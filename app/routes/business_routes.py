from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import BusinessModel
from app.routes.resource_utils import get_owned_startup_or_404

business_bp = Blueprint('business_api', __name__, url_prefix='/api/v1')

@business_bp.route('/business-model/<int:startup_id>', methods=['GET'])
@login_required
def get_business_model(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    bm = BusinessModel.query.filter_by(startup_id=startup_id).first()
    if not bm:
        from ai_engine.agents.business_agent import business_agent
        from app.extensions import db
        from app.services.ai_service import safe_str
        bm_data = business_agent.execute(startup.startup_name, startup.domain, startup.problem, startup.solution)
        bm = BusinessModel(
            startup_id=startup.id,
            customer_segments=safe_str(bm_data.get('customer_segments'), "Engineering Students, Academic Incubators, Bootstrapped Tech Teams"),
            value_proposition=safe_str(bm_data.get('value_proposition'), "Automated 24/7 AI startup mentoring & investor-ready PDF generation"),
            channels=safe_str(bm_data.get('channels'), "Direct Web App, University Incubators, Tech Conferences"),
            customer_relationship=safe_str(bm_data.get('customer_relationship'), "Self-service SaaS UI & Automated Onboarding"),
            revenue_streams=safe_str(bm_data.get('revenue_streams'), "Freemium Access Model, Premium PDF Downloads, B2B University SaaS"),
            key_resources=safe_str(bm_data.get('key_resources'), "AI LLM APIs, Vector Database Knowledge Base, Web Backend"),
            key_activities=safe_str(bm_data.get('key_activities'), "AI Agent Fine-Tuning & Web Platform Maintenance"),
            key_partners=safe_str(bm_data.get('key_partners'), "Google Gemini API, College Innovation Cells, Local Incubators"),
            cost_structure=safe_str(bm_data.get('cost_structure'), "Cloud AI API Tokens, Server Hosting & Maintenance")
        )
        db.session.add(bm)
        db.session.commit()

    return jsonify({"status": "success", "business_model": bm.to_dict()}), 200

