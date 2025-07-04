import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import geopandas as gpd
from geodatasets import get_path

from streamlit_folium import st_folium

#from sqlalchemy import create_engine

import os
#import pg8000
#from dotenv import load_dotenv

def classificar(valor):
  if valor < 0.5:
    return "Abaixo do esperado"
  elif valor < 3.0:
    return "Dentro do esperado"
  else:
    return "Acima do esperado"


# Load environment variables from .env file
#load_dotenv()
#global VALOR_LIMIAR_RELEVANCIA
# Database connection details
#DB_HOST = os.getenv("DB_HOST")
#DB_NAME = os.getenv("DB_NAME")
#DB_USER = os.getenv("DB_USER")
#DB_PASSWORD = os.getenv("DB_PASSWORD")
#DB_PORT = int(os.getenv("DB_PORT"))

#conectando a base de dados
#engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
#print("Iniciando conexão com a base")
# criando um conjunto teste do app
indices_ndvi =  { 'grid' : [1,2,3,4,5,6,7,8,9,10,11,12], 'valor':[0.251, 3.521, 0.272, 2.0, 1.32, 2.02, 2.07, 3.08, 1.09, 2.2, 3.2, 0.512]}
df  = pd.DataFrame(indices_ndvi)
print(df)

# Configurar o layout da página
st.set_page_config(layout="wide")


# Buscando alguns dados da estatística
#df = pd.read_sql_table("estatisticas_r2d2", con=engine, columns=["instante", "distribuidos", "nao_distribuidos", "falha_integracao"], schema="api" )
# Converter a coluna "Date" para o formato de data
#df["instante"] = pd.to_datetime(df["instante"], dayfirst=True)
#df = df.sort_values("instante")

# buscando alguns dados da distribuição de intimação
#df_rel = pd.read_sql_table("relatorio_r2d2", con=engine, columns=["instante", "setor_destino", "ultimo_setor"], schema="api" )
#df_rel["instante"] = pd.to_datetime(df_rel["instante"], dayfirst=True)
#df_rel = df_rel.sort_values("instante")


# Criar uma nova coluna "Month" que contém o ano e o mês
#df["Month"] = df["instante"].apply(lambda x: str(x.year) + "-" + str(x.month))
# Criando uma coluna que diz qual é a semana do ano
st.image('./logo_embrapa.png', width=200)
df["Classe"] = df["valor"].apply(lambda x: classificar(x) )


# Criar uma seleção de meses na barra lateral do dashboard
#semana = st.sidebar.multiselect("Semanas do ano" , df["Semana"].unique())
#df_filtered = df[df["Semana"].isin(semana)]
df_filtered  = df[df['Classe'] == "Abaixo do esperado" ]
explode = (0, 0.2, 0)
col1, col2 = st.columns([2,2])

# Criar o gráfico da situação do NDVI
col1.title("Distribuição das classes de NDVI no talhão XXX")
figNDVI = px.pie(df, "Classe", title="Situação dos Grids em relação ao valor de NDVI (% por classe)", labels={"Classe": "NDVI"})
figNDVI.update_layout(
        plot_bgcolor='white',
        # paper_bgcolor='white',
        legend_title_text='Classes de NDVI'
	)
figNDVI.update_traces(
        pull=[0.05, 0.02, 0.02], # Pull the first slice out by 5%
        marker=dict(line=dict(color='white', width=1))) # Add a black border


col1.plotly_chart(figNDVI, use_container_width=True)


col2.title('Grids abaixo do esperado')
col2.write(df_filtered)


