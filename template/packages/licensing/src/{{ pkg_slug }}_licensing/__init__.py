"""Licensing / entitlement abstraction.

For open-source use this behaves as feature flags. For commercial use, a real
provider (signed token, HTTP license server, Stripe/Lemon Squeezy, …) replaces
the dev stub in P7. No claims of unbreakable protection — this is honest-user
entitlement and commercial-readiness hooks.
"""

from .local import LocalDevLicenseProvider
from .provider import LicenseProvider

__all__ = ["LicenseProvider", "LocalDevLicenseProvider"]
