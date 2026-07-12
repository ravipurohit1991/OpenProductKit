# Settings

Generated OpenProductKit projects use environment variables prefixed with `APP_`. The backend settings class also reads a local `.env` file.

## Common variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_DATABASE_URL` | SQLAlchemy database URL | Local SQLite database |
| `APP_LICENSE_DEV_PLAN` | Development stub plan | `pro` |
| `APP_LICENSE_PUBLIC_KEY` | Ed25519 public key used to verify signed license tokens | unset |
| `APP_LICENSE_TOKEN` | Signed license token supplied directly | unset |
| `APP_LICENSE_FILE` | Path to a signed license token file | `license.key` |
| `APP_LICENSE_URL` | HTTP license validation endpoint | unset |
| `APP_WEB_DIST` | Directory with the built web UI; served at `/` when it exists | `apps/frontend/dist` |
| `APP_MARKETPLACE_CATALOG` | Local marketplace catalog file | `marketplace/catalog.json` |
| `APP_MARKETPLACE_URL` | Hosted catalog URL (replaces the local file when set) | unset |
| `APP_MARKETPLACE_ALLOW_INSTALL` | Allow installing catalog extensions from the running app ([details](marketplace.md#runtime-installs-opt-in)) | `false` |
| `APP_AUTH_ENABLED` | Require user accounts on every API route ([details](auth.md)) | `false` |
| `APP_AUTH_SESSION_DAYS` | Login session lifetime in days | `30` |

Desktop mode sets `APP_DATABASE_URL` and `APP_LICENSE_FILE` to platform-specific app-data paths when they are not already set (the sidecar shells also set `APP_WEB_DIST`).

## License resolution

License providers are resolved in this order:

1. `APP_LICENSE_URL`
2. `APP_LICENSE_TOKEN`
3. `APP_LICENSE_FILE`
4. development stub

Invalid or expired licenses degrade to the free plan with a readable status message.

## Frontend settings

The frontend's product name is generated into `apps/frontend/src/config.ts`.

The API client chooses its transport at runtime:

- browser mode uses HTTP (same origin, or the Vite dev proxy)
- the pywebview desktop shell uses the in-process JS bridge
- the Electron/Tauri shells load the UI *from* the sidecar backend, so plain
  same-origin HTTP applies with no special casing

## Copier answers

Generated projects store template answers in `.copier-answers.yml`. Copier uses this file during `copier update` to re-render the project with the same names and metadata.

Commit `.copier-answers.yml` so updates are reproducible for every developer on the project.
