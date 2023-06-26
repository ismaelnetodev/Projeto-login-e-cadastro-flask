from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(86), nullable=False)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        db.create_all()

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Curso(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float)
    desc = db.Column(db.String(200))

    def __init__(self, name, valor, desc):
        self.name = name
        self.valor = valor
        self.desc = desc
        db.create_all()

class UploadImage(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    curso_img = db.Column(db.Integer, db.ForeignKey('cursos.id'))

    def __init__(self, filename, data, curso_img):
        self.filename = filename
        self.data = data
        self.curso_img = curso_img

class Inscricao(db.Model):
    __tablename__ = 'inscricoes'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'))
    data_inscricao = db.Column(db.DateTime)

    def __init__(self, user_id, curso_id, data_inscricao):
        self.user_id = user_id
        self.curso_id = curso_id
        self.data_inscricao = data_inscricao
        db.create_all()