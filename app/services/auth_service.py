from app.extensions import db
from app.models import User
from app.utils.security import sanitize_input

class AuthService:
    @staticmethod
    def register_user(name, email, password, department='Computer Science', skills='', interest='', role='student'):
        name = sanitize_input(name)
        email = sanitize_input(email).lower()
        department = sanitize_input(department)
        skills = sanitize_input(skills)
        interest = sanitize_input(interest)

        existing = User.query.filter_by(email=email).first()
        if existing:
            return None, "Email address is already registered."

        user = User(
            name=name,
            email=email,
            department=department,
            skills=skills,
            interest=interest,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user, None

    @staticmethod
    def authenticate_user(email, password):
        email = sanitize_input(email).lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None

auth_service = AuthService()
