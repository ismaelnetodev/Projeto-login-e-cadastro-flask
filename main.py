from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.models import User, Curso
import os


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd = request.form['password']

        user = User(name, email, pwd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('cadastrar.html')

@app.route('/cadastro/curso', methods=['GET', 'POST'])
def cadastrarCurso():
    if request.method == 'POST':
        name = request.form['name']
        preco = float(request.form['preco'])
        desc = request.form['desc']
        img = request.files['arquivo']

        curso = Curso(name=name, valor=preco, desc=desc)

        if img:
            curso.imagem = img.read()

        db.session.add(curso)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cadastro-curso.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):
            return redirect(url_for('/'))        

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/cursos')
def cursos():
    pass

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

app.run(debug=True)