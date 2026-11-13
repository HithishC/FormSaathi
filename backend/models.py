from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

def now_utc():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    preferred_language: Mapped[str] = mapped_column(String(10), default="en-IN")
    education_level: Mapped[str | None] = mapped_column(String(80), nullable=True)
    institution_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    readiness_items = relationship("ReadinessItem", back_populates="user", cascade="all, delete-orphan")

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    document_type: Mapped[str] = mapped_column(String(80), default="other")
    original_filename: Mapped[str] = mapped_column(String(255))
    stored_filename: Mapped[str] = mapped_column(String(255), unique=True)
    extracted_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    extraction_status: Mapped[str] = mapped_column(String(40), default="not_started")
    review_status: Mapped[str] = mapped_column(String(40), default="needs_review")
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    user = relationship("User", back_populates="documents")

class ReadinessItem(Base):
    __tablename__ = "readiness_items"
    __table_args__ = (UniqueConstraint("user_id", "scheme_id", "document_type"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    scheme_id: Mapped[str] = mapped_column(String(80), index=True)
    document_type: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default="missing")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)
    user = relationship("User", back_populates="readiness_items")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    role: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(10), default="en-IN")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
