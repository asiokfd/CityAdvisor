from .config import db



def query_rbmedia(ubicacion):
    """
    función que recibe una colección y devueve su renta bruta
    """
    a=  list (db[ubicacion]. find ({"coordenadas": {"$exists": True}},{"renta bruta":1,"renta neta" :1, "nombre":1,"_id":0}))
    return a[0]["renta bruta"]

def query_rnmedia(ubicacion):
    """
    función que recibe una colección y devueve su renta neta
    """
    a=  list (db[ubicacion]. find ({"coordenadas": {"$exists": True}},{"renta bruta":1,"renta neta" :1, "nombre":1,"_id":0}))
    return a[0]["renta neta"]

def colecciones():
    """
    Función que devuelve una lista con nuestras colecciones
    """
    return db.list_collection_names()

def list_categories (collection):
    return (list (db[collection].distinct("categoria")))

def lista_colecciones():
    return list (db.list_collection_names())




