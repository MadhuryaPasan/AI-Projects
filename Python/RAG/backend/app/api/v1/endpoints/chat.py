from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import asyncio
from app.helpers import generate_data_stream

from fastapi.responses import StreamingResponse

lock = asyncio.Lock()


# TODO: this part is the same as that in chat.py in helpers. create a reusable thing later
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


router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/test")
async def testmessage():
    return "This is a test message for chat api"


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    async def locked_stream():
        async with lock:
            async for chunk in generate_data_stream(request.messages):
                yield chunk
    # print(request.messages)
    return StreamingResponse(
        locked_stream(),
        media_type="text/event-stream",
        headers={
            "x-vercel-ai-data-stream": "v1",
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
