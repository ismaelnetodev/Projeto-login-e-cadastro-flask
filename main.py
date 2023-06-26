from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db
from app.models import User, Curso, UploadImage
import base64


@app.route('/')   
def home():
    cursos = Curso.query.all()
    cursos_base64 = []

    for curso in cursos:
        upload = UploadImage.query.filter_by(curso_img=curso.id).first()
        if upload:
            data_base64 = base64.b64encode(upload.data).decode('utf-8')
            cursos_base64.append((curso, upload, data_base64))
    return render_template('index.html', cursos=cursos_base64)

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

        curso = Curso(name, preco, desc)

        db.session.add(curso)
        db.session.flush()
        curso_id = curso.id
        db.session.commit()
        return redirect(url_for('uploadImage', curso_id=curso_id))
    return render_template('cadastro-curso.html')

@app.route('/cadastro/upload/<int:curso_id>', methods=['GET', 'POST'])
def uploadImage(curso_id):
    if request.method == 'POST':
        file = request.files['arquivo']
        upload = UploadImage(filename=file.filename, data=file.read(), curso_img=curso_id)
        db.session.add(upload)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('uploadImage.html')


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