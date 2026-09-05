"""Security utilities for password hashing and JWT authentication."""

from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

SECRET_KEY = getattr(settings, "SECRET_KEY", "super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with salt."""
    salt = "ai_finance_salt_2026"
    return hashlib.sha256(f"{password}{salt}".encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_id(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> str:
    user_id = "demo-user-uuid-1234"
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            sub = payload.get("sub")
            if sub:
                user_id = sub
        except JWTError:
            pass

    # Ensure user exists in database to satisfy foreign key constraint
    existing = db.query(User).filter(User.id == user_id).first()
    if not existing:
        user = User(
            id=user_id,
            email=f"{user_id}@aifinancecontroller.io",
            hashed_password=hash_password("demo1234"),
            risk_tolerance="MODERATE",
            min_reserve_threshold=10000.00
        )
        db.add(user)
        db.commit()

    return user_id
