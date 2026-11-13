# FormSaathi Backend

FastAPI backend for the FormSaathi hackathon project.

## 1. Setup

Python 3.11+ is recommended.

```bash
cd backend
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Sarvam key if available:
```env
SARVAM_API_KEY=your_key_here
```

Without a key, the server starts in demo mode. Chat returns a labelled demo answer; voice and document AI endpoints explain that credentials are required.

## 2. Run

```bash
uvicorn main:app --reload
```

Open:
- http://localhost:8000/api/health
- http://localhost:8000/docs

## 3. Main endpoints

- `GET /api/health`
- `POST /api/users`
- `GET /api/users/{user_id}`
- `GET /api/schemes`
- `GET /api/schemes/{scheme_id}`
- `POST /api/chat`
- `POST /api/eligibility/check`
- `POST /api/documents/upload` (multipart: user_id, document_type, file)
- `POST /api/documents/{id}/extract`
- `GET /api/documents/user/{user_id}`
- `DELETE /api/documents/{id}`
- `POST /api/readiness/create`
- `POST /api/readiness/update`
- `GET /api/readiness/{user_id}/scheme/{scheme_id}`
- `POST /api/voice/transcribe` (multipart audio file)
- `POST /api/voice/speak` (form fields: text, language_code)

## 4. Important demo data warning

`data_schemes.json` contains a deliberately unverified sample record. Replace it with official, checked scheme data before presenting scheme requirements as factual. The API labels this record `demo_unverified`.

## 5. Safety and deployment

This is a hackathon starter backend, not a production-ready public service. It does not include user authentication/authorization, malware scanning, encryption at rest, or managed object storage. Do not upload real sensitive identity documents to a public deployment until those controls are added. Use synthetic demo documents.

Uploaded files are stored locally in `uploads/`. Deleting a user or document deletes its stored file.

Sarvam integrations use the official `sarvamai` Python SDK. Chat, Saaras v4 transcription, Bulbul TTS and Document AI extraction require a valid API key and available account credits.
