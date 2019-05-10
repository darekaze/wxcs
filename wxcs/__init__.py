"""Initial wxcs."""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


# def create_app():
#     app = Flask(__name__)
#     return app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lalalalala'  # HACK: temp
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zetadb.sqlite'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Run only once when db init
# ---
# import wxcs.models
# db.create_all()

from . import routes
