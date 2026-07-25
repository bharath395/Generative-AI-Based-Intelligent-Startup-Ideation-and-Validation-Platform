from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import StartupProject

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def index():
    return render_template('index.html')

@views_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return render_template('login.html')

@views_bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.dashboard'))
    return render_template('register.html')

@views_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@views_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@views_bp.route('/idea-generator')
@login_required
def idea_generator():
    return render_template('idea_generator.html')

@views_bp.route('/market-analysis')
@login_required
def market_analysis():
    return render_template('market_analysis.html')

@views_bp.route('/competitor-analysis')
@login_required
def competitor_analysis():
    return render_template('competitor.html')

@views_bp.route('/validation-score')
@login_required
def validation_score():
    return render_template('validation.html')

@views_bp.route('/business-model')
@login_required
def business_model():
    return render_template('business_model.html')

@views_bp.route('/pitch-generator')
@login_required
def pitch_generator():
    return render_template('pitch.html')

@views_bp.route('/mentor-chat')
@login_required
def mentor_chat():
    return render_template('mentor_chat.html')

@views_bp.route('/reports')
@login_required
def reports():
    return render_template('report.html')
