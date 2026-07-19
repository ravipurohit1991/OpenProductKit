"""Optional user accounts for hosted deployments.

Auth is a **runtime switch, not a build variant**: every install has these
tables and routes, and `APP_AUTH_ENABLED=true` turns enforcement on (typically
only in the hosted Docker stack). The desktop/local story intentionally has no
accounts, so nothing changes there.

Design notes:
- Passwords are hashed with stdlib `hashlib.scrypt` — no extra dependencies.
- Sessions are opaque bearer tokens; the DB stores only their SHA-256, so a
  leaked database cannot be replayed as logins.
- `enforce_auth` is installed as a global dependency in `create_app`. It
  no-ops while auth is disabled and skips the public endpoints (health,
  login, setup, me), so the login screen itself can load.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, Request
from sqlmodel import Session, func, select

from .adapters.db.engine import engine
from .adapters.db.models import AuthSessionRow, UserRow
from .settings import settings

# Endpoints that must work without a session, or logging in would be impossible.
PUBLIC_PATHS = {"/api/health", "/api/auth/me", "/api/auth/login", "/api/auth/setup"}
PUBLIC_PREFIXES = ("/api/ai/assets/", "/api/ai/webhooks/")

_SCRYPT_N, _SCRYPT_R, _SCRYPT_P = 2**14, 8, 1


def _utcnow() -> datetime:
    # Stored naive-UTC: SQLite round-trips naive datetimes, and mixing aware
    # and naive values raises on comparison.
    return datetime.now(UTC).replace(tzinfo=None)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode(), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P, dklen=32
    )
    return f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        scheme, n, r, p, salt_hex, digest_hex = stored.split("$")
        if scheme != "scrypt":
            return False
        digest = hashlib.scrypt(
            password.encode(),
            salt=bytes.fromhex(salt_hex),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=32,
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def count_users(session: Session) -> int:
    return session.exec(select(func.count()).select_from(UserRow)).one()


def create_user(session: Session, email: str, password: str, *, is_admin: bool) -> UserRow:
    email = email.strip().lower()
    if not email or "@" not in email:
        raise ValueError("A valid email address is required.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    if session.exec(select(UserRow).where(UserRow.email == email)).first() is not None:
        raise ValueError(f"A user with email '{email}' already exists.")
    user = UserRow(
        id=str(uuid.uuid4()),
        email=email,
        password_hash=hash_password(password),
        is_admin=is_admin,
        created_at=_utcnow(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate(session: Session, email: str, password: str) -> UserRow | None:
    user = session.exec(
        select(UserRow).where(UserRow.email == email.strip().lower())
    ).first()
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


def create_session(session: Session, user: UserRow) -> str:
    """Create a bearer session and return the raw token (shown exactly once)."""
    token = secrets.token_urlsafe(32)
    session.add(
        AuthSessionRow(
            token_hash=hashlib.sha256(token.encode()).hexdigest(),
            user_id=user.id,
            created_at=_utcnow(),
            expires_at=_utcnow() + timedelta(days=settings.auth_session_days),
        )
    )
    session.commit()
    return token


def revoke_session(session: Session, token: str) -> None:
    row = session.get(AuthSessionRow, hashlib.sha256(token.encode()).hexdigest())
    if row is not None:
        session.delete(row)
        session.commit()


def resolve_user(session: Session, token: str) -> UserRow | None:
    row = session.get(AuthSessionRow, hashlib.sha256(token.encode()).hexdigest())
    if row is None:
        return None
    if row.expires_at < _utcnow():
        session.delete(row)
        session.commit()
        return None
    return session.get(UserRow, row.user_id)


def _bearer_token(request: Request) -> str:
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    return token.strip() if scheme.lower() == "bearer" else ""


def enforce_auth(request: Request) -> None:
    """Global dependency: when auth is on, every API route needs a session.

    Resolved users land on `request.state.user` for downstream dependencies.
    Static mounts and the docs pages are Starlette-level routes, so they stay
    reachable — they expose the schema and the login screen, never data.
    """
    request.state.user = None
    if not settings.auth_enabled:
        return
    public = request.url.path in PUBLIC_PATHS or request.url.path.startswith(
        PUBLIC_PREFIXES
    )
    token = _bearer_token(request)
    if token:
        with Session(engine) as session:
            user = resolve_user(session, token)
        if user is not None:
            request.state.user = user
            return
    if public:
        return
    raise HTTPException(status_code=401, detail={"error": "auth_required"})


def current_user(request: Request) -> UserRow | None:
    """The user resolved by `enforce_auth`, or None while auth is disabled."""
    return getattr(request.state, "user", None)


def require_admin(request: Request) -> None:
    """Route dependency for operator actions (plugin toggles, installs, users).

    A no-op while auth is disabled — single-user installs stay frictionless.
    """
    if not settings.auth_enabled:
        return
    user = current_user(request)
    if user is None or not user.is_admin:
        raise HTTPException(status_code=403, detail={"error": "admin_required"})
