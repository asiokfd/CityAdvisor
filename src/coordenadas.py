from googlemaps import convert
import googlemaps
import pandas as pd
from dotenv import load_dotenv
import os
import foursquare


# separar según utilidad








def get_coordenadas (df,columna, columna2):
    """
    Función que recibe como parámetro un DataFrame y dos columnas (ciudad y pais) donde se encuentren nombres de ciudades y su pais, 
    y dá como salida el DataFrame con cuatro columnas nuevas con la altitud y longitud en varios formatos
    
    La geocidificación se hace mediante la api de googleplace y la libreria gmaps, por lo que es necesario disponer de token
    y ya haberlo incluido en "gmaps"
    
    No recomendable con dataframes demasiado extensos por el número de request

    """
    

    tokg = os.getenv("tokg")
    gmaps = googlemaps.Client(key= tokg )
    latitudes=[]
    longitudes=[]
    coordenadas=[]
    coordenadas2=[]
    for i in range (len (df[columna])):
        busqueda= df[columna][i] + "," + df[columna2][i]
        
        coords = gmaps.geocode( address=busqueda, region="ES")
        longitudes.append (coords[0]["geometry"]["location"]["lng"])
        latitudes.append (coords[0]["geometry"]["location"]["lat"])
        coordenadas.append (coords[0]["geometry"]["location"])
        coordenadas2.append (coords[0]["geometry"]["location"].values())
    df["Lon"]= longitudes
    df["Lat"]= latitudes
    df["coords"] = coordenadas
    df["coords2"] = coordenadas2
    return df


def pasando_a_string (item):
        string_= str (item)
        recortando= string_[13:33]
        return recortando




def rellenando_datasetfsq (df, columna, query, rango, nueva, nueva2):
    """
    Parametros recibidos: 1 dataframe, nombre de una columna (ciudad), una query, en forma de codigo o texto, un rango de búsqueda 
    y dos nombres que le daremos a nuestras columnas.
    Función que, mediante la api de foursquare nos consigue una lista de items con la query y rango que hayamos dado y nos añade
    2 columnas, una con el número de items, y otra con el nombre, coordenadas y dirección en string del item.
    """
    tokf3 = os.getenv ("tokf3")
    client = foursquare.Foursquare( access_token= tokf3 )
    cantidad = []
    sublista = []
    
    for ciudad in df[columna] :
        
        request = client.venues.search(params = {'query': query , 'll': ciudad, "radius": rango, "limit": 50})
        lista = request["venues"]
        cantidad.append (len (lista))
        
        dic = {}
        for i in range ( len (lista)-1) :
            
            dic["name"] = lista[i]["name"]
            dic["latitud"] = lista[i]["location"]["lat"]
            dic["longitud"] = lista[i]["location"]["lng"]
            try:
                dic["direccion"]= lista[i]["location"]["formattedAddress"]
            except:
                pass
        sublista.append (dic)
        
    df[nueva]=cantidad
    df[nueva2] = sublista