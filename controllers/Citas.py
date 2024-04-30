from config.db import db, ma, app
from flask import Flask, Blueprint, request, jsonify, render_template

from models.Citas import Citas, cita_schema, citas_schema

ruta_citas = Blueprint('citas_route', __name__)

@ruta_citas.route('/citas', methods=['GET'])
def indexcitas():
    return render_template('')

#Ruta para crear los usuarios
@ruta_citas.route('/ccita', methods=['POST'])
def create_cita():
    titulo = request.json['titulo']
    fecha = request.json['fecha']
    hora = request.json['hora']
    #Validar que los datos no esten vacios
    if not fecha:
        return jsonify({ 'message': 'Necesita especificar una fecha'})
    if not titulo:
        return jsonify
    
    new_cita = Citas(titulo, fecha, hora)
    
    #Se añade el nuevo usuario a la base de datos
    db.session.add(new_cita)
    db.session.commit()
    return jsonify({ 'message': 'Cita agregado' }), 200

#Ruta para obtener todas las citas
@ruta_citas.route('/ocitas', methods=['GET'])
def get_citas():
    #SELECT * FROM Citas
    result = db.session.query(Citas).all()
    data = {}
    
    i=0
    for cita in result:
        i+=1
        
        data[i]={
            'Titulo': cita.titulo,
            'Fecha': cita.fecha,
            'Hora': cita.hora
        }
    return jsonify(data)

@ruta_citas.route('/ucita', methods=['PUT'])
def update_cita():
    id = request.json['id']
    #Se verifica que los datos no esten vacios
    if not id.isdigit():
        return jsonify({'message': 'ID invalida'}), 400
    #Se filtra la cita en base su id
    cita = Citas.query.filter_by(id=id).first()
    #Se finaliza en caso de que la cita no exista
    if cita == None:
        return jsonify({'message': 'Cita no encontrada'}), 404
    
    titulo = request.json['titulo']
    fecha = request.json['fecha']
    hora = request.json['hora']
    
    if not fecha:
        return jsonify({'message': 'Nombre es requerido'}), 400
    if not titulo:
        return jsonify({'message': 'Titulo es requerido'}), 400
    
    cita.titulo = titulo
    cita.fecha = fecha    
    
    #Se agregan los cambios a la base de datos
    db.session.commit()
    return { 'message': 'Cita actualizada' }

@ruta_citas.route('/dcitas', methods=['DELETE'])
def delete_cita():
    id = request.json['id']
    #Se verifica que la id no este vacia
    if not id.isdigit():
        return jsonify({'message': 'Id invalida'}), 400
    
    cita = cita.query.filter_by(id).first()
    #Se verifica que exista esta cita
    if cita is None:
        return jsonify({'message': 'User no encontrado'}), 404
    
    db.session.delete(cita)
    db.session.commit()
    return { 'message': 'Usuario eliminado' }

@ruta_citas.route('/cita/<int:cita_id>', methods=['GET'])
def get_cita(cita_id):
    cita = Citas.query.get(cita_id)
    if cita:
        return jsonify({'nombre': cita.nombre, 'usuario': cita.usuario})
    else:
        return jsonify({'message': 'User not found'}), 404
    