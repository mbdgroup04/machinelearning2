import streamlit as st
import google.generativeai as genai
from PIL import Image


# ✅ API Configuration
genai.configure(api_key="AIzaSyDcGbQEPqWiwrauiM96h7_uElQIlowUqmM")

# ✅ Load multimodal model
model = genai.GenerativeModel("gemini-1.5-flash")

# ✅ Session state for persistent chat + image
if "bird_image" not in st.session_state:
    st.session_state.bird_image = None
if "chat" not in st.session_state:
    st.session_state.chat = None
if "initial_response" not in st.session_state:
    st.session_state.initial_response = None
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🕊️ Bird Identifier + Gemini Chat")

# ✅ Image upload
uploaded_file = st.file_uploader("Upload a picture of a bird 🐦", type=["jpg", "jpeg", "png"])

# ✅ Load + show image
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Bird", use_container_width=True)

    # ✅ Save to session
    if st.session_state.bird_image is None:
        st.session_state.bird_image = image


prompt_template ="""
This is an image of a bird. Please identify the species and provide:
- Common name
- Scientific name
- Conservation status
- Country where it's most commonly found
- A short description including habitat, diet, and one fun fact
"""
# ✅ Identify bird ONCE
if st.session_state.bird_image and st.session_state.initial_response is None:
    with st.spinner("Identifying bird species..."):
        response = model.generate_content([st.session_state.bird_image, prompt_template])
        st.session_state.initial_response = response.text
        st.session_state.chat = model.start_chat(history=[
            {"role": "user", "parts": [prompt_template]},
            {"role": "model", "parts": [response.text]}
        ])
        st.success("Bird identified!")

# ✅ Show initial response
if st.session_state.initial_response:
    st.markdown(f"**🔍 The Birder says:** {st.session_state.initial_response}")
    st.divider()

# ✅ Chat
if st.session_state.chat:
    user_input = st.text_input("Ask a question about the bird", key="chat_input")

    if user_input:
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message([st.session_state.bird_image, user_input])
            st.session_state.history.append(("You", user_input))
            st.session_state.history.append(("The Birder", response.text))

    # ✅ Show history
    for speaker, msg in st.session_state.history:
        st.markdown(f"**{speaker}:** {msg}")
