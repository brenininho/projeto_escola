import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

conn = sqlite3.connect("system.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS professor ( name text, school_year text)")
conn.close()


@app.route('/')
def home():
    return render_template("home.html", messages=False)


@app.route('/aluno')
def aluno():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    # c.execute("CREATE TABLE IF NOT EXISTS student (name text, school_year text)")
    # c.execute("INSERT INTO student VALUES ('Breno Valle', 3 ano médio'")
    conn.commit()
    data = c.fetchall()
    return render_template("aluno.html", data=data)


@app.route('/aluno/criar')
def aluno_criar():
    return render_template("aluno_criar.html")


@app.route('/aluno/editar/<int:id>')
def aluno_edit(id):
    return render_template("aluno_edit.html")


@app.route('/aluno/deletar/<int:id>')
def aluno_deletar(id):
    pass


@app.route('/professor')
def professor():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM professor")
    data = c.fetchall()
    return render_template("professor.html", data=data)


@app.route('/nota')
def nota():
    return render_template("nota.html")


@app.route('/professor/criar')
def professor_criar():
    return render_template("professor_criar.html")


@app.route('/professor/deletar/<int:id>')
def professor_deletar(id):
    pass


@app.route('/professor/editar/<int:id>')
def professor_editar(id):

    return render_template("professor_editar.html")