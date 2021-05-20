import pandas as pd
from dotenv import load_dotenv
import googlemaps
import os
from pymongo import MongoClient
import foursquare



load_dotenv()
tokg = os.getenv("tokg")
tokf3 = os.getenv ("tokf3")
client2= MongoClient ("localhost:27017")
db = client2.get_database("ciudades")
client = foursquare.Foursquare( access_token= tokf3 )
gmaps = googlemaps.Client(key= tokg )





dic_categorias= { # diccionario que usaré para definir las subcategorias a buscar y a introducir en la db
#infraestructuras transporte
    "aeropuertos" : ["aeropuerto"],
    "estaciones de tren": ["estacion de tren", "renfe"],  
    "parking": ["parking",],
    "estaciones de metro": ["metro"],
    "estaciones de autobús": ["bus","autobus"],
    "carril bici": ["bike trail", "carril bici"],
# infraestructuras sanidad
    "hospitales" : ["hospital", "centro de salud"],
    "clinicas": ["clinica", "dentista"],
    "farmacias": ["pharmacy", "farmacia"],
    "veterinario": ["veterinarian"],
#restauracion
    "restaurantes": ["restaurant", "restaurante"],
    "ocio_nocturno": ["pub","Bar"],
    "hoteles": ["hotel"],
    "cafeterias": ["coffe", "cafeteria"],
#ocio y cultura
    "cines": ["cine", "autocine"],
    "teatros": ["theatre", "teatro"],
    "museos": ["museum", "museo"],
    "salas_de_conciertos": ["sala de conciertos", "jazz club"],
    "bibliotecas" : ["library", "biblioteca"], 
#ocio y deporte
    "ocio_deporte": ["gym", "Fitness"],
    "piscina": ["pool", "piscina"],
    "canchas": ["cancha", "parque"],
    "estadios": ["stadium", "estadio"],
    
#infraestructuras educacion
    "colegios" : ["primary school", "colegio"],
    "guarderias" : ["jardin de infancia", "guarderia"],
    "universidades": ["universidad", "university"],
    "Institutos" : ["instituto", "educacion secundaria"],
    "Escuelas" : ["school", "escuela"],
    
#comercio
    "centros_comerciales": ["centro comercial", "shopping center"],
    "Tiendas minoristas" : ["estanco", "tienda"]
    
}                

