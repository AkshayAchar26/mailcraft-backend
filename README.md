# MailCraft AI — Backend

A production-ready FastAPI backend that streams AI-generated emails using Google Gemini.

## Tech Stack

- **Framework:** FastAPI 0.138+
- **AI:** Google Gemini 2.5 Flash (via `google-genai`)
- **Server:** Uvicorn (ASGI)
- **Config:** Pydantic Settings + python-dotenv
- **Package Manager:** [uv](https://docs.astral.sh/uv/)
- **Python:** 3.12
- **Deployment:** Render.com

---

## Folder Structure

```
deploy-backend/
├── main.py                  # Uvicorn entry point (imports app from app.main)
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependency versions
├── render.yaml              # Render.com deployment config
├── .env                     # Local environment variables (not committed)
├── .env.example             # Environment variable template
├── .python-version          # Pins Python version to 3.12
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── main.py              # FastAPI app factory, middleware, and router registration
    ├── config.py            # Pydantic Settings — loads and validates env vars
    │
    ├── core/
    │   ├── __init__.py
    │   └── client.py        # Gemini client lifespan init + FastAPI dependency
    │
    ├── routers/
    │   ├── __init__.py
    │   ├── health.py        # GET /health
    │   └── generate.py      # POST /api/generate (SSE streaming)
    │
    ├── schemas/
    │   ├── __init__.py
    │   └── email.py         # Pydantic request/response models
    │
    └── services/
        ├── __init__.py
        └── email.py         # Core email generation logic (calls Gemini, yields SSE chunks)
```

---

## API Endpoints

### `GET /health`
Returns service status and active model name.

**Response:**
```json
{ "status": "ok", "model": "gemini-2.5-flash" }
```

---

### `POST /api/generate`
Generates an email and streams it back as Server-Sent Events.

**Request body:**
```json
{
  "prompt": "Write a follow-up email after a job interview",
  "tone": "Professional"
}
```

| Field    | Type   | Required | Default        | Notes                                              |
|----------|--------|----------|----------------|----------------------------------------------------|
| `prompt` | string | Yes      | —              | Min 5 characters                                   |
| `tone`   | string | No       | `Professional` | One of: `Professional`, `Friendly`, `Formal`, `Casual` |

**Response:** `text/event-stream`
```
data: {"text": "{\"subject\": \"Thank you for the opportunity\", \"body\": \"Dear ..."}

data: [DONE]
```

Each `data:` chunk carries a partial JSON string. The final message is `data: [DONE]`.

The full accumulated text is a JSON object:
```json
{
  "subject": "<email subject>",
  "body": "<email body with \\n for line breaks>"
}
```

---

## Local Development

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd deploy-backend

# 2. Install dependencies
uv sync

# 3. Configure environment
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY
```

### Run

```bash
# Development (hot reload)
uv run dev

# Production
uv run start
```

The server starts at `http://localhost:8000`.

---

## Environment Variables

| Variable        | Required | Default                                              | Description                          |
|-----------------|----------|------------------------------------------------------|--------------------------------------|
| `GEMINI_API_KEY` | Yes     | —                                                    | Google Gemini API key                |
| `GEMINI_MODEL`  | No       | `gemini-2.5-flash`                                   | Gemini model to use                  |
| `CORS_ORIGINS`  | No       | `http://localhost:3000,http://127.0.0.1:3000`        | Comma-separated list of allowed origins |
| `MAX_OUTPUT_TOKENS` | No   | `1024`                                               | Token limit for Gemini responses     |
| `TEMPERATURE`   | No       | `0.7`                                                | Generation temperature (0.0–2.0)     |

Copy `.env.example` to `.env` and fill in the required values before running locally.

---

## Deployment (Render.com)

The `render.yaml` file configures a Render web service:

- **Build command:** `pip install uv && uv sync --frozen`
- **Start command:** `uv run uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Runtime:** Python 3.12

Set the following environment variables in the Render dashboard (they are not synced from `render.yaml`):
- `GEMINI_API_KEY`
- `CORS_ORIGINS` (e.g. `https://your-frontend.vercel.app`)
