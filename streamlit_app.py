###########################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


###########################
# Page configuration
st.set_page_config(
    page_title="School Risk Index Dashboard",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


###########################
# Load data
df = pd.read_csv('/Users/Ole/olewelo-Nextcloud/Capstone/Capstone SRI Data Files/Countries/countries_SRI_simplified.csv')


###########################
# Plots

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(df, locations=input_id, color=input_column, locationmode="ISO-3",
                               color_discrete_map=input_color_theme,
                               category_orders={input_column: SRI_categories},
                               projection="robinson",
                               scope="world",
                               labels={input_column:input_column}
                              )
    choropleth.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


###########################
# Colors & Categories

SRI_colors = {
    "Low": "#ebeff1",
    "Low-Medium": "#F2E8CF",
    "Medium-High": "#81B29A",
    "High": "#4C5F70",
    "Extremely High": "#293241"
}

SRI_categories = ["Low", "Low-Medium", "Medium-High", "High", "Extremely High"]

###########################
# Dashboard Main Panel

col = st.columns((1.5, 4.5, 2), gap='medium')


with col[1]:
    st.markdown('#### School Risk Index')
    
    choropleth = make_choropleth(df, 'GID', 'SRI_category', SRI_colors)
    st.plotly_chart(choropleth, use_container_width=True)

