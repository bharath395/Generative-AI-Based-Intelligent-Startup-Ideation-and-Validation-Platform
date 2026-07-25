import pytest
import os

os.environ['DISABLE_LIVE_AI'] = '1'

from app import create_app
from app.extensions import db
from app.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_user(app):
    with app.app_context():
        user = User(
            name="Test Student",
            email="teststudent@gmail.com",
            department="Computer Science",
            skills="Python, AI",
            interest="Agritech",
            role="student"
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user
