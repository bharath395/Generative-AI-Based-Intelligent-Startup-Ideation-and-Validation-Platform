from app import create_app
from app.models import User
from app.services.ai_service import ai_service
from migrate_sqlite_to_mongodb import migrate

def seed_database():
    app = create_app('development')
    with app.app_context():
        print("Initializing MongoDB collections...")
        try:
            migrate()
        except Exception as e:
            print(f"Notice: SQLite migration check: {e}")

        # Check if demo student exists
        demo_student = User.objects(email="student@gmail.com").first()
        if not demo_student:
            print("Seeding initial student account (student@gmail.com / student123)...")
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

            print("Generating initial seed startup project...")
            ai_service.generate_and_save_startup(
                user_id=demo_student.id,
                domain="Agriculture & AI",
                skills="Python, Machine Learning, IoT",
                budget="50000",
                interest="Smart Crop Yield Prediction"
            )

        print("MongoDB initialization complete!")

if __name__ == '__main__':
    seed_database()
