import calendar
import requests
import pandas as pd
from tqdm import tqdm
from time import sleep
from pygbif import species
from pygbif import occurrences as occ
from EcoNameTranslator import to_common
from geopy.geocoders import Nominatim

def get_species_name_from_codes(splist):
    '''
    Receive a list o scientific names to extract the GBIF codes
    
    Args:
        splist(list) the list of target species    
    
    Returns
        Dictionary with the scientific name and their GBIF codes.
        List with the specific codes
    '''
    keys = [species.name_backbone(x)['usageKey'] for x in splist ]
    species_codes = dict(zip(splist, keys))
    sp_list = list(species_codes.values())
    return species_codes, sp_list   
def get_coordinates (sp):
    '''
    Extracts the taxonomic information of each species and the coordinates for each one of them.
    Args:
        List with the codes of the species that we want to download from the database
    Returns: 
        Dataframe with 11 columns: long, lat, locality, year, month, kingdom, class, family, genus,
        species, common_name
    '''
    
    long, lat, month, year_list, kingdom, class_, family, genus, species_, verna, locality  = [], [], [], [], [], [], [], [], [], [], []
   
    
    years = range(2000, 2021)

    for year in years:
        data = occ.search(taxonKey = sp, country = 'ES', year = str(year))
    
        for i in data["results"]:
            month.append(i.get("month"))            
            long.append(i.get("decimalLongitude"))
            lat.append(i.get("decimalLatitude")) 
            year_list.append(i.get("year"))
            species_.append(i.get("scientificName"))
            kingdom.append(i.get("kingdom")) 
            genus.append(i.get("genus"))
            family.append(i.get("family"))
            class_.append(i.get("class"))
            verna.append(i.get("vernacularName"))
            locality.append(i.get("locality"))
        
     
                
    df = pd.DataFrame(list(zip(long, lat, locality, year_list, month, kingdom, class_, family, genus,  species_, verna)),
                      columns=['long','lat', "locality", "year", "month", "kingdom", "class", "family", "genus", "species", "common_name"])
       

    return df
def get_common_names (coll):
    '''
    From the GBIF data, some common names come in Spanish. To unify the names I put them all in English.
    Args:
        A column from the dataframe

    Returns
        Dataframe with a column "common_name" with the common names of each species in English
    '''
    try:
        common_names = to_common([coll]) 
        common_names
        for i in common_names:
            for j in i[1]:
                x = ((i[1][0]))
        return x
    except: 
        return "Este imposible"

def clean (df, col):
    
    df.dropna(axis=0, how="any", inplace=True)
    df.round(3)
    
    #clean the species column
    f = lambda x: x[col].split(" ")[:2]
    df[col] = df.apply(f, axis=1)
    df[col] = df[col].str.join(' ')
    
    #get localities
    #locator = Nominatim(user_agent="myGeocoder") 
    #df["localities"] = df.apply(lambda x: locator.reverse(x.lat, x.lon), axis = 1)
    
    #round the long and lat columns:
    df.lat = df.lat.round(3)
    df.long = df.long.round(3)
       
    #convert numbers to month name
    df['month'] = df['month'].apply(lambda x: calendar.month_abbr[int(x)])
    
    #drop duplicate data
    df.drop_duplicates(df, inplace = True)
    return df


