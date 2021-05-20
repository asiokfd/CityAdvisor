import streamlit as st
from PIL import Image
import src.managedata as dat
import plotly.express as px
import pandas as pd
from streamlit_folium import folium_static
import streamlit.components.v1 as components


st.set_page_config(layout="wide", page_title = "CityAdvisor")

st.write("""
# Welcome to City Advisor
""")


col1,col2 = st.beta_columns([2,3])
imagen = Image.open("images/portada2.jpg")
imagen2= Image.open("images/portada.jpg")
col1.image(imagen)
col2.bar_chart (dat.grafica_intro2())


st.write(""" Bienvenidos a CityAdvisor! comparando códisgos postales desde 2021!

""")

col1,col2 = st.beta_columns([3,2])
                                            
col1.dataframe (dat.grafica_intro())
col2.image (imagen2)


st.write("""
## Empecémos
""")


lista= st.multiselect (" Haz tu selección:", dat.colecciones())
if not lista:
   st.warning('Por favor, seleccione algún elemento')
   st.stop()
cp=st.text_input ("si no encuentras lo que buscas, creemoslo: Introduce un codigo postal")
if cp:
    ubicacion= dat.test_and_create (cp)
    st.write ("El primer codigo postal es:", ubicacion)


items = st.multiselect (

    "Ahora añade tus búsquedas", dat.lista_sub()
)
if not items:
   st.warning('Por favor, seleccione una categoría')
   st.stop()


# mapa2=folium_static (dat.get_map (ubicacion2, items))
#if mapa is False:
 #   st.warning ("Lo sentimos, no hay nada que mostrar para el primer resultado")
#
#elif mapa2 is False:
 #   st.warning ("lo sentimos, no hay nada que mostrar para su segundo resultado")    
#else:
 #   st.write ("estamos preparando sus resultados")

col1,col2 = st.beta_columns([3,2])
col1.header ("cantidad de elementos seleccionados" )                                           
col1.dataframe (dat.grafica_items(lista, items))
col2.header ("Rentas según Codigo postal")
col2.bar_chart (dat.grafica_renta(lista))


st.dataframe (dat.grafica_cat2(lista))
st.write ( "0:desconocido, 1: Infraestructura transporte, 2: Comercio, 3: Infraestructura sanidad, 4: Ocio y Restauración, 5: Ocio y cultura, 6: Ocio y deporte, 7: Infraestructuras educacion")



#col1 (mapa)
#col2 (asiokfd)

st.write ("si quieres, vemos algunos sitios más concretos")

ubicacion= str (st.selectbox (" Vamos a verlo en el mapa", dat.colecciones()))

mapa=folium_static (dat.get_map (ubicacion, items))