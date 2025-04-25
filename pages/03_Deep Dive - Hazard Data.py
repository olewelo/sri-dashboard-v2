import folium
from streamlit_folium import folium_static
import streamlit as st

###########################
# Page configuration
st.set_page_config(
    page_title="School Risk Index: Hazard Data",
    layout="wide",
    initial_sidebar_state="expanded")

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/CUSP Logo Black.png", width=200)

st.title("School Risk Index: Hazard Data")

# Create folium map
m = folium.Map(location=[0, 0], zoom_start=2)

# Add ArcGIS Online tile service
folium.TileLayer(
    tiles="https://tiles.arcgis.com/tiles/ORGID/arcgis/rest/services/LAYERNAME/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="ArcGIS Raster",
    overlay=True,
    control=True
).add_to(m)

folium.LayerControl().add_to(m)
folium_static(m)