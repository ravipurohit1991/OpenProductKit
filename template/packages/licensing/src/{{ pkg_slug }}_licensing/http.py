"""License validation against a vendor-run HTTP endpoint.

Contract (kept deliberately tiny so any stack can implement it):

    POST <url>            body: {"token": "<opaque license key>"}
    200 response          body: {"valid": bool, "plan": str, "licensee": str,
                                 "features": [str], "expires_at": iso8601|null,
                                 "message": str}

Uses only the standard library (urllib) so the licensing package stays light.
Responses are cached for `cache_ttl` seconds; on network failure the last good
response keeps working (offline grace) instead of locking paying users out.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from datetime import datetime

from .plans import plan_satisfies
from .provider import LicenseInfo


class HttpLicenseProvider:
    def __init__(
        self,
        url: str,
        token: str,
        *,
        timeout: float = 5.0,
        cache_ttl: float = 300.0,
    ) -> None:
        self._url = url
        self._token = token
        self._timeout = timeout
        self._cache_ttl = cache_ttl
        self._cached: LicenseInfo | None = None
        self._cached_at: float = 0.0
        self._last_good: LicenseInfo | None = None

    def _validate(self) -> LicenseInfo:
        request = urllib.request.Request(
            self._url,
            data=json.dumps({"token": self._token}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            payload = json.loads(response.read())
        expires_at = None
        if payload.get("expires_at"):
            expires_at = datetime.fromisoformat(payload["expires_at"])
        return LicenseInfo(
            plan=str(payload.get("plan", "free")) if payload.get("valid") else "free",
            licensee=str(payload.get("licensee", "")),
            features=tuple(payload.get("features") or ()) if payload.get("valid") else (),
            expires_at=expires_at,
            valid=bool(payload.get("valid")),
            source="http",
            message=str(payload.get("message", "")),
        )

    def info(self) -> LicenseInfo:
        now = time.monotonic()
        if self._cached is not None and now - self._cached_at < self._cache_ttl:
            return self._cached
        try:
            info = self._validate()
            self._last_good = info
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            if self._last_good is not None:
                info = LicenseInfo(
                    plan=self._last_good.plan,
                    licensee=self._last_good.licensee,
                    features=self._last_good.features,
                    expires_at=self._last_good.expires_at,
                    valid=self._last_good.valid,
                    source="http",
                    message="License server unreachable - using last known state.",
                )
            else:
                info = LicenseInfo(
                    valid=False,
                    source="http",
                    message=f"License server unreachable: {exc}",
                )
        self._cached = info
        self._cached_at = now
        return info

    def current_plan(self) -> str:
        info = self.info()
        return info.plan if info.valid else "free"

    def is_entitled(self, required_plan: str | None) -> bool:
        return plan_satisfies(self.current_plan(), required_plan)

    def has_feature(self, feature: str) -> bool:
        info = self.info()
        return info.valid and feature in info.features
