from __future__ import annotations

# Higher rank satisfies any lower-or-equal requirement.
_PLAN_RANK = {"free": 0, "pro": 1, "enterprise": 2}


class LocalDevLicenseProvider:
    """Development stub: grants a plan locally so everything up to it is unlocked.

    This is a real entitlement check (not a blanket `True`), it just resolves the
    plan from local config instead of a license server. Swap it out in P7.
    """

    def __init__(self, plan: str = "pro") -> None:
        self._plan = plan

    def current_plan(self) -> str:
        return self._plan

    def is_entitled(self, required_plan: str | None) -> bool:
        if required_plan is None:
            return True
        have = _PLAN_RANK.get(self._plan, 0)
        need = _PLAN_RANK.get(required_plan, 99)
        return have >= need
