import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure database
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, f'{os.getenv("DB_NAME")}.db')
db = SQLAlchemy(app)

# Configure Login Manager
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# Configure Mail Server
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.getenv('EMAIL'),
    "MAIL_PASSWORD": os.getenv('PASSWORD')
}

app.config.update(mail_settings)
mail = Mail(app)

# Configure SCSS Compiler
from flask_assets import Environment, Bundle
assets = Environment(app)


assets.url = app.static_url_path
assets.directory = app.static_folder
assets.append_path('static/css')

scss = Bundle('base.scss', 'index.scss', 'login.scss','register.scss', filters='scss', output='all.css')
assets.register('scss_all', scss)


import petcare.models
import petcare.views
