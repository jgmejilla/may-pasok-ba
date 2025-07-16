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

# helper files
from scrapers import rappler
import classify_titles as ct


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


@app.get("/ping")
async def ping():
    date = datetime.now(timezone.utc).isoformat()
    response = (
        supabase.table("ping")
        .upsert({
            "id": 1, 
            "last_pinged": date,
        })
        .execute()
    )

    return response
    

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
        .upsert(articles, on_conflict=["link"], ignore_duplicates=True) 
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

@app.get("/classify")
async def classify():
    fetched = (
        supabase 
        .table("articles")
        .select("*")
        .order("time_scraped", desc=False)
        .eq("classified", False)
        .limit(20)
        .execute()
    )

    titles = [entry['title'] for entry in fetched.data]
    relevance = ct.classify(titles)

    for entry in fetched.data: 

        entry['classified'] = True
        entry['relevant'] = relevance[entry['title']]
        
        _ = (
            supabase
            .table('articles')
            .update({
                'classified': True,
                'relevant': relevance[entry['title']]
            }).eq('id', entry['id'])
            .execute()
        )

    
    relevant_articles = [article for article in fetched.data if article['relevant'] == True]

    if len(relevant_articles) == 0:
        return []

    needed_keys = {"time_scraped", "title", "link"}

    filtered_by_key = [
        {k: d[k] for k in needed_keys if k in d}
        for d in relevant_articles
    ]
    
    inserted = (
        supabase
        .table('suspensions')
        .insert(filtered_by_key)
        .execute()
    )

    return inserted
