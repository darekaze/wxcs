"""Initial wxcs."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# def create_app():
#     app = Flask(__name__)
#     return app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lalalalala'  # HACK: temp
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zetadb.sqlite'
db = SQLAlchemy(app)

from wxcs import routes
