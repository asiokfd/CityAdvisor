import streamlit as st
from PIL import Image

import plotly.express as px
import pandas as pd
from streamlit_folium import folium_static
import src.dataframes as dat
import src.mongo as mdb
from src.maps import get_map
import src.getdata as tac
st.set_page_config(layout="wide", page_title = "CityAdvisor")



col1,col2 = st.beta_columns([2,3])
imagen = Image.open("images/portada2.jpg")
imagen2= Image.open("images/portada.jpg")
col1.image(imagen)
col2.bar_chart (dat.grafica_intro2())


st.write(""" Bienvenidos a CityAdvisor! comparando códigos postales desde 2021!

""")

col1,col2 = st.beta_columns([3,2])
                                            
col1.dataframe (dat.grafica_intro())
col2.image (imagen2)


st.write("""
## Empecémos
""")


lista= st.multiselect (" Haz tu selección:", mdb.colecciones())

cp=st.text_input ("Si no encuentras lo que buscas, creémoslo: Introduce un codigo postal")
if cp:
    ubicacion= tac.test_and_create (cp)
    st.write ("El código", ubicacion, " ya está diponible en nuestra base de datos")


items = st.multiselect (

    "Ahora añade tus búsquedas", dat.lista_sub()
)
if not items:
   st.warning('Por favor, seleccione una categoría')
   st.stop()


col1,col2 = st.beta_columns([2,2])
col1.header ("Suma de los elementos seleccionados" )                                           
col1.dataframe (dat.grafica_items(lista, items))
col2.header ("Rentas según Codigo postal")
col2.line_chart (dat.grafica_renta(lista))

st.header ("Relación de rentas con categorias")
st.line_chart (dat.grafica_renta_cats(lista))
st.subheader ("Las rentas están escaladas para una correcta visualización")

st.header ( "Este es el peso relativo de cada categoria para su selección")

st.bar_chart (dat.porcentajes(lista))


st.write ("Si quieres, vemos algunos sitios más concretos")

ubic= str (st.selectbox (" Vamos a verlo en el mapa", mdb.colecciones()))

mapa=folium_static (get_map (ubic, items))

if not mapa:
    st.write ("Lo sentimos, con la selección actual no hay resultados disponibles")