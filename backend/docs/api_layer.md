# API Layer Foundation — Ephemeral Backend

## Overview & Architecture

The API Layer Foundation provides a thin HTTP REST interface over the Ephemeral service layer. It acts strictly as an entry point for HTTP requests, delegating all domain rules and data query operations down the architectural hierarchy.

### Request Flow Hierarchy

```
HTTP Request
    │
    ▼
FastAPI Router (app/api/*.py)
    │
    ▼
DB Session Dependency (get_db)
    │
    ▼
Service Layer (app/services/*.py)
    │
    ▼
Repository Layer (app/repositories/*.py)
    │
    ▼
SQLAlchemy ORM
    │
    ▼
SQLite Database
```

---

## Core Responsibilities

1. **HTTP Routing & Parameter Extraction**: Deserializing HTTP request payloads, path parameters, and query arguments.
2. **Transaction Boundary Management**: Owning the database transaction lifecycle per HTTP request.
3. **Exception Translation**: Converting domain-level service exceptions into standard HTTP error responses.
4. **Response Serialization**: Formatted JSON output using Pydantic Read DTO contracts.

---

## Router Organization

Routers are modularized by domain under `backend/app/api/`:

| Router File | Prefix / Path Base | Managed Domain Operations |
|---|---|---|
| `users.py` | `/users` | User creation, listing, retrieval, deletion |
| `sessions.py` | `/sessions`, `/users/{user_id}/sessions` | Session lifecycle and status transitions |
| `processing_jobs.py` | `/processing-jobs`, `/sessions/{session_id}/processing-jobs` | Processing job execution state and attempts |
| `memories.py` | `/memories`, `/sessions/{session_id}/memories` | Memory unit creation, retrieval, updates, deletion |
| `memory_evidence.py` | `/memory-evidence`, `/memories/{memory_id}/evidence` | Context evidence linking |
| `memory_feedback.py` | `/memory-feedback`, `/memories/{memory_id}/feedback` | User feedback classification |
| `router.py` | Central Router | Aggregates all domain routers and exposes `GET /health` |

---

## Database Session & Transaction Boundary

The API request boundary strictly owns transaction commit/rollback behavior using the request-scoped `get_db` dependency in `app.core.database`:

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

- **Successful Requests**: If the route and service execute without raising an exception, `get_db()` issues `db.commit()` upon completion.
- **Failed Requests**: If any exception is raised, `get_db()` immediately issues `db.rollback()`, ensuring no partial or invalid state is committed.
- **Repositories & Services**: Intentionally perform `.flush()` only and NEVER execute `.commit()`.

---

## Centralized Exception Translation

Domain exceptions raised by the service layer are translated at the FastAPI application boundary in `app/main.py`:

- `EntityNotFoundError` ➔ **HTTP 404 Not Found**
- `ValidationError` ➔ **HTTP 400 Bad Request**
- Unhandled Exception / Error ➔ **HTTP 500 Internal Server Error** (Preserving server logs without swallowing errors)

Service and repository modules remain completely decoupled from FastAPI HTTP concerns (no `HTTPException` inside services or repos).

---

## Response Schema & DTO Strategy

All endpoints explicitly declare Pydantic `response_model` annotations matching service layer Read DTOs:

- `response_model=UserRead`
- `response_model=list[SessionRead]`
- `response_model=MemoryRead`

Raw SQLAlchemy ORM instances are never exposed across the HTTP API boundary.

---

## Why Business Logic Does Not Live in Routes

Routes remain strictly thin:
1. They do not contain `if/else` business rules or state transition logic.
2. They do not execute direct SQLAlchemy `.query()` or ORM manipulations.
3. Service methods remain the single source of truth for entity business rules, enabling reusability in background workers, CLI tools, or tests without HTTP overhead.

---

## Endpoint Inventory

| HTTP Method | Route | Description | Success Status |
|---|---|---|---|
| `GET` | `/health` | Service health check | 200 OK |
| `POST` | `/users` | Create user | 201 Created |
| `GET` | `/users` | List users | 200 OK |
| `GET` | `/users/{user_id}` | Get user by ID | 200 OK |
| `DELETE` | `/users/{user_id}` | Delete user by ID | 204 No Content |
| `POST` | `/sessions` | Create session | 201 Created |
| `GET` | `/sessions/{session_id}` | Get session by ID | 200 OK |
| `GET` | `/users/{user_id}/sessions` | List user sessions | 200 OK |
| `PATCH` | `/sessions/{session_id}` | Update session / status | 200 OK |
| `DELETE` | `/sessions/{session_id}` | Delete session by ID | 204 No Content |
| `POST` | `/processing-jobs` | Create processing job | 201 Created |
| `GET` | `/processing-jobs/{job_id}` | Get job by ID | 200 OK |
| `GET` | `/sessions/{session_id}/processing-jobs` | List session jobs | 200 OK |
| `PATCH` | `/processing-jobs/{job_id}` | Update job status/attempt | 200 OK |
| `DELETE` | `/processing-jobs/{job_id}` | Delete job by ID | 204 No Content |
| `POST` | `/memories` | Create memory | 201 Created |
| `GET` | `/memories/{memory_id}` | Get memory by ID | 200 OK |
| `GET` | `/sessions/{session_id}/memories` | List session memories | 200 OK |
| `PATCH` | `/memories/{memory_id}` | Update memory content/type | 200 OK |
| `DELETE` | `/memories/{memory_id}` | Delete memory by ID | 204 No Content |
| `POST` | `/memory-evidence` | Create memory evidence | 201 Created |
| `GET` | `/memory-evidence/{evidence_id}` | Get evidence by ID | 200 OK |
| `GET` | `/memories/{memory_id}/evidence` | List memory evidence | 200 OK |
| `DELETE` | `/memory-evidence/{evidence_id}` | Delete evidence by ID | 204 No Content |
| `POST` | `/memory-feedback` | Create memory feedback | 201 Created |
| `GET` | `/memory-feedback/{feedback_id}` | Get feedback by ID | 200 OK |
| `GET` | `/memories/{memory_id}/feedback` | List memory feedback | 200 OK |
| `DELETE` | `/memory-feedback/{feedback_id}` | Delete feedback by ID | 204 No Content |

---

## Explicit Scope Limitations

Module 6 explicitly excludes:
- Authentication & Authorization (JWT, passwords, login endpoints)
- Ingestion workers, Celery, or task queues
- Multimodal AI processing, embeddings, vector database
- Production containerization or external database migrations
