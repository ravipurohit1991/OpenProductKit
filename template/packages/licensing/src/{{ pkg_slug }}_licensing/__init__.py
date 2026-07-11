"""Licensing / entitlement.

For open-source use this behaves as feature flags. For commercial use, real
providers verify Ed25519-signed offline tokens (string or file), ask a
vendor-run HTTP endpoint, or bridge to a vendor-native license manager
(ElecKey, Sentinel, … — see `external.py`). No claims of unbreakable
protection — this is honest-user entitlement and commercial-readiness hooks.
"""

from .external import ExternalLicenseProvider, load_entry_point_provider
from .http import HttpLicenseProvider
from .local import LocalDevLicenseProvider
from .plans import PLAN_RANK, plan_satisfies
from .provider import LicenseInfo, LicenseProvider
from .resolve import resolve_provider
from .signed import SignedLicenseProvider
from .signing import KeyPair, generate_keypair, issue_token, verify_token

__all__ = [
    "PLAN_RANK",
    "ExternalLicenseProvider",
    "HttpLicenseProvider",
    "KeyPair",
    "LicenseInfo",
    "LicenseProvider",
    "LocalDevLicenseProvider",
    "SignedLicenseProvider",
    "generate_keypair",
    "issue_token",
    "load_entry_point_provider",
    "plan_satisfies",
    "resolve_provider",
    "verify_token",
]
