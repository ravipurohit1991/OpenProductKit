from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )

    database_url: str = "sqlite:///./app.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Directory with the built web UI (apps/frontend/dist). When it exists the
    # backend serves it at "/", so one process can deliver the whole product —
    # used by the desktop sidecar shells and single-container deployments.
    web_dist: str = "apps/frontend/dist"

    # --- auth (see auth.py) -----------------------------------------------------
    # Optional user accounts for hosted deployments. Off by default: the
    # desktop/local story has no accounts. When on, every API route except
    # health/login/setup/me requires a bearer session, and operator actions
    # (plugin toggles, marketplace unlock/install, user management) need admin.
    auth_enabled: bool = False
    # How long a login session stays valid.
    auth_session_days: int = 30

    # --- marketplace (see api/routes/marketplace) ------------------------------
    # Local catalog of available extensions shown in the Marketplace tab.
    marketplace_catalog: str = "marketplace/catalog.json"
    # Optional vendor-hosted catalog URL; when set it replaces the local file.
    marketplace_url: str = ""
    # Allow installing catalog extensions from the running app (Marketplace
    # "Install" button / POST /api/marketplace/install). Installing runs pip in
    # the app's environment — enable it only where the catalog is trusted.
    marketplace_allow_install: bool = False

    # --- licensing (see packages/licensing) -----------------------------------
    # The vendor's Ed25519 public key (base64url). Bake it in here or set
    # APP_LICENSE_PUBLIC_KEY; without it signed tokens cannot be verified.
    license_public_key: str = ""
    # A signed license token, verified offline (APP_LICENSE_TOKEN).
    license_token: str = ""
    # Path to a file containing the token; `opk license install` writes it.
    license_file: str = "license.key"
    # A vendor-run validation endpoint; when set it takes precedence.
    license_url: str = ""
    # Plan granted by the dev stub when nothing above is configured.
    license_dev_plan: str = "pro"


settings = Settings()
