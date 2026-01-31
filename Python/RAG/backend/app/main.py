from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Simple Rag app v1")
# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

















# # from components import retrieve_context
# from components import prompt_with_context
# import asyncio
# import json
# import os
# from typing import List

# from dotenv import load_dotenv
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from langchain.agents import create_agent
# from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
# from pydantic import BaseModel, SecretStr

# from helpers import ollama_localmodels

# lock = asyncio.Lock()  # to lock multiple requests

# load_dotenv()
# app = FastAPI()

# # Configure CORS for frontend communication
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Environment Variables
# MODEL_NAME = os.getenv("MODEL_NAME") or ""
# BASE_URL = os.getenv("BASE_URL") or ""
# API_KEY = os.getenv("API_KEY") or ""

# llm = ChatOpenAI(model=MODEL_NAME, base_url=BASE_URL, api_key=SecretStr(API_KEY))


# # tools = [retrieve_context]
# # If desired, specify custom instructions
# prompt = (
#     "You have access to a tool that retrieves context from a blog post. "
#     # "You have access to a tool that retrieves context from a blog post. "
#     "Use the tool to help answer user queries."
# )
# agent = create_agent(
#     model=llm,
#     tools=[],
#     system_prompt=prompt,
#     middleware=[prompt_with_context]
# )


# class MessagePart(BaseModel):
#     """
#     Represents a specific part of a message (text, tool call, etc.)
#     Matches Vercel AI SDK Core 'Message' interface.
#     """

#     type: str
#     text: str = ""  # Default to empty string if not a text part


# class Message(BaseModel):
#     """
#     Represents a full chat message containing multiple parts.
#     Used for AI SDK 5/6 compatibility.
#     """

#     role: str
#     parts: List[MessagePart]


# class ChatRequest(BaseModel):
#     """Schema for the incoming POST request body."""

#     messages: List[Message]


# def convert_to_langchain_messages(messages: List[Message]):
#     lc_messages = []
#     for m in messages:
#         # Extract and join all text parts within a single message
#         text_content = "".join([p.text for p in m.parts if p.type == "text"])

#         if m.role == "user":
#             lc_messages.append(HumanMessage(content=text_content))
#         elif m.role == "assistant":
#             lc_messages.append(AIMessage(content=text_content))
#     print(lc_messages)
#     return lc_messages


# async def generate_data_stream(messages: List[Message]):
#     # async for chunk, metadata in agent.astream(
#     #     {"messages": [{"role": "user", "content": "Tell me a Dad joke"}]},
#     #     stream_mode="messages",
#     # ):

#     lc_messages = convert_to_langchain_messages(messages)

#     # todo: add the real text_id later
#     text_id = "text_0"
#     yield f"data: {json.dumps({'type': 'text-start', 'id': text_id})}\n\n"
#     async for chunk, metadata in agent.astream(
#         # {"messages": [{"role": "user", "content": "Tell me a Dad joke"}]},
#         {"messages": lc_messages},
#         stream_mode="messages",
#     ):
#         # print(chunk)
#         if chunk.content:
#             payload = {"type": "text-delta", "id": text_id, "delta": chunk.content}
#             yield f"data: {json.dumps(payload)}\n\n"
#     yield f"data: {json.dumps({'type': 'text-end', 'id': text_id})}\n\n"
#     yield f"data: {json.dumps({'type': 'finish', 'finishReason': 'stop'})}\n\n"

#     # 4. Final stop signal
#     yield "data: [DONE]\n\n"


# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     # print(request.messages)
#     async def locked_stream():
#         async with lock:
#             async for chunk in generate_data_stream(request.messages):
#                 yield chunk

#     return StreamingResponse(
#         locked_stream(),
#         media_type="text/event-stream",
#         headers={
#             # Required header for Vercel AI SDK to recognize the stream format
#             "x-vercel-ai-data-stream": "v1",
#             "Cache-Control": "no-cache",
#             "X-Accel-Buffering": "no",
#         },
#     )

# class TestMessage(BaseModel):
#     message: str

# @app.post("/no_stream")
# async def chat_endpoint(request:TestMessage):
#     ai_response = agent.invoke({"messages":request.message})
#     # return(ai_response["messages"][-1].content)
#     return(ai_response)

# @app.get("/ollama/localmodels")
# async def localModels():
#     return ollama_localmodels()
