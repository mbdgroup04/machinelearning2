import streamlit as st
import requests
import google.generativeai as genai
import os
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
    "Bird Information": "pages/Birds.py",
    "Flights": None,
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

def resolve_origin_to_iata(user_input, gemini_model):
    prompt = f"Extract the IATA airport code from: \"{user_input}\""
    response = gemini_model.generate_content(prompt)
    iata = response.text.strip().upper()
    if len(iata) == 3:
        return iata
    return None
def get_top_flights(origin: str, destination: str, access_key: str):
    params = {'access_key': access_key, 'limit': 10}
    response = requests.get('http://api.aviationstack.com/v1/flights',params=params)
    if response.status_code != 200:
        return f'Sorry, there was an error: {response.status_code}'
    flights = response.json()
    a=0
    for i in flights:
        if i['data'][0]['departure']['iata']==origin and i['data'][0]['arrival']['iata']==destination:
            a=1
    if a==1:
        return f'You have a flight from {origin} to {destination} on the {datetime.datetime.fromisoformat(flights[flights['data'][0]['departure']['iata']==origin]['data'][0]['departure']['scheduled']).date()} at {datetime.datetime.fromisoformat(flights[flights['data'][0]['departure']['iata']==origin]['data'][0]['departure']['scheduled']).time()}'

st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Flight Booking</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Get ready to be within eyesight of your favorite birds in the world, here are some flight suggestions to fly to the capital of your choosing so you can be as near as possible to the place where your favorite birds live and take the best pictures so you can always remember the experience you lived!</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the iata of the city you want to fly from:</p>", unsafe_allow_html=True)
origin_cap = st.text_input("")
st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the iata of the city you want to fly to:</p>", unsafe_allow_html=True)
dest_cap=st.text_input(" ")

if orig_iata and dest_iata:
    st.write(get_top_flights(orig_iata,dest_iata,'a3a072bdadf1cb65bd0686e36852892a'))