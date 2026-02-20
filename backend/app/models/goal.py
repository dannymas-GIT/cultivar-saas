"""Goal model."""
from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, gen_uuid


class Goal(Base, TimestampMixin):
    __tablename__ = "goals"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=gen_uuid
    )
    initiative_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("initiatives.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    metric: Mapped[str | None] = mapped_column(String(256), nullable=True)
    target: Mapped[str | None] = mapped_column(String(256), nullable=True)
    due_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="planned", nullable=False)
