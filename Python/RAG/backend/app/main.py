from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.helpers.embeding.embeding import initialize_vector_store

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await initialize_vector_store()
    yield
    # Shutdown

app = FastAPI(title="Simple Rag app v1", lifespan=lifespan)
# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")