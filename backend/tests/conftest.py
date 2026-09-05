"""Pytest fixtures for test environment configuration and database isolation."""

from pathlib import Path
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.models import Base  # Explicitly import all models to ensure metadata registration


@pytest.fixture(autouse=True)
def temp_db_isolation(tmp_path: Path, monkeypatch):
    """Isolate database operations during testing using a temporary SQLite database."""
    test_db = tmp_path / "test_ephemeral.db"
    sqlite_url = f"sqlite:///{test_db}"

    test_engine = create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(test_engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    test_sessionmaker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    import app.core.database as db_module

    monkeypatch.setattr(db_module, "engine", test_engine)
    monkeypatch.setattr(db_module, "SessionLocal", test_sessionmaker)

    Base.metadata.create_all(bind=test_engine)
    yield
    test_engine.dispose()
