"""Bridge to vendor-native license managers (ElecKey, Sentinel, Wibu, …).

Many commercial products already own a license stack — usually a native SDK or
DLL with its own activation flow. This module lets such a stack participate as
a first-class `LicenseProvider` so the rest of the app (route gates, CLI
status, desktop dialogs) never knows the difference.

Two pieces:

* `ExternalLicenseProvider` wraps a single `fetch() -> LicenseInfo` callable —
  your adapter queries the native SDK and translates the result. Failures are
  contained: an adapter that raises yields an *invalid* license, never a crash.

* `load_entry_point_provider(group)` discovers an installed adapter through a
  Python entry point, so shipping one is just packaging:

      [project.entry-points."myapp.license_provider"]
      eleckey = "myapp_license_eleckey:provider"

  The entry point resolves to either a ready `LicenseProvider` or a zero-arg
  factory returning one. `resolve_provider()` checks this group before any
  built-in provider — a native manager, when installed, wins.
"""

from __future__ import annotations

import dataclasses
import logging
from collections.abc import Callable
from importlib.metadata import entry_points

from .plans import plan_satisfies
from .provider import LicenseInfo, LicenseProvider

logger = logging.getLogger(__name__)


class ExternalLicenseProvider:
    """Adapts a `fetch() -> LicenseInfo` callable to the LicenseProvider protocol.

    `fetch` runs on every query (like the signed/file providers) so revocation
    or expiry in the native manager takes effect without a restart. Cache inside
    your adapter if the native call is expensive.
    """

    def __init__(self, fetch: Callable[[], LicenseInfo], *, name: str = "external") -> None:
        self._fetch = fetch
        self._name = name

    def info(self) -> LicenseInfo:
        try:
            info = self._fetch()
        except Exception as exc:  # noqa: BLE001 - a broken SDK must lock, not crash
            logger.exception("External license provider %r failed", self._name)
            return LicenseInfo(
                valid=False,
                source=self._name,
                message=f"External license check failed: {exc}",
            )
        if info.source in ("", "none"):
            # Make the origin visible in `license status` output.
            info = dataclasses.replace(info, source=self._name)
        return info

    def current_plan(self) -> str:
        info = self.info()
        return info.plan if info.valid else "free"

    def is_entitled(self, required_plan: str | None) -> bool:
        return plan_satisfies(self.current_plan(), required_plan)

    def has_feature(self, feature: str) -> bool:
        info = self.info()
        return info.valid and feature in info.features


def load_entry_point_provider(group: str) -> LicenseProvider | None:
    """Return the first provider advertised in `group`, or None.

    An adapter factory that raises `ImportError` is saying "my native stack is
    not on this machine" — that is the *normal* dev-checkout case, logged at
    debug and skipped quietly. Any other exception is a bug in the adapter:
    logged loudly, but still skipped — an optional native integration must
    never take the whole app down.
    """
    for entry in entry_points(group=group):
        try:
            candidate = entry.load()
            provider = candidate() if callable(candidate) else candidate
        except ImportError as exc:
            logger.debug("License provider %r unavailable here: %s", entry.name, exc)
            continue
        except Exception:  # noqa: BLE001 - see docstring
            logger.exception("License provider entry point %r failed to load", entry.name)
            continue
        if isinstance(provider, LicenseProvider):
            return provider
        logger.warning(
            "License provider entry point %r returned %r, not a LicenseProvider",
            entry.name,
            type(provider),
        )
    return None
