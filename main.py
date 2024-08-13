from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import app, db
from app.models import User, Curso, UploadImage, Inscricao
import base64
from datetime import date

@app.route('/')   
def home():
    cursos = Curso.query.all()
    cursos_with_images = []

    for curso in cursos:
        upload = UploadImage.query.filter_by(curso_img=curso.id).first()
        if upload:
            data_base64 = base64.b64encode(upload.data).decode('utf-8')
            cursos_with_images.append((curso, upload, data_base64))

    return render_template('index.html', cursos=cursos_with_images)


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
        curso = Curso.query.get(curso_id)

        if curso:
            upload = UploadImage(filename=file.filename, data=file.read(), curso_img=curso_id)
            db.session.add(upload)
            db.session.commit()
            return redirect(url_for('cursos', curso_id=curso_id))
        else:
            return redirect(url_for('home'))
    
    return render_template('uploadImage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):
            flash('E-mail ou senha incorretos, tente novamente. ', 'error')
            return redirect(url_for('login'))        

        login_user(user)
        return redirect(url_for('cursos'))

    return render_template('login.html')

@app.route('/cursos')
def cursos():
    cursos = Curso.query.all()
    cursos_with_images = []

    for curso in cursos:
        upload = UploadImage.query.filter_by(curso_img=curso.id).first()
        if upload:
            data_base64 = base64.b64encode(upload.data).decode('utf-8')
            cursos_with_images.append((curso, upload, data_base64))

    return render_template('cursos.html', cursos=cursos_with_images)

@app.route('/matricular/<int:curso_id>')
def matricular(curso_id):
    if current_user.is_authenticated:
        inscricao = Inscricao(user_id=current_user.id, curso_id=curso_id, data_inscricao=date.today())
        db.session.add(inscricao)
        db.session.commit()
    return redirect(url_for('cursos'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run()

