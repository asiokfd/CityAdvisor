from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import MarkerCluster
import folium
from .config import db
import pandas as pd





def get_map (collection, items):
    """
    función que recibe como parámetro el nombre de una colección, y una lista con las categorias(items) que le interesen al usuario.
    Lo que hago es iterar por la lista para realizar una query para cada item con la colección dada, y nos quedamos con los datos que nos
    interesan para mostrar en un mapa. Si no tenemos nada para mostrar, devolvemos False ( usado en main como error handling), y en caso 
    de tener elementos para mostrar, creamos un dataframe con los datos y llamamos a otra función pasándole el dataframe y el nombre de la
    colección
    """
    lista=[]
    for item in items:
        a=list (db[collection]. find ({"subcategoria": item},{"latitud":1,"nombre":1, "longitud":1, "categoria":1, "subcategoria":1, "_id":0}).limit(15))
        lista.append (a) # agregamos la respuesta para cada una de las querys, tantas como items nos hayan pasado.
    cosa=[]
    print (lista)
    for n in range (len(lista)):
        cosa+= lista[n] # homemade concat, suma las respuestas
    
    if len (cosa)==0:
        return False
    else:
        df=pd.DataFrame (cosa)
    return making_map (df, collection)



def making_map (df,collection):
    """
    Función que recibe un dataframe y el nombre de una colección
    Con la colección lo que hago es una query con el parámetro coordenadas ( que sabemos que solo tiene el documento "fundador") y me
    quedo con latitud y longitud, que usaré para crear un mapa con folium.
    después iteramos por el dataframe para conseguir las localizaciones y la categoría y marcarlas en el mapa
    su salida es un mapa de folium con las ubicaciones marcadas
    
    """
    
    a=list (db[collection]. find ({"coordenadas": {"$exists": True}},{"latitud":1,"longitud" :1, "nombre":1,"_id":0})) 
    
    lat=a[0]["latitud"]
    
    long=a[0]["longitud"]
    
    nombre= a[0]["nombre"]
    
    mapa = folium.Map(location= [lat, long], zoom_start= 15)
    
    for i, row in df.iterrows():
        
        marcador = {
            "location":[row["latitud"], row["longitud"]],
            "tooltip" : row["nombre"]
        }
    
        if row["categoria"] == "Comercio": #ok
            icon = Icon(color = "orange",
                    prefix = "fa",
                    icon = "shopping-cart",
                    icon_color = "blue"
                                            )         
        
        elif row["categoria"] == 'Infraestructura sanidad': #ok
            icon = Icon(color = "green",
                    prefix = "fa",
                    icon = "plus",
                    icon_color = "red"
                                            )
        elif row["categoria"] == 'Infraestructura transporte': #ok
            icon = Icon(color = "green",
                    prefix = "fa",
                    icon = "plane",
                    icon_color = "black"
                                            )                                    
        elif row["categoria"] == 'Infraestructuras educacion':
            icon = Icon(color = "green",
                    prefix = "fa",
                    icon = "pencil",
                    icon_color = "blue")
        elif row["categoria"] ==  'Ocio y Restauración': #ok
            icon = Icon(color = "blue",
                    prefix = "fa",
                    icon = "cutlery",
                    icon_color = "red"
                                      )      
        elif row["categoria"] == 'Ocio y cultura': #ok
            icon = Icon(color = "blue",
                    prefix = "fa",
                    icon = "book",
                    icon_color = "black"
                                            )
        else:
            icon = Icon(color = "blue",
                    prefix = "fa",
                    icon = "tower",
                    icon_color = "orange"
            )
        Marker(**marcador,icon = icon ).add_to(mapa)
    
    return mapa