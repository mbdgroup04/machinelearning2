import re
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

load_dotenv("functions/api.env")
logging.info('API Key and authenticator set up correctly.')

genai.configure(api_key=os.getenv('TMBD_API_KEY2'))

genai.configure(api_key="AIzaSyD6KquAOd7uimtfMgDqkxz-v-EKDUCnUf4")
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

def extract_capital_with_gemini(chat_history: list, gemini_model) -> str:
    try:
        for msg in reversed(chat_history):
            if isinstance(msg, str) and "Common name" in msg and "Country" in msg:
                prompt = (
                    "From the following bird description, return only the capital city of the country "
                    "where the bird is most commonly found. Do not include any explanation or extra text — "
                    "just return the capital city name:\n\n"
                    f"{msg}"
                )
                response = gemini_model.generate_content(prompt)
                capital = response.text.strip()
                return capital
        return None
    except Exception as e:
        print("❌ Error using Gemini to extract capital city:", e)
        return None
