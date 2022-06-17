from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
conexion = MySQL(app)

@app.route('/personas', methods=['GET'])
def listar_personas():
    try:
        cursor=conexion.connection.cursor()
        sql="select * from persona"
        cursor.execute(sql)
        datos=cursor.fetchall()
        personas=[]
        for fila in datos:
            persona={'id':fila[0], 'nombre':fila[1], 'apellido':fila[2], 'tel':fila[3]}
            personas.append(persona)
        return jsonify({'personas': personas, 'mensaje':'Lista de personas'})
    except Exception as e:
        return f'Error {e}'

@app.route('/personas/<id>', methods=['GET'])
def leer_persona(id):
    try:
        cursor=conexion.connection.cursor()
        sql = "select * from persona where id= {0}".format(id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            persona={'id':datos[0], 'nombre':datos[1], 'apellido':datos[2], 'tel':datos[3]}
            return jsonify({'persona': persona, 'mensaje':'Lista de personas'})
        else:
            return jsonify({'mensaje':'persona no encontrada'})
    except Exception as e:
        return f'Error {e}'

@app.route('/registro', methods=['POST'])
def registrar_persona():
    try:
        cursor=conexion.connection.cursor()
        nombre = request.json['nombre']
        apellido = request.json['apellido']
        tel = request.json['tel']
        valores = (nombre, apellido, tel)
        sql = 'INSERT INTO persona (nombre, apellido, tel) VALUES (%s, %s, %s)'
        cursor.execute(sql, valores)
        cursor.connection.commit()
        return jsonify({'mensaje':'Persona registrada!!!'})
    except Exception as e:
        return f'Error {e}'

@app.route('/actualizar/<id>', methods=['PUT'])
def actualizar_persona(id):
    try:
        cursor=conexion.connection.cursor()
        sql = "select * from persona where id= {0}".format(id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            nombre = request.json['nombre']
            apellido = request.json['apellido']
            tel = request.json['tel']
            id=id
            valores = (nombre, apellido, tel, id)
            sql = 'UPDATE persona  SET nombre = %s, apellido=%s, tel=%s where id=%s'
            cursor.execute(sql, valores)
            cursor.connection.commit()
            return jsonify({'mensaje':'Persona actualizada!!!'})
        else:
            return jsonify({'mensaje':'Persona no existe!!!'})
    except Exception as e:
        return f'Error {e}'

@app.route('/eliminar/<id>', methods=['DELETE'])
def eliminar_persona(id):
    try:
        cursor=conexion.connection.cursor()
        sql = "select * from persona where id= {0}".format(id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            valores = (id )
            sql = 'DELETE FROM persona WHERE id = %s'
            cursor.execute(sql,valores)
            cursor.connection.commit()
            return jsonify({'mensaje':'Persona eliminada!!!'})
        else:
            return jsonify({'mensaje':'Persona no existe!!!'})
    except Exception as e:
        return f'Error {e}'

def pag_notfound(error):
    return "<h1> Pagina no encontrada.... </h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pag_notfound)
    app.run()