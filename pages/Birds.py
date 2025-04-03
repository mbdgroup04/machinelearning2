import streamlit as st
import pages.functions.Bird_Identif as bi
from PIL import Image

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

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:40px; font-weight:bold; ">Talk to The Birder!</p>', unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

user_input = st.chat_input("Ask me anything...")
uploaded_file1 = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
if uploaded_file1:
    uploaded_file=Image.open(uploaded_file1)

    if user_input or uploaded_file:
        user_message = {"role": "user", "content": user_input}
        if uploaded_file:
            user_message["image"] = uploaded_file
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
        ai_response = bi.generate_prompt_and_identify(uploaded_file)
        with st.chat_message("assistant"):
            st.markdown(ai_response)

if st.button("Clear Chat 🗑️"):
    st.session_state.messages = []
    st.rerun()