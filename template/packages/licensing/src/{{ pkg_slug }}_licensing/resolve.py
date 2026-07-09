from __future__ import annotations

from pathlib import Path

from .http import HttpLicenseProvider
from .local import LocalDevLicenseProvider
from .provider import LicenseProvider
from .signed import SignedLicenseProvider


def resolve_provider(
    *,
    public_key: str = "",
    token: str = "",
    token_file: str | Path = "",
    url: str = "",
    dev_plan: str = "pro",
) -> LicenseProvider:
    """Pick a provider from configuration, most explicit first.

    1. `url` set        -> HTTP validation (token taken from `token` or the file)
    2. `token` set      -> offline signed-token verification
    3. `token_file` exists -> offline verification of the file's token
    4. otherwise        -> the local development stub with `dev_plan`

    The same settings drive the backend, the CLI and the desktop shell, so an
    install is licensed once, everywhere.
    """
    file_path = Path(token_file) if token_file else None
    if url:
        key = token
        if not key and file_path is not None and file_path.exists():
            key = file_path.read_text(encoding="utf-8").strip()
        return HttpLicenseProvider(url, key)
    if token:
        return SignedLicenseProvider(public_key, token=token)
    if file_path is not None and file_path.exists():
        return SignedLicenseProvider(public_key, token_file=file_path)
    return LocalDevLicenseProvider(dev_plan)
