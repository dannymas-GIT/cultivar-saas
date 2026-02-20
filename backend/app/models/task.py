"""Task model."""
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, gen_uuid


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=gen_uuid
    )
    initiative_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("initiatives.id"), nullable=False, index=True
    )
    goal_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False), ForeignKey("goals.id"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owner: Mapped[str | None] = mapped_column(String(128), nullable=True)
    risk_level: Mapped[str] = mapped_column(String(32), default="low", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="planned", nullable=False)
    estimate_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
