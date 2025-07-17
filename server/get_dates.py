from google import genai
import os
from dotenv import load_dotenv



def get_dates(article):
    load_dotenv(dotenv_path=".env")
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    
    prompt = '''
    ROLE: You are a robot that automates classifying an article by processing it according to the instructions below:
    Respond in the following format: [Example1:Date1\nExplain2:Date2\n]. Do not include anything else.
    The array strings must be a member of the following list: [Caloocan, Malabon, Navotas, Valenzuela, Quezon City, Marikina, Pasig, Taguig, Makati, Manila, Mandaluyong, San Juan, Pasay, Parañaque, Las Piñas, Muntinlupa]
    For each place above in which there is a suspension, add a line <Place>:<Date>
    If none of the places above have a suspension (e.g. only areas in Visayas have a suspension), respond with None
    '''.strip()

    contents = article.strip()

    
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f'{prompt}\n{contents}'
    )    

    return response.text

