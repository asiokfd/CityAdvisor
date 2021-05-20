import random
from .config import db
import pandas as pd
from .testdata import  lista_sub
from .mongo import query_rnmedia, query_rbmedia, colecciones, list_categories









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
    función que crea un dataframe con la cantidad de documentos de cada subcategoria para una colección aleatoria realizando querys para cada
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



def grafica_items(lista, items):
    """
    funcion que recibe como parámetros dos listas acotadas previamente con nuestras colecciones e items a mostrar, recorre ambas listas para
    mediante una consulta a la base de datos, retornar un dataframe con la cantidad de items para cada colección seleccionada
    """
    df= pd.DataFrame (index=lista)
    list_=[]
    for item in items:
        
        
        lista2=[]
        for i in lista:
            i= str(i)
            a=list (db[i].find ({"subcategoria": item},{ item :1, "_id":0}))
            cantidad= len (a)
            lista2.append (cantidad)
            
        df[item]=lista2
    
    return df

def grafica_cat2(lista):
    """
    función que recibe como parámetro una lista previamente acotada con nuestras colecciones y devuelve un dataframe con el total de documentos
    por categorias
    """
    df= pd.DataFrame (index=lista)
    list_=[]
    for cat in list_categories(lista[1]):
        
        
        lista2=[]
        for item in lista:
            item= str(item)
            a=list (db[item].find ({"categoria": cat},{ item :1, "_id":0}))
            cantidad= len (a)
            lista2.append (cantidad)
        df[cat]=lista2
     
    return df

def porcentajes (lista):
    """
    Función que recibe como parámetro una lista previamente acotada con nuestras colecciones y devuelve un dataframe con los porcentajes
    relativos de cada categoria sobre el total
    """

    df=grafica_cat2 (lista) # la anterior
    suma=[]
    for n in range (len (df)):
        suma.append (df.iloc[n].sum()) 
    df["total elementos"]= suma # creamos una columna con el sumativo
    for col in df.columns:
        if df[col].sum() == 0:
            df.drop([col], axis=1, inplace=True)
        else:
            df[col]=df[col]/df["total elementos"]*100 # la utilizamos para sacar el porcentaje
    df.drop (["total elementos"], axis=1, inplace=True) # y la desechamos
    
    return df

def grafica_renta(lista):
    """
    función que recibe una lista de colecciones y devuelve un dataframe con sus renta obtenida mediante una consulta
    """
    list_=[]
    lista2=[]
    for item in lista:
        
        rentaneta = query_rnmedia (str (item))
        rentabruta = query_rbmedia (str(item))
        list_.append ( { "Renta Disponible" : rentaneta} )
        lista2.append (rentabruta)
    df=pd.DataFrame (list_)
    df["Renta Bruta"]=lista2  
    df.index= lista
    return df 

def grafica_renta_cats(lista):
    """
    función que recibe una lista de colecciones y devuelve un dataframe con la renta y las categorias, en este caso la renta la multiplico
    por 3 para una mejor visualización. Se ordena por renta bruta para una mejor visualización. Lo que me interesa es la línea y su forma
    """
    df= porcentajes (lista)
    df2= grafica_renta(lista)
    df["Renta Disponible"] = df2[["Renta Disponible"]]
    df["Renta Bruta"] = df2[["Renta Bruta"]]
    df["Renta Disponible"]= df["Renta Disponible"].apply (lambda x: x*3)
    df["Renta Bruta"]= df["Renta Bruta"].apply (lambda x: x*3)
    df.sort_values ("Renta Bruta", ascending=False, inplace=True) # al ser número no vale para nada esto
    return df