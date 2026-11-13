import json, os, uuid, mimetypes
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import Base, engine, get_db
from models import User, Document, ReadinessItem, ChatMessage
from schemas import UserCreate, UserUpdate, ChatRequest, EligibilityRequest, ReadinessCreate, ReadinessUpdate
from config import APP_NAME, CORS_ORIGINS, UPLOAD_DIR, MAX_UPLOAD_SIZE_MB, SARVAM_API_KEY
from services import chat_answer, transcribe_audio, synthesize, extract_document

Base.metadata.create_all(bind=engine)
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
app = FastAPI(title=APP_NAME, version="1.0.0", description="Multilingual scholarship application preparation assistant")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def load_schemes():
    p = Path(__file__).parent / "data_schemes.json"
    return json.loads(p.read_text(encoding="utf-8"))

def scheme_by_id(scheme_id: str):
    for item in load_schemes():
        if item["id"] == scheme_id:
            return item
    return None

@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(select(1))
        database_status = "connected"
    except Exception:
        database_status = "disconnected"
    return {"status": "healthy" if database_status == "connected" else "degraded",
            "application": APP_NAME, "database": database_status,
            "sarvam": "configured" if SARVAM_API_KEY else "demo_mode"}

@app.post("/api/users", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(**payload.model_dump())
    db.add(user); db.commit(); db.refresh(user)
    return {"id": user.id, **payload.model_dump()}

@app.get("/api/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    return {"id": user.id, "full_name": user.full_name, "preferred_language": user.preferred_language,
            "education_level": user.education_level, "institution_name": user.institution_name}

@app.put("/api/users/{user_id}")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit(); db.refresh(user)
    return {"success": True, "id": user.id}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user: raise HTTPException(404, "User not found")
    for doc in list(user.documents):
        try: (Path(UPLOAD_DIR) / doc.stored_filename).unlink(missing_ok=True)
        except OSError: pass
    db.delete(user); db.commit()
    return {"success": True, "message": "User and associated records deleted"}

@app.get("/api/schemes")
def list_schemes(q: str | None = None, category: str | None = None):
    items = load_schemes()
    if q:
        items = [s for s in items if q.lower() in (s["name"] + " " + s["description"]).lower()]
    if category:
        items = [s for s in items if s.get("category") == category]
    return {"count": len(items), "schemes": items}

@app.get("/api/schemes/{scheme_id}")
def get_scheme(scheme_id: str):
    item = scheme_by_id(scheme_id)
    if not item: raise HTTPException(404, "Scheme not found")
    return item

@app.post("/api/eligibility/check")
def check_eligibility(payload: EligibilityRequest):
    scheme = scheme_by_id(payload.scheme_id)
    if not scheme: raise HTTPException(404, "Scheme not found")
    if scheme.get("verification_status") != "verified":
        return {"result": "scheme_information_unverified", "matched_conditions": [],
                "unmatched_conditions": [], "unknown_conditions": [],
                "disclaimer": "Demo scheme data is not verified. Check the official notification."}
    matched, unmatched, unknown = [], [], []
    for rule in scheme.get("eligibility", []):
        field = rule.get("field")
        actual = payload.profile.get(field)
        if actual is None:
            unknown.append(field); continue
        op, expected = rule.get("operator"), rule.get("value")
        ok = True
        try:
            if op == "eq": ok = actual == expected
            elif op == "gte": ok = float(actual) >= float(expected)
            elif op == "lte": ok = float(actual) <= float(expected)
            elif op == "in": ok = actual in expected
            else: unknown.append(field); continue
        except (TypeError, ValueError):
            unknown.append(field); continue
        (matched if ok else unmatched).append(field)
    result = "needs_more_information" if unknown else ("potentially_not_eligible" if unmatched else "potentially_eligible")
    return {"result": result, "matched_conditions": matched, "unmatched_conditions": unmatched,
            "unknown_conditions": unknown,
            "disclaimer": "Preliminary guidance only; this is not an official eligibility decision."}

@app.post("/api/chat")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    context = "\n".join(
        f"Scheme: {s['name']} | Status: {s['verification_status']} | "
        f"Description: {s['description']} | Documents: {', '.join(s['required_documents'])}"
        for s in load_schemes()
    )
    try:
        result = chat_answer(payload.message, payload.language, context)
    except Exception as exc:
        raise HTTPException(503, "AI service unavailable. Check Sarvam API configuration and credits.") from exc
    if payload.user_id is not None:
        if not db.get(User, payload.user_id): raise HTTPException(404, "User not found")
        db.add(ChatMessage(user_id=payload.user_id, role="user", message=payload.message, language=payload.language))
        db.add(ChatMessage(user_id=payload.user_id, role="assistant", message=result["answer"], language=payload.language))
        db.commit()
    return {"success": True, **result, "sources": [{"name": s.get("source_name"), "url": s.get("official_url"),
            "verification_status": s["verification_status"]} for s in load_schemes()]}

@app.post("/api/documents/upload", status_code=201)
async def upload_document(user_id: int = Form(...), document_type: str = Form("other"),
                          file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not db.get(User, user_id): raise HTTPException(404, "User not found")
    ext = Path(file.filename or "").suffix.lower()
    allowed = {".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}
    if ext not in allowed: raise HTTPException(415, "Only PDF, PNG and JPEG files are supported")
    content = await file.read()
    if not content: raise HTTPException(400, "Empty file")
    if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024: raise HTTPException(413, "File too large")
    # Basic signature checks to avoid trusting the filename alone.
    valid = (ext == ".pdf" and content.startswith(b"%PDF")) or (ext == ".png" and content.startswith(b"\x89PNG")) or (ext in {".jpg", ".jpeg"} and content.startswith(b"\xff\xd8\xff"))
    if not valid: raise HTTPException(415, "File content does not match its extension")
    stored = f"{uuid.uuid4().hex}{ext}"
    (Path(UPLOAD_DIR) / stored).write_bytes(content)
    doc = Document(user_id=user_id, document_type=document_type, original_filename=Path(file.filename).name,
                   stored_filename=stored, extraction_status="not_started", review_status="needs_review")
    db.add(doc); db.commit(); db.refresh(doc)
    return {"id": doc.id, "document_type": doc.document_type, "filename": doc.original_filename,
            "extraction_status": doc.extraction_status, "review_status": doc.review_status}

@app.post("/api/documents/{document_id}/extract")
def extract_uploaded_document(document_id: int, language: str = "en-IN", db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(404, "Document not found")
    path = str(Path(UPLOAD_DIR) / doc.stored_filename)
    try:
        result = extract_document(path, doc.original_filename, language)
    except Exception as exc:
        raise HTTPException(503, "Document AI service failed. Check API key, credits and file limits.") from exc
    doc.extraction_status = result.get("status", "unknown")
    if result.get("extracted_data") is not None:
        doc.extracted_data = json.dumps(result["extracted_data"], default=str)
    db.commit()
    return {"document_id": doc.id, **result,
            "notice": "Extraction is not certificate authentication or official verification."}

@app.get("/api/documents/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(404, "Document not found")
    return {"id": doc.id, "user_id": doc.user_id, "document_type": doc.document_type,
            "filename": doc.original_filename, "extraction_status": doc.extraction_status,
            "review_status": doc.review_status,
            "extracted_data": json.loads(doc.extracted_data) if doc.extracted_data else None}

@app.get("/api/documents/user/{user_id}")
def user_documents(user_id: int, db: Session = Depends(get_db)):
    if not db.get(User, user_id): raise HTTPException(404, "User not found")
    docs = db.scalars(select(Document).where(Document.user_id == user_id)).all()
    return [{"id": d.id, "filename": d.original_filename, "document_type": d.document_type,
             "extraction_status": d.extraction_status, "review_status": d.review_status} for d in docs]

@app.delete("/api/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(404, "Document not found")
    (Path(UPLOAD_DIR) / doc.stored_filename).unlink(missing_ok=True)
    db.delete(doc); db.commit()
    return {"success": True}

@app.post("/api/readiness/create")
def create_readiness(payload: ReadinessCreate, db: Session = Depends(get_db)):
    if not db.get(User, payload.user_id): raise HTTPException(404, "User not found")
    scheme = scheme_by_id(payload.scheme_id)
    if not scheme: raise HTTPException(404, "Scheme not found")
    created = 0
    for name in scheme.get("required_documents", []):
        exists = db.scalar(select(ReadinessItem).where(
            ReadinessItem.user_id == payload.user_id,
            ReadinessItem.scheme_id == payload.scheme_id,
            ReadinessItem.document_type == name))
        if not exists:
            db.add(ReadinessItem(user_id=payload.user_id, scheme_id=payload.scheme_id,
                                 document_type=name, status="missing")); created += 1
    db.commit()
    return {"success": True, "items_created": created, "passport": get_readiness(payload.user_id, payload.scheme_id, db)}

@app.post("/api/readiness/update")
def update_readiness(payload: ReadinessUpdate, db: Session = Depends(get_db)):
    allowed = {"missing", "uploaded", "completed", "needs_review"}
    if payload.status not in allowed: raise HTTPException(422, f"Status must be one of {sorted(allowed)}")
    item = db.scalar(select(ReadinessItem).where(
        ReadinessItem.user_id == payload.user_id,
        ReadinessItem.scheme_id == payload.scheme_id,
        ReadinessItem.document_type == payload.document_type))
    if not item: raise HTTPException(404, "Readiness item not found; create the passport first")
    item.status, item.notes = payload.status, payload.notes
    db.commit()
    return {"success": True, "passport": get_readiness(payload.user_id, payload.scheme_id, db)}

@app.get("/api/readiness/{user_id}/scheme/{scheme_id}")
def get_readiness(user_id: int, scheme_id: str, db: Session = Depends(get_db)):
    if not db.get(User, user_id): raise HTTPException(404, "User not found")
    items = db.scalars(select(ReadinessItem).where(
        ReadinessItem.user_id == user_id, ReadinessItem.scheme_id == scheme_id)).all()
    total = len(items)
    completed = sum(i.status == "completed" for i in items)
    missing = [i.document_type for i in items if i.status == "missing"]
    review = [i.document_type for i in items if i.status == "needs_review"]
    uploaded = [i.document_type for i in items if i.status == "uploaded"]
    return {"user_id": user_id, "scheme_id": scheme_id, "total_required_documents": total,
            "completed_documents": completed, "missing_documents": missing,
            "uploaded_documents": uploaded, "review_needed_documents": review,
            "readiness_percentage": round(completed / total * 100) if total else 0,
            "next_action": f"Prepare {missing[0]}" if missing else ("Review uploaded documents" if review else "Confirm all details before applying"),
            "items": [{"id": i.id, "document_type": i.document_type, "status": i.status, "notes": i.notes} for i in items]}

@app.post("/api/voice/transcribe")
async def voice_transcribe(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in {".wav", ".mp3", ".m4a", ".ogg", ".webm", ".flac"}:
        raise HTTPException(415, "Unsupported audio format")
    content = await file.read()
    if len(content) > MAX_UPLOAD_SIZE_MB * 1024 * 1024: raise HTTPException(413, "Audio too large")
    temp = Path(UPLOAD_DIR) / f"{uuid.uuid4().hex}{ext}"
    temp.write_bytes(content)
    try:
        return transcribe_audio(str(temp))
    except Exception as exc:
        raise HTTPException(503, "Speech recognition failed") from exc
    finally:
        temp.unlink(missing_ok=True)

@app.post("/api/voice/speak")
def voice_speak(text: str = Form(...), language_code: str = Form("en-IN")):
    try:
        result = synthesize(text, language_code)
    except Exception as exc:
        raise HTTPException(503, "Speech synthesis failed") from exc
    if result.get("audio_base64"):
        import base64
        return Response(content=base64.b64decode(result["audio_base64"]), media_type="audio/wav")
    return result
