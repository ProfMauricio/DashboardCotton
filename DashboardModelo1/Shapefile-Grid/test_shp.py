import folium
#from streamlit_folium import st_folium
import geopandas as gpd
from folium import Choropleth, Marker
from folium.plugins import MarkerCluster

import folium

m = folium.Map(location=[51.5074, 0.1278], zoom_start=10)

# Add a circle marker (radius in pixels)
folium.CircleMarker(
    location=[51.5074, 0.1278],
    radius=50,
    color='blue',
    fill=True,
    fill_color='blue',
    popup="London"
).add_to(m)

# Add a circle (radius in meters)
folium.Circle(
    location=[51.55, 0.05],
    radius=1000, # meters
    color='green',
    fill=True,
    fill_color='green',
    popup="1km radius"
).add_to(m)

# Add a polygon
folium.Polygon(
    locations=[[51.5, 0.1], [51.5, 0.2], [51.6, 0.2], [51.6, 0.1]],
    color='purple',
    fill=True,
    fill_color='purple',
    popup="A Square"
).add_to(m)

m.save('Teste.html')