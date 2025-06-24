import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Page config
st.set_page_config(
    page_title="Introducing the School Risk Index",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/I4DI Logo Black.png", width=150)
st.sidebar.image("images/CUSP Logo Black.png", width=200)


st.title("Introducing the School Risk Index")

st.markdown("""
            The **School Risk Index (SRI)** is a comprehensive measure that quantifies the exposure of schools to various climate and weather hazards.
            The calculation methodology of the School Risk Index is inspired by UNICEF's [Children's Climate Risk Index](https://data.unicef.org/resources/childrens-climate-risk-index-report/?_gl=1*bg3k28*_gcl_au*MTEwNTQ1ODk2Ni4xNzQ1NjI2NDk4*_ga*NzM5NTQ4MjIyLjE3Mzc0NzYyNjQ.*_ga_P0DMSZ8KY6*czE3NTA3MDE3MTgkbzEwJGcwJHQxNzUwNzAxNzIyJGo1NiRsMCRoMA..*_ga_ZEPV2PX419*czE3NTA3MDE3MTgkbzEwJGcwJHQxNzUwNzAxNzE4JGo2MCRsMCRoMA..), 
            with adaptions made to reflect the School Risk Index' distinct focus on schools.
            Exposure to the climate hazards listed below was calculated for over 1.3M individual schools globally. 
            Their locations were retrieved from the community mapping platform [OpenStreetMap](https://www.openstreetmap.org/)—currently the by far most comprehensive source of school locations publicly available.
            As a composite index, the School Risk Index is built to easily be expanded, particularly by vulnerability and capacity indicators crucial to holistically measure risk.
""")




###########################

# Load Data
df = pd.read_csv("countries_SRI_simplified_inclWBdata.csv")

# Define color categories
SRI_colors = {
    "Low": "#ebeff1",
    "Low-Medium": "#F2E8CF",
    "Medium-High": "#81B29A",
    "High": "#4C5F70",
    "Extremely High": "#293241"
}
SRI_categories = ["Low", "Low-Medium", "Medium-High", "High", "Extremely High"]

# Choropleth map function
def make_choropleth():
    fig = px.choropleth(
        df,
        locations="GID",
        color="SRI_category",
        locationmode="ISO-3",
        color_discrete_map=SRI_colors,
        category_orders={'SRI_category': SRI_categories},
        projection="robinson",
        custom_data=["COUNTRY", "GID", "REGION", "INCOME GROUP", "SRI", "SRI_category", "coastflood", "rivflood", "watersc", "heatwvs", "pm25", "cyclns"]
    )
    fig.update_layout(
        geo=dict(showland=False, showocean=False, showcountries=False, showframe=False, bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        legend=dict(
            title=dict(
                text="<b>SRI Categories</b>"
            ), 
            orientation="h", 
            yanchor="top", 
            xanchor="auto")
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}: %{customdata[5]}</b><br>"
            "<u>SRI:</u> %{customdata[4]:.2f}<br>"
            "Water Scarcity: %{customdata[8]}<br>"
            "Riverine Flooding: %{customdata[7]}<br>"
            "Coastal Flooding: %{customdata[6]}<br>"
            "Tropical Cyclones: %{customdata[11]}<br>"
            "Air Pollution: %{customdata[10]}<br>"
            "Heatwaves: %{customdata[9]}<br>"
        )
    )
    return fig


###########################
# Tabs to navigate between map and other data
page = st.tabs(["SCHOOL RISK INDEX MAP", "METHODOLOGY", "CONTEXTUAL DATA"])


###########################
# Map page
with page[0]:
    st.markdown("""
            The map below visualizes the School Risk Index for all countries included in the model. Hover over a country to see its School Risk Index and the exposure of schools to the six climate hazards included in the model.
    """)
    st.plotly_chart(make_choropleth(), use_container_width=True, key="map_intro")


###########################
# Methodology page
with page[1]:

    st.markdown("##### A Brief Methodology Overview")


    st.markdown("""
                The School Risk Index was calculated by spatially overlaying individual school locations with fine-grained spatial climate and weather hazard data.
                For each of the over 1.3 million schools, exposure was assessed across six key climate and environmental hazards: 
                water scarcity, riverine flooding, coastal flooding, tropical cyclones, air pollution, and heatwaves. 

                For each hazard, global datasets were used to determine whether a school's location met or exceeded established exposure thresholds. 
                Exposure levels were then aggregated both relatively and absolutely to the country level. Using a sequence of mathematical transformations, 
                a composite exposure score between 0 and 10 was calculated for each country, taking into account variability in school density and data quality.
                The transformation process follows the procedure recommended in the Global INFORM model for risk indices. 
                For a detailed description of the individual calculation and transformation steps, please refer to the [Methodology Paper](https://drive.google.com/file/d/1KcqDYsxFOzbaQK7IcdecrTtaV3MrA-Y5/view?usp=share_link).
    """)

    st.markdown("""            
                The School Risk Index and all included exposure indices range from 0 to 10, with higher values indicating greater exposure to climate hazards. All indices are a relative comparison between countries included in the model, meaning that the performance of a country on the different indices is better or worse in comparison to all other countries included in the model.
    """)

    st.markdown("""
                For better interpretability, the index values are categorized into five levels of exposure:
                - Low: 0-2
                - Low-Medium: 2.1-3.7
                - Medium-High: 3.8-5.4
                - High: 5.5-7
                - Extremely High: 7.1-10
    """)


###########################
# Context Page
with page[2]:

# === Charts ===

    st.markdown("<h5 style='margin-top:0rem;'>Distribution Overview</h5>", unsafe_allow_html=True)

    st.markdown("""
                The charts below provide an overview of the distribution of School Risk Index (SRI) values across World Bank regions and income groups. 
    """)
    
    # Prepare data
    df["REGION"] = df["REGION"].str.strip().str.title()
    df_bar = df.groupby(["REGION", "SRI_category"]).size().reset_index(name="count")
    df_bar = df_bar.pivot(index="REGION", columns="SRI_category", values="count").fillna(0)
    df_bar_pct = df_bar.div(df_bar.sum(axis=1), axis=0).reset_index()

    # --- Sort regions by combined share of "Extremely High" and "High" ---
    df_bar_pct["high_share"] = df_bar_pct.get("High", 0) + df_bar_pct.get("Extremely High", 0)
    region_order = df_bar_pct.sort_values("high_share")["REGION"].tolist()  # ascending: lowest left, highest right

    df_melted = df_bar_pct.melt(id_vars="REGION", var_name="SRI Category", value_name="Percentage")

    df["INCOME GROUP"] = df["INCOME GROUP"].str.strip().str.title()
    df_income = df.groupby(["INCOME GROUP", "SRI_category"]).size().reset_index(name="count")
    df_income = df_income.pivot(index="INCOME GROUP", columns="SRI_category", values="count").fillna(0)
    df_income_pct = df_income.div(df_income.sum(axis=1), axis=0).reset_index()
    df_income_melted = df_income_pct.melt(id_vars="INCOME GROUP", var_name="SRI Category", value_name="Percentage")

    # Create side-by-side subplot
    fig = make_subplots(
        rows=1, cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.08,
        subplot_titles=("SRI Distribution by Region", "SRI Distribution by Income Group")
    )

    # Region bars (left)
    for category in SRI_categories:
        data = df_melted[df_melted["SRI Category"] == category]
        # Ensure the order of regions
        data = data.set_index("REGION").reindex(region_order).reset_index()
        fig.add_trace(
            go.Bar(
                x=data["REGION"],
                y=data["Percentage"],
                name=category,
                marker=dict(color=SRI_colors[category]),
                legendgroup=category,
                legendrank=SRI_categories.index(category)
            ),
            row=1, col=1
        )

    income_order = ["Low Income", "Lower Middle Income", "Upper Middle Income", "High Income"]

    # Income bars (right)
    for category in SRI_categories:
        data = df_income_melted[df_income_melted["SRI Category"] == category]
        # Ensure the order of income groups
        data = data.set_index("INCOME GROUP").reindex(income_order).reset_index()
        fig.add_trace(
            go.Bar(
                x=data["INCOME GROUP"],
                y=data["Percentage"],
                name=category,
                marker=dict(color=SRI_colors[category]),
                legendgroup=category,
                legendrank=SRI_categories.index(category),
                showlegend=False  # Only show once
            ),
            row=1, col=2
        )

    # Final layout tweaks
    fig.update_layout(
        barmode="stack",
        height=500,
        yaxis_tickformat=".0%",
        margin=dict(t=60, b=60),
        xaxis_tickangle=-45,
        xaxis2_tickangle=-45,
        xaxis=dict(title="", showticklabels=True),
        xaxis2=dict(title="", showticklabels=True),
        yaxis=dict(range=[0, 1]),
        legend=dict(
            title='SRI Categories',
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="center",
            x=0.5
        )
    )

    # Display
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


    # === Table ===

    st.markdown("<h5 style='margin-top:0rem;'>Country-Level Data</h5>", unsafe_allow_html=True)

    st.markdown("""
                Hover over the table and select the magnifying glass icon on the top right to search for specific countries or regions.
    """)

    # Drop and rename columns
    df_clean = df.drop(columns=["SOVEREIGN", "CONTINENT", "GID", "INCOME GROUP", "SRI_ncategory"], errors="ignore").rename(columns={
        "SRI_category": "SRI Category",
        "REGION": "Region",
        "coastflood":"Coastal Flooding", 
        "rivflood":"Riverine Flooding", 
        "watersc":"Water Scarcity", 
        "heatwvs":"Heatwaves", 
        "pm25":"Air Pollution", 
        "cyclns":"Tropical Cyclones"
    })

    # Toggle for sorting
    sort_order = st.radio("Sort by:", ["Sort SRI ↓", "Sort SRI ↑"], horizontal=True, label_visibility='collapsed')
    ascending = sort_order == "Sort SRI ↑"

    df_sorted = df_clean.sort_values(by="SRI", ascending=ascending)

    st.dataframe(df_sorted.reset_index(drop=True), use_container_width=True)