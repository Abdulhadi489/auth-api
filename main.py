import os
from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Auth API")


@app.on_event("startup")
async def startup_event():
    print("Server running and connected to supabase")
