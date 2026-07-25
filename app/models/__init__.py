from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    department = db.Column(db.String(100), default='Computer Science')
    skills = db.Column(db.Text, default='')
    interest = db.Column(db.Text, default='')
    role = db.Column(db.String(20), default='student') # student, mentor, admin
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    startups = db.relationship('StartupProject', backref='owner', lazy=True, cascade='all, delete-orphan')
    feedbacks = db.relationship('Feedback', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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


class StartupProject(db.Model):
    __tablename__ = 'startup_projects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    startup_name = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    problem = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)
    technology = db.Column(db.Text, nullable=False)
    target_customer = db.Column(db.Text, nullable=False)
    goal = db.Column(db.Text, nullable=True)
    business_type = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    skill_gap = db.Column(db.Text, nullable=True)
    swot_analysis = db.Column(db.Text, nullable=True)
    innovation_score = db.Column(db.Float, default=85.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    market_analysis = db.relationship('MarketAnalysis', backref='startup', uselist=False, cascade='all, delete-orphan')
    competitors = db.relationship('CompetitorData', backref='startup', lazy=True, cascade='all, delete-orphan')
    validation_result = db.relationship('ValidationResult', backref='startup', uselist=False, cascade='all, delete-orphan')
    business_model = db.relationship('BusinessModel', backref='startup', uselist=False, cascade='all, delete-orphan')
    financial_analysis = db.relationship('FinancialAnalysis', backref='startup', uselist=False, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='startup', lazy=True, cascade='all, delete-orphan')

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


class MarketAnalysis(db.Model):
    __tablename__ = 'market_analysis'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup_projects.id'), nullable=False, index=True)
    market_size = db.Column(db.String(100), default='$10B+')
    growth_rate = db.Column(db.String(50), default='18.5%')
    trend_score = db.Column(db.Float, default=88.0)
    customer_demand = db.Column(db.String(50), default='High')
    future_scope = db.Column(db.Text, default='Rapidly growing AI sector')
    custom_trajectory = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

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



class CompetitorData(db.Model):
    __tablename__ = 'competitors'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup_projects.id'), nullable=False, index=True)
    company_name = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), default='https://example.com')
    strength = db.Column(db.Text, default='Strong brand presence')
    weakness = db.Column(db.Text, default='High price point & complex onboarding')
    technology = db.Column(db.String(100), default='Legacy Cloud APIs')
    pricing = db.Column(db.String(50), default='$99/mo')

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


class ValidationResult(db.Model):
    __tablename__ = 'validation_results'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup_projects.id'), nullable=False, index=True)
    innovation_score = db.Column(db.Float, default=90.0) # 25% weight
    market_score = db.Column(db.Float, default=85.0)     # 30% weight
    technology_score = db.Column(db.Float, default=80.0) # 25% weight
    business_score = db.Column(db.Float, default=88.0)   # 20% weight
    risk_score = db.Column(db.String(20), default='Low')
    overall_score = db.Column(db.Float, default=86.15)
    recommendation = db.Column(db.Text, default='Proceed to MVP development')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

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


class BusinessModel(db.Model):
    __tablename__ = 'business_models'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup_projects.id'), nullable=False, index=True)
    customer_segments = db.Column(db.Text, nullable=False)
    value_proposition = db.Column(db.Text, nullable=False)
    channels = db.Column(db.Text, nullable=False)
    customer_relationship = db.Column(db.Text, nullable=False)
    revenue_streams = db.Column(db.Text, nullable=False)
    key_resources = db.Column(db.Text, nullable=False)
    key_activities = db.Column(db.Text, nullable=False)
    key_partners = db.Column(db.Text, nullable=False)
    cost_structure = db.Column(db.Text, nullable=False)

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


class FinancialAnalysis(db.Model):
    __tablename__ = 'financial_analysis'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup_projects.id'), nullable=False, index=True)
    development_cost = db.Column(db.Float, default=15000.0)
    marketing_cost = db.Column(db.Float, default=5000.0)
    operational_cost = db.Column(db.Float, default=3000.0)
    revenue_prediction = db.Column(db.Float, default=65000.0)
    profit_estimate = db.Column(db.Float, default=42000.0)
    roi = db.Column(db.Float, default=182.6) # Percentage
    break_even_period = db.Column(db.String(50), default='7 Months')

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


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup_projects.id'), nullable=False, index=True)
    report_name = db.Column(db.String(150), nullable=False)
    report_path = db.Column(db.String(300), nullable=False)
    report_type = db.Column(db.String(50), default='PDF')
    generated_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'startup_id': self.startup_id,
            'report_name': self.report_name,
            'report_path': self.report_path,
            'report_type': self.report_type,
            'generated_date': self.generated_date.isoformat() if self.generated_date else None
        }


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
