# main.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import os
import openai  # pip install openai
from ai_sdk_stream import stream_text  # See note below

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

async def generate_stream(messages):
    response = await openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
    )
    async for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data["messages"]
    
    # Simple direct yield (works for basic text)
    # return StreamingResponse(generate_stream(messages), media_type="text/event-stream")
    
    # Recommended: Use a helper to format in Vercel AI SDK protocol for full compatibility (tool calls, etc.)
    from ai_sdk_stream import stream_text  # Community helper: pip install ai-sdk-stream or implement manually
    return stream_text(generate_stream(messages))  # Handles proper formatting



# from langchain_openai import ChatOpenAI
# from fastapi import FastAPI
# from fastapi.responses import StreamingResponse
# import os
# from dotenv import load_dotenv
# import asyncio
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# # load environment variables
# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, specify your frontend URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# MODEL_NAME = os.getenv("MODEL_NAME")
# BASE_URL = os.getenv("BASE_URL")
# API_KEY = os.getenv("API_KEY")

# llm = ChatOpenAI(
#     model=MODEL_NAME,
#     base_url=BASE_URL,
#     api_key=API_KEY,
# )


# async def generate_response(message: str):

#     async for chunk in llm.astream(message):
#         content = chunk.content
#         if content:
#             yield content


# class ChatRequest(BaseModel):
#     message: str


# @app.post("/chat")
# async def chat_endpoint(request: ChatRequest):
#     return StreamingResponse(
#         generate_response(request.message), media_type="text/plain"
#     )
