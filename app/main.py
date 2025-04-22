import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()

#include parsing router
from app.parser import router as parse_router
app.include_router(parse_router)

#include action router
from app.actions import router as action_router
app.include_router(action_router)

# include the chat endpoint
from app.chat import router as chat_router
app.include_router(chat_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/env")
async def show_env():
    return {"openai_key_present": bool(os.getenv("OPENAI_API_KEY"))}

@app.get("/")
async def root():
    return {"message": "Welcome to Custom Chatbot API"}
