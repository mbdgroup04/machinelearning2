import streamlit as st
import pages.functions.Flight_Recommend as flrec
import pages.Birds as bdid

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

capital_given='Madrid'
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Flight Booking</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Get ready to be within eyesight of your favorite birds in the world, here are some flight suggestions to fly to {capital_given} so you can be as near as possible to the place where your favorite birds live and take the best pictures so you can always remember the experience you lived!</p>", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the continent your bird lives in:</p>", unsafe_allow_html=True)
continent_chosen = st.selectbox("", ['Choose a continent','Africa','Americas','Antartica','Asia','Europe','Oceania'])
if continent_chosen!='Choose a continent':
    st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the capital of the country your bird lives in:</p>", unsafe_allow_html=True)
    if continent_chosen=='Africa':
        capital_chosen=st.selectbox("",['Abuja','Accra','Addis Abba','Algiers','Antananarivo','Asmera','Bamako','Bangui','Banjul','Bissau','Brazzaville','Bujumbura','Cairo','Conakry','Dakar','Dar es Salaam','Dijibouti City','Freetown','Gaborone','Harare','Juba','Kampala','Khartoum','Kigali','Kinshasa','Libreville','Lilongwe','Lome','Luanda','Lusaka','Malabo','Maputo','Maseru','Mbabane','Mogadishu','Monrovia','Moroni','Nairobi',"N'Djamena",'Niamey','Nouakchott','Ouagadougou','Port Louis','Pretoria','Porto Novo','Praia','Rabat','Tripoli','Tunis','Victoria','Windhoek','Yamoussoukro','Yaoundé'])
    elif continent_chosen=='Antartica':
        capital_chosen=st.selectbox("",['Antartica'])
    elif continent_chosen=='Asia':
        capital_chosen=st.selectbox("",['Abu Dhabi','Amman','Ankara','Ashgabat','Nur-Sultan','Baghdad','Baku','Bandar Seri Begawan','Bangkok','Beijing','Beirut','Bishkek','Colombo Kotte','Damascus','Dhaka','Dili','Doha','Dushanbe','Hanoi','Islamabad','Jakarta','Jerusalem','Kabul','Kathmandu','Kuala Lumpur','Kuwait-City','Lhasa','Malé','Manama','Manila','Moscow','Muscat','Naypyidaw','New Delhi','Phnom Penh',"P'yongyang",'Riyadh','Sanaa','Seoul ','Singapore','Taipei','Tashkent',"T'bilisi","Tehran","Thimphu",'Tokyo','Ulaanbaatar','Vientiane','Yerevan'])
    elif continent_chosen=='Europe':
        capital_chosen=st.selectbox("",['Amsterdam','Andorra La Vella','Athens ','Belgrade','Berlin','Bern','Bratislava','Brussels','Bucharest','Budapest','Chisinau','Copenhaguen','Dublin','Helsinki','Kiev','Lisbon','Ljubljana','London','Luxembourg ','Madrid','Minsk','Moncao','Moscow','Nicosia','Nuuk','Oslo','Paris','Podgorica','Prague','Reykjavik','Riga','Rome','San Marino','Sarajevo','Skopje',"Sofia",'Stockholm','Tallinn','Tirana','Vaduz','Valletta','Vatican City',"Vienna","Vilnius","Warsaw",'Zagreb'])
    elif continent_chosen=='Americas':
        capital_chosen=st.selectbox("",['Asunción','Basseterre','Belmopan','Bogotá','Brasilia','Bridgetown','Buenos Aires','Caracas','Castries','Georgetown','Guatemala City','Havana','Kingston','Kingstown','La Paz','Lima','Managua','México City','Montevideo','Nassau','Ottawa','Panamá City','Paramaribo','Port au Prince','Port of Spain','Quito','Roseau',"Saint George's","Saint John's",'San José','San Salvador','Santiago','Santo Domingo','Tegucigalpa','Washington D.C.'])
    elif continent_chosen=='Oceania':
        capital_chosen=st.selectbox("",['Adamstown','Alofi','Apia','Avarua','Canberra','Hagåtña','Funafuti','Honiara','Majuro','Ngerulmud','Nouméa',"Nuku'alofa",'Pago Pago','Palikir','Papeete','Port Moresby','Port Vila','Saipan','Suva','Tarawa','Wellington'])
        