"""Auth API: session login plus admin user management.

All of this is inert until APP_AUTH_ENABLED=true (the hosted deployment
story). `GET /api/auth/me` is the frontend's single source of truth: it says
whether auth is on, whether the install still needs its first admin account,
and who is logged in.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import delete, select

from ... import auth
from ...adapters.db.models import AuthSessionRow, UserRow
from ...settings import settings
from ..deps import SessionDep

router = APIRouter(prefix="/api/auth", tags=["auth"])


class UserOut(BaseModel):
    id: str
    email: str
    is_admin: bool
    created_at: datetime


class AuthStatusOut(BaseModel):
    auth_enabled: bool
    #: True when auth is on but no account exists yet — the UI shows first-run
    #: setup instead of a login form.
    needs_setup: bool
    user: UserOut | None


class CredentialsIn(BaseModel):
    email: str
    password: str


class TokenOut(BaseModel):
    token: str
    user: UserOut


class UserCreateIn(BaseModel):
    email: str
    password: str
    is_admin: bool = False


def _require_enabled() -> None:
    if not settings.auth_enabled:
        raise HTTPException(
            status_code=400,
            detail="Auth is disabled. Set APP_AUTH_ENABLED=true to use accounts.",
        )


def _to_out(user: UserRow) -> UserOut:
    return UserOut(
        id=user.id, email=user.email, is_admin=user.is_admin, created_at=user.created_at
    )


@router.get("/me", response_model=AuthStatusOut)
def me(request: Request, session: SessionDep) -> AuthStatusOut:
    """Public: auth mode, setup state and the current user (if any)."""
    if not settings.auth_enabled:
        return AuthStatusOut(auth_enabled=False, needs_setup=False, user=None)
    user = None
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() == "bearer" and token.strip():
        user = auth.resolve_user(session, token.strip())
    return AuthStatusOut(
        auth_enabled=True,
        needs_setup=auth.count_users(session) == 0,
        user=_to_out(user) if user else None,
    )


@router.post("/setup", response_model=TokenOut)
def setup(payload: CredentialsIn, session: SessionDep) -> TokenOut:
    """First-run bootstrap: create the initial admin account and log it in."""
    _require_enabled()
    if auth.count_users(session) > 0:
        raise HTTPException(status_code=403, detail="Setup already completed — log in instead.")
    try:
        user = auth.create_user(session, payload.email, payload.password, is_admin=True)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TokenOut(token=auth.create_session(session, user), user=_to_out(user))


@router.post("/login", response_model=TokenOut)
def login(payload: CredentialsIn, session: SessionDep) -> TokenOut:
    _require_enabled()
    user = auth.authenticate(session, payload.email, payload.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return TokenOut(token=auth.create_session(session, user), user=_to_out(user))


@router.post("/logout")
def logout(request: Request, session: SessionDep) -> dict[str, str]:
    header = request.headers.get("Authorization", "")
    scheme, _, token = header.partition(" ")
    if scheme.lower() == "bearer" and token.strip():
        auth.revoke_session(session, token.strip())
    return {"status": "logged out"}


# --- admin user management ------------------------------------------------------


@router.get("/users", response_model=list[UserOut], dependencies=[Depends(auth.require_admin)])
def list_users(session: SessionDep) -> list[UserOut]:
    _require_enabled()
    return [_to_out(u) for u in session.exec(select(UserRow).order_by(UserRow.created_at))]


@router.post("/users", response_model=UserOut, dependencies=[Depends(auth.require_admin)])
def create_user(payload: UserCreateIn, session: SessionDep) -> UserOut:
    _require_enabled()
    try:
        user = auth.create_user(
            session, payload.email, payload.password, is_admin=payload.is_admin
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _to_out(user)


@router.delete("/users/{user_id}", dependencies=[Depends(auth.require_admin)])
def delete_user(user_id: str, request: Request, session: SessionDep) -> dict[str, str]:
    _require_enabled()
    me_user = auth.current_user(request)
    if me_user is not None and me_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account.")
    user = session.get(UserRow, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user.")
    session.exec(delete(AuthSessionRow).where(AuthSessionRow.user_id == user_id))
    session.delete(user)
    session.commit()
    return {"status": "deleted"}
