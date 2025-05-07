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
tab1, tab2 = st.tabs(["OVERVIEW", "DATA VALIDATION"])

# ===========================
# TAB 1 — Hazard maps

with tab1:
    st.markdown("#### Overview of Hazard Data")
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


# ===========================
# TAB 2 — Hazard validation

with tab2:
    st.markdown("#### Hazard Data Validation")
    st.markdown("Lorem impsum blah blah blah.")

    # Radio button to select which table to view
    table_choice = st.radio(
        "Select a hazard to view:",
        ["Water Scarcity", "Riverine & Coastal Flooding", "Tropical Cyclones", "Air Pollution", "Heatwaves"],
        horizontal=True
    )

    # Define CSV file paths (adjust filenames if needed)
    table_files = {
        "Water Scarcity": "data/climate validation/waterscarcity_missing.csv",
        "Riverine & Coastal Flooding": "data/climate validation/coastalflooding_missing.csv",
        "Air Pollution": "data/climate validation/AQ_missing.csv"
    }

    # If the selected table has a CSV file, load and display
    if table_choice in table_files:
        try:
            df = pd.read_csv(table_files[table_choice])

            # Drop unnamed first column if it exists
            if df.columns[0].lower().startswith("unnamed"):
                df = df.drop(columns=df.columns[0])
            
            # Sort by "Missing (%)" column if it exists
            if "Missing (%)" in df.columns:
                df = df.sort_values(by="Missing (%)", ascending=False)

            st.dataframe(df.reset_index(drop=True), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading data: {e}")
    else:
        st.info("No missing data - the data source covers the globe fully.")