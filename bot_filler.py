from src.getdata import fill_db
import pandas as pd


df= pd.read_csv ("../Data/listacodigos.csv")
madrid=df[7785:7816]

fill_db(madrid["codigopostalid"])