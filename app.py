import sqlite3
from flask import Flask, render_template
from flask import request
from flask import abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey

Base = declarative_base()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@127.0.0.1/sistema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    year = db.Column(db.String(80))


    def __init__(self, name, year):
        self.name = name
        self.year = year
        ## self.boletim = boletim



class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    serie = db.Column(db.String(80))

    def __init__(self, name, serie):
        self.name = name
        self.serie = serie


class Scores(db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('student.id', onupdate="CASCADE", ondelete="CASCADE"), unique=True)
    student = relationship("Student")
    score = db.Column(db.Float)
    topic = db.Column(db.String(80))

    def __init__(self, id_aluno, score, topic):
        self.id_aluno = id_aluno
        self.score = score
        self.topic = topic
        # self.notas = notas


@app.route('/')
def home():
    return render_template("home.html", messages=False)


@app.route('/aluno')
def aluno():
    data = Student.query.all()
    return render_template("aluno.html", data=data)


@app.route('/aluno/criar')
def aluno_criar():
    return render_template("aluno_create.html")


@app.route('/aluno/criar/salvar', methods=['POST'])
def aluno_criar_salvar():
    if request.method == 'POST':
        student1 = Student(name=request.form['name'], year=request.form['year'])
        db.session.add(student1)
        db.session.commit()
        return redirect(url_for('aluno'))


@app.route('/aluno/editar/<int:id>', methods=['GET', 'POST'])
def aluno_edit(id):
    data = Student.query.get(id)
    if request.method == 'POST':
        data.name = request.form['name']
        data.year = request.form['year']
        db.session.commit()
        return redirect(url_for('aluno'))
    return render_template("aluno_edit.html", data=data)


@app.route('/aluno/deletar/<int:id>')
def aluno_deletar(id):
    student_delete = Student.query.get(id)
    db.session.delete(student_delete)
    db.session.commit()
    return redirect(url_for('aluno'))



@app.route('/professor')
def professor():
    data = Professor.query.all()
    return render_template("professor.html", data=data)


@app.route('/professor/criar')
def professor_criar():
    return render_template("professor_criar.html")


@app.route('/professor/criar/salvar', methods=['POST'])
def professor_criar_salvar():
    professor1 = Professor(name=request.form["name"], serie=request.form["serie"])
    db.session.add(professor1)
    db.session.commit()
    return redirect(url_for('professor'))


@app.route('/professor/editar/<int:id>', methods=['GET', 'POST'])
def professor_editar(id):
    data = Professor.query.get(id)
    if request.method == 'POST':
        data.name = request.form['name']
        data.serie = request.form['serie']
        db.session.commit()
        return redirect(url_for('professor'))
    return render_template("professor_editar.html", data=data)


@app.route('/professor/deletar/<int:id>')
def professor_deletar(id):
    professor_delete = Professor.query.get(id)
    db.session.delete(professor_delete)
    db.session.commit()
    return redirect(url_for('professor'))


@app.route('/nota')
def score():
    score = Scores.query.all()
    college = Student.query.all()
    data = {
        'score': score,
        'college': college
    }
    return render_template("score.html", data=data)


@app.route('/nota/criar')
def score_create():
    score = Scores.query.all()
    college = Student.query.all()
    data = {
        'score': score,
        'college': college
    }
    return render_template("score_create.html", data=data)


@app.route('/nota/criar/salvar', methods=['POST'])
def score_create_save():
    score1 = Scores(id_aluno=request.form["id_aluno"], score=request.form["score"], topic=request.form["topic"])
    db.session.add(score1)
    db.session.commit()
    return redirect(url_for('score'))


@app.route('/nota/editar/<int:id>', methods=['POST', 'GET'])
def score_edit(id):
    score = Scores.query.get(id)
    college = Student.query.all()
    data = {
        "score": score,
        "college": college
    }
    if request.method == 'POST':
        score.score = request.form['score']
        score.topic = request.form['topic']
        score.id_aluno = request.form['id_aluno']
        db.session.commit()
        return redirect(url_for('score'))
    return render_template("score_edit.html", data=data)



@app.route('/nota/deletar/<int:id>')
def score_delete(id):
    nota_delete = Scores.query.get(id)
    db.session.delete(nota_delete)
    db.session.commit()
    return redirect(url_for('score'))


