import pandas as pd
from geopy.geocoders import Nominatim
from sklearn.cluster import AgglomerativeClustering, AffinityPropagation, KMeans, DBSCAN
from sklearn.metrics import silhouette_score

def reader(csv, name):
    '''
    Read the CSV of the climate variables that we will use for 
    the clustering model
    
    Receive:
        - Csv and the 
        - Name (string) of the climate variable.
    Returns:
        Dataframe cleaned
    '''
    d = pd.read_csv(csv)
    d.drop(["FID", "POINTID"], axis = 1, inplace = True)
    d.columns = [f"{name}", "lon", "lat"]
    d = d.round(3) #redondear los decimales a 3
    return d

def get_community(x):
    '''
    Extract the community of given coordinates.
    Receive:
        Column from the dataframe
    Returns:
        The community information for each of the coordinates of the dataframe
    '''
    locator = Nominatim(user_agent="myGeocoder", timeout=10)
    location = locator.reverse(x)
    data = location.raw
    try:
        return data.get("address").get("state")
    
    except: 
        return "unknown"

def cv_silhouette_scorer(estimator, X):
    '''
    Function to generate different declustering models.
    Receives:
        The model you want to make.
        Predictor variables to make the model predictions.

    Returns:
        The values ​​of the model and sil predictions
    '''
    try: 
        model = estimator(n_clusters = 5)
        model.fit(X)
    except : 
        model = estimator()
    
    try: 
        y_pred = model.predict(X)
    except:
        y_pred = model.fit_predict(X) # silhouette_score for Aggloemrative
    sil =  silhouette_score(X, y_pred)
    return y_pred , f"The silhouette_score for a '{estimator}' is: '{sil}'"

def remove_dummies(rwo):
    '''
    Reverts the variables that we convert to dummies.
    Receive:
        Dataframe
    Returns:
        Dataframe with the columns dummies and with all the original variables.
    '''
    for c in rwo.columns:
        if rwo[c]==1:
            return c

def cleaning_dataset_dummies(df):
    #genera un pandas Series
    remove = df.apply(remove_dummies, axis=1)
    #juntamos la pandas series con el dataframe original
    joins = pd.merge(df.reset_index(),
                  remove.reset_index(), 
                  left_index=True, 
                  right_index=True)
    #Para eliminar todas las columnas que contengan species_
    df = joins[joins.columns.drop(list(joins.filter(regex='community_')))]
    return df