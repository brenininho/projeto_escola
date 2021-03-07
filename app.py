import sqlite3
from flask import Flask, render_template
import ipdb
from flask import request
from flask import abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@127.0.0.1/sistema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    school_year = db.Column(db.String(80), unique=True)

    def __init__(self, id, name, school_year):
        self.id = id
        self.name = name
        self.school_year = school_year


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    serie = db.Column(db.String(80), unique=True)

    def __init__(self, id, name, serie):
        self.id = id
        self.name = name
        self.serie = serie


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, unique=True)
    score = db.Column(db.Float, unique=True)
    topic = db.Column(db.String(80), unique=True)

    def __init__(self, id, id_aluno, score, topic):
        self.id = id
        self.id_aluno = id_aluno
        self.score = score
        self.topic = topic

conn = sqlite3.connect("system.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS professor ( name text, serie text)
""")
c.execute("CREATE TABLE IF NOT EXISTS scores (id_aluno int, score real, topic text)")
c.execute("CREATE TABLE IF NOT EXISTS student ( name text, school_year text)")
conn.commit()

conn.close()


@app.route('/')
def home():
    return render_template("home.html", messages=False)


@app.route('/aluno')
def aluno():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM student")
    data = c.fetchall()
    return render_template("aluno.html", data=data)


@app.route('/aluno/criar')
def aluno_criar():
    return render_template("aluno_create.html")


@app.route('/aluno/criar/salvar', methods=['POST'])
def aluno_criar_salvar():
    nome = request.form["nome"]
    serie = request.form["serie"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO student VALUES ('{nome}', '{serie}')")
    conn.commit()
    return redirect(url_for('aluno'))


@app.route('/aluno/editar/<int:id>')
def aluno_edit(id):
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"SELECT rowid, * FROM student WHERE rowid = {id}")
    data = c.fetchone()
    return render_template("aluno_edit.html", data=data)


@app.route('/aluno/editar/salvar/<int:id>', methods=['POST'])
def aluno_editar_salvar(id):
    nome = request.form["nome"]
    serie = request.form["serie"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"UPDATE student SET name = '{nome}', school_year = '{serie}'  WHERE rowid = {id}")
    conn.commit()
    return redirect(url_for('aluno'))



@app.route('/aluno/deletar/<int:id>')
def aluno_deletar(id):
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM student WHERE rowid = {id}")
    conn.commit()
    return redirect(url_for('aluno'))



@app.route('/professor')
def professor():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM professor")
    data = c.fetchall()
    return render_template("professor.html", data=data)


@app.route('/professor/criar')
def professor_criar():
    # conn = sqlite3.connect("system.db")
    # c = conn.cursor()
    # data = c.execute("INSERT INTO professor VALUES (")

    return render_template("professor_criar.html")


@app.route('/professor/criar/salvar', methods=['POST'])
def professor_criar_salvar():

    nome = request.form["nome"]
    serie = request.form["serie"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO professor VALUES ('{nome}', '{serie}')")
    conn.commit()
    return redirect(url_for('professor'))


@app.route('/professor/deletar/<int:id>')
def professor_deletar(id):
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
    c.execute(f"UPDATE professor SET score ='{nome}', topic ='{serie}' WHERE rowid = {id} ;")
    conn.commit()
    return redirect(url_for('professor'))


@app.route('/nota')
def score():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM student")
    alunos = c.fetchall()
    c.execute("SELECT rowid, id_aluno, score, topic  FROM scores")
    notas = c.fetchall()
    data = {
        "alunos": alunos,
        "notas": notas
    }
    return render_template("score.html", data=data)


@app.route('/nota/criar')
def score_create():
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM student")
    data = c.fetchall()
    return render_template("score_create.html", data=data)


@app.route('/nota/criar/salvar', methods=['POST'])
def score_create_save():
    score = request.form["score"]
    topic = request.form["topic"]
    id_aluno = request.form["id_aluno"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO scores VALUES ('{id_aluno}', '{score}', '{topic}' )")
    conn.commit()
    return redirect(url_for('score'))


@app.route('/nota/editar/<int:id>')
def score_edit(id):
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"SELECT rowid, * FROM scores WHERE rowid = {id}")
    nota = c.fetchone()
    c.execute("SELECT rowid, * FROM student")
    alunos = c.fetchall()
    data = {
        "nota": nota,
        "alunos": alunos
    }
    return render_template("score_edit.html", data=data)


@app.route('/nota/editar/salvar/<int:id>', methods=['POST'])
def score_edit_save(id):
    score = request.form["score"]
    topic = request.form["topic"]
    id_aluno = request.form["id_aluno"]
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"UPDATE scores SET id_aluno = '{id_aluno}', score = '{score}', topic = '{topic}'  WHERE rowid = {id}")
    conn.commit()
    return redirect(url_for('.score'))


@app.route('/nota/deletar/<int:id>')
def score_delete(id):
    conn = sqlite3.connect("system.db")
    c = conn.cursor()
    c.execute(f"DELETE FROM scores WHERE rowid = {id}")
    conn.commit()
    return redirect(url_for('.score'))
