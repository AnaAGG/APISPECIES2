# -To-see-species-SpeciesAPI
![portada](https://res.cloudinary.com/seana20/image/upload/v1615335723/API_Final%20Proyect/38-380743_bird-spring-flowers-colorful-forces-nature-colors-birds_otvpjn.jpg)

# Repository structure
> 1- Extract the data information from the GBIF 's API  
> 2 - Create the collection in [MongoDB Compass](https://www.mongodb.com/try/download/compass)   
> 3 - Create de API  
> 4 - Perform a CLustering Anlysis
> 5 - Plot some results

`API folder`  
`Notebooks folder`  
`Output folder`: contains all the data files that have been generated throughout the project  
`Images folders`
# Collection data

To store all the date we used a MongaDBCompass. The database is made up of one collection that will receive or give the information through the API. Next I show a table of the information contained in the database and how the codes that you will receive when you make the requests

| API information          | Name in request   | 
|---------------|---------|
| Latitude      | Lat     |
| Longitude      | Long   | 
| Vernacule name     | common_name   | 
| Latin name   | species   | 
| Kingdom| kingdom  | 
| Class   | class |
| Family    |family|  
| Genus     |   genus      |
| Locality     |   location      |
| Province     |   province      |
| Autonomous Community     | community   |
|||

# API description

QuoteAPI is an API to collect famous quotes from different authors throughout history. This API will collect citations from different disciplines which form the basis of the API structure and therefore of the database in mongo.


## Endpoints Structure

> *"/province"* --> GET method. To obtain all the information about locality. All the species that you can see in this location

> *"/province/comun* --> GET method. To obtain all the species that you can find in a given locality

> *"/province/month"* --> GET method. To obtain all the species that you can find in a given month

> *"/insert"* --> POST method. to insert new species. Where it is mandatory that you indicate the location where you are (the name of town or city, the common name of the species, the scientific name, which class it belongs to and the date.

> *"/delete"* --> POST method. Delete a given data. It is mandatory to introduce the _id

> *"/look"* --> POST method. GET method. Returns the 10 localities closest to yo for see any species. 

> *"/map"* --> GET-POST method. returns a heatmap for a given taoxomic group. 

### Some examples of API calls:

To read all the species of a given province
```python: 
("http://127.0.0.1:5000/province")

Returns: 
[{'_id': '6044ec0734b38296f136b6af'},
{'locality': 'Acantilados Jarama'},
{'species': 'Fringilla coeleb'},
{'common_name': 'Common Chaffinch'}]
```

To read information for a given species in a specific province
```python: 
("http://127.0.0.1:5000/province/comun")

Returns:

[{'_id': '6044ec0734b38296f136b6b9'},
{'locality': 'Embalse de Pinilla'},
{'species': 'Podiceps cristatus'},
{'common_name': 'Somormujo lavanco'}]
```
To read infomation for a given species in a specific month
```python: 
("http://127.0.0.1:5000/province/month")
Returns: 
[{"_id": {"$oid": "6049058ec744a637acfeca3f"},
"locality": "Acantilados Jarama",
"species": "Fringilla coelebs", 
"common_name": "Common Chaffinch"}]
```
# Some results

This graph shows the number of data that has been added to the database by years for each of the classes of animals in the API. In general, it is observed that over the years more species have been added to our database, with the exception of Birds, which has decreased over the years.

![species](https://github.com/AnaAGG/To-see-species-SpeciesAPI/blob/main/Images/species_class.png)


The following figures show a characterization of the main predictor variables (maximum temperature, minimum temperature, elevation and precipitation) of the physical conditions for each of the localities that we include in the database.

> Maximum temperature
![temp_max](https://github.com/AnaAGG/APISPECIES2/blob/main/Images/max_temp.png)  
> Minimum temperature
![temp_min](https://github.com/AnaAGG/APISPECIES2/blob/main/Images/min_temp.png)  
> Elevation
![elevation](https://github.com/AnaAGG/APISPECIES2/blob/main/Images/elevation.png)  
> Precipitation
![precip](https://github.com/AnaAGG/APISPECIES2/blob/main/Images/precip.png)  
### Requirements to replicate the methodology
> requirements.txt