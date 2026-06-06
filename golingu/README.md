# GoLingu Translation API

A production-ready translation backend powered by **Google Gemini** and **FastAPI**.  
Supports 100+ languages with auto source-language detection, structured logging, and full Docker support.

---

## Project Structure

```
golingu/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── health.py        # GET /health
│   │       │   └── translation.py   # POST /translate
│   │       └── router.py            # Combines all v1 routes
│   ├── core/
│   │   ├── config.py                # Pydantic settings (env vars)
│   │   ├── exceptions.py            # Custom exception hierarchy
│   │   └── logging.py               # Structured logging setup
│   ├── models/
│   │   └── language.py              # Language registry (100+ languages)
│   ├── schemas/
│   │   └── translation.py           # Pydantic request/response models
│   ├── services/
│   │   ├── gemini_service.py        # Low-level Gemini API wrapper
│   │   └── translation_service.py   # Business logic & prompt engineering
│   └── main.py                      # App factory, middleware, lifespan
├── .env.example                     # Environment variable template
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Quickstart

### 1. Clone & configure

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Docker

```bash
docker-compose up --build
```

---

## API Reference

### `GET /api/v1/health`

Liveness probe.

```json
{
  "status": "ok",
  "version": "1.0.0",
  "service": "GoLingu Translation API"
}
```

---

### `POST /api/v1/translate`

Translate text to any supported language.

**Request**

```json
{
  "text": "Hello World",
  "targetLanguage": "bn",
  "sourceLanguage": "en"   // optional — auto-detected when omitted
}
```

**Response**

```json
{
  "translatedText": "হ্যালো ওয়ার্ল্ড",
  "sourceLanguage": "en",
  "targetLanguage": "bn",
  "characterCount": 11
}
```

**Error codes**

| HTTP | Code | Meaning |
|------|------|---------|
| 400 | `UNSUPPORTED_LANGUAGE` | Unknown BCP-47 language code |
| 422 | `TRANSLATION_FAILED` | Gemini could not produce a translation |
| 429 | `RATE_LIMIT_EXCEEDED` | Gemini quota exceeded |
| 502 | `GEMINI_SERVICE_ERROR` | Gemini API unreachable |
| 500 | `INTERNAL_ERROR` | Unexpected server error |

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | **required** | Your Google Gemini API key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Gemini model to use |
| `GEMINI_TEMPERATURE` | `0.1` | Low = more accurate translations |
| `ENV` | `production` | `development` \| `staging` \| `production` |
| `DEBUG` | `false` | Enable colorised dev logging |
| `LOG_LEVEL` | `INFO` | `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` |
| `ALLOWED_ORIGINS` | localhost ports | JSON array of CORS-allowed origins |

---

## Interactive Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)
