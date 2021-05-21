from .testdata import test, validar_codigo, get_primary
import pandas as pd
from .config import db, client, dic_categorias, gmaps
from selenium import webdriver
import time
from time import sleep
from selenium.webdriver.common.keys import Keys






def test_and_create(cp): 
    """ 
        Esta función recibo dos inputs del usuario, los utiliza para hacer una geolozalización mediante la api de google places, de la que
        obtengo sus coordenadas, que guardamos en 2 formatos, y la dirección, que usaremos como nombre para las colecciones. Meto las variables
        que me interesan en un diccionario, compruebo que la colección no exista por el nombre, si no existe la creo y cómo salida llamámos a
        otra función pasándole el diccionario y el nombre de la colección
    """
    #Validamos el input
    nombre = validar_codigo(cp)
    rentacodigo= new_func()
    #Comprobamos que no esté creada
    if test(nombre):
        return nombre
        
    #Definimos coordenadas
    coords=gmaps.geocode( address= cp, region="ES")
    a=coords[0]["geometry"]["location"]["lat"] 
    b=coords[0]["geometry"]["location"]["lng"]
    c = str (a) +"," + str(b) # Formato que luego entienda foursquare
    
    #Renta
    renta_neta=0
    renta_bruta=0
    
    for n in range (len(rentacodigo)):
        if rentacodigo["codigo postal"][n] == str(nombre):
                renta_neta += rentacodigo["renta disponible media"][n]
                renta_bruta += rentacodigo["renta bruta media"][n]
        else:
            print("El código postal no se encuentra en el df")
        
        #Creamos el diccionario
        dic= {          "nombre": nombre,
                        "coordenadas": c,
                        "latitud":a,
                        "longitud":b,
                        "renta bruta": renta_bruta,
                        "renta neta": renta_neta}
    
    #Creamos la colección
    db.create_collection (str(nombre))   
    
        
    return  get_coords (nombre, dic)


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
    
   
    for categoria, codigo in dic_categorias.items():
        try:  # recorremos diccionario, y para cada key, una consulta
            request = client.venues.search(params = {'query': codigo , 'll': coord, "radius": 800, "limit": 50})
            lista=request["venues"]

        except: # si nos quedamos sin peticiones a foursuare, retornamos error q se printeará, y borramos la colección, que se habrá creado
                # y habrá incluido algunos resultados
            db[collection].drop()
            return "[ERROR: EN ESTE MOMENTO NO PODEMOS PROCESAR SU SOLICITUD]"

        
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




def new_func():
    """
    función que importa un csv y lo convierte en Dataframe, el tipo de los datos es int, y en el importado se pierden los "0" a la izuierda
    que son necesarios en un código postal, así que los agregamos con un lambda. Devuelve el dataframe corregido

    """
    rentacodigo = pd.read_csv ("./Data/rentaporcp.csv")
    rentacodigo['codigo postal'] = rentacodigo['codigo postal'].apply(lambda x: "0" + str(x) if len(str(x))==4 else str(x))
    return rentacodigo


def fill_db (lista):
    """
    Función que recibe como parámetro una lista de códigos postales, y mediante el uso de selenium los introduce en la base de datos
    """
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.get ("http://localhost:8501/")
    for item in lista:
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div/section/div/div[1]/div[6]/div/div[1]/div/input").send_keys(item)
        driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/div/section/div/div[1]/div[6]/div/div[1]/div/input").send_keys(Keys.ENTER)
        time.sleep(15) #damos tiempo a que se metan los datos
        driver.refresh() #y refrescamos para vaciar el campo
        time.sleep(420) 