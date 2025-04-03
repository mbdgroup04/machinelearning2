import os
import requests
from PIL import Image
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
import logging
from dotenv import load_dotenv

logging.basicConfig(
    filename='app.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv("functions/api.env")
logging.info('API Key and authenticator set up correctly.')

genai.configure(api_key=os.getenv('TMBD_API_KEY3'))
model = genai.GenerativeModel("gemini-1.5-pro")

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

memory = ConversationBufferMemory(return_messages=True)

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

memory = BirdingMemory(return_messages=True)

def generate_prompt_and_identify(data):
    image = data["image"]
    user_input = data.get("user_input", {})

    extras = []
    if user_input.get("color"): extras.append(f"Color: {user_input['color']}")
    if user_input.get("size"): extras.append(f"Size: {user_input['size']}")
    if user_input.get("behavior"): extras.append(f"Behavior: {user_input['behavior']}")
    if user_input.get("location"): extras.append(f"Location: {user_input['location']}")
    if user_input.get("origin"): extras.append(f"Origin: {user_input['origin']}")  # <-- NEW LINE

    extra_info = ", ".join(extras) if extras else "N/A"

    prompt = prompt_template.format(extra_info=extra_info)

    memory.chat_memory.add_user_message(prompt)

    response = model.generate_content([prompt, image])
    answer = response.text

    memory.chat_memory.add_ai_message(answer)

    return answer

# ✅ Wrap the function in a LangChain Runnable
identify_chain = RunnableLambda(generate_prompt_and_identify)

# ✅ Country extraction
def extract_country_llm(gemini_model) -> str:
    if memory.resolved_country:
        return memory.resolved_country
    for msg in reversed(memory.messages):
        if isinstance(msg, AIMessage):
            description = msg.content.strip()
            break
    else:
        return None
    prompt = f"Suggest a country where this bird is commonly seen based on this description:\n\"{description}\""
    response = gemini_model.generate_content(prompt)
    country = response.text.strip()
    memory.resolved_country = country
    return country

# ✅ Capital lookup
def get_capital_city_with_gemini(country: str, gemini_model) -> str:
    if memory.resolved_capital:
        return memory.resolved_capital
    prompt = f"What is the capital city of {country}? Return only the name."
    response = gemini_model.generate_content(prompt)
    capital = response.text.strip()
    memory.resolved_capital = capital
    return capital

# ✅ Origin to IATA
def resolve_origin_to_iata(user_input, gemini_model):
    if memory.resolved_origin_iata:
        return memory.resolved_origin_iata
    prompt = f"Extract the IATA airport code from: \"{user_input}\""
    response = gemini_model.generate_content(prompt)
    iata = response.text.strip().upper()
    if len(iata) == 3:
        memory.resolved_origin_iata = iata
        return iata
    return None

# ✅ Flights API
def get_top_flights(origin: str, destination: str, access_key: str):
    params = {'access_key': access_key, 'dep_iata': origin, 'arr_iata': destination, 'limit': 10}
    response = requests.get('http://api.aviationstack.com/v1/flights', params=params)
    if response.status_code != 200:
        return []
    flights = response.json().get('data', [])
    scheduled = [f for f in flights if f.get("flight_status") == "scheduled"][:3]
    return [
        f"{f['airline']['name']} {f['flight']['iata']} → {f['departure']['airport']} to {f['arrival']['airport']} (Status: {f['flight_status']})"
        for f in scheduled
    ]

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# ✅ Simplified Run Flow without Agents
if __name__ == "__main__":
    test_image = Image.open("data/bird1.jpg")  # Replace with actual image path
    result = identify_chain.invoke({
        "image": test_image,
        "user_input": {
            "color": "blue",
            "size": "small",
            "behavior": "flying",
            "location": "Costa Rica"
        }
    })
    print("\n🕊️ Bird Identification:\n", result)