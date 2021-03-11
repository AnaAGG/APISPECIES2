from flask import Flask, request, jsonify, render_template, redirect
from bson import json_util
from pymongo import MongoClient
from endpoints import species_, insert_data, species_month, species_province, delete_data, update_data , get_close, query_map, get_read_df, map_
from flask_pymongo import PyMongo
from functions import create_dict_insert, get_genus, get_date, get_coord, extract_info_form, extract_info_delete, extract_info_update, create_dict_update, extract_info_geo, create_dict_coord, get_info_class, get_info_sp, get_province_month, get_province_species
from json import JSONEncoder    
import pymongo
from flask_session import Session
from geojson import Point
from bson.json_util import dumps
import json
from MongoConnections import queries_maps
import markdown.extensions.fenced_code


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ironhack'
app.config['MONGO_DBNAME'] = 'final'
#app.config['MONGO_URI'] = 'mongodb://localhost:27017/final'
#mongo = PyMongo(app)

@app.route("/")
def home(): #aqui puedo meter como hacer las request a mi APIl.
    return render_template('home.html') #meter aqui htlm index.html

@app.route("/about")
def about(): #aqui puedo meter como hacer las request a mi APIl.
    return render_template('about.html')

@app.route("/province", methods = ["POST", "GET"]) #me devuelve las especies para toda una localidad
def data():    
    if request.method== "POST":
        province = request.form.get("mycheckbox")
        query = {'province':{'$regex': f'{province}', "$options" :'i'}}
        return json_util.dumps(species_(query, province))    
    return render_template("read_province.html")


@app.route("/province/comun", methods = ["POST", "GET"]) #me devuelve las especies para determinada localidad
def species_province_test():
    if request.method == "POST":
        dict_ = get_province_species ()
        return json_util.dumps(species_province(dict_))
    return render_template("read_species_province.html")


@app.route("/province/month", methods = ["POST", "GET"]) #me devuelve las especies para determinado mes
def species_month_test():
    if request.method == "POST":
        dict_ = get_province_month()
        return json_util.dumps(species_month(dict_))
    return render_template("read_province_month.html")

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST': 
        locality, common_name, species, date, class_ = extract_info_form("location", "vernacularname", "scientificname", "Date", "class_" )
        d = create_dict_insert(locality, date,  locality, common_name, species, class_ )
        return (insert_data(d, 'species'))     
    return render_template('insert_intro.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST': 
        d = extract_info_delete("Species_Id")
        return (delete_data(d, 'species'))  
    return render_template('delete_intro.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        id, locality, common_name, species, class_, month, year = extract_info_update("_id", "location", "vernacularname", "scientificname", "class_", "month", "year")
        up = create_dict_update (id, locality, common_name, species, class_, month, year)
        return(update_data(up, "species"))
    return render_template('update_to_change.html')

@app.route('/look', methods=['GET', 'POST'])
def look():
    if request.method == "POST":
        location = extract_info_geo("location")
        q = create_dict_coord(location)
        return str(get_close(q, "species")) 
    return render_template('queries.html')

@app.route('/map')
def get_class():
    return render_template("form_map.html")

@app.route('/map', methods=['GET', 'POST'])
def maps():
    if request.method == "POST":
        class_ = get_info_class()
        df = get_read_df(class_)
        map_(df, class_)
    return render_template("index.html")
app.run(debug=True)

'''
@app.route('/map/pred')
def get_sp():
    return render_template("form_map_pred.html")

@app.route('/map/pred', methods=['GET', 'POST'])
def map_preds():
    if request.method == "POST":
        sp = get_info_sp()
        df = get_sp_df(sp)
        get_map_pred(df)
    return render_template("index.html")
'''
