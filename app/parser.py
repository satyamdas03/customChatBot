import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Load intents file once
_intents_path = os.path.join(os.path.dirname(__file__), "intents.json")
with open(_intents_path, "r") as f:
    INTENTS = json.load(f)["intents"]

class ParseRequest(BaseModel):
    text: str

class ParseResponse(BaseModel):
    intent: str

router = APIRouter(prefix="/parse", tags=["Parsing"])

def parse_intent(text: str) -> str:
    """
    Naïve keyword matcher: looks for any example phrase in the input.
    Returns the first matching intent name, or 'unknown'.
    """
    text_l = text.lower()
    for intent in INTENTS:
        for example in intent["examples"]:
            if example in text_l:
                return intent["name"]
    return "unknown"

@router.post("/", response_model=ParseResponse)
async def parse_endpoint(req: ParseRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    intent = parse_intent(req.text)
    return {"intent": intent}
