import json
from pathlib import Path

from flask import Blueprint, current_app, jsonify, url_for, request
from flask_login import login_required
from app.models import MarketAnalysis
from app.routes.resource_utils import get_owned_startup_or_404
from ai_engine.tools.analytics_tool import (
    build_market_projection,
    build_plotly_market_projection,
    generate_matplotlib_projection_chart,
)
from ai_engine.tools.news_tool import fetch_market_news
from ai_engine.tools.trend_tool import fetch_google_trends_score

market_bp = Blueprint('market_api', __name__, url_prefix='/api/v1')

@market_bp.route('/market-analysis/<int:startup_id>', methods=['GET'])
@login_required
def get_market_analysis(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    market = MarketAnalysis.objects(startup_id=startup.id).first()
    if not market:
        return jsonify({
            "status": "success",
            "market_size": "$10 Billion+",
            "growth_rate": "20%",
            "trend_score": 88.0,
            "customer_demand": "High Demand",
            "future_scope": f"Rapid market growth in {startup.domain}"
        }), 200

    return jsonify({"status": "success", "market": market.to_dict()}), 200


@market_bp.route('/market-analysis/<int:startup_id>', methods=['PUT'])
@login_required
def update_market_analysis(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    market = MarketAnalysis.objects(startup_id=startup.id).first()
    if not market:
        market = MarketAnalysis(startup_id=startup.id)

    data = request.get_json() or {}
    if 'market_size' in data:
        market.market_size = str(data['market_size']).strip()
    if 'growth_rate' in data:
        market.growth_rate = str(data['growth_rate']).strip()
    if 'customer_demand' in data:
        market.customer_demand = str(data['customer_demand']).strip()
    if 'future_scope' in data:
        market.future_scope = str(data['future_scope']).strip()
    if 'custom_trajectory' in data:
        traj = data['custom_trajectory']
        market.custom_trajectory = json.dumps(traj) if isinstance(traj, (dict, list)) else str(traj)

    market.save()
    return jsonify({
        "status": "success",
        "message": f"Market analysis updated for '{startup.startup_name}'!",
        "market": market.to_dict()
    }), 200


@market_bp.route('/market-insights/<int:startup_id>', methods=['GET'])
@login_required
def get_market_insights(startup_id):
    startup = get_owned_startup_or_404(startup_id)
    market = MarketAnalysis.objects(startup_id=startup.id).first()
    trend_data = fetch_google_trends_score(startup.domain, [startup.startup_name])

    domain_hash = abs(hash(startup.domain)) % 12
    base_val = round(3.5 + domain_hash + (startup.id * 1.4), 2)
    annual_growth = round(0.15 + ((startup.id % 4) * 0.06), 3)

    projection = build_market_projection(base_value=base_val, annual_growth=annual_growth)
    
    if market and market.custom_trajectory:
        try:
            custom_data = json.loads(market.custom_trajectory)
            if isinstance(custom_data, (dict, list)):
                projection = custom_data
        except Exception:
            pass

    plotly_chart = build_plotly_market_projection(projection)

    chart_dir = Path(current_app.static_folder) / "generated"
    chart_path = chart_dir / f"market_projection_{startup.id}.png"
    generate_matplotlib_projection_chart(projection, chart_path)

    return jsonify({
        "status": "success",
        "startup_id": startup.id,
        "domain": startup.domain,
        "trend": trend_data,
        "news": fetch_market_news(f"{startup.domain} startup market"),
        "projection": projection,
        "plotly_chart": plotly_chart,
        "matplotlib_chart_url": url_for(
            'static',
            filename=f"generated/market_projection_{startup.id}.png"
        ),
    }), 200
