import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()  

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/env")
async def show_env():
    return {"openai_key_present": bool(os.getenv("OPENAI_API_KEY"))}
