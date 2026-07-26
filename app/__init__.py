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

    # Connect to MongoDB with graceful cloud fallback
    mongo_uri = app.config.get('MONGO_URI') or os.getenv('MONGO_URI', '')

    if app.config.get('TESTING'):
        try:
            import mongomock
            try:
                db.disconnect(alias='default')
            except Exception:
                pass
            db.connect('student_startup_test_db', mongo_client_class=mongomock.MongoClient, alias='default')
        except Exception:
            pass
    else:
        connected = False
        if mongo_uri and ('mongodb://' in mongo_uri or 'mongodb+srv://' in mongo_uri) and 'localhost' not in mongo_uri:
            try:
                db.disconnect(alias='default')
                db.connect(host=mongo_uri, alias='default', serverSelectionTimeoutMS=5000)
                connected = True
            except Exception:
                connected = False

        if not connected:
            try:
                db.disconnect(alias='default')
                local_uri = mongo_uri if (mongo_uri and 'localhost' in mongo_uri) else 'mongodb://localhost:27017/student_startup_db'
                db.connect(host=local_uri, alias='default', serverSelectionTimeoutMS=1000)
                from mongoengine.connection import get_db
                get_db().command('ping')
                connected = True
            except Exception:
                try:
                    import mongomock
                    db.disconnect(alias='default')
                    db.connect('student_startup_db', mongo_client_class=mongomock.MongoClient, alias='default')
                    connected = True
                except Exception:
                    pass

    # Auto-seed demo student if database has no users
    try:
        if User.objects.count() == 0:
            demo_student = User(
                name="Alex Dev",
                email="student@gmail.com",
                department="Computer Science & Engineering",
                skills="Python, Artificial Intelligence, Web Development, Machine Learning",
                interest="Generative AI & Agritech",
                role="student"
            )
            demo_student.set_password("student123")
            demo_student.save()
    except Exception:
        pass

    # Initialize extensions
    login_manager.init_app(app)
    cors.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.objects(id=int(user_id)).first()
        except Exception:
            return None

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


app = create_app(os.getenv('FLASK_ENV', 'default'))
