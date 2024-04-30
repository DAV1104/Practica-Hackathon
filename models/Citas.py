from config.db import db, ma, app
from sqlalchemy import ForeignKey

class Citas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    hora = db.Column(db.String(255))
    fecha = db.Column(db.String(255), nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))
    
    def __init__(self,id, titulo, hora, fecha):
        self.id = id
        self.titulo = titulo
        self.hora = hora
        self.fecha = fecha
        
with app.app_context():
    db.create_all()
        
class CitasSchema():
    class Meta:
        fields = ('id', 'titulo', 'hora', 'fecha')
        
cita_schema = CitasSchema()
citas_schema = CitasSchema(many=True)