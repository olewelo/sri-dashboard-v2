###########################
# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

###########################
# Page configuration
st.set_page_config(
    page_title="School Risk Index Dashboard",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded")

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/CUSP Logo Black.png", width=200)

st.title("School Risk Index")


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
        projection="robinson"
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
    return fig


###########################
# Tabs to navigate between map and other data
page = st.tabs(["MAP", "CONTEXTUAL DATA"])


###########################
# Map page
with page[0]:
    st.plotly_chart(make_choropleth(), use_container_width=True, key="map_intro")


###########################
# Context Page
with page[1]:

# === Charts ===

    st.markdown("<h5 style='margin-top:0rem;'>Distribution Overview</h5>", unsafe_allow_html=True)

    # Prepare data
    df["REGION"] = df["REGION"].str.strip().str.title()
    df_bar = df.groupby(["REGION", "SRI_category"]).size().reset_index(name="count")
    df_bar = df_bar.pivot(index="REGION", columns="SRI_category", values="count").fillna(0)
    df_bar_pct = df_bar.div(df_bar.sum(axis=1), axis=0).reset_index()
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

    # Income bars (right)
    for category in SRI_categories:
        data = df_income_melted[df_income_melted["SRI Category"] == category]
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


    # Drop and rename columns
    df_clean = df.drop(columns=["SOVEREIGN", "CONTINENT", "GID", "INCOME GROUP", "SRI_ncategory", "coastflood", "rivflood", "watersc", "heatwvs", "pm25", "cyclns"], errors="ignore").rename(columns={
        "SRI_category": "SRI Category",
        "REGION": "Region",
    })

    # Toggle for sorting
    sort_order = st.radio("Sort by:", ["Sort SRI ↓", "Sort SRI ↑"], horizontal=True, label_visibility='collapsed')
    ascending = sort_order == "Sort SRI ↑"

    df_sorted = df_clean.sort_values(by="SRI", ascending=ascending)

    st.dataframe(df_sorted.reset_index(drop=True), use_container_width=True)