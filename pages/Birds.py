import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pages.functions.PySimFin as psf
import datetime

st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] ul {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

PAGES = {
    "Home": "Home.py",
    "Bird Information": None,
    "Flights": "pages/Flights.py",
    "Hotels": "pages/Hotels.py",
    "Team": "pages/Team.py"
}

for page_name, file_path in PAGES.items():
    if file_path:
        st.sidebar.page_link(file_path, label=page_name)
    else:
        st.sidebar.write(f"### {page_name}")

col1,col2,col3=st.columns(3)
with col2:
    st.image("data/logo.png", width=200)
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Bird Information</p>', unsafe_allow_html=True)
