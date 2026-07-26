import os
from pathlib import Path
from dotenv import load_dotenv

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    pymysql = None

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

DATABASE_DIR = BASE_DIR / 'database'
REPORTS_DIR = BASE_DIR / 'reports'
LOGS_DIR = BASE_DIR / 'logs'

# Ensure required runtime directories exist
for directory in [DATABASE_DIR, REPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def normalize_database_url(database_url):
    if database_url and database_url.startswith('mysql://'):
        return database_url.replace('mysql://', 'mysql+pymysql://', 1)
    if database_url and database_url.startswith('sqlite:///'):
        sqlite_path = database_url.replace('sqlite:///', '', 1)
        if sqlite_path != ':memory:':
            path = Path(sqlite_path)
            if not path.is_absolute():
                path = BASE_DIR / path
            path.parent.mkdir(parents=True, exist_ok=True)
            return f'sqlite:///{path.as_posix()}'
    return database_url


def get_mongo_uri():
    uri = os.getenv('MONGO_URI') or os.getenv('MONGODB_URI') or os.getenv('MONGODB_URL')
    if uri and (uri.startswith('mongodb://') or uri.startswith('mongodb+srv://')):
        return uri
    db_url = os.getenv('DATABASE_URL')
    if db_url and (db_url.startswith('mongodb://') or db_url.startswith('mongodb+srv://')):
        return db_url
    return 'mongodb://localhost:27017/student_startup_db'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key-student-startup-platform-2026')
    MONGO_URI = get_mongo_uri()
    MONGODB_SETTINGS = {
        'host': MONGO_URI
    }
    
    # Gemini API Key
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # Storage settings
    REPORTS_FOLDER = str(REPORTS_DIR)
    LOGS_FOLDER = str(LOGS_DIR)
    
    # App Settings
    APP_TITLE = "Student Startup Ideation & Validation Platform"
    ITEMS_PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/student_startup_test_db'
    MONGODB_SETTINGS = {
        'host': MONGO_URI
    }
    SECRET_KEY = 'test-secret-key'

class ProductionConfig(Config):
    DEBUG = False
    # Ensure SECRET_KEY is set in production environment
    SECRET_KEY = os.getenv('SECRET_KEY', 'prod-fallback-secure-key-change-in-env')

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
