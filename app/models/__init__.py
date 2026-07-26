from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import mongoengine as db

class User(UserMixin, db.Document):
    meta = {'collection': 'users'}

    id = db.SequenceField(primary_key=True)
    name = db.StringField(required=True, max_length=120)
    email = db.StringField(required=True, unique=True, max_length=120)
    password_hash = db.StringField(required=True, max_length=256)
    department = db.StringField(default='Computer Science', max_length=100)
    skills = db.StringField(default='')
    interest = db.StringField(default='')
    role = db.StringField(default='student', max_length=20) # student, mentor, admin
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'skills': self.skills,
            'interest': self.interest,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class StartupProject(db.Document):
    meta = {'collection': 'startup_projects'}

    id = db.SequenceField(primary_key=True)
    user_id = db.IntField(required=True)
    startup_name = db.StringField(required=True, max_length=150)
    domain = db.StringField(required=True, max_length=100)
    problem = db.StringField(required=True)
    solution = db.StringField(required=True)
    technology = db.StringField(required=True)
    target_customer = db.StringField(required=True)
    goal = db.StringField()
    business_type = db.StringField(max_length=100)
    location = db.StringField(max_length=100)
    skill_gap = db.StringField()
    swot_analysis = db.StringField()
    innovation_score = db.FloatField(default=85.0)
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'startup_name': self.startup_name,
            'domain': self.domain,
            'problem': self.problem,
            'solution': self.solution,
            'technology': self.technology,
            'target_customer': self.target_customer,
            'goal': self.goal,
            'business_type': self.business_type,
            'location': self.location,
            'skill_gap': self.skill_gap,
            'swot_analysis': self.swot_analysis,
            'innovation_score': self.innovation_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MarketAnalysis(db.Document):
    meta = {'collection': 'market_analysis'}

    id = db.SequenceField(primary_key=True)
    startup_id = db.IntField(required=True)
    market_size = db.StringField(default='$10B+', max_length=100)
    growth_rate = db.StringField(default='18.5%', max_length=50)
    trend_score = db.FloatField(default=88.0)
    customer_demand = db.StringField(default='High', max_length=50)
    future_scope = db.StringField(default='Rapidly growing AI sector')
    custom_trajectory = db.StringField()
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'market_size': self.market_size,
            'growth_rate': self.growth_rate,
            'trend_score': self.trend_score,
            'customer_demand': self.customer_demand,
            'future_scope': self.future_scope,
            'custom_trajectory': self.custom_trajectory,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CompetitorData(db.Document):
    meta = {'collection': 'competitors'}

    id = db.SequenceField(primary_key=True)
    startup_id = db.IntField(required=True)
    company_name = db.StringField(required=True, max_length=100)
    product_name = db.StringField(required=True, max_length=100)
    website = db.StringField(default='https://example.com', max_length=200)
    strength = db.StringField(default='Strong brand presence')
    weakness = db.StringField(default='High price point & complex onboarding')
    technology = db.StringField(default='Legacy Cloud APIs', max_length=100)
    pricing = db.StringField(default='$99/mo', max_length=50)

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'company_name': self.company_name,
            'product_name': self.product_name,
            'website': self.website,
            'strength': self.strength,
            'weakness': self.weakness,
            'technology': self.technology,
            'pricing': self.pricing
        }


class ValidationResult(db.Document):
    meta = {'collection': 'validation_results'}

    id = db.SequenceField(primary_key=True)
    startup_id = db.IntField(required=True)
    innovation_score = db.FloatField(default=90.0) # 25% weight
    market_score = db.FloatField(default=85.0)     # 30% weight
    technology_score = db.FloatField(default=80.0) # 25% weight
    business_score = db.FloatField(default=88.0)   # 20% weight
    risk_score = db.StringField(default='Low', max_length=20)
    overall_score = db.FloatField(default=86.15)
    recommendation = db.StringField(default='Proceed to MVP development')
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def calculate_overall(self):
        self.overall_score = round(
            (self.innovation_score * 0.25) +
            (self.market_score * 0.30) +
            (self.technology_score * 0.25) +
            (self.business_score * 0.20), 2
        )
        return self.overall_score

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'innovation_score': self.innovation_score,
            'market_score': self.market_score,
            'technology_score': self.technology_score,
            'business_score': self.business_score,
            'risk_score': self.risk_score,
            'overall_score': self.overall_score,
            'recommendation': self.recommendation,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class BusinessModel(db.Document):
    meta = {'collection': 'business_models'}

    id = db.SequenceField(primary_key=True)
    startup_id = db.IntField(required=True)
    customer_segments = db.StringField(required=True)
    value_proposition = db.StringField(required=True)
    channels = db.StringField(required=True)
    customer_relationship = db.StringField(required=True)
    revenue_streams = db.StringField(required=True)
    key_resources = db.StringField(required=True)
    key_activities = db.StringField(required=True)
    key_partners = db.StringField(required=True)
    cost_structure = db.StringField(required=True)

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'customer_segments': self.customer_segments,
            'value_proposition': self.value_proposition,
            'channels': self.channels,
            'customer_relationship': self.customer_relationship,
            'revenue_streams': self.revenue_streams,
            'key_resources': self.key_resources,
            'key_activities': self.key_activities,
            'key_partners': self.key_partners,
            'cost_structure': self.cost_structure
        }


class FinancialAnalysis(db.Document):
    meta = {'collection': 'financial_analysis'}

    id = db.SequenceField(primary_key=True)
    startup_id = db.IntField(required=True)
    development_cost = db.FloatField(default=15000.0)
    marketing_cost = db.FloatField(default=5000.0)
    operational_cost = db.FloatField(default=3000.0)
    revenue_prediction = db.FloatField(default=65000.0)
    profit_estimate = db.FloatField(default=42000.0)
    roi = db.FloatField(default=182.6) # Percentage
    break_even_period = db.StringField(default='7 Months', max_length=50)

    def calculate_financials(self):
        total_initial_investment = self.development_cost + self.marketing_cost + self.operational_cost
        if total_initial_investment > 0:
            self.profit_estimate = self.revenue_prediction - total_initial_investment
            self.roi = round((self.profit_estimate / total_initial_investment) * 100, 2)
            monthly_profit = self.profit_estimate / 12.0 if self.profit_estimate > 0 else 1.0
            months = max(1, round(total_initial_investment / monthly_profit))
            self.break_even_period = f"{months} Months"

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'development_cost': self.development_cost,
            'marketing_cost': self.marketing_cost,
            'operational_cost': self.operational_cost,
            'revenue_prediction': self.revenue_prediction,
            'profit_estimate': self.profit_estimate,
            'roi': self.roi,
            'break_even_period': self.break_even_period
        }


class Report(db.Document):
    meta = {'collection': 'reports'}

    id = db.SequenceField(primary_key=True)
    startup_id = db.IntField(required=True)
    report_name = db.StringField(required=True, max_length=150)
    report_path = db.StringField(required=True, max_length=300)
    report_type = db.StringField(default='PDF', max_length=50)
    generated_date = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'report_name': self.report_name,
            'report_path': self.report_path,
            'report_type': self.report_type,
            'generated_date': self.generated_date.isoformat() if self.generated_date else None
        }


class Feedback(db.Document):
    meta = {'collection': 'feedback'}

    id = db.SequenceField(primary_key=True)
    user_id = db.IntField(required=True)
    message = db.StringField(required=True)
    rating = db.IntField(default=5)
    created_at = db.DateTimeField(default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
