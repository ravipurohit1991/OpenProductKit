from __future__ import annotations

from .plans import plan_satisfies
from .provider import LicenseInfo


class LocalDevLicenseProvider:
    """Development stub: grants a plan locally so everything up to it is unlocked.

    This is a real entitlement check (not a blanket `True`), it just resolves the
    plan from local config instead of a verified license. It also grants every
    named feature flag, so nothing is locked while developing. Production
    installs should configure a real provider (signed token, file or HTTP).
    """

    def __init__(self, plan: str = "pro") -> None:
        self._plan = plan

    def current_plan(self) -> str:
        return self._plan

    def is_entitled(self, required_plan: str | None) -> bool:
        return plan_satisfies(self._plan, required_plan)

    def has_feature(self, feature: str) -> bool:
        return True

    def info(self) -> LicenseInfo:
        return LicenseInfo(
            plan=self._plan,
            licensee="local development",
            valid=True,
            source="dev",
            message="Development stub - configure a real license provider for production.",
        )
