import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
from typing import Optional, List, Dict
from uuid import uuid4

# Simple in‑process context store: { session_id: [ {role, content}, … ] }
CONVERSATIONS: dict[str, list[dict]] = {}

# load key
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    session_id: Optional[str] = None    # client‑generated or you fallback to UUID
    user_input: str

class ChatResponse(BaseModel):
    session_id: str                     # echo back so client can reuse
    response: str
    history: List[dict]  # (optional) full message history if you want

router = APIRouter(prefix="/chat", tags=["Chat"])

# function definitions for OpenAI
function_defs = [
    {
        "name": "turn_on_device",
        "description": "Turn on a device by name",
        "parameters": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Name of the device to turn on"
                }
            },
            "required": ["device_name"]
        }
    },
    {
        "name": "turn_off_device",
        "description": "Turn off a device by name",
        "parameters": {
            "type": "object",
            "properties": {
                "device_name": {
                    "type": "string",
                    "description": "Name of the device to turn off"
                }
            },
            "required": ["device_name"]
        }
    }
]

from app.functions import turn_on_device, turn_off_device

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        # Determine or create session
        sid = req.session_id or str(uuid4())
        history = CONVERSATIONS.get(sid, [])

        # Append the new user message to history
        history.append({"role": "user", "content": req.user_input})

        # Build the messages payload: system + past turns
        messages = [
            {"role": "system", "content": "You are a helpful home‑automation assistant."}
        ] + history

        # Call the LLM with function metadata
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=function_defs,
            function_call="auto"
        )
        msg = resp.choices[0].message

        # If the model decided to call a function, execute it
        if msg.function_call:
            fn_name = msg.function_call.name
            args = json.loads(msg.function_call.arguments)

            if fn_name == "turn_on_device":
                result = turn_on_device(args["device_name"])
            elif fn_name == "turn_off_device":
                result = turn_off_device(args["device_name"])
            else:
                raise HTTPException(400, f"Unknown function: {fn_name}")
        else:
            # Otherwise use the model’s reply
            result = msg.content

        # Append assistant’s response to history and save
        assistant_msg = {"role": "assistant", "content": result}
        history.append(assistant_msg)
        CONVERSATIONS[sid] = history

        # Return the session ID, response, and updated history
        return ChatResponse(
            session_id=sid,
            response=result,
            history=history
        )

    except Exception as e:
        raise HTTPException(500, str(e))
