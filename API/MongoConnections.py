from pymongo import MongoClient
from bson.json_util import dumps
import json
from flask import render_template


client = MongoClient()
db = client.final

#FUNCIÓN PARA INSERTAR DATOS

def insert(obj, coll, database = db):
    insert = db[coll].insert_one(obj)
    return insert
def read(query, project, coll, database = db):
    info = list(db[coll].find(query, project))
    return info

def delete(query, coll, database = db):
    deletion = db[coll].delete_one(query)
    return deletion

def update(query, coll, update, database = db):
    setting = {"push": update}
    update = db[coll].update_one(query, setting)
    return update

def queries_close(long, lat, coll):
    query = [{
    "$geoNear": {'near': [long, lat],
                 'distanceField': 'distance',
                 'maxDistance': 2000 , #2000 m de las coordenadas que le pasemos
                 'distanceMultiplier': 6371, 
                 'spherical'  : True, 
                 '$num': 10}}, 
    {"$limit": 10}, 
    { '$project' : { 'locality' : 1 , 'province' : 1, 'common_name': 1, '_id': 0, 'distance': 1}}]
    try: # para que no me salte un error de que no pasan la ubicacion. 
        geoloc = db[coll].aggregate(query)
        response_json = json.loads(dumps(geoloc))
        return response_json
    except:
        return render_template('queries_error.html')


def queries_maps(coll , database = db):
    query = {}
    project = {}
    res = str(db[coll].find(query, project))
    return res

