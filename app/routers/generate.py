from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.client import GeminiClient
from app.schemas.email import GenerateRequest
from app.services.email import stream_email

router = APIRouter(tags=["email"])


@router.post("/api/generate")
async def generate(req: GenerateRequest, client: GeminiClient) -> StreamingResponse: # type: ignore
    """Stream an AI-generated email as Server-Sent Events.

    Each chunk: `data: {"text": "..."}` — stream ends with `data: [DONE]`.
    """
    return StreamingResponse(
        stream_email(client, req.prompt, req.tone),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
