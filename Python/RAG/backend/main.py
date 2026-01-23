import os
import json
from typing import List, Union, Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain Imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# --- INITIALIZATION ---
load_dotenv()

app = FastAPI()

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Variables
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

# Initialize LangChain LLM
llm = ChatOpenAI(
    model=MODEL_NAME,
    base_url=BASE_URL,
    api_key=API_KEY,
)

# --- MODELS ---

class MessagePart(BaseModel):
    """
    Represents a specific part of a message (text, tool call, etc.)
    Matches Vercel AI SDK Core 'Message' interface.
    """
    type: str
    text: str = ""  # Default to empty string if not a text part

class Message(BaseModel):
    """
    Represents a full chat message containing multiple parts.
    Used for AI SDK 5/6 compatibility.
    """
    role: str
    parts: List[MessagePart]

class ChatRequest(BaseModel):
    """Schema for the incoming POST request body."""
    messages: List[Message]

# --- UTILS ---

def convert_to_langchain_messages(messages: List[Message]):
    """
    Maps incoming Vercel AI SDK message formats to LangChain's 
    HumanMessage and AIMessage objects.
    """
    lc_messages = []
    for m in messages:
        # Extract and join all text parts within a single message
        text_content = "".join([p.text for p in m.parts if p.type == "text"])

        if m.role == "user":
            lc_messages.append(HumanMessage(content=text_content))
        elif m.role == "assistant":
            lc_messages.append(AIMessage(content=text_content))
    return lc_messages

# --- STREAMING LOGIC ---

async def generate_data_stream(messages: List[Message]):
    """
    Generator that yields data formatted for the 
    Vercel AI SDK Data Stream Protocol (v1).
    """
    lc_messages = convert_to_langchain_messages(messages)
    print("\n\n======================generate_data_stream:lc_messages=========================")
    print(lc_messages)
    print("===============================================\n\n")
    # todo: add the real text_id later
    text_id = "text_0"

    # 1. Signal the start of a text block
    yield f'data: {json.dumps({"type": "text-start", "id": text_id})}\n\n'

    # 2. Stream chunks from LangChain LLM
    async for chunk in llm.astream(lc_messages):
        if chunk.content:
            payload = {"type": "text-delta", "id": text_id, "delta": chunk.content}
            yield f"data: {json.dumps(payload)}\n\n"

    # 3. Signal the end of the text block and finish the stream
    yield f'data: {json.dumps({"type": "text-end", "id": text_id})}\n\n'
    yield f'data: {json.dumps({"type": "finish", "finishReason": "stop"})}\n\n'
    
    # 4. Final stop signal
    yield "data: [DONE]\n\n"

# --- ENDPOINTS ---

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Main endpoint for chat interactions. 
    Returns a Server-Sent Events (SSE) stream.
    """
    print("\n\n======================chat_endpoint=========================")
    print(request.messages)
    print("===============================================\n\n")
    return StreamingResponse(
        generate_data_stream(request.messages),
        media_type="text/event-stream",
        headers={
            # Required header for Vercel AI SDK to recognize the stream format
            "x-vercel-ai-data-stream": "v1",
            "Cache-Control": "no-cache",
        },
    )