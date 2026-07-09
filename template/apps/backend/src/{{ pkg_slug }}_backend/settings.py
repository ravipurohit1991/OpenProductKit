from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )

    database_url: str = "sqlite:///./app.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

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
