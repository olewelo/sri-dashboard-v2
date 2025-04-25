import streamlit as st
import pandas as pd
import plotly.express as px

###########################
# Page configuration
st.set_page_config(
    page_title="School Risk Index: School Data",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded")

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/CUSP Logo Black.png", width=200)

st.title("School Risk Index: School Data")