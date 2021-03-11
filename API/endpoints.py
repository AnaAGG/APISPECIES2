from MongoConnections import read, insert, delete, update, queries_close, queries_maps
from flask import jsonify, render_template
from bson import ObjectId
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import pandas as pd
import json
import os


def species_(query, location):
    res = read(query, {"locality": 1, "species":1, "common_name": 1, "_id":1}, "species")
    if len(res) < 1:
        return render_template("province_noexist.html")
    elif not location:
        return "{Sorry necesito una localizacion}"
    else:
        return res

def species_province(dict_ ): #esta funcion es para obtener todas las especies para una determinada epoca
    any_empty_vals = bool(len(['' for x in dict_.values() if not x]))
    query = {'$and': [{'province':dict_["locality"]}, {'species':dict_["species"]}]}
    res = read(query, {"locality": 1, "species":1, "common_name": 1, "_id":1}, "species")
    if any_empty_vals: #para chequear si nos pasan todas los parametros del formulario
        return render_template("read_species_month_error.html")
    elif len(res) == 0: # para chequear si hay en nuestra base de datos
        return render_template("read_province_month_not.html")
    else:
        return res

def species_month(dict_ ): #esta funcion es para obtener todas las especies para una determinada epoca
    any_empty_vals = bool(len(['' for x in dict_.values() if not x]))
    query = {'$and': [{'province':dict_["locality"]}, {'month':dict_["month"]}]}
    res = read(query, {"locality": 1, "species":1, "common_name": 1, "_id":1}, "species")
    if any_empty_vals:
        return render_template("read_species_month_error.html")
    elif len(res) == 0:
        return render_template("read_province_month_not.html")
    else:
        return res

def insert_data (dict_, coll):
    any_empty_vals = bool(len(['' for x in dict_.values() if not x]))
    query = {"$and": [{"locality": {'$regex' : dict_["locality"], "$options" :'i'}}, {"species": {'$regex' : dict_["species"], "$options" :'i'}}, {"month": {'$regex' : dict_["month"], "$options" :'i'}}]}
    exist = read(query, {}, coll)
    #check if all the parameters are passed
    if any_empty_vals:
        return render_template('insert_incomplete.html')
    elif len(exist) > 0:
        return render_template('insert_exists.html')
    else:
        insert(dict_, "species")
        return render_template('insert_success.html')

def delete_data (_id, coll):
    try: 
        query = {"_id":ObjectId(f'{_id}')}
        print(type(query))
    except:
        return render_template("delete_error_bson.html")
    exist = read(query, {}, coll)
    #check if all the parameters are passed
    if len(exist) == 0:
        return render_template('delete_noexist.html')
    else:
        delete(query, "species")
        return render_template('delete_success.html')


def update_data (dict_, coll):
    print(dict_)
    try: 
        query = {"_id":ObjectId(dict_["_id"])}
        print(query)
    except:
        return render_template("update_error_bson.html")
    exist = read(query, {}, coll)
    #check if all the parameters are passed
    if len(exist) == 0:
        return render_template('update_noexist.html')
    else:
        update(query, "species", dict_)

def get_close (dict_, coll):
    print(dict_)
    res = queries_close(dict_["long"], dict_["lat"], "species")
    for element in dict_.values():
        if isinstance(element, float):
            return res
        else:
            return "Lo siento me tienes que pasar unas coordenadas"
       
def query_map(): #esta funcion es para obtener todas las especies para una determinada epoca
    query = {}
    res = read(query, {"locality": 0, "common_name": 0, "_id":0}, "species")
    if len(res) < 1:
        return render_template("read_species_month_error.html")
    else:
        return res

def map_(df, class_): #para poder plotear el mapa

    initial_lat = 40.4146500
    initial_long = -3.7004000
    target = df[df["class"]== f'{class_}']
    print(type(target))
    print(target)
    m = folium.Map(location = [initial_lat, initial_long], tiles='CartoDB dark_matter',  zoom_start = 6)
    group = folium.FeatureGroup(name = f'{class_}')
    HeatMap(data=target[["lat","long"]],radius=15).add_to(group)
    group.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    m.save("API/templates/mapff.html")
     

def get_read_df(class_): #para convertir la query qu nos pasan para los mapas(es decir clase) en un dataframe y luego poder insertarlo en folium
    query = {"class": f"{class_}"}
    project = {"lat": 1, "long": 1, "class": 1, "species": 1, "_id": 0}
    res = list(read(query, project, "species"))
    # lo convierto a dataframe para luego poder meterlo en la funcion de folium
    df = pd.DataFrame(res, columns = ["long", "lat", "class", "species"])
    return df


