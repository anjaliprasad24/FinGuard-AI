# Repository Layer Foundation (Module 4)

This document describes the design, responsibilities, session lifecycle, transaction handling rules, and query conventions for the Repository Layer of the Ephemeral backend.

---

## Architecture & Layering

```
API
 ↓
Service
 ↓
Repository
 ↓
SQLAlchemy Session
 ↓
ORM Models
 ↓
SQLite
```

The repository layer isolates database operations from business logic and API route handlers.

---

## 1. Why the Repository Layer Exists

- **Separation of Concerns**: Encapsulates raw database queries and persistence details behind explicit Python classes.
- **Decoupled Data Access**: Keeps API routes and service logic focused on request handling and business rules rather than SQLAlchemy query mechanics.
- **Testability**: Enables straightforward testing of data access operations using isolated SQLAlchemy sessions without running the full API framework.
- **Maintainability**: Centralizes database access patterns and ordering conventions across all 6 domain entities.

---

## 2. Repository Responsibilities

Repositories are strictly responsible for:
- Constructing and executing SQLAlchemy 2.x `select()`, `add()`, `delete()`, and field update queries.
- Flushing pending operations (`db.flush()`) so auto-generated IDs and database defaults are populated.
- Filtering entities by primary key (`get_by_id`) or parent relationship (`list_by_user`, `list_by_session`, `list_by_memory`).
- Returning ORM entity instances, lists of entities, or boolean delete status.

---

## 3. Session Ownership

- **Caller Ownership**: Repositories receive an active SQLAlchemy `Session` instance upon initialization (`repo = UserRepository(db)`).
- **No Self-Created Sessions**: Repositories MUST NOT create, open, or close database sessions.
- **Framework Independence**: Repositories do not import FastAPI dependencies (such as `Depends(get_db)`).

Example:
```python
class BaseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
```

---

## 4. Transaction & Commit Ownership

- **No Automatic Commits**: Repositories MUST NOT call `db.commit()`.
- **Atomic Service Operations**: Transaction lifecycle (`commit()` and `rollback()`) is controlled entirely by the caller or business service layer.
- **Flush Usage**: Repositories call `db.flush()` to send changes to the database buffer and populate generated fields (such as primary key UUIDs) without committing the transaction.

Example workflow:
```python
user = user_repo.create()
session = session_repo.create(user_id=user.id)
db.commit()  # Controlled by caller/service
```

---

## 5. Error Propagation

- **No Exception Swallowing**: Repositories do not catch or suppress database exceptions (e.g. `IntegrityError`).
- **No Broad Catch Blocks**: No generic `except Exception:` blocks are used. Database errors propagate to the caller/service layer for appropriate handling or transaction rollback.
- **No HTTP Exceptions**: Repositories never raise FastAPI `HTTPException`.

---

## 6. Relationship Query & Update Patterns

- **SQLAlchemy 2.x Style**: All query operations use `sqlalchemy.select()` statements executed via `self.db.execute(statement)`. The legacy `db.query()` syntax is NOT used.
- **Deterministic Ordering**: List queries sort results deterministically, typically by `created_at` ascending.
- **Missing Records**: `get_by_id()` returns `None` when a record is not found; list methods return `[]`; `delete()` returns `False`.
- **Partial Updates**: `update()` methods modify existing attached ORM instances in-place for explicitly provided fields only, preserving all unspecified fields.

---

## 7. What Repositories Must NOT Contain

Repositories MUST NOT contain:
- Business logic or domain rules.
- Request parsing, validation, or response formatting.
- `db.commit()` or `db.rollback()` calls.
- Self-instantiated database engines or sessionmakers.
- FastAPI dependencies, router handlers, or `HTTPException` raises.
- Background task dispatch, AI/LLM logic, or external network calls.

---

## Exported Repositories (`app.repositories`)

- `UserRepository`
- `SessionRepository`
- `ProcessingJobRepository`
- `MemoryRepository`
- `MemoryEvidenceRepository`
- `MemoryFeedbackRepository`
