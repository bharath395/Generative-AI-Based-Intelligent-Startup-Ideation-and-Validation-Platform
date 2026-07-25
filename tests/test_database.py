"""
Test Suite: Database Models — User, StartupProject, ValidationResult CRUD and relationships.
"""
from app.extensions import db
from app.models import User, StartupProject, ValidationResult, MarketAnalysis

def test_user_creation(app):
    """Test creating a User model and password hashing."""
    with app.app_context():
        user = User(name='DB Test User', email='dbuser@test.com', department='CSE')
        user.set_password('mypassword')
        db.session.add(user)
        db.session.commit()

        fetched = User.query.filter_by(email='dbuser@test.com').first()
        assert fetched is not None
        assert fetched.name == 'DB Test User'
        assert fetched.check_password('mypassword') is True
        assert fetched.check_password('wrongpw') is False

def test_user_to_dict(app):
    """Test User model serialization."""
    with app.app_context():
        user = User(name='Serial User', email='serial@test.com', department='IT', skills='Java', interest='Cloud')
        user.set_password('pass')
        db.session.add(user)
        db.session.commit()

        d = user.to_dict()
        assert d['name'] == 'Serial User'
        assert d['email'] == 'serial@test.com'
        assert 'password_hash' not in d

def test_startup_project_creation(app):
    """Test creating a StartupProject linked to a User."""
    with app.app_context():
        user = User(name='Founder', email='founder@test.com')
        user.set_password('pw')
        db.session.add(user)
        db.session.commit()

        startup = StartupProject(
            user_id=user.id,
            startup_name='Test AI App',
            domain='Technology',
            problem='Manual workflows',
            solution='AI automation',
            technology='Python, Flask',
            target_customer='Students'
        )
        db.session.add(startup)
        db.session.commit()

        assert startup.id is not None
        assert startup.owner.name == 'Founder'

def test_validation_result_calculation(app):
    """Test ValidationResult weighted score formula."""
    with app.app_context():
        user = User(name='Val User', email='val@test.com')
        user.set_password('pw')
        db.session.add(user)
        db.session.commit()

        startup = StartupProject(
            user_id=user.id, startup_name='Val Startup', domain='AI',
            problem='p', solution='s', technology='t', target_customer='c'
        )
        db.session.add(startup)
        db.session.commit()

        val = ValidationResult(
            startup_id=startup.id,
            innovation_score=90.0,
            market_score=85.0,
            technology_score=80.0,
            business_score=88.0
        )
        overall = val.calculate_overall()
        # (90*0.25) + (85*0.30) + (80*0.25) + (88*0.20) = 22.5 + 25.5 + 20.0 + 17.6 = 85.6
        assert overall == 85.6

def test_startup_relationship_cascade(app):
    """Test that deleting a startup cascades to MarketAnalysis."""
    with app.app_context():
        user = User(name='Cascade User', email='cascade@test.com')
        user.set_password('pw')
        db.session.add(user)
        db.session.commit()

        startup = StartupProject(
            user_id=user.id, startup_name='Cascade Startup', domain='Tech',
            problem='p', solution='s', technology='t', target_customer='c'
        )
        db.session.add(startup)
        db.session.commit()

        market = MarketAnalysis(startup_id=startup.id, market_size='$5B')
        db.session.add(market)
        db.session.commit()

        startup_id = startup.id
        db.session.delete(startup)
        db.session.commit()

        assert MarketAnalysis.query.filter_by(startup_id=startup_id).first() is None
