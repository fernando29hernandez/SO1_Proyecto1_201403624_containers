#!/usr/bin/env python3

# step 1: import the redis-py client package
import redis
from typing import List, Dict  # import del manejo de listas
from flask import Flask  # import para el funcionamiento general de flask
import mysql.connector  # import de conexion con mysql
import json  # import para el manejo de variables tipo json
from flask import render_template ## Import encargado de renderizar las templates 

app = Flask(__name__)  # creacion de la app en python de flask
# step 2: define our connection information for Redis
# Replaces with your configuration information
redis_host = "redis"
redis_port = 6379
redis_password = ""

def datos() -> List[Dict]:
    """Example Hello Redis Program"""
   
    # step 3: create the Redis Connection object
    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True,db=0)
    valores = []
    keys = redis.keys('*')
    for key in keys:
        type = redis.type(key)
        if type == "string":
            val = redis.get(key)
            valores.append(val)
        if type == "hash":
            vals = redis.hgetall(key)
        if type == "zset":
            vals = redis.zrange(key, 0, -1)
        if type == "list":
            vals = redis.lrange(key, 0, -1)
        if type == "set":
            vals = redis. smembers(key)
    return valores
# FUNCION de tipo get para mostrar los datos de la BD
@app.route('/')
def index():
    return render_template("index.html", results=datos())

if __name__ == '__main__':
    # comando para configurar la ip del servicio
    app.run(host='0.0.0.0')