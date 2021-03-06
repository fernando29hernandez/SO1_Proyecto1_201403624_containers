#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis
from typing import List, Dict  # import del manejo de listas
from flask import Flask  # import para el funcionamiento general de flask
import json  # import para el manejo de variables tipo json
from flask import render_template ## Import encargado de renderizar las templates 
from flask_cors import CORS, cross_origin
from flask import jsonify
app = Flask(__name__)  # creacion de la app en python de flask
CORS(app, resources={r"/*": {"origins": "*"}})
# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""
def datos1():
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True,db=1)
    valores =  []
    val = r.get("0")
    valores.append(val)
    val = r.get("1")
    valores.append(val)
    return valores

def datos():
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True,db=0)
    valores =  []
    val = r.get("0")
    valores.append(val)
    val = r.get("1")
    valores.append(val)
    return valores
# FUNCION de tipo get para mostrar los datos de la BD
@app.route('/')
@cross_origin()
def index():
    return render_template("index.html")

@app.route('/memoria')
@cross_origin()
def memoria():
    temporal = datos()
    dato_ultimo = temporal[0]
    dato_pen = temporal [1]
    print(dato_ultimo)
    temporal1 = datos1()
    dato_ultimo1 = temporal1[0]
    dato_pen1 = temporal1 [1]
    print(dato_ultimo1)
    response = {'memoria1': dato_ultimo,'memoria2':dato_pen,'cpu1':dato_ultimo1,'cpu2':dato_pen1}
    return jsonify(response)


if __name__ == '__main__':
    # comando para configurar la ip del servicio
    app.run(host='0.0.0.0')
