from config.db import db, ma, app
from sqlalchemy.orm import relationship, backref

class Users(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(255), nullable = False)
    usuario = db.Column(db.String(255), nullable = False)
    contrseña = db.Column(db.String(255), nullable = False)
    citas = db.Column(relationship('Citas', backref='usuario'))
    
    def __init__ (self, id, nombre, usuario, contraseña):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.contraseña = contraseña
        
with app.app_context():
    db.create_all()

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'usuario', 'contraseña')

users_schema = UsersSchema(many = True)
user_schema = UsersSchema()