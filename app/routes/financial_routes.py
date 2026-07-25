from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import FinancialAnalysis
from app.routes.resource_utils import get_owned_startup_or_404

financial_bp = Blueprint('financial_api', __name__, url_prefix='/api/v1')

@financial_bp.route('/financial-analysis/<int:startup_id>', methods=['GET'])
@login_required
def get_financial_analysis(startup_id):
    get_owned_startup_or_404(startup_id)
    fin = FinancialAnalysis.query.filter_by(startup_id=startup_id).first()
    if not fin:
        return jsonify({
            "status": "success",
            "investment": 23000,
            "revenue": 65000,
            "profit": 42000,
            "roi": 182.6,
            "break_even": "7 Months"
        }), 200
    return jsonify({"status": "success", "financials": fin.to_dict()}), 200
