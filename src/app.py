from bson import ObjectId
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["MONGO_URI"] =os.getenv("MONGO_URI")

mongo = PyMongo(app)

app.config["MYSQL_HOST"] =os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] =os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] =os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] =os.getenv("MYSQL_DB")
app.config["SECRET_KEY"] =os.getenv("SECRET_KEY")

db = MySQL(app)


#################################################################
#CONSULTAS CON MYSQL
#################################################################

@app.route('/users_mysql', methods=['POST'])
def add_users_mysql():
    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    ciudad = request.json["ciudad"]
    pais = request.json["pais"]
    
    print(nombre,apellido, ciudad, pais)

    if nombre and apellido and ciudad and pais:

        cur = db.connection.cursor()
        sql=("INSERT INTO users (nombre, apellido,ciudad, pais) VALUES (%s,%s,%s,%s)")
        cur.execute(sql,(nombre,apellido,ciudad,pais))
        db.connection.commit()

        return jsonify({"message": "Usuario añadido con éxito"})
    
    return jsonify({"message": "Rellena todos los campos"})


@app.route('/')
def get_users_mysql():

    cur = db.connection.cursor()  

    cur.execute("SELECT * FROM users")

    users = cur.fetchall()  
    return jsonify({"Estos son todos los usuarios de la base de datos": users})

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    
    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    ciudad = request.json["ciudad"]
    pais = request.json["pais"]

    if nombre and apellido and ciudad and pais:

        cur = db.connection.cursor()
        sql = ("UPDATE users SET nombre = %s, apellido = %s, ciudad = %s, pais =%s WHERE id= %s")
        cur.execute(sql,(nombre,apellido, ciudad, pais,id))
        db.connection.commit()


        return jsonify({"message": "Usuario modificado con éxito"})
    
    return jsonify({"message": "Usuario modificado con éxito"})


@app.route('/delete_mysql/<id>', methods=['DELETE'])
def delete_user_mysl(id):

    cur = db.connection.cursor()

    sql = ("DELETE FROM users WHERE id= %s")

    cur.execute(sql,(id,))

    db.connection.commit()

    return jsonify({"message": "Usuario eliminado con éxito"})


#################################################################
#CONSULTAS CON MONGODB
#################################################################

@app.route('/users_mongo', methods=['POST'])
def add_users_mongo():
    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    ciudad = request.json["ciudad"]
    pais = request.json["pais"]
    
    print(nombre,apellido, ciudad, pais)

    if nombre and apellido and ciudad and pais:

        mongo.db.users.insert_one({"nombre":nombre, "apellido":apellido, "ciudad":ciudad, "pais":pais})

        return jsonify({"message": "Usuario añadido con éxito"})
    
    return jsonify({"message": "Rellena todos los campos"})


@app.route('/users_mongo')
def get_users_mongo():
    users = mongo.db.users.find()

    return jsonify({"Estos son todos los usuarios de esta base de datos": users})

@app.route('/update_mongo/<id>', methods=['PUT'])
def update_users_mongo(id):

    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    ciudad = request.json["ciudad"]
    pais = request.json["pais"]
    
    print(nombre,apellido, ciudad, pais)

    if nombre and apellido and ciudad and pais:

        mongo.db.users.update_one({"_id":ObjectId(id)}, {"$set":{"nombre":nombre, "apellido":apellido, "ciudad":ciudad,"pais":pais}})

        return jsonify({"message": "Usuario modificado con éxito"})

    return jsonify({"message":"Rellena todos los usuarios"})


@app.route('/delete_mongo/<id>', methods=['DELETE'])
def delete_users_mongo(id):
    
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Usuario eliminado con exito"})

if __name__ == '__main__':
    app.run(debug=True)


