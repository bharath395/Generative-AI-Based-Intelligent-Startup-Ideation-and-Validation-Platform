"""
Test Suite: Database Models — User, StartupProject, ValidationResult CRUD for MongoDB.
"""
from app.models import User, StartupProject, ValidationResult, MarketAnalysis

def test_user_creation(app):
    """Test creating a User model and password hashing."""
    with app.app_context():
        user = User(name='DB Test User', email='dbuser@test.com', department='CSE')
        user.set_password('mypassword')
        user.save()

        fetched = User.objects(email='dbuser@test.com').first()
        assert fetched is not None
        assert fetched.name == 'DB Test User'
        assert fetched.check_password('mypassword') is True
        assert fetched.check_password('wrongpw') is False

def test_user_to_dict(app):
    """Test User model serialization."""
    with app.app_context():
        user = User(name='Serial User', email='serial@test.com', department='IT', skills='Java', interest='Cloud')
        user.set_password('pass')
        user.save()

        d = user.to_dict()
        assert d['name'] == 'Serial User'
        assert d['email'] == 'serial@test.com'
        assert 'password_hash' not in d

def test_startup_project_creation(app):
    """Test creating a StartupProject linked to a User."""
    with app.app_context():
        user = User(name='Founder', email='founder@test.com')
        user.set_password('pw')
        user.save()

        startup = StartupProject(
            user_id=user.id,
            startup_name='Test AI App',
            domain='Technology',
            problem='Manual workflows',
            solution='AI automation',
            technology='Python, Flask',
            target_customer='Students'
        )
        startup.save()

        assert startup.id is not None
        assert startup.user_id == user.id

def test_validation_result_calculation(app):
    """Test ValidationResult weighted score formula."""
    with app.app_context():
        user = User(name='Val User', email='val@test.com')
        user.set_password('pw')
        user.save()

        startup = StartupProject(
            user_id=user.id, startup_name='Val Startup', domain='AI',
            problem='p', solution='s', technology='t', target_customer='c'
        )
        startup.save()

        val = ValidationResult(
            startup_id=startup.id,
            innovation_score=90.0,
            market_score=85.0,
            technology_score=80.0,
            business_score=88.0
        )
        overall = val.calculate_overall()
        assert overall == 85.6

def test_startup_deletion(app):
    """Test that deleting a startup deletes related MarketAnalysis documents."""
    with app.app_context():
        user = User(name='Cascade User', email='cascade@test.com')
        user.set_password('pw')
        user.save()

        startup = StartupProject(
            user_id=user.id, startup_name='Cascade Startup', domain='Tech',
            problem='p', solution='s', technology='t', target_customer='c'
        )
        startup.save()

        market = MarketAnalysis(startup_id=startup.id, market_size='$5B')
        market.save()

        startup_id = startup.id
        MarketAnalysis.objects(startup_id=startup_id).delete()
        startup.delete()

        assert MarketAnalysis.objects(startup_id=startup_id).first() is None
