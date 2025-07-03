import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Page config
st.set_page_config(
    page_title="School Risk Index: Hazard Data",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/I4DI Logo Black.png", width=150)
st.sidebar.image("images/CUSP Logo Black.png", width=200)


st.title("School Risk Index: Hazard Data")


# ===========================
# TABS
tab1, tab2 = st.tabs(["OVERVIEW", "HAZARD MAPS"])


# ===========================
# TAB 1 — OVERVIEW

with tab1:
    st.markdown("""
                The School Risk Index uses six climate and weather hazards to measure the exposure of schools globally. These hazards were selected based on their relevance to education systems and impact on school operations, as well as the following criteria pertaining to the data being:
                1. publicly available;
                2. global in scope;
                3. reliable and regularly updated;
                4. comparable across countries;
                5. maintained by a single global source.
                """)
    st.markdown("""
                Given data availability challenges and the limited resources of this project, the hazards included in the School Risk Index are by no means exhaustive.
                For each hazard, exposure thresholds were calculated based on a review of relevant literature. 
                All data sources were validated with additional global climate data sources to confirm areas of exposure.
                Please refer to the table below for an overview of the hazards included, their data sources, and respective exposure thresholds.
                For a detailed description of the data preparation and exposure calculation process, please refer to the [Methodology Paper](https://drive.google.com/file/d/1KcqDYsxFOzbaQK7IcdecrTtaV3MrA-Y5/view?usp=share_link).
                """)


    st.markdown("""
    <table>
        <thead>
            <tr>
                <th>Hazard</th>
                <th>Data Source</th>
                <th>Exposure Threshold</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Water Scarcity</td>
                <td><a href="https://www.wri.org/data/aqueduct-global-maps-40-data" target="_blank">WRI Aqueduct Water Risk Atlas 4.0</a></td>
                <td>Composite indicator: Average score 2+ of baseline water stress, seasonal variability, interannual variability, groundwater table decline, and drought risk</td>
            </tr>
            <tr>
                <td>Riverine Flooding</td>
                <td><a href="https://www.wri.org/data/aqueduct-global-maps-40-data" target="_blank">WRI Aqueduct Water Risk Atlas 4.0</a></td>
                <td>High or Very High Risk</td>
            </tr>
            <tr>
                <td>Coastal Flooding</td>
                <td><a href="https://www.wri.org/data/aqueduct-global-maps-40-data" target="_blank">WRI Aqueduct Water Risk Atlas 4.0</a></td>
                <td>High or Very High Risk</td>
            </tr>
            <tr>
                <td>Tropical Cyclones</td>
                <td><a href="https://giri.unepgrid.ch/map?list=explore&view=MX-UG0KA-OIQSJ-FIMNA" target="_blank">CDRI Tropical Cyclone Wind - 100yr Return Period</a></td>
                <td>119 km/h, 178 km/h (geometric mean)</td>
            </tr>
            <tr>
                <td>Air Pollution</td>
                <td><a href="https://sites.wustl.edu/acag/datasets/surface-pm2-5/" target="_blank">ACAG Satellite-derived PM2.5 Concentrations</a></td>
                <td>μg/m³, 35μg/m³ (arithmetic mean)</td>
            </tr>
            <tr>
                <td>Heatwaves</td>
                <td><a href="https://berkeleyearth.org/data/" target="_blank">Berkeley Earth Global Gridded Temperature Data</a></td>
                <td>9 average annual heatwaves from 2000-2024</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)


# ===========================
# TAB 2 — Hazard maps

with tab2:
    st.markdown("##### Hazard Maps")
    st.markdown("The maps below show the global hazard rasters used to overlay with the school location data. The first map is an overlay of all six hazard rasters. Switch between rasters using the toggles above the map.")

    # Radio button to select layer
    layer_choice = st.radio(
        "Select a hazard layer:",
        ["OVERLAY", "Water Scarcity", "Riverine Flooding", "Coastal Flooding", "Tropical Cyclones", "Air Pollution", "Heatwaves"],
        horizontal=True
    )

    # Tile URLs
    tile_urls = {
        "OVERLAY": "https://tiles.arcgis.com/tiles/OO2s4OoyCZkYJ6oE/arcgis/rest/services/OverlayMap_V1/MapServer/tile/{z}/{y}/{x}",
        "Water Scarcity": "https://tiles.arcgis.com/tiles/OO2s4OoyCZkYJ6oE/arcgis/rest/services/WaterScarcity_V4/MapServer/tile/{z}/{y}/{x}",
        "Riverine Flooding": "https://tiles.arcgis.com/tiles/OO2s4OoyCZkYJ6oE/arcgis/rest/services/RiverineFlooding_V1/MapServer/tile/{z}/{y}/{x}",
        "Coastal Flooding": "https://tiles.arcgis.com/tiles/OO2s4OoyCZkYJ6oE/arcgis/rest/services/CoastalFlooding_V2/MapServer/tile/{z}/{y}/{x}",
        "Tropical Cyclones": "https://tiles.arcgis.com/tiles/OO2s4OoyCZkYJ6oE/arcgis/rest/services/TropicalCyclones_V2/MapServer/tile/{z}/{y}/{x}",
        "Air Pollution": "https://tiles.arcgis.com/tiles/OO2s4OoyCZkYJ6oE/arcgis/rest/services/AirPollution_V1/MapServer/tile/{z}/{y}/{x}"
    }

    # === LEGEND HTML ===

    if layer_choice == "OVERLAY":
        legend_md = """
        <b>Overall Degree of Exposure</b><br>
        <div style='display: flex; gap: 15px; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#F5F500; width:15px; height:15px; border:0px solid #aaa;'></div> Low (≤1)
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#F5B800; width:15px; height:15px; border:0px solid #aaa;'></div> Low-Medium (2)
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#F57A00; width:15px; height:15px; border:0px solid #aaa;'></div> Medium-High (3)
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#F53D00; width:15px; height:15px; border:0px solid #aaa;'></div> High (4)
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#F50000; width:15px; height:15px; border:0px solid #aaa;'></div> Extremely High (5+)
            </div>
        </div>
        """

    elif layer_choice in ["Air Pollution"]:
        legend_md = """
        <b>Exposure</b><br>
        <div style='display: flex; gap: 15px; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#e1e1e1; width:15px; height:15px; border:0px solid #aaa;'></div> Not Exposed
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#ffbdbe; width:15px; height:15px; border:0px solid #aaa;'></div> Exposed (9μg/m³)
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#f64142; width:15px; height:15px; border:0px solid #aaa;'></div> Exposed (35μg/m³)
            </div>
        </div>
        """
    elif layer_choice in ["Tropical Cyclones"]:
        legend_md = """
        <b>Exposure</b><br>
        <div style='display: flex; gap: 15px; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#e1e1e1; width:15px; height:15px; border:0px solid #aaa;'></div> Not Exposed
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#ffbdbe; width:15px; height:15px; border:0px solid #aaa;'></div> Exposed (119 km/h)
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#f64142; width:15px; height:15px; border:0px solid #aaa;'></div> Exposed (178 km/h)
            </div>
        </div>
        """
    else:
        legend_md = """
        <b>Exposure</b><br>
        <div style='display: flex; gap: 15px; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#e1e1e1; width:15px; height:15px; border:0px solid #aaa;'></div> Not Exposed
            </div>
            <div style='display: flex; align-items: center; gap: 5px;'>
                <div style='background:#f64142; width:15px; height:15px; border:0px solid #aaa;'></div> Exposed
            </div>
        </div>
        """

    # Render the legend with padding below only
    st.markdown(
        f"<div style='margin-bottom: 20px;'>{legend_md}</div>",
        unsafe_allow_html=True
    )

    # === CONDITIONAL DISPLAY ===

    if layer_choice != "Heatwaves":
        # Folium map for other layers
        m = folium.Map(location=[0, 0], zoom_start=1.5, tiles="CartoDB positron", control_scale=True)

        folium.TileLayer(
            tiles=tile_urls[layer_choice],
            name=layer_choice,
            attr="Esri",
            overlay=True,
            control=False
        ).add_to(m)

        st_folium(m, height=600, use_container_width=True)

    else:
        # Static image for Heatwaves
        st.image(
            "images/heatwaves.png",
            use_container_width=True,
            caption="Due to its different cell size, the heatwaves raster can only be displayed as a static image on this dashboard."
        )

