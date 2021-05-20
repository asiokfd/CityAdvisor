
import pgeocode
import numpy as np
from .config import db, dic_categorias, gmaps

def validar_codigo (cp):
    '''Esta función comprueba que el código postal devuevla una dirección y que tenga una longitud de 5'''
    
    coords=gmaps.geocode( address= cp, region="ES")
    nombre = coords[0]["address_components"][0]["short_name"]
    
    if type(nombre) == int and len(nombre)==5: 
        return nombre
    else:
        nomi = pgeocode.Nominatim("es") #la ubicación del CP no es uiforme respuestas de gplaces no son uniformes, 
        a = nomi.query_postal_code(cp)  # así que incluyo una alternativa
        if a["latitude"]==np.nan:
            return "Latitude es un NaN"
        else:
            nombre=a["postal_code"]
            if len(nombre)==5:
                return nombre



def test (nombre):
    """
        Función que comprueba si la colleción existe, devuelve un booleano
    """
    lista= db.list_collection_names()
    return nombre in lista


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



    

def lista_sub():
    c= list (dic_categorias.keys())
    return c