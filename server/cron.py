# get the current date time
# connect to supabase
# run chron job to update

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone
import requests 
import json


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

# prevent api from spinning down 
response = requests.get(f"https://may-pasok-ba.onrender.com/?nocache={datetime.now()}")
supabase.table("entries") \
        .insert({
            "created_at": datetime.now(timezone.utc).isoformat(), 
            "response": response.json()['message']
        }) \
        .execute()



