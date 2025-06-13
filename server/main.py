# FastAPI skeleton
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Supabase interactions
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import requests 
import json

# webscraping using BeautifulSoup
from server.scrapers import rappler

# initialize app
load_dotenv() 
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize database connection
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# pathing
HOST_ROOT = "https://may-pasok-ba.onrender.com"
LOCAL_ROOT = "http://localhost:8000/"

# --------------------
# endpoints begin here 
# --------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    date = datetime.now(timezone.utc).isoformat()
    response = (
        supabase.table("tests") 
        .update({
            "last_modified": date,
        }) 
        .eq("response", "spin") 
        .execute()
    )
    
    return response

@app.get("/scrape")
async def scrapers():
    articles = rappler()

    response = (
        supabase 
        .table("articles") 
        .upsert(articles, on_conflict=["link"]) 
        .execute()
    )
    
    return response

@app.get("/clear")
async def clear():
    # clears articles over 3 days of age
    three_days_ago = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    
    response = (
        supabase
        .table("articles")
        .delete()
        .lt("time_scraped", three_days_ago)
        .execute()
    )
    
    return response