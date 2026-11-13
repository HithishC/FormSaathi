import logging

logger = logging.getLogger(__name__)
import json, base64, mimetypes, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from sarvamai import SarvamAI
from config import SARVAM_API_KEY, SARVAM_CHAT_MODEL, SARVAM_STT_MODEL, SARVAM_TTS_MODEL

_pool = ThreadPoolExecutor(max_workers=4)

def _client():
    if not SARVAM_API_KEY:
        return None
    return SarvamAI(api_subscription_key=SARVAM_API_KEY)

def chat_answer(question: str, language: str, context: str):
    client = _client()
    if client is None:
        return {
            "answer": (
                "DEMO MODE: I can help you prepare your scholarship application. "
                "Please check the official department notification for final eligibility "
                "and document requirements. Your question was: " + question
            ),
            "demo_mode": True
        }
    system = (
        "You are FormSaathi, a responsible public-service application assistant. "
        "Use only the supplied scheme context. Never invent eligibility, deadlines, "
        "benefits or official URLs. If context is insufficient, say so. "
        "Do not claim to approve applications or authenticate certificates. "
        f"Respond in language {language} when possible.\nVerified context:\n{context}"
    )
    response = client.chat.completions(
        model=SARVAM_CHAT_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": question}
        ],
        reasoning_effort=None,
        max_tokens=700
    )
    content = response.choices[0].message.content
    if not content:
        content = "I couldn't generate a response. Please try again."
    return {"answer": content, "demo_mode": False}

def transcribe_audio(file_path: str):
    client = _client()
    if client is None:
        return {"transcript": "", "language_code": None, "demo_mode": True,
                "message": "Configure SARVAM_API_KEY to enable speech recognition."}
    with open(file_path, "rb") as audio:
        result = client.speech_to_text.transcribe(
            file=audio, model=SARVAM_STT_MODEL, mode="transcribe"
        )
    return {"transcript": result.transcript, "language_code": getattr(result, "language_code", None), "demo_mode": False}

def synthesize(text: str, language_code: str):
    client = _client()
    if client is None:
        return {"demo_mode": True, "message": "Configure SARVAM_API_KEY to enable speech synthesis."}
    result = client.text_to_speech.convert(
        text=text[:2500], model=SARVAM_TTS_MODEL, language_code=language_code
    )
    audios = getattr(result, "audios", [])
    if not audios:
        raise RuntimeError("Sarvam returned no audio.")
    return {"audio_base64": audios[0], "demo_mode": False, "content_type": "audio/wav"}


def extract_document(file_path: str, original_filename: str, language: str = "en-IN"):
    client = _client()

    if client is None:
        return {
            "status": "not_configured",
            "demo_mode": True,
            "message": "Configure SARVAM_API_KEY."
        }

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    if path.stat().st_size == 0:
        raise ValueError("Uploaded document is empty.")

    mime = mimetypes.guess_type(original_filename)[0] or "application/octet-stream"

    schema = {
        "type": "object",
        "properties": {
            "person_name": {
                "type": "string",
                "description": "Full name printed on the document"
            },
            "date_of_birth": {
                "type": "string",
                "description": "Date of birth, preferably YYYY-MM-DD"
            },
            "institution_name": {
                "type": "string",
                "description": "School or college name"
            },
            "certificate_type": {
                "type": "string",
                "description": "Type of document"
            },
            "issue_date": {
                "type": "string",
                "description": "Document issue date"
            },
            "issuing_authority": {
                "type": "string",
                "description": "Issuing authority printed on document"
            }
        }
    }

    try:
        logger.info("Starting Sarvam extraction: %s", original_filename)

        with open(file_path, "rb") as f:
            job = client.doc_ai.extract(
                file=[(original_filename, f, mime)],
                schema=json.dumps(schema),
                language=language,
                output_format="json"
            )

        logger.info(
            "Sarvam job created: job_id=%s status=%s",
            job.job_id, job.status
        )

        terminal = {
            "completed",
            "partially_completed",
            "failed",
            "rejected"
        }

        deadline = time.time() + 90
        status = str(job.status).lower()

        while status not in terminal and time.time() < deadline:
            time.sleep(5)

            status_obj = client.doc_ai.get_status(
                job_id=job.job_id
            )

            status = str(status_obj.status).lower()

            logger.info("Sarvam extraction status: %s", status)

        if status not in {"completed", "partially_completed"}:
            logger.error(
                "Sarvam extraction did not complete. Job: %s, status: %s",
                job.job_id, status
            )

            return {
                "status": status,
                "job_id": job.job_id,
                "demo_mode": False
            }

        result = client.doc_ai.get_results(
            job_id=job.job_id
        )

        logger.info("Sarvam extraction completed: %s", job.job_id)

        return {
            "status": status,
            "job_id": job.job_id,
            "extracted_data": result.result,
            "demo_mode": False
        }

    except Exception as e:
        logger.exception(
            "Sarvam Document AI extraction failed: %s",
            original_filename
        )
        raise

    client = _client()
    if client is None:
        return {"status": "not_configured", "demo_mode": True,
                "message": "Configure SARVAM_API_KEY to enable document extraction."}
    mime = mimetypes.guess_type(original_filename)[0] or "application/octet-stream"
    schema = {
        "type": "object",
        "properties": {
            "person_name": {"type": "string", "description": "Full name printed on the document"},
            "date_of_birth": {"type": "string", "description": "Date of birth if present, preferably YYYY-MM-DD"},
            "institution_name": {"type": "string", "description": "School or college name if present"},
            "certificate_type": {"type": "string", "description": "Type of certificate or document"},
            "issue_date": {"type": "string", "description": "Document issue date if present"},
            "issuing_authority": {"type": "string", "description": "Issuing authority if printed"}
        }
    }
    with open(file_path, "rb") as f:
        job = client.doc_ai.extract(
            file=[(original_filename, f, mime)],
            schema=json.dumps(schema),
            language=language,
            output_format="json"
        )
    terminal = {"completed", "partially_completed", "failed", "rejected"}
    deadline = time.time() + 90
    status = job.status
    while str(status).lower() not in terminal and time.time() < deadline:
        time.sleep(3)
        status_obj = client.doc_ai.get_status(job_id=job.job_id)
        status = status_obj.status
    if str(status).lower() not in {"completed", "partially_completed"}:
        return {"status": str(status), "job_id": job.job_id, "demo_mode": False}
    result = client.doc_ai.get_results(job_id=job.job_id)
    raw = getattr(result, "result", result)
    return {"status": str(status), "job_id": job.job_id, "extracted_data": raw, "demo_mode": False}
