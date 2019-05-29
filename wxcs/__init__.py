"""The wxcs package containing configs and extecsions."""
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_flatpages import FlatPages
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'
moment = Moment()
pages = FlatPages()
migrate = Migrate()


def create_app(configs='wxcs.config'):
    """Init app."""
    app = Flask(__name__)
    app.config.from_object(configs)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    pages.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    from wxcs.core.routes import core
    from wxcs.admin.routes import admin

    app.register_blueprint(core)
    app.register_blueprint(admin)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template.

        If a HTTPException, pull the `code` attribute;
        Default to 500
        """
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.jinja'.format(error_code)), error_code

    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        from wxcs.models import Admin
        return {'db': db, 'Admin': Admin}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    from wxcs.commands import seed, clean
    app.cli.add_command(seed)
    app.cli.add_command(clean)
