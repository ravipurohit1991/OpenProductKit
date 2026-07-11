from __future__ import annotations

from pathlib import Path

from .external import load_entry_point_provider
from .http import HttpLicenseProvider
from .local import LocalDevLicenseProvider
from .provider import LicenseProvider
from .signed import SignedLicenseProvider


def resolve_provider(
    *,
    entry_point_group: str = "",
    public_key: str = "",
    token: str = "",
    token_file: str | Path = "",
    url: str = "",
    dev_plan: str = "pro",
) -> LicenseProvider:
    """Pick a provider from configuration, most explicit first.

    0. an installed entry point in `entry_point_group` -> vendor-native manager
       (ElecKey, Sentinel, …; see `external.py`)
    1. `url` set        -> HTTP validation (token taken from `token` or the file)
    2. `token` set      -> offline signed-token verification
    3. `token_file` exists -> offline verification of the file's token
    4. otherwise        -> the local development stub with `dev_plan`

    The same settings drive the backend, the CLI and the desktop shell, so an
    install is licensed once, everywhere.
    """
    if entry_point_group:
        external = load_entry_point_provider(entry_point_group)
        if external is not None:
            return external
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
