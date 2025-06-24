import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pydeck as pdk

###########################
# Page configuration
st.set_page_config(
    page_title="School Risk Index: School Data",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded")

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/I4DI Logo Black.png", width=150)
st.sidebar.image("images/CUSP Logo Black.png", width=200)


st.title("School Risk Index: School Data")

# Load data
@st.cache_data
def load_data():
    return gpd.read_parquet("data/schools_exposure_cleaned.parquet")

gdf = load_data()
gdf["lon"] = gdf.geometry.x
gdf["lat"] = gdf.geometry.y

# ===========================
# TABS
tab1, tab2, tab3 = st.tabs(["OVERVIEW", "INTERACTIVE COUNTRY EXPLORER", "DATA VALIDATION"])

# ===========================
# TAB 1 — Overview Map (static, no zoom/pan)

with tab1:
    st.markdown("#### Overview of School Coverage")
    st.markdown("""
                School location data was retrieved from [OpenStreetMap](https://www.openstreetmap.org/), the currently most comprehensive source of school locations wordwide publicly available. 
                The map below shows a simplified overview of the distribution of schools included in the data. The total number of schools included in the School Risk Index is 1.34 million. 
                To explore individual schools, please switch to the 'Interactive Country Explorer' tab. For a detailed description of the data processing steps, please refer to the [Methodology Paper](https://drive.google.com/file/d/1KcqDYsxFOzbaQK7IcdecrTtaV3MrA-Y5/view?usp=share_link).
    """)

    with open("images/schools_overview.html", "r") as f:
        html = f.read()

    st.components.v1.html(html, height=700)

# ===========================
# TAB 2 — Filter by Country

with tab2:
    st.markdown("#### Explore Individual Schools by Country")
    st.markdown("Use the drop-down menu below to select a country of interest. This displays all schools in that country that are included in our data. Hover over a school point to display a pop-up with contextual information.")

    # Select and filter
    country = st.selectbox("Select a country", sorted(gdf["Country"].dropna().unique()))
    country_data = gdf[gdf["Country"] == country].copy()

    # Show count
    st.markdown(f"**Total schools mapped in {country}:** {len(country_data):,}")

    # Handle missing values
    country_data.fillna("N/A", inplace=True)

    # Extract hazards
    hazard_columns = ["Water Scarcity", "Coastal Flooding", "Riverine Flooding", "Heatwaves", "Cyclones Cat 1&2", "Cyclones Cat 3+", "PM2.5 above 9μg/m³", "PM2.5 above 35μg/m³"]

    def extract_hazards(row):
        return ", ".join([hazard for hazard in hazard_columns if row.get(hazard, 0) == 1]) or "None"
    country_data["Hazards"] = country_data.apply(extract_hazards, axis=1)

    # Map center
    lat_center = country_data["lat"].mean()
    lon_center = country_data["lon"].mean()

    # Layer setup
    detailed_layer = pdk.Layer(
        "ScatterplotLayer",
        data=country_data,
        get_position=["lon", "lat"],
        get_radius=8,
        get_radius_units="pixels",
        radius_min_pixels=4,    # fallback minimum size
        radius_max_pixels=10,   # optional
        get_fill_color=[30, 150, 60, 150],
        pickable=True,
    )

    # Tooltip
    tooltip = {
        "html": (
            "<b>{School Name}</b><br>"
            "<u>Country:</u> {Country}<br>"
            "<u>Affected by:</u> {Hazards}"
        ),
        "style": {
            "backgroundColor": "white",
            "color": "black",
            "fontSize": "12px"
        }
    }

    # Display map
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat_center,
            longitude=lon_center,
            zoom=4
        ),
        layers=[detailed_layer],
        tooltip=tooltip
    ))

# ===========================
# TAB 3 — Data validation

with tab3:
    st.markdown("#### Data Validation using Government Data")
    st.markdown(
        "The SRI's school location data was validated to measure quality using a stratified sample " \
        "of countries, selected across regions and income groups. Two countries per stratum were " \
        "chosen—one with a high, one with a low number of schools relative to the country's child " \
        "population—based on data availability. The SRI data's total number of schools in each sample country was " \
        "compared to official government data on school numbers to assess the quality of the SRI school coverage.")

    # Load Data
    val_df = pd.read_csv("data/schools_validation.csv")


    # Scale percentage
    val_df["PERCENT COVERED (%)"] = val_df["PERCENT COVERED"] * 100

    # Create hover text column
    val_df["hover_text"] = (
        "<b>" + val_df["Country"] + "</b><br>" +
        "SRI Data Number of Schools: " + val_df["OSM Number of Schools"].astype(str) + "<br>" +
        "GOV Data Number of Schools: " + val_df["GOV Number of Schools "].astype(str) + "<br>" +
        "↳" + "<u>" + "Percent Covered: " + (val_df["PERCENT COVERED (%)"]).round(1).astype(str) + "%" + "</u>"
    )


# === MAP ===

    st.markdown("<h5 style='margin-top:2rem;'>Cross-Validated Countries: Overview Map</h5>", unsafe_allow_html=True)
    st.markdown("The map below displays the sample of validation countries, their school counts in our data, their school counts in government data, and the coverage percentage indicator resulting from it. Hover over a country for detailed information.")

    # Choropleth
    fig = px.choropleth(
        val_df,
        locations="ISO3",  # ISO-3 country codes
        color="PERCENT COVERED (%)",
        locationmode="ISO-3",
        color_continuous_scale=px.colors.sequential.Greens,
        range_color=(0, 100),
        projection="robinson",
        labels={"PERCENT COVERED (%)": "Percent of schools covered"},
        hover_name="hover_text",
    )


    fig.update_traces(
        marker_line_color="white",
        marker_line_width=0.4,
        hovertemplate="%{hovertext}<extra></extra>"  # tell Plotly to use our hover text
    )

    fig.update_layout(
        geo=dict(showland=True, showocean=False, showcountries=False, showcoastlines=False, showframe=False, landcolor='lightgray', bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=0, b=0, l=0, r=0),
        height=500,
        coloraxis_colorbar=dict(
            title="Percent of schools covered",
            ticksuffix="%",
            orientation='h',
            x=0.5,
            y=-0.2,
            yanchor="bottom", 
            xanchor="center")
    )

    st.plotly_chart(fig, use_container_width=True)


# === GRAPHS ===

    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    st.markdown("<h5 style='margin-top:2rem;'>Validation Coverage Breakdown</h5>", unsafe_allow_html=True)
    st.markdown("The graphs below display the average percentage to which the SRI school numbers cover official government school numbers, by world region and by World Bank income group.")

    # Clean + prepare data
    val_df["Region"] = val_df["Region"].str.strip().str.title()
    val_df["Income Group"] = val_df["Income Group"].str.strip().str.title()

    # === Averages ===
    region_avg = val_df.groupby("Region")["PERCENT COVERED (%)"].mean().sort_values(ascending=False).reset_index()
    income_avg = val_df.groupby("Income Group")["PERCENT COVERED (%)"].mean().sort_values(ascending=False).reset_index()

    # === Side-by-side chart setup ===
    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.08,
        subplot_titles=("Average Coverage by Region", "Average Coverage by Income Group")
    )

    # Region bars (left)
    fig.add_trace(
        go.Bar(
            x=region_avg["Region"],
            y=region_avg["PERCENT COVERED (%)"],
            marker_color="#4C5F70",  # Dark blue/gray
            hovertemplate="%{x}<br>Avg. Coverage: %{y:.1f}%<extra></extra>"
        ),
        row=1, col=1
    )

    # Income Group bars (right)
    fig.add_trace(
        go.Bar(
            x=income_avg["Income Group"],
            y=income_avg["PERCENT COVERED (%)"],
            marker_color="#81B29A",  # Soothing green
            hovertemplate="%{x}<br>Avg. Coverage: %{y:.1f}%<extra></extra>"
        ),
        row=1, col=2
    )

    # Layout
    fig.update_layout(
        height=450,
        margin=dict(t=60, b=60),
        yaxis=dict(title="Average % Covered", range=[0, 100]),
        xaxis_tickangle=-45,
        xaxis2_tickangle=-45,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})