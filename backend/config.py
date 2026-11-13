import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "FormSaathi")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./formsaathi.db")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "").strip()
SARVAM_CHAT_MODEL = os.getenv("SARVAM_CHAT_MODEL", "sarvam-105b")
SARVAM_STT_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v4")
SARVAM_TTS_MODEL = os.getenv("SARVAM_TTS_MODEL", "bulbul:v3")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))
CORS_ORIGINS = [x.strip() for x in os.getenv(
    "CORS_ORIGINS", "http://localhost:5173"
).split(",") if x.strip()]
