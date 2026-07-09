"""Offline license tokens: Ed25519-signed JSON, verifiable without a server.

Token format (three dot-separated parts, URL-safe):

    LIC1.<base64url(payload json)>.<base64url(ed25519 signature)>

The vendor generates a keypair once (`keygen`), keeps the private key secret and
bakes the public key into the app (settings / env). `issue` signs a payload with
the private key; the app verifies with only the public key, fully offline.

Honest positioning: this proves the token came from you and was not edited. It
does not stop a determined user from patching the binary — no client-side
licensing does. It is honest-user licensing.
"""

from __future__ import annotations

import base64
import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .provider import LicenseInfo

TOKEN_PREFIX = "LIC1"


@dataclass(frozen=True)
class KeyPair:
    """Raw Ed25519 keys, base64url-encoded — easy to store in env vars/files."""

    private_key: str
    public_key: str


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def generate_keypair() -> KeyPair:
    private = Ed25519PrivateKey.generate()
    return KeyPair(
        private_key=_b64encode(private.private_bytes_raw()),
        public_key=_b64encode(private.public_key().public_bytes_raw()),
    )


def issue_token(
    private_key: str,
    *,
    licensee: str,
    plan: str,
    features: list[str] | None = None,
    expires_at: datetime | None = None,
    valid_days: int | None = None,
) -> str:
    """Sign a license token with the vendor's private key."""
    if expires_at is None and valid_days is not None:
        expires_at = datetime.now(UTC) + timedelta(days=valid_days)
    payload = {
        "id": uuid.uuid4().hex,
        "licensee": licensee,
        "plan": plan,
        "features": sorted(features or []),
        "issued_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "expires_at": expires_at.isoformat(timespec="seconds") if expires_at else None,
    }
    payload_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    key = Ed25519PrivateKey.from_private_bytes(_b64decode(private_key))
    signature = key.sign(payload_bytes)
    return f"{TOKEN_PREFIX}.{_b64encode(payload_bytes)}.{_b64encode(signature)}"


def verify_token(
    token: str, public_key: str, *, at: datetime | None = None, source: str = "token"
) -> LicenseInfo:
    """Verify a token's signature and expiry; never raises, always returns info.

    An invalid token yields `LicenseInfo(valid=False, plan="free", message=...)`
    so callers degrade to the free plan instead of crashing the app.
    """

    def invalid(message: str) -> LicenseInfo:
        return LicenseInfo(valid=False, source=source, message=message)

    if not public_key:
        return invalid("No license public key configured - cannot verify tokens.")
    token = token.strip()
    parts = token.split(".")
    if len(parts) != 3 or parts[0] != TOKEN_PREFIX:
        return invalid("Malformed license token.")
    try:
        payload_bytes = _b64decode(parts[1])
        signature = _b64decode(parts[2])
        key = Ed25519PublicKey.from_public_bytes(_b64decode(public_key))
    except (ValueError, TypeError):
        return invalid("Malformed license token or public key.")
    try:
        key.verify(signature, payload_bytes)
    except InvalidSignature:
        return invalid("License signature is invalid (tampered or wrong key).")
    try:
        payload = json.loads(payload_bytes)
    except ValueError:
        return invalid("License payload is not valid JSON.")

    expires_at = None
    if payload.get("expires_at"):
        expires_at = datetime.fromisoformat(payload["expires_at"])
    info = LicenseInfo(
        plan=str(payload.get("plan", "free")),
        licensee=str(payload.get("licensee", "")),
        features=tuple(payload.get("features") or ()),
        expires_at=expires_at,
        valid=True,
        source=source,
        message="License OK.",
    )
    now = at or datetime.now(UTC)
    if expires_at is not None and now > expires_at:
        return LicenseInfo(
            plan="free",
            licensee=info.licensee,
            features=(),
            expires_at=expires_at,
            valid=False,
            source=source,
            message=f"License expired on {expires_at.date().isoformat()}.",
        )
    return info
