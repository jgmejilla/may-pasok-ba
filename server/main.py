from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone
import requests 
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# endpoints begin here 
# --------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}