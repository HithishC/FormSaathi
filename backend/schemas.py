from pydantic import BaseModel, Field
from typing import Any

class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    preferred_language: str = "en-IN"
    education_level: str | None = None
    institution_name: str | None = None

class UserUpdate(BaseModel):
    full_name: str | None = None
    preferred_language: str | None = None
    education_level: str | None = None
    institution_name: str | None = None

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    user_id: int | None = None
    language: str = "en-IN"

class EligibilityRequest(BaseModel):
    scheme_id: str
    profile: dict[str, Any] = Field(default_factory=dict)

class ReadinessCreate(BaseModel):
    user_id: int
    scheme_id: str

class ReadinessUpdate(BaseModel):
    user_id: int
    scheme_id: str
    document_type: str
    status: str
    notes: str | None = None
