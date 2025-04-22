import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional 

# Load intents file once
_intents_path = os.path.join(os.path.dirname(__file__), "intents.json")
with open(_intents_path, "r") as f:
    INTENTS = json.load(f)["intents"]

with open(os.path.join(os.path.dirname(__file__), "entities.json"), "r") as f:
    ENTITIES = json.load(f)["devices"]

class ParseRequest(BaseModel):
    text: str

class ParseResponse(BaseModel):
    intent: str
    entity: Optional[str] = None

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

def extract_entity(text: str) -> Optional[str]:
    text_l = text.lower()
    # find the longest matching device name
    matches = [dev for dev in ENTITIES if dev in text_l]
    if not matches:
        return None
    return sorted(matches, key=len, reverse=True)[0]


@router.post("/", response_model=ParseResponse)
async def parse_endpoint(req: ParseRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    intent = parse_intent(req.text)
    # return {"intent": intent}
    entity = extract_entity(req.text)
    return {"intent": intent, "entity": entity}
