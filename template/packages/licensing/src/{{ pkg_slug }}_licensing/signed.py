from __future__ import annotations

from pathlib import Path

from .plans import plan_satisfies
from .provider import LicenseInfo
from .signing import verify_token


class SignedLicenseProvider:
    """Entitlement from an Ed25519-signed offline token (string or file).

    Verification runs on every `info()` call: it is microseconds of work and
    means expiry takes effect while a server is running, and a re-written
    license file is picked up without a restart.
    """

    def __init__(
        self,
        public_key: str,
        *,
        token: str | None = None,
        token_file: str | Path | None = None,
    ) -> None:
        if token is None and token_file is None:
            raise ValueError("SignedLicenseProvider needs a token or a token_file")
        self._public_key = public_key
        self._token = token
        self._token_file = Path(token_file) if token_file else None

    def info(self) -> LicenseInfo:
        if self._token is not None:
            return verify_token(self._token, self._public_key, source="token")
        assert self._token_file is not None
        try:
            token = self._token_file.read_text(encoding="utf-8").strip()
        except OSError:
            return LicenseInfo(
                valid=False,
                source="file",
                message=f"License file not found: {self._token_file}",
            )
        return verify_token(token, self._public_key, source="file")

    def current_plan(self) -> str:
        info = self.info()
        return info.plan if info.valid else "free"

    def is_entitled(self, required_plan: str | None) -> bool:
        return plan_satisfies(self.current_plan(), required_plan)

    def has_feature(self, feature: str) -> bool:
        info = self.info()
        return info.valid and feature in info.features
