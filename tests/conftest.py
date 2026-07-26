import pytest
import os

os.environ['DISABLE_LIVE_AI'] = '1'

from app import create_app
from app.models import (
    User, StartupProject, MarketAnalysis, CompetitorData,
    ValidationResult, BusinessModel, FinancialAnalysis, Report, Feedback
)

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        User.objects.delete()
        StartupProject.objects.delete()
        MarketAnalysis.objects.delete()
        CompetitorData.objects.delete()
        ValidationResult.objects.delete()
        BusinessModel.objects.delete()
        FinancialAnalysis.objects.delete()
        Report.objects.delete()
        Feedback.objects.delete()

        yield app

        User.objects.delete()
        StartupProject.objects.delete()
        MarketAnalysis.objects.delete()
        CompetitorData.objects.delete()
        ValidationResult.objects.delete()
        BusinessModel.objects.delete()
        FinancialAnalysis.objects.delete()
        Report.objects.delete()
        Feedback.objects.delete()

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
        user.save()
        return user
