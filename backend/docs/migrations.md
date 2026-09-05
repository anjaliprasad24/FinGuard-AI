# Database Migration Guide (Alembic)

This document describes the database schema migration architecture, rules, and operational workflows for the Ephemeral backend.

---

## 1. Role of Alembic

Alembic is the **authoritative database schema migration mechanism** for Ephemeral. 

While SQLAlchemy ORM models define Python entity classes, Alembic manages the lifecycle of the actual database schema versions across environments.

```
SQLAlchemy ORM Models (app/models/*)
           ↓
Alembic Metadata (Base.metadata)
           ↓
Migration Revision (alembic/versions/*.py)
           ↓
SQLite Database Schema (ephemeral.db)
```

---

## 2. Architectural Rules & Separation of Concerns

1. **Isolation**: Alembic is strictly database infrastructure.
2. **No Import Leaks**: Application runtime code (FastAPI routers, service layer, repository layer, domain models) MUST NOT import Alembic.
3. **Application Autonomy**: Business logic and request handlers operate through SQLAlchemy sessions and repositories, remaining unaware of Alembic.
4. **Relationship with `init_db()`**:
   - `init_db()` in `app/core/database.py` executes `Base.metadata.create_all()` during FastAPI lifespan startup as a local-development fallback.
   - `init_db()` is a **transitional developer convenience safeguard**, NOT a replacement for Alembic schema migrations.
   - All production and persistent environment schema evolution must be applied via Alembic migrations.

---

## 3. SQLite Compatibility Considerations

- **Foreign Key Enforcement**: SQLite requires `PRAGMA foreign_keys=ON` on every database connection. `alembic/env.py` configures connection events to enforce foreign key constraints during online migration execution.
- **Batch Operations**: SQLite has limited native support for `ALTER TABLE` operations. `alembic/env.py` sets `render_as_batch=True` so that table schema modifications automatically use batch alter copy-and-move operations.

---

## 4. Key CLI Commands

All commands should be executed from `backend/`:

```powershell
# Verify current migration status
.\.venv\Scripts\python.exe -m alembic current

# Inspect migration history
.\.venv\Scripts\python.exe -m alembic history --verbose

# Apply all pending migrations to the latest revision (head)
.\.venv\Scripts\python.exe -m alembic upgrade head

# Roll back all migrations to base (empty database schema)
.\.venv\Scripts\python.exe -m alembic downgrade base

# Roll back the single most recent migration
.\.venv\Scripts\python.exe -m alembic downgrade -1

# Generate a new migration script based on ORM model changes
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "describe_schema_change"
```

---

## 5. Development Workflow for Future Schema Changes

When modifying or adding domain models in `app/models/`:

1. **Update ORM Models**: Define or update SQLAlchemy mapped columns in `app/models/`.
2. **Generate Migration**: Run `alembic revision --autogenerate -m "description"`.
3. **Review Migration Script**: Inspect the generated file under `alembic/versions/` to verify:
   - Types, constraints, and nullability settings are correct.
   - Upgrade and downgrade logic are symmetrical.
   - No unintended schema changes were captured.
4. **Apply Migration**: Run `alembic upgrade head`.
5. **Verify Drift**: Run `alembic revision --autogenerate -m "check"` to confirm zero remaining schema drift, then delete the temporary check file.
6. **Run Tests**: Execute `.\.venv\Scripts\python.exe -m pytest` to ensure all tests and migration verifications pass cleanly.
