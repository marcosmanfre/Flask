from flask import Flask
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<p> Bom dia</p>"

@app.route("/sobre")
def sobre():
    return "<h1> portal de vendas </h1>"

@app.route("/teste")
def teste():
    return render_template('index.html')

@app.route("/user/<username>")
def username(username):
    return render_template('user.html',username=username)