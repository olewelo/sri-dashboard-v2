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
    initial_sidebar_state="expanded"
    )

st.sidebar.title("School Risk Index Dashboard")
st.sidebar.markdown("Welcome to the SRI dashboard. Navigate using the menu above.")
st.sidebar.image("images/I4DI Logo Black.png", width=150)
st.sidebar.image("images/CUSP Logo Black.png", width=200)



st.markdown("<h1 style='text-align: center; font-size: 60px;'>Education at Risk: Mapping Climate Threats to Schools</h1>", unsafe_allow_html=True)

st.markdown("<div style='height: 62px;'></div>", unsafe_allow_html=True)

st.markdown("""
            **The climate crisis has a disproportionate and devastating impact on children's education globally.** Since 2022, more than 400 million students globally have been affected by temporary school closures because of climate-related events (World Bank, 2024). 
            To date, approximately 1 billion children live in areas at risk of extremely strong impacts by the climate crisis (UNICEF, 2021a). 
            Nevertheless, the impact of climate change on education systems is still frequently overlooked in climate policy agendas around the globe.
            Partially to blame is the fact that data at the intersection of climate and education is incredibly fragmented, massive data gaps exist, and available data remains underused (e.g., AidData, 2017).
            
            This project demonstrates a path to making this data more accessible: The **School Risk Index** takes complex data on climate hazards and measures the exposure schools,
            globally, face by these hazards. By harmonizing and standardizing this information through a number of
            steps outlined in detail in the methodology section of this report, the School Risk Index can serve as a
            simple but powerful indicator of where, globally, schools are most exposed to climate and weather
            hazards. Its simplicity makes it an attractive tool for decision-makers wishing to better understand school
            exposure and serves as an example for how existing data at the climate-education intersection can be
            processed and communicated thoughtfully.
            
            The School Risk Index was conceptualized and developed by Ole Siever and Madison Buchholz, graduate students at New York University's [Center for Urban Science and Progress](https://engineering.nyu.edu/research-innovation/centers/cusp) (NYU CUSP), 
            in collaboration with the [Institute for Development Impact](https://i4di.org) (I4DI).
""")



st.markdown("""
    <hr style="margin-top:48px; margin-bottom:32px;">

    <div style="display: flex; justify-content: center; align-items: center; gap: 60px; flex-wrap: wrap;">

    <div style="display: flex; align-items: center; gap: 16px;">
        <img src="https://olewelo.thegood.cloud/apps/files_sharing/publicpreview/j4RZ26SbKEqt2AY?file=/&fileId=8060&x=3024&y=1964&a=true&etag=1f2e4c08aba95fd7cf63e1188984a9bd" alt="Ole Siever" style="width:100px; height:100px; object-fit:cover; border-radius:50%; border:2px solid #ccc;">
        <div>
        <b>Ole Siever</b><br>
        <a href="mailto:ole.siever@nyu.edu">ole.siever@nyu.edu</a>
        </div>
    </div>

    <div style="display: flex; align-items: center; gap: 16px;">
        <img src="https://olewelo.thegood.cloud/apps/files_sharing/publicpreview/GBcgPxNZ3DNoNi9?file=/&fileId=8079&x=3024&y=1964&a=true&etag=1e09a35a5abf31d2dfac82934e492370" alt="Madison Buchholz" style="width:100px; height:100px; object-fit:cover; border-radius:50%; border:2px solid #ccc;">
        <div>
        <b>Madison Buchholz</b><br>
        <a href="mailto:madison.buchholz@nyu.edu">madison.buchholz@nyu.edu</a>
        </div>
    </div>

    </div>
""", unsafe_allow_html=True)