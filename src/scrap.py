from selenium import webdriver
import pandas as pd



def get_df ( body):
    """
    función que recibe el body de una tabla de hml en forma de response de selenium, y nos devuelve un dataframe con los datos de la tabla
    """
    tabladatos=[]
    for dato in body.find_elements_by_tag_name("tr"):
        fila=[d for d in dato.find_elements_by_tag_name ("td")]
        if len (fila)>1 :
            fila= {
                "codigo postal": fila[0].text,
                "renta bruta media": fila[1].text,
                "renta disponible media": fila[2].text
                }
            tabladatos.append (fila)
    df=  pd.DataFrame (tabladatos)
    return df

def limpia_codigo (a):
    return a[:5]