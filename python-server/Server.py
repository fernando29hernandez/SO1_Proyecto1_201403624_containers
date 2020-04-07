#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis
from typing import List, Dict  # import del manejo de listas
from flask import Flask  # import para el funcionamiento general de flask
import json  # import para el manejo de variables tipo json
from flask import render_template ## Import encargado de renderizar las templates 
from flask_cors import CORS

app = Flask(__name__)  # creacion de la app en python de flask
CORS(app)
# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""

def datos():
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True,db=0)
    valores = []
    keys = r.keys('*')
    for key in keys:
        type = r.type(key)
        if type == "string":
            val = r.get(key)
            valores.append(val)
        if type == "hash":
            vals = r.hgetall(key)
        if type == "zset":
            vals = r.zrange(key, 0, -1)
        if type == "list":
            vals = r.lrange(key, 0, -1)
        if type == "set":
            vals = r. smembers(key)
    return valores
# FUNCION de tipo get para mostrar los datos de la BD
@app.route('/')
def index():
    return render_template("index.html", results=datos())

@app.route('/memoria')
@crossdomain(origin='*',headers=['access-control-allow-origin','Content-Type'])
def memoria():
    temporal = datos()
    dato_ultimo = temporal[-1]
    response = {'memoria': dato_ultimo}
    return jsonify(response)

if __name__ == '__main__':
    # comando para configurar la ip del servicio
    app.run(host='0.0.0.0')
