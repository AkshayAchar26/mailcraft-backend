import asyncio
import json
from typing import AsyncIterator

from google import genai
from google.genai import types

from app.config import settings

SYSTEM_INSTRUCTION = """You are an expert email writer. Generate a complete, professional email based on the user's request.

IMPORTANT: Return ONLY a JSON object with exactly these two fields:
{
  "subject": "<email subject line>",
  "body": "<full email body with proper greeting, content, and sign-off>"
}

In the body, use \\n for line breaks. Do NOT include markdown, code fences, or any text outside the JSON."""


async def stream_email(
    client: genai.Client,
    prompt: str,
    tone: str,
) -> AsyncIterator[str]:
    full_prompt = f"Tone: {tone}\n\n{prompt}"
    loop = asyncio.get_running_loop()

    def _collect_chunks() -> list[str]:
        chunks: list[str] = []
        for chunk in client.models.generate_content_stream(
            model=settings.gemini_model,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=settings.max_output_tokens,
                temperature=settings.temperature,
            ),
        ):
            if chunk.text:
                chunks.append(chunk.text)
        return chunks

    chunks = await loop.run_in_executor(None, _collect_chunks)

    for token in chunks:
        yield f"data: {json.dumps({'text': token})}\n\n"
        await asyncio.sleep(0)

    yield "data: [DONE]\n\n"
