import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage

logging.basicConfig(
    filename='app.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv("functions/api.env")
logging.info('API Key and authenticator set up correctly.')

genai.configure(api_key=os.getenv('TMBD_API_KEY'))

model = genai.GenerativeModel("gemini-1.5-pro")
chat_history = []

def identify_bird_with_gemini(image, user_input=None) -> str:
    try:
        image_rgb = image

        prompt = (
            "This is an image of a bird. Please identify the species and provide:\n"
            "- Common name\n"
            "- Scientific name\n"
            "- Conservation status\n"
            "- Country where it's most commonly found\n"
            "- A short description including habitat, diet, and one fun fact"
        )

        if user_input:
            extras = []
            if user_input.get("color"): extras.append(f"Color: {user_input['color']}")
            if user_input.get("size"): extras.append(f"Size: {user_input['size']}")
            if user_input.get("behavior"): extras.append(f"Behavior: {user_input['behavior']}")
            if user_input.get("location"): extras.append(f"Location: {user_input['location']}")
            if extras:
                prompt += "\nAdditional observations: " + ", ".join(extras)

        chat_history.append(prompt)
        chat_history.append(image_rgb)

        response = model.generate_content(chat_history)
        reply = response.text.strip()

        chat_history.append(reply)
        return reply

    except Exception as e:
        print("Error in identify_bird_with_gemini:", e)
        return "Failed to identify bird."


def chat_followup_with_gemini(user_query: str) -> str:
    try:
        chat_history.append(user_query)
        response = model.generate_content(chat_history)
        reply = response.text.strip()
        chat_history.append(reply)
        return reply

    except Exception as e:
        print("Error in chat_followup_with_gemini:", e)
        return "Failed to get a follow-up response."