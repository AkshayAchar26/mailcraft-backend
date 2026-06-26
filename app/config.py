from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str
    gemini_model: str = "gemini-3.5-flash"
    # Comma-separated origins — set CORS_ORIGINS env var on Render to add your Vercel URL
    cors_origins: str = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    max_output_tokens: int = 1024
    temperature: float = 0.7


settings = Settings()
