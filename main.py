import streamlit as st
from PIL import Image
import src.managedata as dat
import plotly.express as px
import pandas as pd
from streamlit_folium import folium_static
import codecs
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


st.write(""" Bienvenidos a CityAdvisor! Tu comparador urbano!

""")

col1,col2 = st.beta_columns([3,2])
                                            
col1.dataframe (dat.grafica_intro())
col2.image (imagen2)
#

st.write("""
## Empecémos
""")


calle = st.text_input("¿Por dónde quieres empezar? Introduce una calle a continuación:")
if not calle:
   st.warning('Por favor, introduzca una calle')
   st.stop()

ciudad = st.text_input("Concretemos un poco más, ¿En qué ciudad quieres buscar?")
if not ciudad:
   st.warning('Por favor, introduzca la ciudad o región')
   st.stop()


ubicacion= dat.test_and_create (calle, ciudad)

st.write ("usted ha elegido:", ubicacion)

items = st.multiselect (

    "Ahora añade tus búsquedas", dat.lista_sub()
)
if not items:
   st.warning('Por favor, seleccione una categoría')
   st.stop()

mapa=dat.get_map (ubicacion, items)

if mapa is False:
    st.warning ("Lo sentimos, no hay nada que mostrar con su selección")
else:
    folium_static (mapa, width=900, height=600)


col1,col2 = st.beta_columns ([2,2])
col1.dataframe (dat.grafica_cat(ubicacion))
col1.subheader ("Totales por categoría" )
col2.bar_chart (dat.grafica_sub (ubicacion))
col2.subheader ("Totales por subcategoria")
