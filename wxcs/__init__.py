from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# def create_app():
#     app = Flask(__name__)
#     return app

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lalalalala' # HACK: temp
app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


from wxcs import routes
