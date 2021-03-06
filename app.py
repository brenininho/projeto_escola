import sqlite3
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html", messages=False)


@app.route('/aluno')
def aluno():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    # c.execute("CREATE TABLE IF NOT EXISTS student (name text, school_year text)")
    c.execute("INSERT INTO student VALUES ('Breno Valle', 3º Ano Médio'")
    conn.commit()
    data = c.fetchall()
    return render_template("aluno.html", data=data)


@app.route('/professor')
def professor():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    # c.execute("CREATE TABLE IF NOT EXISTS professor (name text, school_year text)")
    conn.commit()
    return render_template("professor.html")


@app.route('/nota')
def nota():
    return render_template("nota.html")