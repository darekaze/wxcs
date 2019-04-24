from flask import Flask, render_template

# def create_app():
#     app = Flask(__name__)
#     return app

app = Flask(__name__)

from wxcs import routes
