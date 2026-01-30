from fastapi import APIRouter
from app.helpers import ollama_localmodels

router = APIRouter(prefix="/ollama", tags=["ollama"])


@router.get("/")
async def availableLocalModels():
    """to get available ollama local models."""
    return ollama_localmodels()
