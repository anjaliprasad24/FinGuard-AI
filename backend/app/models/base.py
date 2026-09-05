"""Base SQLAlchemy ORM declarative model class and domain model utilities."""

from datetime import datetime, timezone
import uuid

from sqlalchemy.orm import DeclarativeBase


def generate_uuid() -> str:
    """Generate a 36-character UUID string for primary keys."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Generate a timezone-aware UTC datetime for timestamp columns."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Base declarative class for all SQLAlchemy ORM models in Ephemeral."""

    pass

