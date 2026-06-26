from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.client import lifespan
from app.routers import generate, health


def create_app() -> FastAPI:
    application = FastAPI(
        title="MailCraft AI — Backend",
        description="FastAPI backend for AI-powered email generation using Google Gemini.",
        version="2.0.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(generate.router)

    return application


app = create_app()
