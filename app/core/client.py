from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Request
from google import genai

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.gemini_client = genai.Client(api_key=settings.gemini_api_key)
    yield
    app.state.gemini_client = None


async def get_client(request: Request) -> genai.Client:
    client: genai.Client | None = getattr(request.app.state, "gemini_client", None)
    if client is None:
        raise HTTPException(status_code=503, detail="AI client not available.")
    return client


GeminiClient = Annotated[genai.Client, Depends(get_client)]
