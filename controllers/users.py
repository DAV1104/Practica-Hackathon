from flask import Flask, Blueprint, request, render_template, jsonify
from config.db import db, ma, app

from models.users import Users, user_schema, users_schema
from models.Citas import Citas, cita_schema, citas_schema

ruta_user = Blueprint('route_user', __name__)

#Se define la ruta que devuelva la pagina de los usuarios
@ruta_user.route('/user', methods=['GET'])
def indexuser():
    return render_template('')

#Ruta para crear los usuarios
@ruta_user.route('/cuser', methods=['POST'])
def create_user():
    nombre = request.json['nombre']
    usuario = request.json['usuario']
    contraseña = request.json['contraseña']
    
    #Si el usuario existe, no se puede crear
    Usuario = Users.query.filter_by(usuario=usuario).first()
    if usuario == Usuario.usuario:
        return jsonify({ 'message': 'Este usuario ya existe'}, 400)
    
    new_user = Users(nombre, usuario, contraseña)
    
    #Se añade el nuevo usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()
    return jsonify({ 'message': 'Usuario agregado' }), 201

#Ruta para obtener todos los usuarios
@ruta_user.route('/ouser', methods=['GET'])
def get_users():
    #SELECT * FROM USERS
    result = db.session.query(Users).all()
    data = {}
    
    i=0
    for user in result:
        i+=1
        
        data[i]={
            'nombre': user.nombre,
            'usuario': user.usuario
        }
    return jsonify(data)

@ruta_user.route('/uuser/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    Usuario = Users.query.get(user_id)
    if not Usuario:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    usuario = request.json['usuario']
    nombre = request.json['nombre']
    
    #Se verifica que los datos no esten vacios
    if not nombre:
        return jsonify({'message': 'Nombre es requerido'}), 400
    if not usuario:
        return jsonify({'message': 'Usuario es requerido'}), 400
    
    Usuario.nombre = nombre
    Usuario.usuario = usuario    
    
    #Se agregan los cambios a la base de datos
    db.session.commit()
    return { 'message': 'Usuario actualizdo' }

@ruta_user.route('/duser/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    Usuario = Users.query.get(user_id)
    #Se verifica que exista este usuario
    if Usuario is None:
        return jsonify({'message': 'User no encontrado'}), 404
    
    db.session.delete(Usuario)
    db.session.commit()
    return { 'message': 'Usuario eliminado' }

@ruta_user.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    if user:
        return jsonify({'nombre': user.nombre, 'usuario': user.usuario})
    else:
        return jsonify({'message': 'User not found'}), 404
    
@ruta_user.route('/addcitas/<int:user_id>/citas', methods=['POST'])
def add_citas_to_user(user_id):
    try:
        # Busca un usuario existente y lo devuelve
        user = Users.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found"}), 404
        
        # Extrae los datos de la request
        titulo = request.json['titulo']
        hora = request.json['hora']
        fecha = request.json['fecha']
        
        if not all([titulo, fecha]):
            return jsonify({ 'message': 'Se necesita de un titulo y una fecha'}), 400
        
        # Crea una nueva instancia de Citas
        new_citas = Citas(titulo=titulo, hora=hora, fecha=fecha)
        
        # Añade la cita a la lista de citas del usuario
        user.citas.append(new_citas)
        
        # Añade los cambios a la base de datos
        db.session.add(new_citas)
        db.session.commit()
        
        return cita_schema.jsonify(new_citas), 201
    
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@ruta_user.route('/gusercitas/<int:user_id>', methods=['GET'])
def get_citas_from_user(user_id):
    try:
        # Verifica que el usuario exista
        if not user_id.isdigit():
            return jsonify({ 'message': 'ID es requerida' }), 400
        user = Users.query.get(user_id)
        if user is None:
            return jsonify({ 'message': 'Este usuario no existe' }), 404
        
        # Filtra un usuario por la id
        result = Citas.session.query.filter_by(usuario_id=user_id)
        data = {}
        
        # Itera sobre los resultados y los devuelve en formato JSON
        i=0
        for cita in result:
            i+=1
            data[i] = {
                'titulo': cita.titulo,
                'fecha': cita.fecha,
                'hora': cita.hora
            }
            
        return jsonify(data)
    except Exception as e:
        return jsonify({ 'message': str(e)}), 500