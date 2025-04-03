import streamlit as st
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
from langchain.prompts import PromptTemplate
from PIL import Image
import io
from dotenv import load_dotenv
import os

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

genai.configure(api_key='AIzaSyDPjZ0ukK3VYc1adVN5ruCaKlwxA5KfHrE')
model = genai.GenerativeModel("gemini-1.5-pro")
st.markdown(f'<p style="font-size:25px; text-align:left; "><br></p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:40px; font-weight:bold; ">Talk to The Birder!</p>', unsafe_allow_html=True)

class BirdingMemory(ConversationBufferMemory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._resolved_country = None
        self._resolved_capital = None
        self._resolved_origin_iata = None
        self._messages = []

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, value):
        self._messages = value

    @property
    def resolved_country(self): return self._resolved_country
    @resolved_country.setter
    def resolved_country(self, value): self._resolved_country = value

    @property
    def resolved_capital(self): return self._resolved_capital
    @resolved_capital.setter
    def resolved_capital(self, value): self._resolved_capital = value

    @property
    def resolved_origin_iata(self): return self._resolved_origin_iata
    @resolved_origin_iata.setter
    def resolved_origin_iata(self, value): self._resolved_origin_iata = value

if "memory" not in st.session_state:
    st.session_state.memory = BirdingMemory(return_messages=True)

if "last_bird_info" not in st.session_state:
    st.session_state.last_bird_info = None

memory = st.session_state.memory

prompt_template = PromptTemplate.from_template("""
This is an image of a bird. Please identify the species and provide:
- Common name
- Scientific name
- Conservation status
- Country where it's most commonly found
- A short description including habitat, diet, and one fun fact

Additional Observations:
{extra_info}
""")

def generate_prompt_and_identify(image_bytes, extra_info="N/A"):
    prompt = prompt_template.format(extra_info=extra_info)
    memory.messages.append(HumanMessage(content=prompt))

    response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
    answer = response.text.strip()

    memory.messages.append(AIMessage(content=answer))
    st.session_state.last_bird_info = answer

    return answer

for message in memory.messages:
    with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
        st.markdown(message.content)

uploaded_file = st.file_uploader("Upload an image of a bird", type=["png", "jpg", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)

    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)
    image_bytes = image_bytes.getvalue()

    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Identifying the bird..."):
        bird_info = generate_prompt_and_identify(image_bytes)
        memory.messages.append(AIMessage(content=bird_info))

    st.write("### 🦜 Bird Identification Result:")
    st.write(bird_info)

user_input = st.chat_input("Ask about birds or upload an image...")
if user_input:
    memory.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    if st.session_state.last_bird_info:
        user_input = f"Based on this bird information:\n\n{st.session_state.last_bird_info}\n\n{user_input}"

    chat_history = [msg.content for msg in memory.messages]
    response = model.generate_content(user_input)
    answer = response.text.strip()
    memory.messages.append(AIMessage(content=answer))

    with st.chat_message("assistant"):
        st.markdown(answer)

if st.button("🗑️ Clear Chat"):
    st.session_state.memory = BirdingMemory(return_messages=True)
    st.session_state.last_bird_info = None
    st.rerun()