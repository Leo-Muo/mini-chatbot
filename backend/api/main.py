from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import os

app = FastAPI(docs_url="/api/docs", redoc_url=None, openapi_url="/api/openapi.json")  

API_URL = os.getenv("API_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[API_URL], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = ollama.Client(
    host='http://localhost:11434',
)


class ChatRequest(BaseModel):
    message: str

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    response = client.chat(
        model='gunther',
        messages=[{"role": "user", "content": request.message}],
    )

    content = response["message"]["content"]
    
    return {"message": content}