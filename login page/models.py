from db import db

class Usuarios(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), nullable=True, unique=True)
    password = db.Column(db.String())