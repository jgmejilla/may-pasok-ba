from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
from google import genai
import os

# load .env from parent directory
load_dotenv(dotenv_path="../.env")

app = FastAPI()

@app.get("/classify-excerpt", response_class=PlainTextResponse)
async def root():
    client = genai.Client(api_key=os.getenv("API_KEY"))
    prompt = '''
    Respond in the following format: ["ExampleOne, "ExampleTwo"]. Do not include anything else.
    The array strings must be a member of the following list: [Caloocan, Malabon, Navotas, Valenzuela, Quezon City, Marikina, Pasig, Taguig, Makati, Manila, Mandaluyong, San Juan, Pasay, Parañaque, Las Piñas, Muntinlupa]
    Given an excerpt, identify which of the aformentioned places there is a suspension. Only include it if it is guaranteed.
    If nation-wide suspension, response with the entire list
    If no suspension, respond with empty list
    '''.strip()

    contents = '''Walang pasok ang lahat ng lugar maliban sa Caloocan City.
    '''.strip()
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f'{prompt}\n{contents}'
    )
    return response.text

