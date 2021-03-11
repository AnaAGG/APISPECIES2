from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import geopandas as gdp
import shapely
import json
from bson.json_util import dumps


def create_collections(df): # to create one BBDD with multiple collections
    
    #get the different classes in teh dataframe
    classes = df["class"].unique()
    
    #subset the species dataset in different collections
    for i in classes:
    
        if i == "Aves":
            birds = df[df["class"] == "Aves"].to_dict(orient = "records")
        elif i == "Mammalia":
            mammals = df[df["class"] == "Mammalia"].to_dict(orient = "records")
        elif i == "Reptilia":
            reptilia = df[df["class"] == "Reptilia"].to_dict(orient = "records")
        elif i == "Actinopterygii":
            actinopterygii = df[df["class"] == "Actinopterygii"].to_dict(orient = "records")
        else:
            amphibia = df[df["class"] == "Amphibia"].to_dict(orient = "records")
    
    #conect with MongoDB
    client = MongoClient()
    db = client.Species
    
    #create the different collections
    try:
        db.Mammals.insert_many(mammals)
        db.Birds.insert_many(birds)
        db.Reptilia.insert_many(reptilia)
        db.Amphibia.insert_many(amphibia)
        db.Actinopterygii.insert_many(actinopterygii)
        return "Nice! There are new collections"
    except:
        return "Sorry something went wrong"


def create_geoloc(path_csv, nombre): # To create a DDBB with one collection ad geojson
    '''
    Receives a path and returns  a dataframe with a new column with the geopoints.
    Args:
        Path : of the csv file containing information about the coordinates and names of all information downloaded from the API
    
    Return:
        Dataframe: with one more column with the geopoints
    '''
    
    #recibe el dataframe
    df = pd.read_csv(path_csv, sep = ";")
    
    #Crea el loc con los geopuntos.
    gdf = gdp.GeoDataFrame(df, geometry= gdp.points_from_xy(df.long, df.lat ))
    gdf.columns=['long','lat','locality','province', 'year', 'month', 'kingdom', 'class', 'family', 'genus', 'species', 'common_name', 'loc' ]
    
    #Lo aplicamos a toda la columna
    gdf['loc']= gdf['loc'].apply(lambda x:shapely.geometry.mapping(x))
    
    #First
    client = MongoClient()
    db = client.final
    collection = db.create_collection(name = f"{nombre}")
    collection = db[f"{nombre}"]
    collection.create_index([("loc", "2dsphere")])

    data = gdf.to_dict(orient='records')
    collection.insert_many(data)
    return "Nice the collection has been created"