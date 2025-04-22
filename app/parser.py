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

    """    Keyword matcher that picks the intent whose example (keyword/phrase)
    is the longest match in the input. Falls back to 'unknown'.
    """
    text_l = text.lower()
    matches = []
    for intent in INTENTS:
        for example in intent["examples"]:
            if example in text_l:
                # record (intent_name, length_of_match)
                matches.append((intent["name"], len(example)))
    if not matches:
        return "unknown"
    # pick the intent whose example is the longest phrase
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[0][0]

    


@router.post("/", response_model=ParseResponse)
async def parse_endpoint(req: ParseRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    intent = parse_intent(req.text)
    return {"intent": intent}
