from __future__ import annotations

# Higher rank satisfies any lower-or-equal requirement.
PLAN_RANK = {"free": 0, "pro": 1, "enterprise": 2}


def plan_satisfies(have: str, need: str | None) -> bool:
    """Whether plan `have` satisfies a `need` requirement (None = free/no gate).

    Unknown `have` plans rank as free; unknown `need` plans are unsatisfiable —
    a typo in a gate should lock, not silently unlock.
    """
    if need is None:
        return True
    return PLAN_RANK.get(have, 0) >= PLAN_RANK.get(need, 99)
