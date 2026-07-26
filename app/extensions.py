import mongoengine as db
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()
cors = CORS()

login_manager.login_view = 'views.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Please log in to access this page.'

