# app/actions.py
import os
import json
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Pydantic models
class ActionRequest(BaseModel):
    intent: str
    entity: Optional[str] = None

class ActionResponse(BaseModel):
    result: str

# Router
router = APIRouter(prefix="/action", tags=["Action"])

# import your functions
from app.functions import turn_on_device, turn_off_device

@router.post("/", response_model=ActionResponse)
async def action_endpoint(req: ActionRequest):
    intent = req.intent
    entity = req.entity

    if intent == "turn_on_device":
        if not entity:
            raise HTTPException(400, "No device specified for turn_on_device")
        result = turn_on_device(entity)

    elif intent == "turn_off_device":
        if not entity:
            raise HTTPException(400, "No device specified for turn_off_device")
        result = turn_off_device(entity)

    else:
        # you can add more intents here
        raise HTTPException(400, f"Unhandled intent: {intent}")

    return {"result": result}
