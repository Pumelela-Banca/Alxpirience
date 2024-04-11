from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'


def create_app(config_class=Config):
    """
    creates app using the config class or the default config class
    This makes state is not stored on the object
    """
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)

    from expirience.users.routes import users
    from expirience.projects.routes import jobs
    from expirience.main.routes import main
    from expirience.skills.routes import skills
    from expirience.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(jobs)
    app.register_blueprint(main)
    app.register_blueprint(skills)
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()

    return app

