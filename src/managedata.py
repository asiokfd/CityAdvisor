import pandas as pd
from dotenv import load_dotenv
from googlemaps import convert
import googlemaps
import os
import foursquare
from pymongo import MongoClient
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import MarkerCluster
import random
import Data

dic_categorias= { # diccionario que usaré para definir las subcategorias a buscar y a introducir en la db
#infraestructuras transporte
    "aeropuertos" : ["airport"],
    "estaciones de tren": ["train station", "renfe"],  
    "parques": ["park",],
    "estaciones de metro": ["metro", "subway station"],
    "estaciones de autobús": ["bus"],
    "carril bici": ["bike trail"],
# infraestructuras sanidad
    "hospitales" : ["hospital"],
    "clinicas": ["medical center", "clinic"],
    "farmacias": ["pharmacy", "farmacia"],
    "veterinario": ["veterinarian"],
#restauracion
    "restaurantes": ["restaurant"],
    "ocio_nocturno": ["pub","Cocktail Bar"],
    "hoteles": ["hotel"],
    "cafeterias": ["coffe"],
#ocio y cultura
    "cines": ["cinema", "movie theatre"],
    "teatros": ["theatre", "teatro"],
    "museos": ["museum"],
    "salas_de_conciertos": ["rock club", "concert"],
    "bibliotecas" : ["library", "biblioteca"], 
#ocio y deporte
    "ocio_deporte": ["gym", "Fitness"],
    "piscina": ["pool", "piscina"],
    "canchas": ["cancha", "court"],
    "estadios": ["stadium", "estadio"],
    
#infraestructuras educacion
    "colegios" : ["primary school", "elemental school"],
    "guarderias" : ["kindergarden", "guarderia"],
    "universidades": ["college", "university"],
    "Institutos" : ["secundary school", "bachiller"],
    "Escuelas" : ["school", "escuela"],
    
#comercio
    "centros_comerciales": ["mall", "shopping center"],
    "Tiendas minoristas" : ["shop", "tienda"]
    
                             }              
def new_func():
    rentacodigo = pd.read_csv ("../Data/rentaporcp.csv")
    return rentacodigo

rentacodigo = new_func() 


load_dotenv()
tokg = os.getenv("tokg")
tokf3 = os.getenv ("tokf3")
client2= MongoClient ("localhost:27017")

client = foursquare.Foursquare( access_token= tokf3 )
gmaps = googlemaps.Client(key= tokg )
db = client2.get_database("ciudades")

# todo lo anterior no está en config por problemas de importación.


def test_and_create( ubicacion, region):
    """ 
        Esta función recibo dos inputs del usuario, los utiliza para hacer una geolozalización mediante la api de google places, de la que
        obtengo sus coordenadas, que guardamos en 2 formatos, y la dirección, que usaremos como nombre para las colecciones. Meto las variables
        que me interesan en un diccionario, compruebo que la colección no exista por el nombre, si no existe la creo y cómo salida llamámos a
        otra función pasándole el diccionario y el nombre de la colección
    """
    try: 
        busqueda= ubicacion + ", " + region #unimos en un string para pasarselo como búsqueda a gplaces
        coords=gmaps.geocode( address= busqueda)
        nombre = coords[0]["address_components"][5]["short_name"] # nos quedamos con el nombre, que será el de la colección
        a=coords[0]["geometry"]["location"]["lat"] 
        b=coords[0]["geometry"]["location"]["lng"]
        c = str (a) +"," + str(b) # Formato que luego entienda foursquare
        
        for n in range (len (rentacodigo)):
            if rentacodigo["codigo postal"][n] == nombre:
                renta_neta= rentacodigo["renta disponible media"][n]
                renta_bruta= rentacodigo["renta bruta media"][n]
        else:
            pass
        
        dic= {"nombre": nombre,
                "coordenadas": c,
                 "latitud":a,
                 "longitud":b,
                "renta bruta": renta_bruta,
                 "renta neta": renta_neta}
            
        if test(nombre) == True:
            
            return (nombre)
        
        else:
            
            pass
        
            db.create_collection (nombre)   
    except: "los datos introducidos no son correctos"
        
    return  get_coords (nombre, dic)


def test (nombre):
    """
        Función que comprueba si la colleción existe, devuelve un booleano
    """
    lista= db.list_collection_names()
    return nombre in lista


def get_coords(nombre, dic):
    """
        Función que recibe como parámetro un diccionario y el nombre de una colección y crea el primer documento de la colección con los
        datos del diccionario. Su salida es otra llamada pasándo el nombre de la colección y uno de sus parámetros, las coordenadas.
    """
    collection= nombre 
    db[collection].insert_one (dic)
    coord= dic["coordenadas"]
    return get_data_fields (coord, collection)


def get_data_fields (coord, collection):
    """
    función que recibe unas coordenadas en string y el nombre de una colección, con esas coordendas hago request a la api de foursquare
    con las categorías de dic_categorias como consulta para conseguir una lista de diccionarios que insertaremos en nuestra colección.
    Devuelve el nombre de la colección
    """
    
   
    for categoria, codigo in dic_categorias.items():  # recorremos diccionario, y para cada key, una consulta
        request = client.venues.search(params = {'query': codigo , 'll': coord, "radius": 800, "limit": 50})
        lista=request["venues"]
        
        
        dice=[]
        for i in range (0,len (lista)): # recorremos las respuestas, y para cada una de ellas, creamos un diccionario con los parámetros
                                        # que nos interesan
            nombre = lista[i]["name"]
            latitud= lista[i]["location"]["lat"]
            longitud= lista[i]["location"]["lng"]
            try:
                tipo = lista[i]["categories"][0]["name"] # no todas tienen tipo
            except:
                tipo= "no definido"
            try:
                direccion= str (lista[i]["location"]["formattedAddress"])[2:-2]# ni dirección, aquí lo paso a string y le recorto [' de 
            except:                                                         #cada lado, porque pensaba usarlo para visualizar e iba a quedar feo
                direccion= "no disponible"
        
            dice2 = {"nombre": nombre,
                "categoria": get_primary(categoria),
                "subcategoria": categoria,
               "latitud":latitud,
               "longitud": longitud,
                "tipo" : tipo,
               "direccion":direccion }
            dice.append (dice2)          
        
        try:   # cuando dice está vacio, dá error, así lo obviamos.
            db[collection].insert_many (dice)
        except:
            pass
    
    return (collection)



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
    
        if row["categoria"] == "Festivo": #personalizar por categorias (7)
            icon = Icon(color = "green",
                    prefix = "fa",
                    icon = "glass",
                    icon_color = "black"
        )
        
        elif row["categoria"] == "Vispera":
            icon = Icon(color = "blue",
                    prefix = "fa",
                    icon = "home",
                    icon_color = "black"
        )
        
        else:
            icon = Icon(color = "red",
                    prefix = "fa",
                    icon = "briefcase",
                    icon_color = "black"
            )
        Marker(**marcador,icon = icon ).add_to(mapa)
    
    return mapa



def grafica_intro():
    """
    función que crea un dataframe con la cantidad de documentos de cada categoria para una colección aleatoria realizando querys para cada
    categoría y quedándose con el len
    """
  
    collection= random.choice (db.list_collection_names())
    lista=[]
    for item in list_categories(collection):
        a=list (db[collection].find ({"categoria": item},{ item :1, "_id":0}))
        cantidad= len (a)
        lista.append ( { collection : cantidad } )
    df=pd.DataFrame (lista, index=list_categories(collection))
    return df


def grafica_intro2():
    """
    función que crea un dataframe con la cantidad de documentos de cada categoria para una colección aleatoria realizando querys para cada
    categoría y quedándose con el len
    """
  
    collection= random.choice (db.list_collection_names())
    lista=[]
    for item in lista_sub():
        a=list (db[collection].find ({"subcategoria": item},{ item :1, "_id":0}))
        cantidad= len (a)
        lista.append ( { collection : cantidad } )
    df=pd.DataFrame (lista, index=lista_sub())
    return df

def grafica_sub(collection):
    """
    Clon del anterior, pero con una coleción definida
    """
  
    lista=[]
    for item in lista_sub():
        a=list (db[collection].find ({"subcategoria": item},{ item :1, "_id":0}))
        cantidad= len (a)
        lista.append ( { collection : cantidad } )
    df=pd.DataFrame (lista, index=lista_sub())
    return df

def grafica_cat(collection):
    """
    Clon del anterior, pero con una coleción definida
    """
  
    lista=[]
    for item in list_categories(collection):
        a=list (db[collection].find ({"categoria": item},{ item :1, "_id":0}))
        cantidad= len (a)           #pasar a metodo count
        lista.append ( { collection : cantidad } )
    df=pd.DataFrame (lista, index=list_categories(collection))
    return df

def list_categories (collection):
    return (list (db[collection].distinct("categoria")))

def lista_colecciones():
    return list (db.list_collection_names())
    

def lista_sub():
    c= list (dic_categorias.keys())
    return c


def get_primary (categoria):
    """
    Esta función recibe una categoria, y la compara con nuestro dic_categorias, según sea la categoría devuelve su categoría superior.
    para esto he agrupado las categorías por el indice
    """
    keys= list (dic_categorias.keys())
    cat1= keys[:6]
    cat2= keys[6:10]
    cat3= keys[10:14]
    cat4= keys [14:19]
    cat5= keys [19:23]
    cat6= keys [23:28]
    cat7= keys[-2:]
    
    if categoria in cat1:
        clase = "Infraestructura transporte"
        return clase
    elif categoria in cat2:
        clase= "Infraestructura sanidad"
        return clase
    elif categoria in cat3:
        clase= "Ocio y Restauración"
        return clase
    elif categoria in cat4:
        clase= "Ocio y cultura"
        return clase
    elif categoria in cat5:
        clase= "Ocio y deporte"
        return clase
    elif categoria in cat6:
        clase= "Infraestructuras educacion"
        return clase
    elif categoria in cat7:
        clase= "Comercio"
        return clase
    else:
        return "desconocido"




    


