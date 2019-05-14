"""The wxcs package containing configs and extecsions."""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'


def create_app(configs='wxcs.config'):
    """Init app."""
    app = Flask(__name__)
    app.config.from_object(configs)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from wxcs.core.routes import core
    from wxcs.admin.routes import admin
    app.register_blueprint(core)
    app.register_blueprint(admin)

    return app
