# Entry point for: uvicorn main:app
from app.main import app  # noqa: F401

__all__ = ["app"]
