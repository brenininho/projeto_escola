import sqlite3
from flask import Flask, render_template
import ipdb
from flask import request
from flask import abort, redirect, url_for

app = Flask(__name__)

conn = sqlite3.connect("system.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS professor ( name text, serie text)")
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
    # conn = sqlite3.connect("system.db")
    # c = conn.cursor()
    # data = c.execute("INSERT INTO professor VALUES (")

    return render_template("professor_criar.html")


@app.route('/professor/deletar/<int:id>')
def aluno_deletar(id):
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM professor WHERE rowid = {id}")
    conn.commit()
    return redirect(url_for('professor'))


@app.route('/professor/editar/<int:id>')
def professor_editar(id):
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"SELECT rowid, * FROM professor WHERE rowid = {id}")
    data = c.fetchone()
    return render_template("professor_editar.html", data=data)


@app.route('/professor/editar/salvar/<int:id>',  methods=['POST'])
def professor_editar_salvar(id):
    nome = request.form["name"]
    serie = request.form["serie"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"UPDATE professor SET name ='{nome}', serie ='{serie}' WHERE rowid = {id} ;")
    conn.commit()
    return redirect(url_for('professor'))


@app.route('/professor/criar/salvar', methods=['POST'])
def professor_criar_salvar():

    nome = request.form["nome"]
    serie = request.form["serie"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO professor VALUES ('{nome}', '{serie}')")
    conn.commit()
    return redirect(url_for('professor'))