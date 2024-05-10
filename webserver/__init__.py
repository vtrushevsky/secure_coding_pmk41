from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_limiter import Limiter
from flask_sslify import SSLify

curr_cart = dict({})

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdoSDF2394+OQIE_QSDAqq1'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_COOKIE_SECURE'] = True  # VULNERABILITY session hijacking prevention - HTTPS for session cookie
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # prevents client-side JavaScript from accessing the session cookie

    db.init_app(app)
    sslify = SSLify(app=app)  # MITM prevention - force redirect from 80/8080 to 443

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # limiter = Limiter(app, default_limits=["10 per minute"])
    # limiter.key_func = lambda: request.headers.get('X-Real-IP')

    # limiter.limit(views)
    # limiter.limit(auth)

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
