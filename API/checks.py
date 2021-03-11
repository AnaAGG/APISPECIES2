from MongoConnections import insert, read, delete, update
from pymongo import MongoClient

client = MongoClient()
db = client.Test
coll = client.Test.name

def check_parameters(kwargs, mandatory):
    
    for inf in mandatory:
        if inf not in kwargs.keys():
            return False
    return True

def check_data(query, collection = coll):
    exist = read(query, {}, coll)
    if len(exist) > 0:
        return True
    else:
        return False

def check_form (obj):
    obj = {}
    any_empty_vals = bool(len(['' for x in obj.values() if not x]))

    if any_empty_vals:
        return True
    return False