import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

from fastapi_clerk_auth import (
    ClerkConfig,
    ClerkHTTPBearer,
    HTTPAuthorizationCredentials,
)

# -----------------------------------
# Load environment variables
# -----------------------------------
load_dotenv()

# -----------------------------------
# Create FastAPI app
# -----------------------------------
app = FastAPI(title="Chatbot Backend")

# -----------------------------------
# CORS CONFIGURATION (VERY IMPORTANT)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",              # Local Vite frontend
        "https://your-frontend-domain",       # 👈 replace (explained below)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],                     # Required for Authorization header
)

# -----------------------------------
# Clerk Authentication Setup
# -----------------------------------
clerk_config = ClerkConfig(
    jwks_url=os.getenv("CLERK_JWKS_URL")
)

clerk_guard = ClerkHTTPBearer(clerk_config)

# -----------------------------------
# OpenAI Client
# -----------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------
# Schemas
# -----------------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# -----------------------------------
# Health check (PUBLIC)
# -----------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------------
# Protected Chat Endpoint
# -----------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    creds: HTTPAuthorizationCredentials = Depends(clerk_guard),
):
    """
    This route is protected by Clerk.
    If this function runs:
    - JWT is valid
    - User is authenticated
    """

    # Unique Clerk user ID
    user_id = creds.decoded["sub"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"User ID: {user_id}"},
            {"role": "user", "content": req.message},
        ],
    )

    reply = response.choices[0].message.content
    return {"reply": reply}






