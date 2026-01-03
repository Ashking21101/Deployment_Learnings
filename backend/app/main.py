from dotenv import load_dotenv
import os
from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from backend/.env into OS environment
load_dotenv()

# Create OpenAI client using API key from environment
# This key NEVER comes from frontend
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create FastAPI application
# This object receives ALL HTTP requests
app = FastAPI(title="Demo Backend")

# Add CORS middleware
# Required so browser-based React app (localhost:5173)
# can call backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (tighten in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model describing what frontend must SEND
class ChatRequest(BaseModel):
    message: str  # user input text

# Pydantic model describing what backend will RETURN
class ChatResponse(BaseModel):
    reply: str    # LLM response text

# Simple health check endpoint
# Used by cloud providers & for debugging
@app.get("/health")
def health():
    return {"status": "ok"}

# Simple GET endpoint to test frontend-backend connectivity
@app.get("/message")
def message():
    return {"message": "Hello from FastAPI 🚀"}

# Main chat endpoint used by frontend
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # Send user message to OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": req.message}
        ]
    )

    # Extract text reply from OpenAI response
    reply = response.choices[0].message.content

    # Return JSON response to frontend
    return {"reply": reply}
