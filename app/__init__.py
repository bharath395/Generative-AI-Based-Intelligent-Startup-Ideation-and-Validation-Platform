import os
from flask import Flask, jsonify, render_template
from config import config_by_name
from app.extensions import db, login_manager, cors
from app.models import User

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)

    with app.app_context():
        db.create_all()
        try:
            from sqlalchemy import text
            db.session.execute(text("ALTER TABLE market_analysis ADD COLUMN custom_trajectory TEXT"))
            db.session.commit()
        except Exception:
            db.session.rollback()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Register Blueprints
    from app.routes.view_routes import views_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.idea_routes import idea_bp
    from app.routes.market_routes import market_bp
    from app.routes.competitor_routes import competitor_bp
    from app.routes.validation_routes import validation_bp
    from app.routes.business_routes import business_bp
    from app.routes.financial_routes import financial_bp
    from app.routes.pitch_routes import pitch_bp
    from app.routes.report_routes import report_bp
    from app.routes.chat_routes import chat_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.advanced_routes import advanced_bp

    app.register_blueprint(views_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(idea_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(competitor_bp)
    app.register_blueprint(validation_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(financial_bp)
    app.register_blueprint(pitch_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(advanced_bp)

    # Register Global Error Handlers (400, 401, 403, 404, 500)
    @app.errorhandler(400)
    def bad_request_error(e):
        return jsonify({"status": "error", "error": "Bad Request", "status_code": 400}), 400

    @app.errorhandler(401)
    def unauthorized_error(e):
        return jsonify({"status": "error", "error": "Unauthorized Access", "status_code": 401}), 401

    @app.errorhandler(403)
    def forbidden_error(e):
        return jsonify({"status": "error", "error": "Forbidden", "status_code": 403}), 403

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({"status": "error", "error": "Resource Not Found", "status_code": 404}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"status": "error", "error": "Internal Server Error", "status_code": 500}), 500

    return app
