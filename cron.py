import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timezone
# get the current date time
# connect to supabase
# run chron job to update

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

supabase.table("entries") \
        .insert({"created_at": datetime.now(timezone.utc).isoformat()}) \
        .execute()