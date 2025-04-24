import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
from typing import Optional, List, Dict, Any
from uuid import uuid4

# In-memory stores:
#   CONVERSATIONS[sid]     → chat history list
#   CONVERSATIONS[f"{sid}_doc"] → Slate document model
CONVERSATIONS: dict[str, list[dict]] = {}

# Load OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_input: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: List[Dict[str, Any]]
    document: Optional[List[Dict[str, Any]]] = None

router = APIRouter(prefix="/chat", tags=["Chat"])

# OpenAI function definitions
function_defs = [
    # … your other functions if still needed …
    {
        "name": "set_font_size",
        "description": "Set the font size of a specific paragraph in the document.",
        "parameters": {
            "type": "object",
            "properties": {
                "paragraph_index": {
                    "type": "integer",
                    "description": "Zero-based index of the paragraph to resize."
                },
                "size": {
                    "type": "number",
                    "description": "New font size (in points)."
                }
            },
            "required": ["paragraph_index", "size"]
        }
    },
    {
        "name": "toggle_bold",
        "description": "Toggle bold styling on a specific paragraph.",
        "parameters": {
            "type": "object",
            "properties": {
                "paragraph_index": {
                    "type": "integer",
                    "description": "Zero-based index of the paragraph to toggle bold."
                }
            },
            "required": ["paragraph_index"]
        }
    },
    {
        "name": "align_paragraph",
        "description": "Set the alignment of a specific paragraph.",
        "parameters": {
            "type": "object",
            "properties": {
                "paragraph_index": {
                    "type": "integer",
                    "description": "Zero-based index of the paragraph to align."
                },
                "alignment": {
                    "type": "string",
                    "enum": ["left", "center", "right", "justify"],
                    "description": "Desired text alignment."
                }
            },
            "required": ["paragraph_index", "alignment"]
        }
    }
]

# Import your formatting stubs
from app.formatting import set_font_size, toggle_bold, align_paragraph

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        # 1. Determine session and load history + doc
        sid = req.session_id or str(uuid4())
        history = CONVERSATIONS.get(sid, [])
        current_doc = CONVERSATIONS.get(f"{sid}_doc", [])

        # 2. Append user message
        history.append({"role": "user", "content": req.user_input})

        # 3. Build the prompt
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that edits a rich-text document model. "
                           "When given a natural-language command, call the appropriate function."
            }
        ] + history

        # 4. Call the OpenAI function-calling API
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            functions=function_defs,
            function_call="auto"
        )
        msg = resp.choices[0].message

        # 5. Dispatch to formatting stubs
        if msg.function_call:
            fn = msg.function_call.name
            args = json.loads(msg.function_call.arguments)

            if fn == "set_font_size":
                new_doc = set_font_size(current_doc, args["paragraph_index"], args["size"])
                result = "Font size updated."
            elif fn == "toggle_bold":
                new_doc = toggle_bold(current_doc, args["paragraph_index"])
                result = "Toggled bold."
            elif fn == "align_paragraph":
                new_doc = align_paragraph(
                    current_doc, args["paragraph_index"], args["alignment"]
                )
                result = f"Paragraph aligned {args['alignment']}."
            else:
                raise HTTPException(400, f"Unknown function: {fn}")
        else:
            # No function call → just a chat reply and doc stays the same
            new_doc = current_doc
            result = msg.content or ""

        # 6. Persist history and updated doc
        history.append({"role": "assistant", "content": result})
        CONVERSATIONS[sid] = history
        CONVERSATIONS[f"{sid}_doc"] = new_doc

        # 7. Return everything
        return ChatResponse(
            session_id=sid,
            response=result,
            history=history,
            document=new_doc,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
