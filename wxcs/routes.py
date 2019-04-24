from flask import render_template, url_for, flash, redirect
from wxcs import app

@app.route("/")
@app.route("/home")
def hello_world():
    return render_template('home.html')
