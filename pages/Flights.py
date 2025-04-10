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
    "The Birder AI": "pages/Birds.py",
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
    response = requests.get('http://api.aviationstack.com/v1/flights', params=params)

    if response.status_code != 200:
        return f'Sorry, there was an error: {response.status_code}'
    flights = response.json()
    for flight in flights['data']:
        if flight['departure']['iata'] == origin and flight['arrival']['iata'] == destination:
            departure_time = datetime.datetime.fromisoformat(flight['departure']['scheduled'][:-6])
            flight_date = departure_time.date()
            flight_time = departure_time.time()
            departing_airport= flight['departure']['airport']
            arriving_airport=flight['arrival']['airport']
            flight_list=[flight_date,flight_time,departing_airport,arriving_airport]
            return flight_list
    return "No matching flights found."

st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Flight Booking</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Get ready to be within eyesight of your favorite birds in the world, here are some flight suggestions to fly to the capital of your choosing so you can be as near as possible to the place where your favorite birds live and take the best pictures so you can always remember the experience you lived!</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the iata of the city you want to fly from:</p>", unsafe_allow_html=True)
origin_cap = st.text_input("")
st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the iata of the city you want to fly to:</p>", unsafe_allow_html=True)
dest_cap=st.text_input(" ")
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
if origin_cap and dest_cap:
    answer=get_top_flights(origin_cap,dest_cap,'a3a072bdadf1cb65bd0686e36852892a')
    st.markdown(f"<p style='font-size:30px; text-align:left; '><b>Congrats! There is a flight from {answer[2]} to {answer[3]} on the {answer[0]} at {answer[1]}. Make sure you don't miss it!</b></p>", unsafe_allow_html=True)
    