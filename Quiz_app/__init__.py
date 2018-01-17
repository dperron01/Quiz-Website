# import for app
from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from Quiz_app.proxy import ReverseProxied
#import flask_whooshalchemy as whooshalchemy

#configurtion
app = Flask(__name__, instance_relative_config= True)
app.config.from_pyfile('flask.config')

#database using SQLAlchemy and postgresql
db = SQLAlchemy(app)
db.init_app(app)

#flask_whooshalchemy for full text search
#from Quiz_app.models import QuizDatabase
#whooshalchemy.whoosh_index(app, QuizDatabase)
#MAX_SEARCH_RESULTS = 25

#flask_mail
mail = Mail(app)

#flask_login
from .models import User
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader #can use session_token instead of user_if for more security
def load_user(userID):
    return User.query.filter(User.userID == int(userID)).first()

# Used for deployment using ReverseProxied class
app.wsgi_app = ReverseProxied(app.wsgi_app)

from . import routes
