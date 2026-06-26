from pydantic import BaseModel, field_validator

VALID_TONES: frozenset[str] = frozenset({"Professional", "Friendly", "Formal", "Casual"})


class GenerateRequest(BaseModel):
    prompt: str
    tone: str = "Professional"

    @field_validator("prompt")
    @classmethod
    def prompt_not_empty(cls, v: str) -> str:
        if len(v.strip()) < 5:
            raise ValueError("Prompt must be at least 5 characters.")
        return v.strip()

    @field_validator("tone")
    @classmethod
    def tone_must_be_valid(cls, v: str) -> str:
        if v not in VALID_TONES:
            raise ValueError(f"Tone must be one of: {', '.join(sorted(VALID_TONES))}")
        return v
