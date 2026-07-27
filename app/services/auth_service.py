from app.models import User
from app.utils.security import sanitize_input

class AuthService:
    @staticmethod
    def register_user(name, email, password, department='Computer Science', skills='', interest='', role='student'):
        try:
            name = sanitize_input(name)
            email = sanitize_input(email).lower()
            department = sanitize_input(department)
            skills = sanitize_input(skills)
            interest = sanitize_input(interest)

            existing = User.objects(email=email).first()
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
            user.save()
            return user, None
        except Exception as e:
            return None, f"Registration error: {str(e)}"

    @staticmethod
    def authenticate_user(email, password):
        try:
            email = sanitize_input(email).lower()
            user = User.objects(email=email).first()
            if user and user.check_password(password):
                return user
            return None
        except Exception:
            return None

auth_service = AuthService()
