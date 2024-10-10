from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class usuarios(db.Model):
    __tablename__ = 'usuarios'

    cedula = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)

    def __init__(self, cedula, nombre, email, contraseña):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña