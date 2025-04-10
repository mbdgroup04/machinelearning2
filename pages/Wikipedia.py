import streamlit as st
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun

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
st.markdown(f'<p style="font-size:40px; text-align:center; font-weight:bold; ">Hotel Booking</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:20px; text-align:left; font-weight:bold; "><br></p>', unsafe_allow_html=True)

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
st.markdown(f"<p style='font-size:20px; text-align:left; '>Please insert the name of the bird you want to know more about:</p>", unsafe_allow_html=True)
bird=st.text_input("  ")
st.write(wikipedia.run(bird))