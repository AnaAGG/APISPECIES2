from geopy.geocoders import Nominatim
from bson import json_util
from flask import request, jsonify
import calendar
from MongoConnections import insert
from bson import ObjectId


def get_coord(city): #para sacar la lat y log de la provincia que nos pasan
    try: 
        locator = Nominatim(user_agent="myGeocoder")
        location = locator.geocode(city)
        lat, lon = (round((location.latitude), 3), (round(location.longitude, 3)))
        return lat, lon
    except:
        lat = float('NaN')
        lon = float('NaN')
        return lat, lon #devuelve una tupla

def get_genus(sp): #nos devuelve el genero de una especie recibida en el form
    return sp.split(" ")[0]

def get_date (date): #sacamos el mes y el año de la fecha que nos pasan en el formulario dia/mes/año
    new = date.split("-")
    year = new[0]
    month = new[1]
    month = calendar.month_abbr[int(month)]
    return month, year

def create_dict_insert (city, date, locality, common_name, species, kingdom = "Animmalia" ):
    #creamos un diccionario del form recibido en insert
    lat, long = get_coord(city)
    month, year = get_date(date)
    genus = get_genus(species)
    dict_ = {}
    for i in ("kingdom", "lat", "long", "locality", "month", "year",   "genus", "common_name", "species"):
        dict_[i] = locals()[i]
    return dict_


def get_province_species (): #extraemos la informacion del formulario para el endpoint de provincia/common
    locality = request.form.get("province")
    species = request.form.get("species")
    dict_ = {}
    for i in ("locality", "species"):
        dict_[i] = locals()[i]
    print(dict_)
    return dict_

def get_province_month (): #extraemos la informacion del formulario para el endpoint de provincia/common
    locality = request.form.get("province")
    month = request.form.get("month")
    print(month)
    dict_ = {}
    for i in ("locality", "month"):
        dict_[i] = locals()[i]
    print(dict_)
    return dict_
    

def extract_info_form(location, vernacularname, scientificname, Date, class_ ):
    #Extraemos toda la informacion recibida del formulario del insert
        location = request.form.get(f"{location}")
        common_name = request.form.get(f"{vernacularname}")
        species = request.form.get(f"{scientificname}")
        date = request.form.get(f"{Date}")
        class_ = request.form.get(f"{class_}")

        return location, common_name, species, date, class_

def extract_info_update_id(Species_Id): # lo primero es que me tienen que decir que objeto de mi coleccion quieren cambiar
    #extraigo la informacion del form de actualizar datos
    _id = request.form.get(f'{Species_Id}')
    return _id

def create_dict_update (_id, locality, common_name, species, class_, month, year, kingdom = "Animmalia" ):
    #extraigo la informacion de las coordenadas de la localidad que nos pasan. Provincia = lat, long
    lat, long = get_coord(locality)
    genus = get_genus(species)
    dict_ = {}
    #creo un diccionario con los datos del form
    for i in ("_id" , "lat", "long", "locality", "genus", "common_name", "species", "kingdom", "month", "year" ):
        dict_[i] = locals()[i]
    #Pero puede haber campos vacios que hagan que campos que estan en mi vase de datos se reemplacen por nada. Para evitarlo elimino todas las k, v que estan vacias 
    dict_2 = dict(x for x in dict_.items() if any(x)) #esto no me esta funcionando
    print(dict_2)
    return dict_2

def extract_info_update(_Id, location, vernacularname, scientificname, class_, month, year):
    n_id = request.form.get(f'{_Id}')
    location = request.form.get(f'{location}')
    common_name = request.form.get(f'{vernacularname}')
    species = request.form.get(f'{scientificname}')
    class_ = request.form.get(f'{class_}')
    month = request.form.get(f'{month}')
    year = request.form.get(f'{year}')
    print(n_id)
    return n_id, location, common_name, species, class_, month, year

def extract_info_delete(Species_Id):
    #extraigo la informacion del form de eliminar 
    _id = request.form.get(f'{Species_Id}')
    return _id

def extract_info_geo(location):
    #para exrtaer la informacion de la localidad que se crea en el formulario de buscar por provincia
    location = request.form.get(f'{location}')
    print(location)
    return location

def create_dict_coord (location ):
    lat, long = get_coord(location)
    dict_ = {}
    #creo un diccionario con los datos del form
    for i in ("lat", "long" ):
        dict_[i] = locals()[i]
 
    dict_2 = dict(x for x in dict_.items() if any(x)) 
    return dict_2

def get_info_class(): #para el el mapa de calor. Nos pasaran la clase para poder sacar una de las clases ploteadas
    class_ = request.form.get("class_")
    return class_


def get_info_sp(): #para el el de clusters. Nos pasaran la sp para poder sacar una de las clases ploteadas
    class_ = request.form.get("species")
    return class_