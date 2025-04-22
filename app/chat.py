# app/chat.py
import os, json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai

# load key
openai.api_key = os.getenv("OPENAI_API_KEY")

# models
class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str

router = APIRouter(prefix="/chat", tags=["Chat"])

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
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role":"user","content":req.user_input}],
            functions=function_defs,
            function_call="auto"
        )
        msg = resp.choices[0].message

        if msg.get("function_call"):
            fn_name = msg["function_call"]["name"]
            args = json.loads(msg["function_call"]["arguments"])

            if fn_name == "turn_on_device":
                result = turn_on_device(args["device_name"])
            elif fn_name == "turn_off_device":
                result = turn_off_device(args["device_name"])
            else:
                raise HTTPException(400, f"Unknown function: {fn_name}")

            return {"response": result}

        # Otherwise just return the model’s chat reply
        return {"response": msg["content"]}

    except Exception as e:
        raise HTTPException(500, str(e))
