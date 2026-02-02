import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import SecretStr, BaseModel
from typing import List
from langchain_core.messages import HumanMessage, AIMessage
from app.helpers import prompt_with_context
import json

# loading env variables
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME") or ""
BASE_URL = os.getenv("BASE_URL") or ""
API_KEY = os.getenv("API_KEY") or ""

# loading the model
model = ChatOpenAI(model=MODEL_NAME, base_url=BASE_URL, api_key=SecretStr(API_KEY), temperature=0.9)
prompt = (
    "You have access to a tool that retrieves context form documents. "
    "Use the tool to help answer user queries."
)
# loading the agent
agent = create_agent(
    model=model, tools=[], system_prompt=prompt, middleware=[prompt_with_context]
)


# TODO: this part is the same as that in chat.py in endpoint. create a reusable thing later
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


def convert_to_langchain_messages(messages: List[Message]):
    lc_messages = []
    for message in messages:
        text_content = "".join([p.text for p in message.parts if p.type == "text"])
        if message.role == "user":
            lc_messages.append(HumanMessage(content=text_content))
        elif message.role == "assistant":
            lc_messages.append(AIMessage(content=text_content))
    return lc_messages


async def generate_data_stream(messages: List[Message]):
    lc_messages = convert_to_langchain_messages(messages)

    # todo: add the real text_id later
    text_id = "text_0"

    # Start signal
    yield f"data: {json.dumps({'type': 'text-start', 'id': text_id})}\n\n"

    # generating stream message
    async for chunk, metadata in agent.astream(
        # {"messages": [{"role": "user", "content": "Tell me a Dad joke"}]},
        {"messages": lc_messages},
        stream_mode="messages",
    ):
        if chunk.content:
            payload = {"type": "text-delta", "id": text_id, "delta": chunk.content}
            yield f"data: {json.dumps(payload)}\n\n"

    yield f"data: {json.dumps({'type': 'text-end', 'id': text_id})}\n\n"

    yield f"data: {json.dumps({'type': 'finish', 'finishReason': 'stop'})}\n\n"

    # Final stop signal
    yield "data: [DONE]\n\n"
