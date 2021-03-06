import sqlite3
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", messages=False)


@app.route('/aluno')
def aluno():
    return render_template("aluno.html")


@app.route('/nota')
def nota():
    return render_template("nota.html")


@app.route('/professor')
def professor():
    return render_template("professor.html")