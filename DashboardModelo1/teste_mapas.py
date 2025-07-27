import geopandas as gpd
import geobr
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#import folium
import streamlit as st
from shapely.geometry import Polygon, Point

import pandas as pd
import plotly.express as px


## main
#municipios = geobr.read_municipality(year=2010, code_muni='MT')

## obtendo o municipio
#gdf_muni =  municipios[municipios.name_muni == 'Primavera Do Leste']
#gdf_muni.crs = "EPSG:4326"
#print(gdf_muni.head())

# Configurar o layout da página
#st.set_page_config(layout="wide")

#fig = gdf_muni.plot()
#st.pyplot(gdf_muni.empty)
#st.write(municipios.name_muni)

fig, ax = plt.subplots(figsize=(10,10))
def numft(x, pos):
    s = f'{x/1000:,.0f}'
    return s


shape_file_name = r'/home/mauricio/PycharmProjects/DashboardCotton/DashboardModelo1/Shapefile-Grid/grid.shp'
shape_file = gpd.read_file(shape_file_name)
p = shape_file.crs
shape_file.plot(facecolor='none', linewidth=0.5, edgecolor='black')
for axis in [ax.xaxis, ax.yaxis]:
    formatter = mtick.FuncFormatter(numft)
    axis.set_major_formatter(formatter)
plt.show()
