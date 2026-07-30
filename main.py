import os
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import FastAPI, HTTPException, status, Header
from pydantic import BaseModel
# stage 0
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# stage 1


class AuthRequest(BaseModel):
    email: str | None = None
    password: str | None = None


app = FastAPI(title="Auth API")


@app.on_event("startup")
async def startup_event():
    print("Server running and connected to supabase")


@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(request: AuthRequest):
    # Implementation for signup logic
    if not request.email or not request.password:
        raise HTTPException(
            status_code=400, detail="Email and password are required")
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        return response.user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login", status_code=status.HTTP_200_OK)
async def login(request: AuthRequest):
    # Implementation for login logic
    if not request.email or not request.password:
        raise HTTPException(
            status_code=400, detail="Email and password are required")
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid login credentials")


# stage 2
@app.get("/public/info")
async def public_info():
    return {"message": "This is a public endpoint accessible without authentication."}


@app.get("/protected/profile")
async def protected_profile(authorization: str = Header(None)):
    if authorization is None or not authorization.startswith("Bearer"):
        raise HTTPException(
            status_code=401, detail="Access token required")
    token = authorization.split(" ")[1]
    return {"message": "token recieved", "token_preview": token[:20]}
